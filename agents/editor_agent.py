
import re
from agents.llm_client import client, MODEL_NAME
from agents.quality_evaluator import evaluate_article
from agents.text_metrics import (
    diagnose_article,
    rebuild_from_sections,
    seq_similarity,
    find_unsourced_numeric_claim_paragraphs,
    find_unsourced_example_markers,
    strip_stray_framework_mentions,
    H2_CEILING,
    NON_CORE_SECTION_KEYWORDS,
)
from agents.uniqueness_agent import (
    regenerate_quote,
    regenerate_framework_name,
    regenerate_conclusion,
)
from agents.history_manager import (
    get_used_quotes,
    get_used_conclusions,
    remember_quote,
    remember_framework,
    remember_conclusion,
)
from agents.text_metrics import strip_leaked_meta_lines


HEADER_RE = re.compile(
    r"Title:\s*(?P<title>.*?)\n"
    r"Subtitle:\s*(?P<subtitle>.*?)\n"
    r"Source URL:\s*(?P<url>.*?)\n"
    r"Image Prompt:\s*(?P<image>.*?)\n"
    r"Blog:\s*(?P<blog>.*)",
    re.DOTALL,
)

OVERLAP_GROUPS = [
    ["implementation"],
    ["risk assessment", "risk"],
    ["lessons learned", "lessons"],
    ["key takeaway", "takeaway"],
    ["balancing", "balance"],
]
KPI_HEADING_HINTS = ("case study", "scenario", "rollout", "framework", "implementation")
KPI_CONTENT_HINTS = ("%", "reduction", "increase", "decrease", "cost", "cycle time", "kpi")

PROTECTED_HEADING_KEYWORDS = [
    "framework", "case study", "illustrative", "trade-off", "tradeoff",
    "q&a", "tl;dr", "key takeaway", "quick answers",
]

BANNED_CLICHES = [
    "ever-evolving market",
    "cornerstone",
    "testament to",
    "imperative for survival",
    "game-changer",
    "game-changing",
    "transformative journey",
    "unprecedented",
    "rapidly evolving landscape",
    "revolutionize",
    "paradigm shift",
    "holistic approach",
    "synergies",
    "cutting-edge",
    "in today's fast-paced world",
    "more important than ever",
    "the future is now",
    "digital transformation journey",
    "unlock the full potential",
    "a global bank",
    "a mid-sized firm",
    "a healthcare provider",
    "a leading retailer",
    "a Fortune 500 company",
    "a global technology organization",
    "a major financial institution",
    "transformative shift",
    "unlock value",
    "future-ready",
    "strategic imperative",
    "rapidly evolving",
    "ever-changing",
    "business landscape",
]

AI_FILLER_REPLACEMENTS = {
    "furthermore": "also",
    "in this scenario": "here",
    "profound shift": "major shift",
    "indeed": "",
    "as such": "so",
    "to fully harness": "to use",
    "rapidly becoming": "becoming",
    "catalyze": "drive",
    "catalyzes": "drives",
    "formidable advantage": "strong advantage",
    "recalibrated view": "revised view",
}


def approve_article(article):
    return evaluate_article(article)


def _parse(article):
    m = HEADER_RE.search(article)
    if not m:
        return "", "", "", "", article
    return (
        m.group("title").strip(),
        m.group("subtitle").strip(),
        m.group("url").strip(),
        m.group("image").strip(),
        m.group("blog").strip(),
    )


def _rebuild(title, subtitle, url, image, blog):
    return (
        f"Title: {title}\n"
        f"Subtitle: {subtitle}\n"
        f"Source URL: {url}\n"
        f"Image Prompt: {image}\n"
        f"Blog:\n{blog}"
    )


