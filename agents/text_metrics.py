
"""
Shared, dependency-free text analysis utilities used by the editor,
quality evaluator, and uniqueness agent.
"""

import re
from difflib import SequenceMatcher


H2_CEILING = 7


NON_CORE_SECTION_KEYWORDS = [
    "key fact", "quick answer", "ai overview", "featured snippet",
    "executive summary", "unified", "conclusion",
]


STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "for",
    "with", "is", "are", "was", "were", "be", "been", "being", "this",
    "that", "these", "those", "it", "its", "as", "at", "by", "from",
    "into", "than", "then", "so", "not", "no", "will", "would", "can",
    "could", "should", "may", "might", "their", "they", "we", "you",
    "your", "our", "enterprise", "enterprises", "ai", "organizations",
    "organization", "business", "businesses",
}


FRAMEWORK_KEYWORDS = [
    "framework", "model", "layers", "stages", "roadmap", "blueprint",
    "maturity", "pyramid", "loop", "lifecycle", "stack", "curve",
    "ladder", "playbook", "strategy",
]


CASE_STUDY_KEYWORD_PATTERNS = [
    r"\bcase stud(?:y|ies)\b",
    r"\billustrative\b",
    r"\bfaced the challenge\b",
    r"\bthe organization\b(?!s)",
    r"\bthe company adopted\b",
    r"\blessons learned\b",
    r"\bgovernance:\s",
    r"\boutcome:\s",
    r"\bapproach:\s",
]


CASE_STUDY_RE = re.compile("|".join(CASE_STUDY_KEYWORD_PATTERNS), re.IGNORECASE)


FABRICATION_MARKER_RE = re.compile(
    r'\b(?:a|an|the)\s+(?:leading|prominent|notable|mid-sized|large|global|'
    r'major|regional)?\s*(?:bank|banking sector|financial institution|'
    r'logistics company|healthcare (?:industry|provider)|hospital system|'
    r'manufacturer|retailer|insurer|software (?:firm|company)|'
    r'technology (?:firm|company))\s+'
    r'(?:demonstrated|exemplifies|recently|successfully|has|have|'
    r'is experiencing|are integrating|implemented|adopted)\b',
    re.IGNORECASE
)


AI_FILLER_TRANSITIONS_RE = re.compile(
    r"\b(?:indeed|as such|furthermore|in this scenario|to fully harness|"
    r"rapidly becoming|catalyz(?:e|es)|formidable advantage|"
    r"recalibrated view|profound shift)\b",
    re.IGNORECASE,
)


NOT_MERELY_BUT_RE = re.compile(
    r'\bnot merely\s+(.+?)\s+but\b(\s+also\b)?',
    re.IGNORECASE
)


META_LEAK_LINE_RE = re.compile(
    r'^\s*[*_]{0,3}\s*(Section heading:|Current (content|body):|Article thesis:'
    r'|Other section headings.*)',
    re.IGNORECASE,
)


BANNED_PHRASE_PATTERNS = [
    r"\bthe advent of\b",
    r"\bthis shift underscores\b",
    r"\bin today'?s rapidly evolving\b",
    r"\bas organizations navigate\b",
    r"\bit is important to note that\b",
    r"\bseismic shift\b",
    r"\bripple effect\b",
    r"\bnot merely\b.{0,40}\bbut\b",
    r"\borganizations that adapt will (?:win|thrive|succeed)\b",
    r"\bthose that (?:don'?t|do not|fail to) (?:adapt|will fall behind)\b",
]


BANNED_PHRASE_RE = re.compile("|".join(BANNED_PHRASE_PATTERNS), re.IGNORECASE)


HEADING_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)
QUESTION_HEADING_RE = re.compile(r"^##\s+(.+\?)\s*$", re.MULTILINE)
BLOCKQUOTE_RE = re.compile(r"^>\s?(.+)$", re.MULTILINE)
BULLET_LINE_RE = re.compile(r"^\s*[-*]\s+.+$", re.MULTILINE)


FALLBACK_QUOTES = [
    "Governance transforms intelligence into enterprise capability.",
    "Execution is replacing automation as the competitive advantage.",
    "Enterprise value begins where intelligent execution scales.",
    "Competitive advantage now belongs to operational intelligence.",
    "Intelligence becomes valuable through disciplined execution.",
    "Enterprises compete through operational intelligence.",
    "Visibility precedes control in enterprise AI governance.",
    "Unmanaged AI adoption is a governance failure, not a security one.",
]


