# from agents.prompt_parts.title_rules import TITLE_RULES
# from agents.prompt_parts.article_style import ARTICLE_STYLE
# from agents.prompt_parts.article_structure import ARTICLE_STRUCTURE
# from agents.prompt_parts.quote_rules import QUOTE_RULES
# from agents.prompt_parts.information_density import INFORMATION_DENSITY
# from agents.prompt_parts.evidence import EVIDENCE_RULES
# from agents.prompt_parts.governance_rules import GOVERNANCE_RULES
# from agents.prompt_parts.sourcing_rules import SOURCING_RULES
# from agents.prompt_parts.aeo_lead_rules import AEO_LEAD_RULES
# from agents.prompt_parts.decision_matrix_rules import DECISION_MATRIX_RULES
# from agents.history_manager import (
#     get_used_titles,
#     get_used_quotes,
#     get_used_frameworks,
#     get_used_section_titles,
#     get_used_visual_concepts,
# )

# def build_prompt(news, insight, previous_titles, template, article_type):
#     used_titles = "\n".join((previous_titles or [])[-3:])
#     memory_titles = "\n".join(get_used_titles()[-2:])
#     memory_quotes = "\n".join(get_used_quotes()[-2:])
#     memory_frameworks = "\n".join(get_used_frameworks()[-2:])
#     memory_sections = "\n".join(get_used_section_titles()[-2:])
#     memory_visuals = "\n".join(get_used_visual_concepts()[-2:])

#     # Inject governance rules for governance-relevant archetypes only
#     GOVERNANCE_ARCHETYPES = {
#         "Technical Architecture",
#         "Governance Deep Dive",
#         "Implementation Playbook",
#         "CIO Advisory",
#         "Enterprise Case Study",
#     }
#     governance_section = ""
#     if article_type in GOVERNANCE_ARCHETYPES:
#         governance_section = f"""
# ==================================================
# GOVERNANCE, SECURITY & REGULATORY CONTEXT
# ==================================================

# {GOVERNANCE_RULES}
# """

#     return f"""
# You are a senior Enterprise AI strategist writing premium executive intelligence articles.

# ==================================================
# EDITORIAL THESIS
# ==================================================

# {insight}

# This editorial insight is the PRIMARY source of truth.
# The article must be built around this thesis.
# The supplied news is ONLY supporting evidence.
# Do NOT summarize the news.

# Instead:

# • explain WHY this matters
# • explain WHY it is changing
# • explain WHY executives should care

# The article should teach the thesis, not the news.

# ==================================================
# RESEARCH EVIDENCE
# ==================================================

# {news}

# ==================================================
# PREVIOUS TITLES
# ==================================================

# {used_titles}

# ==================================================
# LONG-TERM MEMORY
# ==================================================

# USED TITLES

# {memory_titles}

# USED QUOTES

# {memory_quotes}

# USED FRAMEWORKS

# {memory_frameworks}

# USED SECTION TITLES

# {memory_sections}

# USED VISUAL CONCEPTS

# {memory_visuals}

# Never generate content that closely resembles any of the above.
# Avoid repeating titles, quotes, frameworks, section headings, or visual concepts.
# Generate fresh editorial content every time.

# ==================================================
# WRITING OBJECTIVE
# ==================================================

# Imagine this article will be published six months from now.
# It should still be valuable.
# Avoid describing today's announcement.
# Instead explain the larger business pattern revealed by today's news.
# Readers should finish the article with one memorable executive insight.

# Do not simply report events.
# Teach executives how the market is changing.

# ==================================================
# ARTICLE TEMPLATE
# ==================================================

# Use this template as guidance.

# {template}

# ==================================================
# ARTICLE ARCHETYPE
# ==================================================

# Today's article type:

# {article_type}

# The article MUST follow the selected archetype.
# Do not mix multiple archetypes.

# The selected archetype takes priority over the default article structure.

# ==================================================
# TITLE RULES
# ==================================================

# {TITLE_RULES}

# ==================================================
# TITLE SELECTION
# ==================================================

# The Editorial Insight already contains FIVE suggested titles.
# Select the strongest one.
# Only create a new title if all five suggested titles are weak.

# Avoid repeatedly beginning titles with:
# Enterprise, AI, Future, Operational, Digital, Intelligent.

# The title should communicate the article's thesis rather than summarize the news.

# ==================================================
# ARTICLE STYLE
# ==================================================

# {ARTICLE_STYLE}

# ==================================================
# QUOTE RULES
# ==================================================