def _llm_fix(system, user, _retries=2):
    import time
    from openai import APIConnectionError

    for attempt in range(_retries + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            break
        except APIConnectionError:
            if attempt == _retries:
                raise
            time.sleep(2 ** attempt)  # 1s, then 2s backoff before giving up

    raw = response.choices[0].message.content.strip()
    return strip_leaked_meta_lines(raw)


def _split_generated_section(markdown_section, default_heading):
    heading_match = re.search(r"^##\s+(.+)$", markdown_section, re.MULTILINE)
    heading = heading_match.group(1).strip() if heading_match else default_heading
    body = re.sub(r"^##\s+.+\n?", "", markdown_section, count=1).strip()
    return {"heading": heading, "body": body, "paragraphs": body.split("\n\n")}


def _expand_thin_section(heading, body, other_headings):
    system = (
        "You are a senior Luvana enterprise editor. Expand ONE section of an existing article to 3-5 paragraphs "
        "(220-320 words total). Keep it focused on a single new strategic insight. "
        "Follow this flow: (1) strategic shift, (2) enterprise consequence, (3) implementation or governance implication, "
        "(4) enterprise example or trade-off, (5) optional second-order consequence or competitive angle. "
        "Do not repeat ideas already covered in other sections, do not pad, and do not sound generic. "
        "Return ONLY the paragraph text -- no heading, no preamble."
    )
    user = (
        f"Section heading: {heading}\n"
        f"Current content:\n{body}\n\n"
        f"Other section headings already in the article (avoid repeating their content):\n"
        + ", ".join(other_headings)
    )
    return _llm_fix(system, user)


def _rewrite_similar_paragraph(paragraph, sibling_paragraph):
    system = (
        "You rewrite ONE paragraph of an executive article so it teaches a different idea than a sibling paragraph "
        "it currently overlaps with. Keep similar length. Return only the rewritten paragraph."
    )
    user = (
        f"Paragraph to rewrite:\n{paragraph}\n\n"
        f"It currently overlaps in meaning with this other paragraph (keep that one as-is, make yours distinct):\n{sibling_paragraph}"
    )
    return _llm_fix(system, user)


def _generate_missing_component(kind, thesis_hint):
    instructions = {
        "framework": (
    "Write ONE new H2 section introducing exactly ONE enterprise framework specific to this article's thesis. "
    "The framework must be clearly named and original. Use one of these patterns if appropriate:\n"
    "  - MATURITY MODEL: 4-5 stages with a unique name specific to the article thesis.\n"
    "  - DECISION MATRIX (prose): compare 3-4 options across Cost Profile, Latency, Operational Complexity, and Vendor Lock-in.\n"
    "  - PHASED IMPLEMENTATION: 3-5 phases with what teams do, what they measure, and what signals readiness for the next phase.\n"
    "The framework must appear as exactly one named H2 section.\n"
    "Do not title the framework section as a question.\n"
    "Do not create partial framework variants in other headings.\n"
    "Do not repeat the framework name in abbreviated form.\n"
    "Do not use a generic label like 'AI Maturity Model'. Explain what makes it structurally different from existing enterprise paradigms. "
    "Develop it in depth. Return markdown starting with '## '."
),
        "case_study": (
            "Write ONE new H2 section containing a realistic enterprise case study. Use a precise sector descriptor unless a real named enterprise "
            "is clearly supported by the article source package. Include: Challenge, Approach, Outcome, and Executive Lesson. "
            "Do not invent exact statistics unless they are explicitly available in the source package. Return markdown starting with '## '."
        ),
        "tradeoff": (
            "Write ONE new H2 section discussing a single executive trade-off directly relevant to this article's thesis. "
            "Use precise business language and include: why the tension exists, business consequence, and executive recommendation. "
            "Keep it narrow and decision-oriented. Return markdown starting with '## '."
        ),
        "qa_block": (
            "Write ONE new H2 section titled '## Quick Answers' containing exactly 3 short question/answer pairs. "
            "Each answer must be direct, self-contained, and 1-2 sentences. Include one cost question, one governance question, "
            "and one contrarian or risk question. Format each as bolded question followed by the answer. Return markdown starting with '## '."
        ),
        "forward_looking": (
            "Write ONE new H2 section covering what AI infrastructure or organizational capability will look like in 3-5 years. "
            "Structure: (1) the assumption that will no longer hold, (2) the capability executives must start building now, "
            "(3) the competitive gap between early movers and laggards. Return markdown starting with '## '."
        ),
    }
    system = (
        "You are a Luvana enterprise editor adding one missing section to an existing article. "
        "Avoid clichés, avoid repetition, and stay focused on agentic AI."
    ) + instructions[kind]
    user = f"Article thesis / topic: {thesis_hint}"
    raw = _llm_fix(system, user)
    return strip_leaked_meta_lines(raw)


def _merge_duplicate_case_studies(sections, case_study_headings):
    if len(case_study_headings) < 2:
        return sections
    drop_headings = set(case_study_headings[1:])
    return [
        s for s in sections
        if (s["heading"] or "(untitled intro/lead section)") not in drop_headings
    ]

    def _rewrite_lead_for_direct_answer(lead_body, thesis_hint):
      system = (
        "You are a Luvana enterprise editor. Rewrite this article's opening so the FIRST sentence "
        "directly answers the article's core question in plain language -- the kind of sentence an "
        "AI search tool or a skimming executive could lift standalone and understand with zero context. "
        "Start with the answer itself, not a scene-setting or background sentence. Keep 2-4 short "
        "paragraphs total. Do not add new claims not implied by the thesis. Return only the revised lead."
    )
    user = f"Article thesis: {thesis_hint}\n\nCurrent opening:\n{lead_body}"
    return _llm_fix(system, user)


def _rewrite_title_for_seo(title, thesis_hint):
    system = (
        "You are a Luvana enterprise editor rewriting a headline for SEO. Produce ONE headline under 70 "
        "characters that leads with a concrete claim, entity, or number rather than a generic 'How/Why/What' "
        "framing -- while keeping the article's actual argument intact. Return ONLY the headline, no quotes."
    )
    user = f"Current title: {title}\nArticle thesis: {thesis_hint}"
    return _llm_fix(system, user).strip().strip('"')


def _tighten_long_paragraphs(sections, flagged):
    flagged_by_heading = {}
    for f in flagged:
        flagged_by_heading.setdefault(f["heading"], set()).add(f["index"])

    for s in sections:
        indices = flagged_by_heading.get(s["heading"])
        if not indices:
            continue
        for idx in indices:
            if idx >= len(s["paragraphs"]):
                continue
            system = (
                "You are a Luvana enterprise editor. This paragraph is too long for a busy-reader business "
                "audience. Split it into 2 shorter paragraphs OR tighten it to under 60 words, whichever "
                "preserves the content better. Do not drop any distinct point. Return only the revised text, "
                "with a blank line between paragraphs if you split it."
            )
            user = f"Paragraph:\n{s['paragraphs'][idx]}"
            s["paragraphs"][idx] = _llm_fix(system, user)
        s["body"] = "\n\n".join(s["paragraphs"])
        s["paragraphs"] = s["body"].split("\n\n")
    return sections


def _add_concreteness_to_section(heading, body, thesis_hint):
    system = (
        "You are a Luvana enterprise editor. This recommendations section is generic -- no named vendor, "
        "product, dollar figure, percentage, or concrete timeframe. Revise it to include at least one "
        "specific, concrete anchor (a real company/tool name, a realistic cost or timeframe, or a labeled "
        "illustrative figure). Do NOT fabricate a precise statistic attributed to a real event -- if you "
        "don't have a sourced number, use a named entity or concrete timeframe instead. Return the FULL "
        "revised section body."
    )
    user = f"Section heading: {heading}\nCurrent body:\n{body}\n\nArticle thesis: {thesis_hint}"
    return _llm_fix(system, user)


def _is_protected_heading(heading):
    h = (heading or "").lower()
    return any(k in h for k in PROTECTED_HEADING_KEYWORDS)


def _enforce_h2_ceiling(sections, ceiling=H2_CEILING):
    real = [s for s in sections if s["heading"]]
    if len(real) <= ceiling:
        return sections

    def _merge_at(idx):
        removed = real.pop(idx)
        merge_target_idx = max(0, idx - 1)
        real[merge_target_idx]["body"] = real[merge_target_idx]["body"] + "\n\n" + removed["body"]
        real[merge_target_idx]["paragraphs"] = real[merge_target_idx]["body"].split("\n\n")

    non_core_indices = [
        i for i, s in enumerate(real)
        if any(k in s["heading"].lower() for k in NON_CORE_SECTION_KEYWORDS)
        and not _is_protected_heading(s["heading"])
    ]
    while len(real) > ceiling and non_core_indices:
        idx = non_core_indices.pop()
        _merge_at(idx)
        non_core_indices = [i - 1 if i > idx else i for i in non_core_indices]

    while len(real) > ceiling:
        candidates = [i for i in range(1, len(real)) if not _is_protected_heading(real[i]["heading"])]
        if not candidates:
            candidates = [i for i in range(1, len(real))]
            if not candidates:
                break
        shortest_idx = min(candidates, key=lambda i: len(real[i]["body"].split()))
        _merge_at(shortest_idx)

    intro = [s for s in sections if not s["heading"]]
    return intro + real

def _fix_key_takeaways_format(sections, thesis_hint):
    for i, s in enumerate(sections):
        if "key takeaway" in s["heading"].lower() or "key takeaways" in s["heading"].lower():
            system = (
                "Convert this Key Takeaways section into EXACTLY 5 markdown bullet points using '- ' syntax. "
                "Each bullet must be one sentence, executive-focused, and distinct. "
                "No intro paragraph, no closing paragraph, no sub-bullets. Return ONLY the 5 bullets."
            )
            user = f"Current content:\n{s['body']}\n\nArticle thesis: {thesis_hint}"
            new_body = _llm_fix(system, user)
            sections[i]["body"] = new_body
            sections[i]["paragraphs"] = new_body.split("\n\n")
            break
    return sections


GENERIC_TRADEOFF_HEADING_RE = re.compile(
    r"\bbalanc\w+\s+.+\s+(with|vs\.?|against|and)\b",
    re.IGNORECASE,
)


def _cap_generic_tradeoff_sections(sections, max_allowed=1):
    """Originality/Strategic Depth killer: multiple sections all titled
    'Balancing X with Y' / 'Balancing A vs B' restate the same trade-off
    framing repeatedly instead of advancing distinct ideas. Keep at most
    one; merge the rest into it via the existing overlap-consolidation path."""
    matches = [
        s["heading"] for s in sections
        if s.get("heading") and GENERIC_TRADEOFF_HEADING_RE.search(s["heading"])
    ]
    if len(matches) <= max_allowed:
        return sections

    keep = matches[0]
    drop = matches[max_allowed:]
    for heading in drop:
        sections = _merge_sections_by_headings(
            sections=sections,
            keep_heading=keep,
            drop_headings=[heading],
            thesis_hint=keep,
        )
    return sections


def _find_overlap_group_headings(sections):
    real_headings = [s["heading"] for s in sections if s["heading"]]
    matched = []
    for group in OVERLAP_GROUPS:
        for heading in real_headings:
            if any(kw in heading.lower() for kw in
                   group):
                matched.append(heading)
                break
    return matched


def _consolidate_overlapping_sections(sections, thesis_hint):
    overlap_headings = _find_overlap_group_headings(sections)
    if len(overlap_headings) < 2:
        return sections

    overlap_set = set(overlap_headings)
    overlap_sections = [s for s in sections if s["heading"] in overlap_set]
    keep_heading = overlap_sections[0]["heading"]

    system = (
        "You are a Luvana enterprise editor tightening an article that has too many small, overlapping operational sections. "
        "Merge the sections below into ONE leaner section under the first heading's theme. Preserve every genuinely distinct point, "
        "cut restated ideas and connective filler, and keep the editorial tone sharp. Return ONLY the merged section body, 250-350 words."
    )
    user = (
        f"Article thesis: {thesis_hint}\n\n"
        + "\n\n---\n\n".join(f"[{s['heading']}]\n{s['body']}" for s in overlap_sections)
    )
    merged_body = _llm_fix(system, user)

    new_sections = []
    inserted = False
    for s in sections:
        if s["heading"] == keep_heading and not inserted:
            new_sections.append({
                "heading": keep_heading,
                "body": merged_body,
                "paragraphs": merged_body.split("\n\n"),
            })
            inserted = True
        elif s["heading"] in overlap_set:
            continue
        else:
            new_sections.append(s)
    return new_sections if inserted else sections


def _needs_kpis(heading, body):
    if not any(h in heading.lower() for h in KPI_HEADING_HINTS):
        return False
    lowered = body.lower()
    return not any(hint in lowered for hint in KPI_CONTENT_HINTS)


def _add_kpis_to_section(heading, body, thesis_hint):
    system = (
        "You are a Luvana enterprise editor. This section describes a rollout, framework, or case study but has no measurable outcomes. "
        "Add 1-2 sentences of illustrative, clearly labeled measurable KPIs that fit the scenario. "
        "Any numbers MUST be explicitly framed as illustrative or representative (e.g. 'organizations following this pattern typically see roughly a 20-30% reduction'), "
        "never stated as a precise, verified outcome from a real event. "
        "Do NOT invent precise real-world statistics attributed to a real or implied-real company. Return the FULL revised section body."
    )
    user = f"Section heading: {heading}\nCurrent body:\n{body}\n\nArticle thesis: {thesis_hint}"
    return _llm_fix(system, user)


CASE_STUDY_UNLABELED_STAT_RE = re.compile(
    r"(\b(reduc\w+|increas\w+|decreas\w+|improv\w+|cut|save[ds]?)\b[^.]{0,60}\bby\s+(over\s+|more than\s+)?\d{1,3}(\.\d+)?%)"
    r"|(\d{1,3}(\.\d+)?%\s+(reduction|increase|decrease|improvement))"
    r"|((over|more than)\s+\d{1,3}(\.\d+)?%)",
    re.IGNORECASE,
)


def _relabel_unlabeled_case_study_stats(sections, thesis_hint):
    """Catches precise, unlabeled percentage claims in case study / KPI-bearing
    sections and rewrites them to be explicitly illustrative, rather than
    only flagging with a citation-needed tag."""
    for s in sections:
        heading_lower = (s["heading"] or "").lower()
        if not any(h in heading_lower for h in KPI_HEADING_HINTS):
            continue
        if not CASE_STUDY_UNLABELED_STAT_RE.search(s["body"]):
            continue
        already_labeled = any(
            marker in s["body"].lower()
            for marker in ("illustrative", "representative", "hypothetical", "typically see", "roughly")
        )
        if already_labeled:
            continue
        system = (
            "You are a Luvana enterprise editor. This section states a precise percentage outcome as if it were a "
            "verified real-world fact, but it is not sourced to real, verifiable data. Rewrite ONLY the sentence(s) "
            "containing the statistic so the number is explicitly framed as illustrative or representative, not a "
            "confirmed outcome. Keep everything else in the section unchanged. Return the FULL revised section body."
        )
        user = f"Section heading: {s['heading']}\nCurrent body:\n{s['body']}\n\nArticle thesis: {thesis_hint}"
        s["body"] = _llm_fix(system, user)
        s["paragraphs"] = s["body"].split("\n\n")
    return sections


def _needs_originality_note(body):
    lowered = body.lower()
    return not any(
        phrase in lowered
        for phrase in ("unlike", "differs from", "distinct from", "in contrast to", "what makes this different")
    )


def _add_originality_note(heading, body, thesis_hint):
    system = (
        "You are a Luvana enterprise editor. Add ONE closing paragraph (60-90 words) to this framework section that explicitly states "
        "what is structurally novel about this framework compared with existing DevSecOps/FinOps-style concepts. "
        "The framework must remain a single named H2 and must not be split into question-style variants. "
        "Return the FULL section body with this paragraph appended."
    )
    user = f"Section heading: {heading}\nCurrent body:\n{body}\n\nArticle thesis: {thesis_hint}"
    return _llm_fix(system, user)


def _flag_unsourced_stats(sections):
    flagged = find_unsourced_numeric_claim_paragraphs(sections)
    if not flagged:
        return sections

    flagged_indices_by_heading = {}
    for f in flagged:
        flagged_indices_by_heading.setdefault(f["heading"], set()).add(f["index"])

    for s in sections:
        indices = flagged_indices_by_heading.get(s["heading"])
        if not indices:
            continue
        new_paragraphs = []
        for idx, p in enumerate(s["paragraphs"]):
            if idx in indices:
                p = p.rstrip() + " *(citation needed)*"
            new_paragraphs.append(p)
        s["paragraphs"] = new_paragraphs
        s["body"] = "\n\n".join(new_paragraphs)
    return sections


def _normalize_framework_heading(h):
    h = h.lower().strip()
    h = re.sub(r'^(the|a|an)\s+', '', h)
    # Strip ANY generic "container word" for a framework -- not just the
    # literal word "framework" -- so "X Blueprint" and "X Strategy" and
    # "X Model" all normalize toward the same key when they're really the
    # same underlying concept, catching duplicate frameworks that use
    # different container nouns.
    h = re.sub(r'\b(framework|blueprint|strategy|model|architecture|approach)\b', '', h)
    h = re.sub(r'\s+', ' ', h)
    return h.strip()
    
def _is_valid_framework_heading(heading):
    h = (heading or "").strip()
    low = h.lower()

    if not h:
        return False
    if h.endswith("?"):
        return False
    if len(h.split()) < 3:
        return False
    if low in {"what", "this", "that", "these", "those", "the", "framework"}:
        return False
    if low.startswith("the ") and len(h.split()) < 4:
        return False
    return True


def _find_framework_headings(sections):
    """
    Must match the gate's own definition (text_metrics._heading_ends_with_framework_keyword),
    or the merge step will systematically miss headings the gate flags as duplicate
    frameworks (e.g. "... Engagement Model", "... Behavioral Model") — this was the
    root cause of frameworks surviving improve_article() only to fail the hard gate.
    """
    from agents.text_metrics import (
        find_named_framework_mentions,
        _heading_ends_with_framework_keyword,
    )

    strict_heads = [
        s["heading"] for s in sections
        if s.get("heading")
        and _heading_ends_with_framework_keyword(s["heading"])
        and _is_valid_framework_heading(s["heading"])
    ]
    strict_lower = {h.lower() for h in strict_heads}

    named_heads = []
    for s in sections:
        heading = s.get("heading")
        if not heading or heading.lower() in strict_lower:
            continue
        if not _is_valid_framework_heading(heading):
            continue
        own_mentions = find_named_framework_mentions(s.get("body", ""))
        if any(m.lower() == heading.lower() for m in own_mentions):
            named_heads.append(heading)

    return strict_heads + named_heads

def _merge_sections_by_headings(sections, keep_heading, drop_headings, thesis_hint):
    keep_section = None
    drop_set = set(drop_headings)
    collected = []

    for s in sections:
        if s["heading"] == keep_heading:
            keep_section = s
        elif s["heading"] in drop_set:
            collected.append(s["body"])

    if not keep_section:
        return sections

    merged_input = keep_section["body"]
    for body in collected:
        merged_input += "\n\n" + body

    system = (
    "You are a Luvana enterprise editor. Merge overlapping framework sections into ONE coherent framework. "
    "Keep the strongest name, preserve distinct ideas only, remove repetition, and return only the revised body. "
    "Preserve one canonical framework heading only. Remove fragments, abbreviations, and question-style variants."
)
    user = f"Article thesis: {thesis_hint}\n\nMerged source text:\n{merged_input}"
    merged_body = _llm_fix(system, user)

    new_sections = []
    replaced = False
    for s in sections:
        if s["heading"] == keep_heading and not replaced:
            s["body"] = merged_body
            s["paragraphs"] = merged_body.split("\n\n")
            new_sections.append(s)
            replaced = True
        elif s["heading"] in drop_set:
            continue
        else:
            new_sections.append(s)
    return new_sections


def _merge_duplicate_frameworks(sections, thesis_hint):
    framework_heads = _find_framework_headings(sections)
    if len(framework_heads) < 2:
        return sections

    groups = {}
    for h in framework_heads:
        key = _normalize_framework_heading(h)
        groups.setdefault(key, []).append(h)

    for _, group in groups.items():
        if len(group) < 2:
            continue
        sections = _merge_sections_by_headings(
            sections=sections,
            keep_heading=group[0],
            drop_headings=group[1:],
            thesis_hint=thesis_hint,
        )

    # Safety net: the article rule is "exactly ONE framework section,"
    # not "one per unique normalized name." If normalization still left
    # 2+ distinct framework headings (different enough wording that they
    # didn't group), merge them all into the first one anyway.
    remaining = _find_framework_headings(sections)
    if len(remaining) >= 2:
        sections = _merge_sections_by_headings(
            sections=sections,
            keep_heading=remaining[0],
            drop_headings=remaining[1:],
            thesis_hint=thesis_hint,
        )
    return sections

ANONYMIZED_PROXY_RE = re.compile(
    r"\ban?\s+(?:(major|leading|global|mid-sized|large|prominent|well-known|top|regional)\s+)?"
    r"(\w+\s+){0,2}"
    r"(firm|company|provider|bank|retailer|institution|enterprise|organization|corporation)\b",
    re.IGNORECASE,
)

def _has_banned_cliches(text):
    from agents.text_metrics import (
        find_banned_phrases,
        find_repeated_sentence_skeletons,
        find_ai_filler_transitions,
    )
    text_lower = text.lower()
    local_cliche_hit = any(phrase in text_lower for phrase in BANNED_CLICHES)
    gate_pattern_hit = bool(find_banned_phrases(text))
    skeleton_hit = len(find_repeated_sentence_skeletons(text)) >= 1
    anonymized_proxy_hit = bool(ANONYMIZED_PROXY_RE.search(text))
    # The hard gate rejects articles with 3+ AI-prose filler transitions
    # (e.g. "furthermore", "in this scenario", "profound shift") -- catch
    # them here too so this purge pass actually removes them before the
    # article ever reaches that gate, instead of only being detected there
    # with nothing upstream that fixes it.
    filler_hit = len(find_ai_filler_transitions(text)) >= 1
    return local_cliche_hit or gate_pattern_hit or skeleton_hit or anonymized_proxy_hit or filler_hit


def _deterministic_strip_ai_filler(text):
    """Last-resort, non-context-aware cleanup for AI-prose filler
    transitions still present after LLM rewrite attempts. Mirrors
    _deterministic_strip_anonymized_proxies -- an honest mechanical
    fallback rather than silently publishing filler the LLM pass missed."""
    fixed = text
    for filler, replacement in AI_FILLER_REPLACEMENTS.items():
        pattern = re.compile(re.escape(filler), re.IGNORECASE)
        fixed = pattern.sub(replacement, fixed)
    fixed = re.sub(r'\s{2,}', ' ', fixed)  # collapse double spaces left by empty replacements
    return fixed

def _deterministic_strip_anonymized_proxies(text):
    """Last-resort, non-context-aware cleanup for anonymized enterprise
    proxy phrases (e.g. 'a leading firm', 'a major technology provider')
    still present after LLM rewrite attempts. Mirrors
    _deterministic_strip_ai_filler -- an honest mechanical fallback
    rather than silently publishing a proxy phrase the LLM pass missed."""
    def _replace(match):
        return "a representative enterprise"

    fixed = ANONYMIZED_PROXY_RE.sub(_replace, text)
    fixed = re.sub(r'\s{2,}', ' ', fixed)  # collapse double spaces left by replacements
    return fixed


def _purge_banned_cliches(sections, thesis_hint, max_attempts=2):
    from agents.text_metrics import find_ai_filler_transitions
    changed = False
    for s in sections:
        # Pull the blockquote line(s) out before any LLM rewrite touches
        # this section -- the quote must never be silently altered by a
        # cleanup pass whose job is unrelated to quote quality.
        body_lines = s["body"].split("\n")
        quote_lines = [l for l in body_lines if l.strip().startswith(">")]
        working_body = "\n".join(l for l in body_lines if not l.strip().startswith(">"))

        attempts = 0
        while _has_banned_cliches(working_body) and attempts < max_attempts:
            system = (
                "You are a Luvana enterprise editorial editor. Rewrite the supplied section body to remove banned clichés "
                "and generic AI-prose phrases, and replace them with precise, specific enterprise language. "
                "You MUST also remove generic AI-prose filler transitions -- words and phrases like 'furthermore', "
                "'indeed', 'as such', 'in this scenario', 'profound shift', 'formidable advantage', 'rapidly becoming', "
                "'catalyze/catalyzes', 'to fully harness', 'recalibrated view' -- replacing them with plain, direct "
                "language or removing them outright when they add no meaning. "
                "You MUST replace every anonymized enterprise proxy (e.g. 'a leading firm', 'a technology enterprise', "
                "'a major provider') with either a real named enterprise if the article's context supports one, or a "
                "clearly-labeled hypothetical framing (e.g. 'in a representative mid-market scenario'). Do not introduce "
                "a new anonymized proxy phrase while removing the old one. "
                "Return only the revised section body. Do not add new content or change the article structure."
            )

            user = f"Article thesis: {thesis_hint}\n\nSection body:\n{working_body}"
            working_body = _llm_fix(system, user)
            changed = True
            attempts += 1

        if _has_banned_cliches(working_body) and ANONYMIZED_PROXY_RE.search(working_body):
            working_body = _deterministic_strip_anonymized_proxies(working_body)
            changed = True
        if find_ai_filler_transitions(working_body):
            working_body = _deterministic_strip_ai_filler(working_body)
            changed = True

        if quote_lines:
            s["body"] = working_body.rstrip() + "\n\n" + "\n".join(quote_lines)
        else:
            s["body"] = working_body
        s["paragraphs"] = s["body"].split("\n\n")
 
    return sections, changed


def _is_key_takeaways_section(section):
    h = (section.get("heading") or "").lower()
    return h == "key takeaways" or "key takeaways" in h


def _rewrite_key_takeaways(sections, thesis_hint):
    for s in sections:
        if _is_key_takeaways_section(s):
            system = (
                "You are a Luvana enterprise editorial editor. Rewrite the supplied Key Takeaways section so it contains exactly 5 "
                "top-level bullet points, with no intro paragraph, no closing paragraph, and no sub-bullets. Each bullet must be "
                "concise, specific, and executive-oriented. Return only the section body."
            )
            user = f"Article thesis: {thesis_hint}\n\nCurrent Key Takeaways section:\n{s['body']}"
            s["body"] = _llm_fix(system, user)
            s["paragraphs"] = s["body"].split("\n\n")
            return sections, True
    return sections, False


def _has_contrarian_element(sections):
    contrarian_signals = [
        "however", "counter", "contrarian", "not always", "not every",
        "caution", "risk", "downside", "trade-off", "tradeoff",
        "overhead", "complexity", "before it reduces", "when it does not",
        "the case against", "challenging assumption", "opposing view",
        "when this fails", "limits of", "limitations of",
    ]
    full_text = " ".join(s["body"].lower() for s in sections)
    return any(signal in full_text for signal in contrarian_signals)


def _ensure_contrarian_tension(sections, thesis_hint):
    if _has_contrarian_element(sections):
        return sections

    target = None
    for s in sections:
        h = (s.get("heading") or "").lower()
        if any(kw in h for kw in ["recommend", "strategy", "analysis", "framework", "infrastructure"]):
            target = s
            break
    if not target and sections:
        target = sections[max(len(sections) - 2, 0)]

    if not target:
        return sections

    system = (
        "You are a Luvana enterprise editor. Add ONE paragraph of genuine contrarian tension to the end of the supplied section body. "
        "The contrarian point must challenge the section's primary recommendation with a legitimate counter-argument. "
        "Name the specific assumption being challenged and identify the enterprise conditions under which the opposing view is correct. "
        "Use precise business language. Avoid clichés. Do not summarize the section. Return the full section body with the contrarian paragraph appended."
    )
    user = f"Article thesis: {thesis_hint}\n\nSection to extend:\n{target['body']}"
    target["body"] = _llm_fix(system, user)
    target["paragraphs"] = target["body"].split("\n\n")
    return sections

def _has_banned_example_phrases(rebuilt_blog):
    from agents.text_metrics import split_h2_sections, find_all_case_study_headings
    sections = split_h2_sections(rebuilt_blog)
    sanctioned = find_all_case_study_headings(sections)
    markers = find_unsourced_example_markers(sections, sanctioned_case_study_headings=sanctioned)
    return len(markers) > 1


def _cleanup_banned_example_phrases(sections, thesis_hint):
    from agents.text_metrics import find_all_case_study_headings
    sanctioned = set(find_all_case_study_headings(sections))

    for s in sections:
        label = s["heading"] or "(untitled intro/lead section)"
        if label in sanctioned:
            continue
        markers = find_unsourced_example_markers([s], sanctioned_case_study_headings=[])
        if not markers:
            continue
        system = (
            "You are a Luvana enterprise editor. This section contains a vague, fabricated-sounding example outside the article's "
            "designated case study. Rewrite it into precise, hedged strategic language without inventing a specific named or implied company. "
            "Return the FULL revised section body."
        )
        user = f"Article thesis: {thesis_hint}\n\nSection body:\n{s['body']}"
        s["body"] = _llm_fix(system, user)
        s["paragraphs"] = s["body"].split("\n\n")

    return sections

def _enforce_quick_answers_position(sections):
    """Quick Answers must sit second-to-last, immediately before whatever
    closes the article -- not buried mid-article with more essay sections
    trailing after it. This matters for AEO structure and for honoring the
    brief's article_flow (quick answers -> conclusion, in that order)."""
    qa_idx = None
    for i, s in enumerate(sections):
        h = (s.get("heading") or "").lower()
        if "quick answers" in h or "q&a" in h:
            qa_idx = i
            break
    if qa_idx is None or qa_idx >= len(sections) - 2:
        return sections
    qa_section = sections.pop(qa_idx)
    insert_at = max(len(sections) - 1, 0)
    sections.insert(insert_at, qa_section)
    return sections

def apply_targeted_revision(blog, gating_breakdown, improvement_suggestions, thesis_hint):
    """
    One content-level revision pass driven by the quality evaluator's actual
    critique. This is what the retry loop should call FIRST -- structural
    cleanup (improve_article) already ran once during the initial editor
    pass and doesn't need blind re-running; what's missing on a low score
    is usually content depth (originality, evidence, strategic depth), not
    structure. Preserves headings/framework/case study/Quick Answers as-is.
    """
    weakest = sorted(
        [(k, v) for k, v in gating_breakdown.items() if k != "raw"],
        key=lambda kv: kv[1],
    )[:3]
    weak_labels = ", ".join(f"{k.replace('_', ' ')} ({v}/10)" for k, v in weakest)

    # Compute structural metrics on the PRE-revision article so the LLM is
    # told exactly what's duplicated/thin/unsourced -- not just the vague
    # evaluator prose. This is what was missing: the retry could reword a
    # lede paragraph and "sound" more original while leaving the literal
    # duplicate heading/mention untouched, because nothing ever named it.
    pre_report = diagnose_article(blog)
    structural_notes = []
    if pre_report["has_duplicate_frameworks"]:
        names = pre_report["all_framework_headings"] + pre_report["named_framework_mentions"]
        structural_notes.append(
            "DUPLICATE FRAMEWORK NAMES DETECTED: "
            + "; ".join(sorted(set(names)))
            + ". Keep exactly ONE framework name across the entire article "
            "(heading + every in-body mention). Rename or delete every other occurrence -- "
            "do not just rephrase the sentence around it."
        )
    if pre_report["repetitive_paragraph_pairs"]:
        structural_notes.append(
            f"{len(pre_report['repetitive_paragraph_pairs'])} paragraph(s) substantially restate "
            "another paragraph's idea. Rewrite the later paragraph in each pair to add a NEW point, "
            "not reword the same one."
        )
    if pre_report["unsourced_numeric_claims"]:
        structural_notes.append(
            f"{len(pre_report['unsourced_numeric_claims'])} numeric claim(s) lack a clear source. "
            "Either attribute them to the article's research context or rewrite them as unquantified, "
            "reasoned claims -- never invent a new statistic to fix this."
        )
    if pre_report["banned_phrases"]:
        structural_notes.append(
            "Banned filler phrases present: " + "; ".join(sorted(set(pre_report["banned_phrases"])))
            + ". Remove or replace every instance."
        )
    if pre_report["thin_sections"]:
        structural_notes.append(
            "Thin section(s) needing real development, not padding: "
            + "; ".join(pre_report["thin_sections"])
        )
    structural_block = (
        "\n\nSTRUCTURAL METRICS (computed directly on the article, not opinion -- fix these exact items):\n"
        + "\n".join(f"- {n}" for n in structural_notes)
        if structural_notes else ""
    )

    system = (
         "You are a senior Luvana enterprise editor doing a targeted revision pass on a full article. "
        "You are given specific, expert critique identifying the article's weakest dimensions. "
        "Rewrite the article to directly and substantively address EVERY improvement suggestion below -- "
        "not superficially, but by adding genuinely new specificity, evidence, or strategic depth. "
        "ABSOLUTE REQUIREMENT: every existing H2 section heading in the input article must still exist, in the same "
        "order, in your output -- including 'Quick Answers' (or 'Q&A'), the framework section, the case study section, "
        "and the blockquote. You may improve the CONTENT inside a section, but you may NEVER delete, rename, merge, "
        "or replace a section with unrelated content, and you may NEVER add a brand-new '## ' section heading that "
        "was not in the input article. If a suggestion tempts you to add a new topic (e.g. a new "
        "company example, a new sub-theme), ADD it as new paragraphs inside an existing relevant section -- do not "
        "let it replace or crowd out Quick Answers or any other required section, and do not give it its own heading. "
        "If a STRUCTURAL METRICS block is present below, those items are computed directly from the text, not "
        "opinion -- treat them as mandatory fixes with priority over the general improvement suggestions, and fix "
        "the EXACT item named (e.g. the exact duplicate framework name), not just the general theme around it. "
        "CRITICAL: If you strengthen the Evidence dimension, you MUST use only facts, names, or figures already "
        "present in the article or its research context -- NEVER invent a new statistic, study, survey, or percentage "
        "to fill a gap. If you don't have a real, sourced number to add, strengthen evidence through more specific "
        "reasoning or a more concrete (but unquantified) example instead. A fabricated statistic is worse than no statistic. "
        "Return the FULL revised article in the exact same 'Title: / Subtitle: / Source URL: / Image Prompt: / Blog:' "
        "format it was given in -- do not drop or reformat the header fields. "
        "Do not repeat any '## ' heading line twice in a row -- write each heading exactly once, "
        "immediately followed by its body text."
    )
    user = (
        f"Weakest dimensions to fix: {weak_labels}\n\n"
        f"Specific improvement suggestions from the quality reviewer:\n"
        + "\n".join(f"- {s}" for s in improvement_suggestions)
        + structural_block
        + f"\n\nArticle thesis: {thesis_hint}\n\nFULL ARTICLE:\n{blog}"
    )
    revised_article = _llm_fix(system, user)
    title, subtitle, url, image, revised_blog = _parse(revised_article)

    if not revised_blog:
        # LLM didn't return the expected header format -- fall back to
        # treating the raw response as the blog body rather than crashing
        # or silently discarding the revision.
        title, subtitle, url, image = "", "", "", ""
        revised_blog = revised_article

    report = diagnose_article(revised_blog)
    sections = report["sections"]

    if report["exceeds_h2_ceiling"]:
        # Enforce against report["sections"] (freshly re-parsed from the
        # actual markdown), not the stale in-memory `sections` list. An
        # upstream LLM rewrite may have embedded a stray '## ' heading
        # INSIDE a section's body text rather than as its own section --
        # that's invisible to a dict-count over the old list, so enforcing
        # against it silently does nothing even when diagnose_article
        # correctly detected the overage.
        sections = _enforce_h2_ceiling(report["sections"], ceiling=H2_CEILING)

    # The revision prompt above tells the LLM never to add a new '## '
    # section or duplicate the framework heading, but that's a soft
    # instruction -- the LLM can and does ignore it (e.g. when an
    # improvement suggestion says "add a memorable strategic framework").
    # improve_article() guards against this with a merge + stray-mention
    # cleanup pass; this retry path skipped that guard entirely, so any
    # duplicate framework introduced here sailed straight through to the
    # hard gate. Run the same safety net here.
    sections = _merge_duplicate_frameworks(sections, thesis_hint)
    framework_headings_now = _find_framework_headings(sections)
    if framework_headings_now:
        canonical = _normalize_framework_heading(framework_headings_now[0])
        sections = strip_stray_framework_mentions(sections, canonical)

    rebuilt_blog = rebuild_from_sections(sections)
    rebuilt_blog = strip_leaked_meta_lines(rebuilt_blog)

    return _rebuild(title, subtitle, url, image, rebuilt_blog)


def improve_article(article):
    from agents.text_metrics import title_needs_seo_rewrite

    title, subtitle, url, image, blog = _parse(article)
    report = diagnose_article(blog)
    sections = report["sections"]
    thesis_hint = title or (sections[0]["body"][:200] if sections else "")

    if title_needs_seo_rewrite(title):
        title = _rewrite_title_for_seo(title, thesis_hint)

    if report["has_duplicate_frameworks"]:
        sections = _merge_duplicate_frameworks(sections, thesis_hint)

    if report["has_duplicate_case_studies"]:
        sections = _merge_duplicate_case_studies(sections, report["all_case_study_headings"])

    sections = _consolidate_overlapping_sections(sections, thesis_hint)
    sections = _cap_generic_tradeoff_sections(sections)

    report = diagnose_article(rebuild_from_sections(sections))
    if report["exceeds_h2_ceiling"]:
        # Enforce against report["sections"] (freshly re-parsed from the
        # actual markdown), not the stale in-memory `sections` list. An
        # upstream LLM rewrite may have embedded a stray '## ' heading
        # INSIDE a section's body text rather than as its own section --
        # that's invisible to a dict-count over the old list, so enforcing
        # against it silently does nothing even when diagnose_article
        # correctly detected the overage.
        sections = _enforce_h2_ceiling(report["sections"], ceiling=H2_CEILING)

    report = diagnose_article(rebuild_from_sections(sections))
    if report["takeaways_needs_bullet_fix"]:
        sections = _fix_key_takeaways_format(sections, thesis_hint)
        report = diagnose_article(rebuild_from_sections(sections))
        sections = report["sections"]

    other_headings = [s["heading"] for s in sections if s["heading"]]
    for s in sections:
        if s["heading"] and s["heading"] in report["thin_sections"]:
            s["body"] = _expand_thin_section(
                s["heading"],
                s["body"],
                [h for h in other_headings if h != s["heading"]],
            )
            s["paragraphs"] = s["body"].split("\n\n")

    if report["repetitive_paragraph_pairs"]:
        flat = []
        for s in sections:
            flat.extend(s["paragraphs"])
        fixed = set()
        for i, j, _score in report["repetitive_paragraph_pairs"]:
            if j in fixed or j >= len(flat):
                continue
            flat[j] = _rewrite_similar_paragraph(flat[j], flat[i])
            fixed.add(j)
        idx = 0
        for s in sections:
            count = len(s["paragraphs"])
            s["paragraphs"] = flat[idx: idx + count]
            s["body"] = "\n\n".join(s["paragraphs"])
            idx += count

    sections, _ = _purge_banned_cliches(sections, thesis_hint)

    if not report["has_framework"]:
        new_section = _split_generated_section(
            _generate_missing_component("framework", thesis_hint), "Enterprise Framework"
        )
        sections.insert(max(len(sections) - 1, 0), new_section)
        remember_framework(new_section["heading"])

    if not report["has_case_study"]:
        new_section = _split_generated_section(
            _generate_missing_component("case_study", thesis_hint), "Enterprise Case Study"
        )
        sections.insert(max(len(sections) - 1, 0), new_section)

    if not report["has_tradeoff"]:
        new_section = _split_generated_section(
            _generate_missing_component("tradeoff", thesis_hint), "The Executive Trade-off"
        )
        sections.insert(max(len(sections) - 1, 0), new_section)

    vendor_topic_keywords = ("vendor", "supplier", "procurement", "build-vs-buy", "build vs buy", "partnership")
    is_vendor_topic = any(kw in thesis_hint.lower() for kw in vendor_topic_keywords) or any(
        kw in (s["heading"] or "").lower() for s in sections for kw in vendor_topic_keywords
    )
    has_markdown_table = "|---" in rebuild_from_sections(sections) or re.search(r"^\|.+\|$", rebuild_from_sections(sections), re.MULTILINE)
    if is_vendor_topic and not has_markdown_table:
        system = (
            "You are a Luvana enterprise editor. Add ONE new H2 section titled '## Decision Matrix' containing "
            "an actual markdown table (at least 3 rows, 3 columns) comparing options relevant to this article's "
            "vendor/supplier/procurement decision. Use real, specific comparison criteria (e.g. Cost, Lock-in Risk, "
            "Lead Time, Flexibility) -- not vague labels. Return markdown starting with '## Decision Matrix'."
        )
        user = f"Article thesis: {thesis_hint}"
        table_section = _split_generated_section(_llm_fix(system, user), "Decision Matrix")
        sections.insert(max(len(sections) - 1, 0), table_section)

    has_qa_block = any(
        s["heading"] and ("q&a" in s["heading"].lower() or "quick answers" in s["heading"].lower())
        for s in sections
    )
    if not has_qa_block:
        new_section = _split_generated_section(
            _generate_missing_component("qa_block", thesis_hint), "Quick Answers"
        )
        sections.insert(max(len(sections) - 1, 0), new_section)

    sections = _ensure_contrarian_tension(sections, thesis_hint)

    for s in sections:
        if s["heading"] and _needs_kpis(s["heading"], s["body"]):
            s["body"] = _add_kpis_to_section(s["heading"], s["body"], thesis_hint)
            s["paragraphs"] = s["body"].split("\n\n")

    for s in sections:
        if s["heading"] and "framework" in s["heading"].lower() and _needs_originality_note(s["body"]):
            s["body"] = _add_originality_note(s["heading"], s["body"], thesis_hint)
            s["paragraphs"] = s["body"].split("\n\n")
            break

    sections = _flag_unsourced_stats(sections)
    sections = _relabel_unlabeled_case_study_stats(sections, thesis_hint)
    sections = _cleanup_banned_example_phrases(sections, thesis_hint)

    sections = _merge_duplicate_frameworks(sections, thesis_hint)

    framework_headings_now = _find_framework_headings(sections)
    if framework_headings_now:
        canonical = _normalize_framework_heading(framework_headings_now[0])
        sections = strip_stray_framework_mentions(sections, canonical)

    sections = _enforce_quick_answers_position(sections)

    pre_final_report = diagnose_article(rebuild_from_sections(sections))
    if pre_final_report["exceeds_h2_ceiling"]:
        sections = _enforce_h2_ceiling(pre_final_report["sections"], ceiling=H2_CEILING)

    rebuilt_blog = rebuild_from_sections(sections)

    # Conclusion rewrite if overly repetitive -- runs BEFORE the quote is
    # appended, so a full-body conclusion replacement can never wipe out
    # a quote that was already appended as trailing text.
    final_report = diagnose_article(rebuilt_blog)
    final_sections = final_report["sections"]
    last = ""

    if final_report["conclusion_needs_rewrite"]:
        real = [s for s in final_sections if s["heading"]]
        if real:
            covered = "; ".join(s["heading"] for s in real[:-1])
            new_conclusion = regenerate_conclusion(covered, get_used_conclusions())
            real[-1]["body"] = new_conclusion
            rebuilt_blog = rebuild_from_sections(final_sections)
            remember_conclusion(new_conclusion)
            final_sections = diagnose_article(rebuilt_blog)["sections"]
            real = [s for s in final_sections if s["heading"]]
        if real:
            last = real[-1]["body"].strip()

    quotes = re.findall(r"^>\s?(.+)$", rebuilt_blog, re.MULTILINE)
    history_quotes = get_used_quotes()

    if len(quotes) == 0:
        new_quote = regenerate_quote(thesis_hint, history_quotes)
        new_line = new_quote if new_quote.startswith(">") else f"> {new_quote}"
        rebuilt_blog += f"\n\n{new_line}"
        remember_quote(new_quote)
    else:
        needs_new = len(quotes) > 1 or (
            history_quotes and max(seq_similarity(quotes[0], h) for h in history_quotes) >= 0.80
        )
        if needs_new:
            new_quote = regenerate_quote(thesis_hint, history_quotes)
            new_line = new_quote if new_quote.startswith(">") else f"> {new_quote}"
            rebuilt_blog = re.sub(
                r"^>\s?.+$", new_line, rebuilt_blog, count=1, flags=re.MULTILINE
            )
            if len(quotes) > 1:
                lines, seen, cleaned = rebuilt_blog.split("\n"), False, []
                for line in lines:
                    if line.strip().startswith(">"):
                        if not seen:
                            cleaned.append(line)
                            seen = True
                        continue
                    cleaned.append(line)
                rebuilt_blog = "\n".join(cleaned)
            remember_quote(new_quote)

    if last and not last.endswith((".", "!", "?", '"', "”")):
        last += "."
        real[-1]["body"] = last
        rebuilt_blog = rebuild_from_sections(final_sections)

    final_sections = diagnose_article(rebuilt_blog)["sections"]
    final_sections, purged = _purge_banned_cliches(final_sections, thesis_hint)
    if purged:
        rebuilt_blog = rebuild_from_sections(final_sections)
        final_sections = diagnose_article(rebuilt_blog)["sections"]

    final_sections, fixed = _rewrite_key_takeaways(final_sections, thesis_hint)
    if fixed:
        rebuilt_blog = rebuild_from_sections(final_sections)
        final_sections = diagnose_article(rebuilt_blog)["sections"]

    final_check = diagnose_article(rebuilt_blog)
    if final_check["exceeds_h2_ceiling"]:
        final_sections = _enforce_h2_ceiling(final_check["sections"], ceiling=H2_CEILING)
        rebuilt_blog = rebuild_from_sections(final_sections)

    final_sections = diagnose_article(rebuilt_blog)["sections"]
    final_sections = _flag_unsourced_stats(final_sections)
    rebuilt_blog = rebuild_from_sections(final_sections)
    rebuilt_blog = strip_leaked_meta_lines(rebuilt_blog)

    return _rebuild(title, subtitle, url, image, rebuilt_blog)