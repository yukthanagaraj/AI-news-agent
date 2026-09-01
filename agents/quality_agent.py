import re

from agents.llm_client import client, MODEL_NAME
from agents.quality_parts.title import TITLE_CHECK_RULES
from agents.quality_parts.quote import QUOTE_CHECK_RULES
from agents.quality_parts.faq import FAQ_CHECK_RULES
from agents.quality_parts.duplicate import DUPLICATE_CHECK_RULES
from agents.quality_parts.structure import STRUCTURE_CHECK_RULES
from agents.quality_parts.article_length import LENGTH_CHECK_RULES
from agents.quality_parts.seo_rules import SEO_CHECK_RULES
from agents.quality_parts.aeo_rules import AEO_CHECK_RULES
from agents.quality_parts.evidence_rules import EVIDENCE_CHECK_RULES
from agents.quality_parts.entities_rules import ENTITY_CHECK_RULES
from agents.quality_parts.executive_rules import EXECUTIVE_CHECK_RULES
from agents.quality_parts.originality_rules import ORIGINALITY_CHECK_RULES
from agents.quality_parts.tradeoffs_rules import TRADEOFF_CHECK_RULES
from agents.quality_parts.implementation_rules import IMPLEMENTATION_CHECK_RULES
from agents.quality_parts.framework_rules import FRAMEWORK_CHECK_RULES

# The 5 dimensions that gate publication (per editorial plan).
# Everything else in this file is informational/diagnostic only.
QUALITY_THRESHOLD = 8.0  # out of 10, on the computed gating score


def quality_check(title, article):

    prompt = f"""
TITLE

{title}

ARTICLE

{article}

{TITLE_CHECK_RULES}

{QUOTE_CHECK_RULES}

{STRUCTURE_CHECK_RULES}

{LENGTH_CHECK_RULES}

{SEO_CHECK_RULES}

{AEO_CHECK_RULES}

{FAQ_CHECK_RULES}

{DUPLICATE_CHECK_RULES}

{EVIDENCE_CHECK_RULES}

{ENTITY_CHECK_RULES}

{EXECUTIVE_CHECK_RULES}

{ORIGINALITY_CHECK_RULES}

{TRADEOFF_CHECK_RULES}

{IMPLEMENTATION_CHECK_RULES}

{FRAMEWORK_CHECK_RULES}


OUTPUT ONLY

Evaluate the article objectively.

Assign realistic scores.

Scoring Guide

10 = Publication quality

8-9 = Strong

6-7 = Average

Below 6 = Weak

==================================================
GATING SCORES (these five decide publish/revise -- score carefully and honestly)
==================================================

Originality Score: X/10
(Does this contain a genuinely non-obvious insight, not something any AI publication could produce from the same news?)

Executive Insight Score: X/10
(Would a CIO/CTO/COO/CFO learn something that changes a decision they're facing?)

SEO Score: X/10

AEO Score: X/10

Evidence Score: X/10
(Are claims backed by sourced, specific enterprise detail rather than vague or invented examples?)

Actionability Score: X/10
(Can a reader actually act on this article -- a decision framework, a checklist, a clear recommendation -- or is it purely descriptive?)

Strategic Depth Score: X/10
(Does this go beyond the immediate news to a durable, non-obvious strategic implication -- or does it stay at the surface level of "this trend matters, plan ahead"?)

Readability Score: X/10
(Clear sentence structure, no bloated corporate-speak, scannable for a time-pressed executive -- penalize passive voice overload and vague hedging language.)
==================================================
ADDITIONAL DIAGNOSTIC SCORES (informational only, do not affect gating)
==================================================

Title Score:
/10

Quote Score:
/10

Quote Result:
PASS or FAIL

Reason:
<one sentence>

Structure Score:
/10

Length Score:
/10

Entity Authority Score:
/10

Trade-off Score:
/10

Implementation Score:
/10

Framework Score:
/10

FAQ Score:
/10

Duplicate Score:
/10

Improvement Suggestions

Provide ONLY the five highest-impact improvements.

Use concise bullet points.

Do NOT rewrite the article.

Do NOT explain the scoring.

Return ONLY this format.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": """
You are the Chief Editorial Reviewer for a premium Enterprise AI publication.