BANNED_PHRASE_REPLACEMENTS = {
    "as organizations navigate": "as organizations manage",
    "the advent of": "the emergence of",
    "this shift underscores": "this shift confirms",
    "in today's rapidly evolving": "in the current",
    "it is important to note that": "notably,",
    "seismic shift": "structural shift",
    "ripple effect": "downstream effect",
}


REPEATED_SENTENCE_SKELETON_PATTERNS = [
    r"\bthe consequence of this (?:shift|pivot|transition|transformation) is profound\b",
    r"\ba significant strategic shift\b",
    r"\bthis strategic shift\b",
    r"\bin this scenario\b",
    r"\bwhat this means for enterprises\b",
    r"\bthe implications are significant\b",
    r"\bthis represents a significant\b",
    r"\bthe enterprise consequence\b",
]
SKELETON_RE = re.compile("|".join(REPEATED_SENTENCE_SKELETON_PATTERNS), re.IGNORECASE)

STRAY_HEADING_IN_BODY_RE = re.compile(r'^##\s+.+$', re.MULTILINE)

def strip_embedded_headings(text):
    """Section-body rewrites (KPIs, originality notes, concreteness passes,
    etc.) must return prose only -- never a '## ' heading, since that would
    silently create a phantom section invisible to in-memory section counts
    until the markdown is re-parsed. Strip any stray heading line as a
    last-resort guard against the LLM ignoring that instruction."""
    return STRAY_HEADING_IN_BODY_RE.sub('', text).strip()


def find_ai_filler_transitions(body_markdown):
    return sorted(set(m.group(0).lower() for m in AI_FILLER_TRANSITIONS_RE.finditer(body_markdown)))


def find_thesis_restatement_count(sections, thesis_keywords):
    hits = 0
    for s in sections:
        low = s["body"].lower()
        if sum(1 for kw in thesis_keywords if kw in low) >= len(thesis_keywords) - 1:
            hits += 1
    return hits


def find_unsourced_example_markers(sections, sanctioned_case_study_headings=None):
    sanctioned = set(sanctioned_case_study_headings or [])
    markers = []
    for s in sections:
        label = s["heading"] or "(untitled intro/lead section)"
        if label in sanctioned:
            continue
        markers.extend(FABRICATION_MARKER_RE.findall(s["body"]))
    return markers


TRADEOFF_PATTERNS = [
    r"\bvs\.?\b", r"\btrade-?off\b", r"\bbalance(?:d|s)? between\b",
    r"\bat the cost of\b", r"\bcomes at the expense of\b",
]


NUMERIC_CLAIM_RE = re.compile(
    r"\b\d+(?:\.\d+)?\s*(?:%|percent|ms|milliseconds?|mw|kw|megawatts?|"
    r"kilowatts?|x|times)\b",
    re.IGNORECASE,
)


NAMED_FRAMEWORK_MENTION_RE = re.compile(
    r'\b(?:the\s+)?\**([A-Z][A-Za-z0-9\-]*(?:\s+[A-Z][A-Za-z0-9\-]*){1,3})\**'
    r'\s+[Ff]ramework\b'
)

FRAMEWORK_MENTION_STOPWORDS = {
    "this", "that", "these", "those", "what", "which", "such", "it",
}

META_LEAK_LINE_RE = re.compile(
    r'^\s*(Section heading:|Current (content|body):|Article thesis:'
    r'|Other section headings.*)',
    re.IGNORECASE,
)


def find_named_framework_mentions(body_markdown):
    raw_names = []
    for line in body_markdown.split("\n"):
        line = line.strip()
        if not line:
            continue
        for m in NAMED_FRAMEWORK_MENTION_RE.finditer(line):
            name = m.group(1).strip().strip("*").strip()
            if not name:
                continue
            if name.split()[0].lower() in FRAMEWORK_MENTION_STOPWORDS:
                continue
            raw_names.append(name)

    if not raw_names:
        return []

    ordered = sorted(set(raw_names), key=len, reverse=True)
    canonical = []
    for name in ordered:
        if not any(name.lower() in kept.lower() for kept in canonical):
            canonical.append(name)
    return canonical


def autofix_structural_phrases(body_markdown):
    def _replace(match):
        clause = match.group(1).strip()
        return f"{clause}, and"

    return NOT_MERELY_BUT_RE.sub(_replace, body_markdown)


