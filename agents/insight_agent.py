import json
import re

from agents.llm_client import client, MODEL_NAME
from agents.history_manager import (
    get_used_frameworks,
    remember_framework,
    get_used_theses,
    remember_thesis,
)
from agents.text_metrics import seq_similarity
from agents.uniqueness_agent import regenerate_framework_name, regenerate_thesis

BRIEF_SYSTEM_PROMPT = """
You are the Editorial Strategy Director of a premium Enterprise AI publication.
Your job is NOT to write an article.
Your job is to produce a structured editorial brief that a writer will follow exactly.
Think like an editor, not a journalist.
The news is evidence. The brief's thesis is the story.
Always select the single most appropriate article archetype from the approved list.
Prioritize originality, strategic thinking, and enterprise relevance over news reporting.
Return ONLY valid JSON. No markdown fences, no preamble, no trailing commentary.
"""

ARTICLE_TYPES = [
    "Executive Briefing", "Market Analysis", "Competitive Strategy",
    "Governance Deep Dive", "Implementation Playbook", "Enterprise Case Study",
    "Technical Architecture", "Future Scenario", "AI Economics", "CIO Advisory",
]

THESIS_COLLISION_THRESHOLD = 0.80

BRIEF_JSON_SCHEMA = """
Return a JSON object with EXACTLY this shape:

{
  "thesis": "<one executive-level paragraph: the larger enterprise transformation this news reveals, why it matters, what decision leaders must make. This is the PRIMARY source of truth for the article.>",
  "executive_decision": "<the single hardest leadership decision this trend creates -- specific, not generic>",
  "search_intent": "<what a CIO/CTO/COO/CFO is actually trying to find out when they search for this topic>",
   "contrarian_view": "<ONE non-obvious, genuinely uncomfortable opposing viewpoint. It must be a FALSIFIABLE CLAIM that a reasonable, informed executive would actually disagree with -- not a hedge, not 'consider multiple options', not generic risk-mitigation advice. Test: if 80%+ of CIOs would nod along without objection, it is NOT contrarian -- rewrite it. Name the specific assumption being challenged, why the counter-argument is legitimate, and the enterprise conditions under which it is correct.>",
  "second_order_insight": "<ONE durable strategic implication that is STRUCTURALLY DIFFERENT from the thesis and the contrarian_view -- not a restatement or extension of either. This should answer: 'if this trend continues for 2-3 more years, what changes that isn't obvious today?' Test: if this insight could be swapped into a different article about a different company in the same industry without changing a word, it's too generic -- rewrite it to be specific to THIS news. Examples of the right shape: a shift in who captures the value (not who adopts the tech), a second-order market structure change, a capability that becomes table-stakes vs. one that becomes differentiating, a constraint that becomes binding only after mass adoption.>",
  "key_questions": ["<question the reader should still be asking after reading>", "..."],
  "article_flow": ["<ordered list of section beats, e.g. 'Open on the strategic shift, not the announcement'>", "<one narrow enterprise problem>", "<one original framework>", "<one enterprise case study>", "<the contrarian view, developed>", "<practical executive recommendation>", "<quick answers block>", "<decisive strategic conclusion>"],
  "framework": {
    "name": "<2-5 word Title Case framework name>",
    "layers": ["<layer 1>", "<layer 2>", "<layer 3>", "<layer 4 optional>"],
    "explanation": "<brief explanation of the framework and what makes it structurally different from existing paradigms>"
  },
  "real_bottleneck": "<the actual, specific enterprise pain this news exposes -- e.g. GPU availability, spot preemption, egress costs, scheduling complexity, token pricing opacity. Not generic 'AI scaling challenges'.>",
  "governance_angle": "<which governance/regulatory framework intersects with this topic (EU AI Act, HIPAA, SOC 2, data sovereignty, financial services AI regulation) and why. State the most relevant category even if indirect. Do not fabricate requirements.>",
  "article_type": "<exactly one of: """ + ", ".join(ARTICLE_TYPES) + """>",
  "keywords": {
    "primary": ["<5 high-volume executive search terms>"],
    "long_tail": ["<8 long-tail phrases, at least 3 from infrastructure/FinOps/governance/platform domains>"],
    "semantic": ["<10 related concepts and synonyms>"]
  },
  "title_ideas": ["<5 editorial title options>"],
  "editorial_summary": "<one sentence summarizing today's editorial direction>"
}

Rules:
- "thesis" must be genuinely opinionated and specific -- not a restatement of the news.
- "contrarian_view" must challenge the article's primary recommendation, not a minor detail.
- "contrarian_view" must NOT be generic risk-management advice (e.g. "diversify suppliers", "assess risk before deciding", "balance cost and security"). It must take an actual side on a real disagreement -- something a credible expert would push back on.
- "second_order_insight" must be structurally distinct from "thesis" and "contrarian_view" -- it must not simply restate either in different words. It must NOT use generic trade-off framing ("balance X with Y", "companies must weigh A against B") -- that pattern belongs to contrarian_view if anywhere, not here. This field should read like a prediction or structural observation, not advice.
- "article_flow" must have 6-9 entries, ordered, each a short instruction not a full sentence.
- "article_flow" must include exactly ONE entry for "the second-order insight, developed as its own section" -- do not create more than one trade-off/dilemma-framed section in the flow.
- "article_type" must be copied exactly from the approved list, case-sensitive.
- Do not fabricate statistics, named companies, or regulatory requirements not credibly implied by the research.
"""