# {QUOTE_RULES}

# ==================================================
# INFORMATION DENSITY
# ==================================================

# {INFORMATION_DENSITY}

# ==================================================
# ARTICLE STRUCTURE
# ==================================================

# {ARTICLE_STRUCTURE}

# ==================================================
# EVIDENCE STANDARDS
# ==================================================

# {EVIDENCE_RULES}

# ==================================================
# SOURCING RULES
# ==================================================

# {SOURCING_RULES}

# ==================================================
# AEO LEAD RULES
# ==================================================

# {AEO_LEAD_RULES}

# ==================================================
# DECISION FRAMEWORK RULES
# ==================================================

# {DECISION_MATRIX_RULES}

# {governance_section}
# ==================================================
# ORIGINALITY
# ==================================================

# ==================================================
# ORIGINALITY
# ==================================================

# Every article should:
# - introduce at least one fresh executive insight
# - avoid repeating ideas across sections
# - explain business consequences instead of technology features
# - include one realistic enterprise scenario
# - include one practical recommendation
# - substantively develop the CONTRARIAN VIEW from the editorial thesis
#   above into its own paragraph or subsection — do not just acknowledge
#   it exists in passing. A contrarian view mentioned in one clause and
#   never returned to does not count.

# Treat the research as evidence, not the story.
# Do not summarize the news.
# Build a strategic executive analysis.

# ==================================================
# FINAL WRITER VALIDATION
# ==================================================

# Before returning the article verify:
# ✓ The article teaches the editorial thesis — not the news.
# ✓ The news supports the thesis as evidence only.
# ✓ The introduction opens with a direct, opinionated executive thesis claim.
# ✓ Every section introduces a different executive lesson.
# ✓ At least one section covers GPU scheduling, FinOps, observability, governance, or data platform strategy.
# ✓ The article contains ONE contrarian counter-argument that challenges the primary recommendation.
# ✓ No banned clichés appear anywhere (game-changer, cornerstone, testament to, ever-evolving,
#   unprecedented, paradigm shift, holistic approach, transformative journey, cutting-edge).
# ✓ No anonymized enterprise proxies appear ("a global bank", "a mid-sized firm").
# ✓ Named enterprises from the research are used when available.
# ✓ No fabricated statistics appear — all numbers trace to the research.
# ✓ A 2-3 sentence direct-answer summary appears immediately under the title, before the first H2.
# ✓ Every H2 phrased as a question answers it directly in the first 1-2 sentences before elaborating.
# ✓ If the article discusses partnership, vendor, or build-vs-buy decisions, it includes a practical
#   decision artifact (scorecard, comparison table, or lock-in/exit checklist) — not just narrative advice.
# ✓ The article type is clearly reflected.
# ✓ The title comes from the Insight Agent whenever possible.
# ✓ The title is different from recent articles.
# ✓ The conclusion delivers a decisive strategic thesis, not a summary of prior points.
# ✓ The article feels like a premium enterprise intelligence editorial, not an AI-generated summary.

# ==================================================
# OUTPUT FORMAT
# ==================================================

# Return ONLY the following format.

# Title: <title>

# Source URL: <source url>

# Image Prompt: <25–40 word editorial illustration prompt>

# Blog:

# <complete markdown article>

# The article must use Markdown.
# Use Markdown H2 (##) headings for every major section.
# Do not use plain text, numbered, or bold-only headings.
# """

# agents/prompt_builder.py
from agents.prompt_parts.title_rules import TITLE_RULES
from agents.prompt_parts.article_style import ARTICLE_STYLE
from agents.prompt_parts.article_structure import ARTICLE_STRUCTURE
from agents.prompt_parts.quote_rules import QUOTE_RULES
from agents.prompt_parts.information_density import INFORMATION_DENSITY
from agents.prompt_parts.evidence import EVIDENCE_RULES
from agents.prompt_parts.governance_rules import GOVERNANCE_RULES
from agents.prompt_parts.sourcing_rules import SOURCING_RULES
from agents.prompt_parts.aeo_lead_rules import AEO_LEAD_RULES
from agents.prompt_parts.decision_matrix_rules import DECISION_MATRIX_RULES
from agents.history_manager import (
    get_used_titles,
    get_used_quotes,
    get_used_frameworks,
    get_used_section_titles,
    get_used_visual_concepts,
)