def autofix_banned_phrases(body_markdown):
    fixed = body_markdown
    for banned, replacement in BANNED_PHRASE_REPLACEMENTS.items():
        pattern = re.compile(re.escape(banned), re.IGNORECASE)
        fixed = pattern.sub(replacement, fixed)
    return fixed


def ensure_single_quote(body_markdown, used_quotes=None):
    existing = extract_quotes(body_markdown)

    if len(existing) == 1:
        return body_markdown

    if len(existing) > 1:
        lines = body_markdown.split("\n")
        kept_first = False
        cleaned = []
        for line in lines:
            if BLOCKQUOTE_RE.match(line):
                if not kept_first:
                    cleaned.append(line)
                    kept_first = True
            else:
                cleaned.append(line)
        return "\n".join(cleaned)

    used_quotes = set(used_quotes or [])
    pool = [q for q in FALLBACK_QUOTES if q not in used_quotes] or FALLBACK_QUOTES
    quote_text = pool[0]

    paragraphs = body_markdown.split("\n\n")
    insert_at = min(2, len(paragraphs))
    paragraphs.insert(insert_at, f"> {quote_text}")
    return "\n\n".join(paragraphs)

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

    # --- SEO: weak/generic title detection ---

GENERIC_TITLE_OPENERS_RE = re.compile(
    r'^(how|why|what|the future of|understanding|exploring|navigating)\b',
    re.IGNORECASE,
)

def title_needs_seo_rewrite(title):
    """Flags titles that are structurally weak for SEO: too generic an
    opener with no concrete claim/number/entity, or too long to render
    fully in search results (~60 chars)."""
    if not title:
        return True
    has_number_or_entity = bool(re.search(r'\d', title)) or bool(
        re.search(r'\b[A-Z]{2,}\b', title)  # acronym like EU, AI, GDPR
    )
    weak_opener = bool(GENERIC_TITLE_OPENERS_RE.match(title.strip()))
    too_long = len(title) > 70
    # Weak only if it opens generically AND has no concrete anchor --
    # an acronym/number alone isn't enough to save a title that also runs long.
    return (weak_opener and not has_number_or_entity) or too_long


# --- Readability: overlong paragraphs ---

def find_long_paragraphs(sections, word_limit=90):
    """Long, unbroken paragraphs are the main readability killer for a
    busy-reader business audience. Flags any paragraph over word_limit."""
    flagged = []
    for s in sections:
        for idx, p in enumerate(s["paragraphs"]):
            if len(p.split()) > word_limit:
                flagged.append({"heading": s["heading"], "index": idx})
    return flagged


# --- Strategic Depth / Enterprise Insight: generic recommendation detection ---

CONCRETE_SIGNAL_RE = re.compile(
    r'(\$\d|\d+%|\d+\s*(days|months|weeks)|\b[A-Z][a-z]+(?:soft|Cloud|Labs|Corp|Inc)\b|'
    r'\b(?:STMicroelectronics|OVHcloud|AWS|Azure|GCP|Nvidia)\b)',
)

RECOMMENDATION_HEADING_HINTS = (
    "recommendation", "strategic", "next step", "action", "playbook",
)

def find_generic_recommendation_sections(sections):
    """A 'Strategic Recommendations' section with no named vendor, no
    dollar figure, no percentage, no concrete timeframe reads as
    consulting-deck boilerplate -- low Strategic Depth / Enterprise
    Insight even if the structure is fine. Flags sections that need a
    concreteness pass."""
    flagged = []
    for s in sections:
        h = (s["heading"] or "").lower()
        if not any(hint in h for hint in RECOMMENDATION_HEADING_HINTS):
            continue
        if not CONCRETE_SIGNAL_RE.search(s["body"]):
            flagged.append(s["heading"])
    return flagged


def split_paragraphs(text):
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def _words(text):
    return set(re.findall(r"[a-zA-Z]{3,}", text.lower())) - STOPWORDS


def jaccard(a, b):
    wa, wb = _words(a), _words(b)
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


def seq_similarity(a, b):
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def split_h2_sections(markdown):
    matches = list(HEADING_RE.finditer(markdown))

    if not matches:
        return [{
            "heading": "",
            "body": markdown.strip(),
            "paragraphs": split_paragraphs(markdown),
        }]

    sections = []

    if matches[0].start() > 0:
        intro = markdown[:matches[0].start()].strip()
        if intro:
            sections.append({
                "heading": "",
                "body": intro,
                "paragraphs": split_paragraphs(intro),
            })

    for i, m in enumerate(matches):
        heading = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(markdown)
        body = markdown[start:end].strip()
        sections.append({
            "heading": heading,
            "body": body,
            "paragraphs": split_paragraphs(body),
        })

    return sections