def _strip_json_fences(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _fix_framework_collision(brief):
    framework = brief.get("framework") or {}
    name = (framework.get("name") or "").strip()
    if not name:
        return brief

    history = get_used_frameworks()
    if history and max(seq_similarity(name, h) for h in history) >= 0.80:
        thesis_hint = brief.get("thesis", "")[:300]
        new_name = regenerate_framework_name(thesis_hint, history).strip()
        brief["framework"]["name"] = new_name
        remember_framework(new_name)
    else:
        remember_framework(name)

    return brief


def _fix_thesis_collision(brief):
    """Checks the brief's thesis against recently used theses BEFORE any
    article is written. This is the cheapest point to catch repetition --
    regenerating a thesis paragraph costs one LLM call, versus regenerating
    an entire article after the fact."""
    thesis = (brief.get("thesis") or "").strip()
    if not thesis:
        return brief

    history = get_used_theses()
    if history and max(seq_similarity(thesis, h) for h in history) >= THESIS_COLLISION_THRESHOLD:
        context_hint = (
            brief.get("editorial_summary", "")
            or brief.get("real_bottleneck", "")
            or thesis[:200]
        )
        new_thesis = regenerate_thesis(context_hint, history).strip()
        brief["thesis"] = new_thesis
        remember_thesis(new_thesis)
    else:
        remember_thesis(thesis)

    return brief


def _validate_brief(brief):
    required_top = [
        "thesis", "executive_decision", "search_intent", "contrarian_view",
        "second_order_insight", "key_questions", "article_flow", "framework",
        "real_bottleneck", "governance_angle", "article_type", "keywords", "title_ideas",
    ]
    missing = [k for k in required_top if k not in brief]
    if missing:
        raise ValueError(f"Brief missing required fields: {missing}")

    if brief["article_type"] not in ARTICLE_TYPES:
        # tolerate near-matches (case/whitespace) before giving up
        matched = next(
            (t for t in ARTICLE_TYPES if t.lower() == str(brief["article_type"]).strip().lower()),
            None,
        )
        if matched:
            brief["article_type"] = matched
        else:
            raise ValueError(f"Invalid article_type: {brief['article_type']!r}")

    return brief


def generate_insight(research_package):
    """
    Returns a structured brief (dict) -- see BRIEF_JSON_SCHEMA -- instead of
    a raw text blob. This is the single source of truth the Writer consumes.
    """
    prompt = f"""
RESEARCH PACKAGE

{research_package}


EXECUTIVE ANALYSIS


Before producing the brief, think through:
1. What long-term enterprise shift does this news reveal?
2. Which business assumption is changing?
3. What executive decision becomes harder?
4. What is the single strongest strategic insight hidden inside this news?
5. What is the REAL operational bottleneck this news exposes?
6. What governance or regulatory constraint intersects with this shift?


OUTPUT

{BRIEF_JSON_SCHEMA}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": BRIEF_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )

    raw = response.choices[0].message.content
    cleaned = _strip_json_fences(raw)

    try:
        brief = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Insight agent returned invalid JSON: {e}\n\nRaw output:\n{raw[:1000]}"
        ) from e

    brief = _validate_brief(brief)
    brief = _fix_framework_collision(brief)
    brief = _fix_thesis_collision(brief)

    print("INSIGHT AGENT COMPLETE (structured brief)")
    return brief


if __name__ == "__main__":
    sample = """
Google announced a $1B investment in AI infrastructure across Africa.
"""
    print(json.dumps(generate_insight(sample), indent=2))