LUVANA_PROMPT_HEADER = """
You are writing for Luvana AI Journal.

Write a premium enterprise intelligence article in Luvana's editorial voice:
- original
- opinion-led
- sharp
- decision-useful
- framework-driven
- non-generic
- highly structured
- tailored for CIOs, CTOs, COOs, CFOs, and enterprise leaders

The article must focus on agentic AI only.
Do not drift into broad AI transformation, generic digital transformation, cloud strategy, finance strategy, customer engagement, or unrelated enterprise AI themes.
Luvana articles should feel like strategic editorial analysis, not news summaries.
Treat the news as evidence. The brief's thesis is the story.
Luvana's editorial voice is NOT interchangeable with generic enterprise-consulting content. Avoid the "McKinsey deck" register: sentences that could be produced by any AI writing about any company's tech strategy. Instead, write with a specific, opinionated point of view -- the kind an editor would defend in a room full of skeptical executives, not the kind that hedges to please everyone. When in doubt, cut the sentence that sounds safest and replace it with the one that sounds like it could be wrong.
"""

GOVERNANCE_ARCHETYPES = {
    "Technical Architecture",
    "Governance Deep Dive",
    "Implementation Playbook",
    "CIO Advisory",
    "Enterprise Case Study",
    "Agentic AI Strategy",
    "Agentic AI Governance",
    "Agentic AI Operations",
}

DECISION_MATRIX_ARCHETYPES = {
    "Technical Architecture", "Implementation Playbook", "CIO Advisory", "Agentic AI Strategy",
}


def _render_brief(brief):
    """Render the structured brief as explicit, labeled fields -- not prose --
    so the Writer reads it as instructions, not as something to paraphrase."""

    key_questions = "\n".join(f"- {q}" for q in brief.get("key_questions", []))
    article_flow = "\n".join(f"{i+1}. {beat}" for i, beat in enumerate(brief.get("article_flow", [])))

    framework = brief.get("framework", {}) or {}
    framework_layers = "\n".join(f"- {layer}" for layer in framework.get("layers", []))

    kw = brief.get("keywords", {}) or {}
    primary_kw = ", ".join(kw.get("primary", []))
    long_tail_kw = ", ".join(kw.get("long_tail", []))

    title_ideas = "\n".join(f"- {t}" for t in brief.get("title_ideas", []))

    return f"""
THESIS (primary source of truth -- the article must be built around this)
{brief.get("thesis", "")}

EXECUTIVE DECISION (the hardest leadership decision this trend creates)
{brief.get("executive_decision", "")}

SEARCH INTENT (what the reader is actually trying to find out)
{brief.get("search_intent", "")}

CONTRARIAN VIEW (must be developed into its own paragraph or subsection -- not mentioned once and dropped)
{brief.get("contrarian_view", "")}

SECOND-ORDER INSIGHT (must be its own H2 section, distinct from the thesis and the contrarian view -- this is the article's strategic-depth payload)
{brief.get("second_order_insight", "")}

KEY QUESTIONS (should linger in the reader's mind)
{key_questions}

ARTICLE FLOW (follow this beat order)
{article_flow}

FRAMEWORK (create exactly this one framework, as a single named H2 section -- MANDATORY)
Name: {framework.get("name", "")}
Layers:
{framework_layers}
Explanation: {framework.get("explanation", "")}
CRITICAL: This framework MUST appear as its own "## {framework.get("name", "")}" heading with its own dedicated section body. Do NOT describe it in passing inside another section's prose -- that is a structural failure.

REAL BOTTLENECK (the specific enterprise pain this news exposes)
{brief.get("real_bottleneck", "")}

GOVERNANCE ANGLE
{brief.get("governance_angle", "")}

SUGGESTED TITLES (select the strongest one; only write a new title if these are weak)
{title_ideas}

PRIMARY KEYWORDS: {primary_kw}
LONG-TAIL KEYWORDS: {long_tail_kw}
""".strip()