DUPLICATE_CONSECUTIVE_HEADING_RE = re.compile(
    r'(^##[ \t]+(.+?)[ \t]*$)\n+(?:^##[ \t]+\2[ \t]*$\n+)+',
    re.MULTILINE,
)

def collapse_duplicate_consecutive_headings(text):
    """
    Full-article LLM rewrites (e.g. apply_targeted_revision) occasionally
    echo the same H2 heading twice in a row -- '## X\n## X\n...' -- a
    stutter artifact, not a genuine second section. Collapse it
    deterministically.
    """
    return DUPLICATE_CONSECUTIVE_HEADING_RE.sub(r'\1\n', text)


def rebuild_from_sections(sections):
    parts = []
    for s in sections:
        if s["heading"]:
            parts.append(f"## {s['heading']}\n\n{s['body']}".strip())
        else:
            parts.append(s["body"])
    return "\n\n".join(p for p in parts if p.strip())


def paragraph_repetition_pairs(paragraphs, threshold=0.42):
    pairs = []
    n = len(paragraphs)
    for i in range(n):
        if len(paragraphs[i].split()) < 12:
            continue
        for j in range(i + 1, n):
            if len(paragraphs[j].split()) < 12:
                continue
            score = jaccard(paragraphs[i], paragraphs[j])
            if score >= threshold:
                pairs.append((i, j, round(score, 2)))
    return pairs

def strip_stray_framework_mentions(sections, canonical_name):
    if not canonical_name:
        return sections

    canonical_lower = canonical_name.lower()
    canonical_norm = _normalize_framework_heading(canonical_name)

    # First, fix any other section whose HEADING still names a
    # non-canonical framework (e.g. a duplicate "AI Empowerment Strategy
    # Framework" heading left behind after merging). Strip the trailing
    # container word so it no longer reads as its own framework heading.
    for s in sections:
        if not s.get("heading"):
            continue
        if "framework" in s["heading"].lower():
            if _normalize_framework_heading(s["heading"]) != canonical_norm:
                s["heading"] = s["heading"].replace("Framework", "").strip()

    def _maybe_replace(m):
        full_match = m.group(0)
        name = m.group(1).strip().strip("*").strip()
        if not name:
            return full_match

        # If this is the canonical name (or a subset), keep it.
        if name.lower() in canonical_lower or canonical_lower in name.lower():
            return full_match

        # Otherwise, normalize to "the framework" / "this framework"
        pre_context = m.string[max(0, m.start() - 15):m.start()]
        if re.search(r'\b(the|a|an|this)\s*$', pre_context, re.IGNORECASE):
            replacement = "the framework"
        else:
            replacement = "this framework"

        # Preserve initial capital if the original looked like a sentence start.
        if full_match[0].isupper():
            replacement = replacement[0].upper() + replacement[1:]

        return replacement

    for s in sections:
        new_body = NAMED_FRAMEWORK_MENTION_RE.sub(_maybe_replace, s["body"])
        if new_body != s["body"]:
            s["body"] = new_body
            s["paragraphs"] = new_body.split("\n\n")

    return sections

def section_topic_overlap(sections):
    real = [s for s in sections if s["heading"]]
    overlaps = []
    for i in range(len(real)):
        for j in range(i + 1, len(real)):
            score = jaccard(real[i]["body"], real[j]["body"])
            if score >= 0.35:
                overlaps.append((real[i]["heading"], real[j]["heading"], round(score, 2)))
    return overlaps


def count_blockquotes(text):
    return len(BLOCKQUOTE_RE.findall(text))


def extract_quotes(text):
    return [m.strip() for m in BLOCKQUOTE_RE.findall(text)]


def has_framework(sections):
    for s in sections:
        if s["heading"] and _heading_ends_with_framework_keyword(s["heading"]):
            return s["heading"]
    return None