Your responsibility is to evaluate publication quality -- not to rewrite the article.

Be objective. Do not inflate scores. Score exactly according to the supplied rubric.

The five GATING SCORES (Originality, Executive Insight, SEO, AEO, Evidence, Actionability)
matter most -- these determine whether the article is ready to publish. Score them with
real discrimination: an article that merely restates the news with competent prose should
score in the 4-6 range on Originality and Actionability, not 8+. Reserve 8+ for articles
that would genuinely stand out against Harvard Business Review, MIT Technology Review, or
The Information.

Return ONLY the requested format.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    print("QUALITY CHECK COMPLETE")

    return response.choices[0].message.content

_GATING_FIELD_PATTERNS = {
    "originality": r"Originality Score:\s*\n?\s*(\d+(?:\.\d+)?)\s*/\s*10",
    "executive_insight": r"Executive Insight Score:\s*\n?\s*(\d+(?:\.\d+)?)\s*/\s*10",
    "seo": r"SEO Score:\s*\n?\s*(\d+(?:\.\d+)?)\s*/\s*10",
    "aeo": r"AEO Score:\s*\n?\s*(\d+(?:\.\d+)?)\s*/\s*10",
    "evidence": r"Evidence Score:\s*\n?\s*(\d+(?:\.\d+)?)\s*/\s*10",
    "actionability": r"Actionability Score:\s*\n?\s*(\d+(?:\.\d+)?)\s*/\s*10",
    "strategic_depth": r"Strategic Depth Score:\s*\n?\s*(\d+(?:\.\d+)?)\s*/\s*10",
    "readability": r"Readability Score:\s*\n?\s*(\d+(?:\.\d+)?)\s*/\s*10",
}

def extract_improvement_suggestions(quality_data):
    """Pulls the bullet points under 'Improvement Suggestions' out of
    quality_check()'s text output, so the retry pass can act on the
    evaluator's actual critique instead of guessing what's weak."""
    m = re.search(r"Improvement Suggestions:?\s*\n(.*)", quality_data, re.DOTALL | re.IGNORECASE)
    if not m:
        return []
    block = m.group(1)
    bullets = re.findall(r"^-+\s*(.+)$", block, re.MULTILINE)
    return [b.strip() for b in bullets if b.strip()][:5]

def extract_gating_score(quality_data):
    """
    Parses the 5 gating dimensions out of quality_check()'s text output and
    computes a single numeric score (out of 10) in code -- rather than
    trusting an LLM-declared PASS/FAIL. SEO and AEO are averaged together
    into one 'SEO/AEO' component per the editorial plan, so the final
    average is over 5 conceptual dimensions.

    Returns (gating_score: float, breakdown: dict). If a field can't be
    parsed, it's treated as 0 for that dimension (fails safe -- triggers
    a revision pass rather than silently passing).
    """
    parsed = {}
    for key, pattern in _GATING_FIELD_PATTERNS.items():
        m = re.search(pattern, quality_data, re.IGNORECASE)
        parsed[key] = float(m.group(1)) if m else 0.0

    seo_aeo = (parsed["seo"] + parsed["aeo"]) / 2

    dimensions = {
        "originality": parsed["originality"],
        "executive_insight": parsed["executive_insight"],
        "seo_aeo": seo_aeo,
        "evidence": parsed["evidence"],
        "actionability": parsed["actionability"],
        "strategic_depth": parsed["strategic_depth"],
        "readability": parsed["readability"],
    }
    gating_score = round(sum(dimensions.values()) / len(dimensions), 2)

    breakdown = {**dimensions, "raw": parsed}
    return gating_score, breakdown