def build_prompt(news, brief, previous_titles, template, article_type):
    used_titles = "\n".join((previous_titles or [])[-3:])
    memory_titles = "\n".join(get_used_titles()[-2:])
    memory_quotes = "\n".join(get_used_quotes()[-2:])
    memory_frameworks = "\n".join(get_used_frameworks()[-2:])
    memory_sections = "\n".join(get_used_section_titles()[-2:])
    memory_visuals = "\n".join(get_used_visual_concepts()[-2:])

    governance_section = ""
    if article_type in GOVERNANCE_ARCHETYPES:
        governance_section = f"""

GOVERNANCE, SECURITY & REGULATORY CONTEXT
{GOVERNANCE_RULES}
"""

    decision_matrix_section = ""
    if article_type in DECISION_MATRIX_ARCHETYPES:
        decision_matrix_section = f"""

DECISION MATRIX / ARCHITECTURE TRADE-OFFS
{DECISION_MATRIX_RULES}
"""

    brief_block = _render_brief(brief)

    return f"""
{LUVANA_PROMPT_HEADER}


EDITORIAL BRIEF
{brief_block}

This brief is the PRIMARY source of truth.
The article must be built around the thesis, contrarian view, and article flow above.
The supplied news is ONLY supporting evidence.
Do NOT summarize the news.
Do NOT introduce a second framework, a second case study, or ideas absent from this brief.

The article should teach the thesis, not the news.

==================================================
RESEARCH EVIDENCE
==================================================

{news}

==================================================
PREVIOUS TITLES
==================================================

{used_titles}

==================================================
LONG-TERM MEMORY
==================================================

USED TITLES

{memory_titles}

USED QUOTES

{memory_quotes}

USED FRAMEWORKS

{memory_frameworks}

USED SECTION TITLES

{memory_sections}

USED VISUAL CONCEPTS

{memory_visuals}

Never generate content that closely resembles any of the above.
Avoid repeating titles, quotes, frameworks, section headings, visual concepts, or conclusion styles.
Generate fresh editorial content every time.


WRITING OBJECTIVE


Imagine this article will be published six months from now.
It should still be valuable.
Do not write a news recap.
Do not describe the announcement first.
Instead follow the ARTICLE FLOW in the brief above.

Readers should finish the article with one memorable executive insight and one practical decision framework.


ARTICLE TEMPLATE


Use this template as guidance.

{template}


ARTICLE ARCHETYPE

Today's article type:

{article_type}

The article MUST follow the selected archetype.
Do not mix multiple archetypes.
The selected archetype takes priority over default article structure.


TITLE RULES


{TITLE_RULES}


TITLE SELECTION
Select the strongest title from the brief's SUGGESTED TITLES.
Only create a new title if the suggested titles are weak.

Avoid repeatedly beginning titles with:
Enterprise, AI, Future, Operational, Digital, Intelligent, Transforming, Embracing, Rethinking, Navigating, Balancing.

The title should communicate the thesis rather than summarize the news.
The title must be specific enough that it could not easily fit five unrelated articles.


ARTICLE STYLE
{ARTICLE_STYLE}

Style requirements for this article:
- Luvana perspective
- premium enterprise editorial tone
- concise but high-information prose
- no generic AI phrasing
- no recycled thought leadership language
- no overexplaining basic AI concepts
- no padding
- no repetitive thesis restatement


QUOTE RULES
{QUOTE_RULES}

The article MUST contain exactly one original blockquote, formatted as a markdown blockquote starting with "> " on its own line (e.g. "> The real bottleneck isn't compute -- it's who controls the queue.").
The quote must feel like a Luvana editorial line, not a motivational slogan.
It should support the thesis and be memorable.
This is a hard structural requirement -- an article with zero blockquotes or a quote not using "> " syntax will fail validation.


INFORMATION DENSITY

{INFORMATION_DENSITY}

The article should:
- introduce one new strategic idea per paragraph
- avoid repeated phrasing across sections
- avoid filler
- keep every section information-dense
- prefer specific business consequences over broad technology claims


ARTICLE STRUCTURE
{ARTICLE_STRUCTURE}

Structure requirements:
- start with a direct thesis summary immediately after the title
- use markdown H2 headings for every major section
- include one narrow enterprise problem only
- include the ONE framework named in the brief -- do not rename or duplicate it
- include one enterprise case study only
- include the contrarian view from the brief, developed into its own paragraph or subsection
- include the SECOND-ORDER INSIGHT from the brief as its own dedicated H2 section (not folded into the contrarian view, framework, or recommendations section). This section should read as a forward-looking strategic observation, not advice -- avoid phrasing it as "companies should..." and instead phrase it as "what changes is..." or "the second-order effect is..."
- do NOT create more than ONE "balancing X against Y" or "trade-off between A and B" style section anywhere in the article. If the contrarian view and a later section both want to use that framing, only the contrarian view section may use it -- rewrite the other into a direct statement instead.
- include one practical executive recommendation section
- include one short Quick Answers or FAQ-style block
- end with a decisive strategic conclusion, not a summary
- the framework must appear as exactly one named H2 section
- do not title the framework section as a question
- do not create partial framework variants in other headings
- do not repeat the framework name in abbreviated form
- the framework heading must be the only framework heading in the article


AEO LEAD RULES

{AEO_LEAD_RULES}

The opening should be answer-first and should directly address the brief's SEARCH INTENT.
The article should support answer engines with:
- direct claims
- clear section headers
- concise explanation before elaboration
- short definition-like phrasing where useful
- a quick-answer block near the end that addresses the brief's KEY QUESTIONS

EVIDENCE STANDARDS
{EVIDENCE_RULES}

Every major section must contain at least one sourced enterprise element whenever the supplied research supports it.
Do not invent numbers or metrics and present them as real, verified outcomes.
If a case study is illustrative rather than drawn from the supplied research, any numbers in it MUST be explicitly labeled as illustrative (e.g. "in a representative scenario, a firm following this approach might reduce X by roughly 30-40%") -- never state a precise invented percentage as fact.
Do not use vague example language where a specific enterprise detail is available.
Do not refer to unnamed companies as "a major [type] firm," "a leading [type]," "a global [type]" -- if the research doesn't name a real company, use a clearly-labeled hypothetical framing instead (e.g. "consider a mid-market financial services firm evaluating this trade-off").


SOURCING RULES
{SOURCING_RULES}

Use the supplied research as evidence, not as the story.
Do not summarize the news.
Do not over-cite or convert the article into a source roundup.
Integrate sources naturally in executive analysis.


GOVERNANCE CONTEXT
{governance_section}


DECISION FRAMEWORK RULES
{decision_matrix_section}

If the article discusses build-vs-buy, vendor selection, supplier strategy, partnership strategy, procurement, or architecture choices:
- include a practical decision artifact AS AN ACTUAL MARKDOWN TABLE, not a prose description of one
- the table must have at least 3 rows (options/scenarios) and 3 columns (criteria) with real comparative content
- do not rely on narrative advice alone -- a paragraph describing what a scorecard "could" include does not satisfy this requirement


ORIGINALITY
Every article should:
- introduce at least one fresh executive insight beyond the brief's thesis
- avoid repeating ideas across sections
- explain business consequences instead of technology features
- include one realistic enterprise scenario
- include one practical recommendation
- substantively develop the contrarian view into its own paragraph or subsection

ENTERPRISE INSIGHT SPECIFICITY TEST
Before finishing each major section, apply this test: "Could this exact paragraph appear unchanged in a different article about a different company in the same industry?" If yes, that paragraph is too generic -- revise it to include something that only makes sense given THIS specific news item: an actual mechanism (not just "AI improves efficiency" but what specifically changes and why), a specific named constraint, or a specific numeric threshold from the research. Generic strategic-consulting language ("organizations must align," "leaders should prioritize") should never appear more than once per article -- if you find yourself reaching for it a second time, replace it with something concrete instead.

The framework must remain singular and canonical. Do not split it into question-style or abbreviated variants.

A contrarian view mentioned once and never returned to does not count.

Treat the research as evidence, not the story.
Do not summarize the news.
Build a strategic executive analysis around the brief.

FINAL WRITER VALIDATION
Before returning the article verify:
✓ The article teaches the brief's thesis -- not the news.
✓ The news supports the thesis as evidence only.
✓ The introduction opens with a direct, opinionated executive thesis claim.
✓ A 2-3 sentence direct-answer summary appears immediately under the title, before the first H2.
✓ Every H2 phrased as a question answers it directly in the first 1-2 sentences before elaborating.
✓ Every section introduces a different executive lesson.
✓ The article contains ONE contrarian counter-argument that challenges the primary recommendation.
✓ No banned clichés appear anywhere.
✓ No anonymized enterprise proxies appear.
✓ Named enterprises from the research are used when available.
✓ No fabricated statistics appear.
✓ If the article discusses partnership, vendor, or build-vs-buy decisions, it includes a practical decision artifact.
✓ The article type is clearly reflected.
✓ The title is different from recent articles.
✓ The conclusion delivers a decisive strategic thesis, not a summary of prior points.
✓ The article feels like premium enterprise intelligence editorial, not an AI-generated summary.


OUTPUT FORMAT
Return ONLY the following format.

Title: <title>

Subtitle: <one-sentence subtitle, 12-20 words, that adds a specific angle beyond the title -- not a restatement of it>

Source URL: <source url>

Image Prompt: <25–40 word editorial illustration prompt>

Blog:

<complete markdown article>

The article must use Markdown.
Use Markdown H2 (##) headings for every major section.
Do not use plain text, numbered, or bold-only headings.
"""