def _heading_ends_with_framework_keyword(heading):
    # A heading that NAMES a framework/model/strategy uses the container
    # word as its final noun ("Intelligent Model Routing Framework",
    # "AI Maturity Model"). A heading that merely DISCUSSES models/strategy
    # buries the word mid-phrase ("...with Model Performance", "Model
    # Routers", "Direct Model Usage") -- that's not a framework heading,
    # it's ordinary prose about the article's subject matter. Checking the
    # trailing word (ignoring punctuation) separates the two cases cheaply
    # without needing full NLP.
    words = re.findall(r"[a-zA-Z']+", heading.lower())
    if not words:
        return False
    return words[-1] in FRAMEWORK_KEYWORDS


def find_all_framework_headings(sections):
    return [
        s["heading"] for s in sections
        if s["heading"]
        and _heading_ends_with_framework_keyword(s["heading"])
        and _is_valid_framework_heading(s["heading"])
    ]


def _find_framework_headings(sections):
    heads = []
    for s in sections:
        heading = s.get("heading")
        if not heading:
            continue
        if "framework" not in heading.lower():
            continue
        if not _is_valid_framework_heading(heading):
            continue
        heads.append(heading)
    return heads

def _is_valid_framework_heading(heading):
    h = (heading or "").strip()
    low = h.lower()

    if not h:
        return False
    if h.endswith("?"):
        return False
    if len(h.split()) < 3:
        return False
    if low in {"this", "that", "these", "those", "what", "framework"}:
        return False
    if low.startswith("this ") or low.startswith("that ") or low.startswith("what "):
        return False
    return True


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
    return sections
def _merge_sections_by_headings(sections, keep_heading, drop_headings, thesis_hint):
    keep_section = None
    drop_set = set(drop_headings)
    collected = []

    for s in sections:
        if s.get("heading") == keep_heading:
            keep_section = s
        elif s.get("heading") in drop_set:
            collected.append(s.get("body", ""))

    if not keep_section:
        return sections

    merged_input = keep_section.get("body", "")
    for body in collected:
        merged_input += "\n\n" + body

    new_sections = []
    replaced = False
    for s in sections:
        if s.get("heading") == keep_heading and not replaced:
            s["body"] = merged_input
            s["paragraphs"] = merged_input.split("\n\n")
            new_sections.append(s)
            replaced = True
        elif s.get("heading") in drop_set:
            continue
        else:
            new_sections.append(s)
    return new_sections

def has_case_study(sections):
    for s in sections:
        label = s["heading"] or "(untitled intro/lead section)"
        body = s["body"].lower()
        if (
            CASE_STUDY_RE.search(body)
            or "illustrative" in label.lower()
            or body.count("challenge") + body.count("approach") + body.count("outcome") >= 2
        ):
            return label
    return None


def find_all_case_study_headings(sections):
    out = []
    for s in sections:
        label = s["heading"] or "(untitled intro/lead section)"
        body = s["body"].lower()
        if (
            CASE_STUDY_RE.search(body)
            or "illustrative" in label.lower()
            or body.count("challenge") + body.count("approach") + body.count("outcome") >= 2
        ):
            out.append(label)
    return out


def find_duplicate_mechanism_case_studies(sections, case_study_headings):
    bodies = {}
    for s in sections:
        label = s["heading"] or "(untitled intro/lead section)"
        if label in case_study_headings:
            bodies[label] = s["body"]

    headings = list(bodies.keys())
    dupes = []
    for i in range(len(headings)):
        for j in range(i + 1, len(headings)):
            score = jaccard(bodies[headings[i]], bodies[headings[j]])
            if score >= 0.30:
                dupes.append((headings[i], headings[j], round(score, 2)))
    return dupes


def has_tradeoff(sections):
    for s in sections:
        low = s["body"].lower()
        if any(re.search(p, low) for p in TRADEOFF_PATTERNS):
            return s["heading"]
    return None


def conclusion_novelty(sections):
    real = [s for s in sections if s["heading"]]
    if len(real) < 2:
        return 0.0

    conclusion_body = real[-1]["body"]
    rest_body = "\n".join(s["body"] for s in real[:-1])
    return round(jaccard(conclusion_body, rest_body), 2)


def _strip_trailing_markdown_emphasis(text):
    """Strip trailing markdown bold/italic markers (**, *, __, _) and
    blockquote '>' prefixes so terminal-punctuation checks look at the
    actual sentence ending, not markdown syntax wrapping it."""
    text = text.rstrip()
    text = re.sub(r"[*_]{1,3}$", "", text).rstrip()
    return text


def conclusion_ends_cleanly(sections):
    real = [s for s in sections if s["heading"]]
    if not real:
        return True
    last_body = real[-1]["body"].strip()
    if not last_body:
        return True
    last_line = last_body.split("\n")[-1].strip()
    if last_line.startswith(">"):
        last_line = last_line.lstrip(">").strip()
    checked_line = _strip_trailing_markdown_emphasis(last_line)
    if checked_line.startswith(("-", "*")) and not checked_line.rstrip().endswith((".", "!", "?")):
        return False
    if checked_line and not checked_line.rstrip().endswith((".", "!", "?", '"', "\u201d")):
        return False
    return True

def find_banned_phrases(body_markdown):
    return sorted(set(m.group(0).lower() for m in BANNED_PHRASE_RE.finditer(body_markdown)))


def extract_title(full_text):
    m = re.search(r"^Title:\s*(.+)$", full_text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def count_real_h2_sections(sections):
    return len([s for s in sections if s["heading"]])


def key_takeaways_is_prose(sections):
    for s in sections:
        if "key takeaway" in s["heading"].lower():
            bullets = BULLET_LINE_RE.findall(s["body"])
            return len(bullets) < 3
    return False


def find_unsourced_numeric_claim_paragraphs(sections):
    flagged = []
    for s in sections:
        for idx, p in enumerate(s["paragraphs"]):
            if NUMERIC_CLAIM_RE.search(p):
                flagged.append({"heading": s["heading"], "index": idx})
    return flagged


def strip_leaked_meta_lines(text):
    lines = text.split("\n")
    cleaned = [l for l in lines if not META_LEAK_LINE_RE.match(l)]
    return "\n".join(cleaned)


def strip_duplicate_heading_echo(sections):
     for s in sections:
        if not s["heading"]:
            continue
        lines = s["body"].split("\n")
        if lines and lines[0].strip():
            first_line = lines[0].strip()
            if seq_similarity(first_line, s["heading"]) >= 0.85:
                remaining = "\n".join(lines[1:]).lstrip("\n")
                s["body"] = remaining
                s["paragraphs"] = remaining.split("\n\n")
     return sections


def find_repeated_closers(sections, threshold=0.55):
    """
    Flags when 3+ sections end on near-identical rhetorical closers.
    """
    real = [s for s in sections if s["heading"]]
    closers = []
    for s in real:
        last_para = s["paragraphs"][-1] if s["paragraphs"] else ""
        last_sentence = last_para.split(". ")[-1].strip()
        if len(last_sentence.split()) >= 6:
            closers.append(last_sentence)

    repeated_groups = 0
    checked = set()
    for i in range(len(closers)):
        if i in checked:
            continue
        group = [i]
        for j in range(i + 1, len(closers)):
            if jaccard(closers[i], closers[j]) >= threshold:
                group.append(j)
        if len(group) >= 3:
            repeated_groups += 1
            checked.update(group)

    return repeated_groups > 0


def find_repeated_sentence_skeletons(body_markdown):
    """
    Detects repeated sentence templates that recur across the same article.
    """
    return sorted(set(m.group(0).lower() for m in SKELETON_RE.finditer(body_markdown)))


def is_question_heading(heading):
    return bool(QUESTION_HEADING_RE.match(f"## {heading}".strip()))


def find_question_headings(sections):
    return [s["heading"] for s in sections if s["heading"] and heading_is_question(s["heading"])]


def heading_is_question(heading):
    return bool(heading and heading.strip().endswith("?"))


def has_direct_answer_lead(sections):
    if not sections:
        return False
    lead = sections[0]
    if lead["heading"]:
        return False
    body = lead["body"].strip()
    if not body:
        return False
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
    if not paragraphs:
        return False
    first = paragraphs[0].lower()
    answer_starters = (
        "yes", "no", "the short answer", "the answer", "in short",
        "directly", "simply put", "the core issue", "the main point",
        "it means", "it is", "the key is", "the result is"
    )
    if not first.startswith(answer_starters):
        if not any(first.startswith(x) for x in ("this", "that", "for enterprises", "for leaders", "agentic ai")):
            return False
    if len(paragraphs[0].split()) > 120:
        return False
    return True


def lead_needs_rewrite(sections):
    return not has_direct_answer_lead(sections)


def has_quick_answers(sections):
    for s in sections:
        h = (s["heading"] or "").lower()
        if "quick answers" in h or "qa" in h or "q&a" in h:
            return True
    return False


def has_executive_summary(sections):
    for s in sections:
        h = (s["heading"] or "").lower()
        if "executive summary" in h or "tl;dr" in h:
            return True
    return False


def detect_question_headings(markdown):
    return QUESTION_HEADING_RE.findall(markdown)


def diagnose_article(body_markdown):
    """
    Single entry point: runs every deterministic structural check and
    returns a report the Editor and Evaluator can both consume.
    """
    sections = split_h2_sections(body_markdown)
    sections = strip_duplicate_heading_echo(sections)

    thin_sections = [
        s["heading"] for s in sections
        if s["heading"] and len(s["paragraphs"]) < 3
    ]

    all_paragraphs = []
    for s in sections:
        all_paragraphs.extend(s["paragraphs"])

    repetitive_pairs = paragraph_repetition_pairs(all_paragraphs)
    section_overlaps = section_topic_overlap(sections)

    quotes = extract_quotes(body_markdown)
    framework_heading = has_framework(sections)
    all_framework_headings = find_all_framework_headings(sections)
    named_framework_mentions = find_named_framework_mentions(body_markdown)
    has_duplicate_frameworks = (
        len(all_framework_headings) > 1
        or len(named_framework_mentions) > 1
    )

    case_study_heading = has_case_study(sections)
    all_case_study_headings = find_all_case_study_headings(sections)
    duplicate_case_studies = find_duplicate_mechanism_case_studies(
        sections, all_case_study_headings
    )

    tradeoff_heading = has_tradeoff(sections)

    conclusion_overlap = conclusion_novelty(sections)
    conclusion_clean = conclusion_ends_cleanly(sections)
    total_h2 = count_real_h2_sections(sections)
    takeaways_needs_bullet_fix = key_takeaways_is_prose(sections)
    unsourced_numeric_claims = find_unsourced_numeric_claim_paragraphs(sections)
    banned_phrases = find_banned_phrases(body_markdown)
    unsourced_example_markers = find_unsourced_example_markers(
        sections, sanctioned_case_study_headings=all_case_study_headings
    )
    question_headings = detect_question_headings(body_markdown)

    return {
        "sections": sections,
        "thin_sections": thin_sections,
        "repetitive_paragraph_pairs": repetitive_pairs,
        "section_overlaps": section_overlaps,
        "quote_count": len(quotes),
        "quotes": quotes,
        "has_framework": bool(framework_heading),
        "framework_heading": framework_heading,
        "all_framework_headings": all_framework_headings,
        "named_framework_mentions": named_framework_mentions,
        "has_duplicate_frameworks": has_duplicate_frameworks,
        "has_case_study": bool(case_study_heading),
        "case_study_heading": case_study_heading,
        "all_case_study_headings": all_case_study_headings,
        "has_duplicate_case_studies": len(duplicate_case_studies) > 0,
        "duplicate_case_study_pairs": duplicate_case_studies,
        "has_tradeoff": bool(tradeoff_heading),
        "tradeoff_heading": tradeoff_heading,
        "conclusion_overlap": conclusion_overlap,
        "conclusion_needs_rewrite": conclusion_overlap >= 0.30,
        "conclusion_ends_cleanly": conclusion_clean,
        "total_h2_count": total_h2,
        "exceeds_h2_ceiling": total_h2 > H2_CEILING,
        "takeaways_needs_bullet_fix": takeaways_needs_bullet_fix,
        "unsourced_numeric_claims": unsourced_numeric_claims,
        "banned_phrases": banned_phrases,
        "unsourced_example_markers": unsourced_example_markers,
        "has_excess_unsourced_examples": len(unsourced_example_markers) > 1,
        "has_repeated_closers": find_repeated_closers(sections),
        "ai_filler_transitions": find_ai_filler_transitions(body_markdown),
        "repeated_sentence_skeletons": find_repeated_sentence_skeletons(body_markdown),
        "has_excess_skeleton_repetition": len(find_repeated_sentence_skeletons(body_markdown)) >= 3,
        "question_headings": question_headings,
        "has_question_headings": len(question_headings) > 0,
        "has_quick_answers": has_quick_answers(sections),
        "has_executive_summary": has_executive_summary(sections),
        "lead_needs_rewrite": lead_needs_rewrite(sections),
        "has_direct_answer_lead": has_direct_answer_lead(sections),
        "long_paragraphs": find_long_paragraphs(sections),
        "generic_recommendation_sections": find_generic_recommendation_sections(sections)
    }