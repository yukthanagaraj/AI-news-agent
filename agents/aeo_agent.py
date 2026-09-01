from agents.llm_client import client, MODEL_NAME
from agents.aeo_parts.answer import QUICK_ANSWER_RULES
from agents.aeo_parts.faq_rules import FAQ_RULES
from agents.aeo_parts.schema_rules import SCHEMA_RULES
from agents.aeo_parts.entity_rules import ENTITY_RULES
from agents.aeo_parts.executive_rules import EXECUTIVE_RULES
from agents.aeo_parts.retrieval_rules import RETRIEVAL_RULES


def generate_aeo(
    title,
    article,
    source_url="",
    published_date=""
):

    prompt = f"""
TITLE

{title}

SOURCE URL (use exactly this for mainEntityOfPage -- do not invent a different URL)

{source_url or "[no source URL provided]"}

PUBLISHED DATE (use exactly this ISO date for datePublished -- do not invent a date)

{published_date or "[no date provided]"}

ARTICLE

{article}
{QUICK_ANSWER_RULES}

{FAQ_RULES}

{SCHEMA_RULES}

{ENTITY_RULES}

{EXECUTIVE_RULES}

{RETRIEVAL_RULES}

OBJECTIVE

Generate premium Answer Engine Optimization (AEO) content for an Enterprise AI publication.

Optimize for:

- Google AI Overviews
- ChatGPT Search
- Claude
- Gemini
- Perplexity
- Microsoft Copilot

Prioritize executive search intent.

Produce answers that are easy for AI systems to quote directly.

Every section should directly answer one executive question.

Use concise, factual language.

Avoid repetition.

EXTRACTION METHOD

Each H2 section in the article now opens with a direct-answer first
sentence (this is a deliberate writer convention). Use those opening
sentences as your PRIMARY source for Quick Answer, Featured Snippet,
Key Facts, and AI Overview Summary — do not re-derive a new framing
from scratch. Pull the strongest 1-2 section-opening claims verbatim
or near-verbatim (light editing for standalone clarity is fine) rather
than synthesizing new language that might drift from what the article
itself asserts. This keeps the AEO output and the article's actual
content in sync, which improves consistency scoring across answer
engines.

CONDITIONAL SECTION DISCIPLINE

Definition Blocks, FinOps & Infrastructure Metrics, and Governance &
Compliance Notes are OPTIONAL, not default-on. Before including any of
these three sections, verify the article body actually contains
substantive content on that exact topic — not just an adjacent mention.
A single passing reference to "compliance" does NOT justify a full
Governance & Compliance Notes section. If you would need to invent or
stretch content to fill one of these sections, OMIT the section
entirely rather than including a thin or generic version. A missing
section is better than a padded one — semantic completeness is judged
on quality of what's present, not on section count.

OUTPUT ONLY THE FOLLOWING SECTIONS IN EXACT ORDER:

## Executive Summary

<2–3 sentence executive summary capturing the article's primary thesis and business implication>

## Quick Answer

<50–80 word direct answer to the article's primary executive question. State the answer first, then support it. Suitable for Google AI Overview extraction.>

## Definition Blocks

<For technical or infrastructure articles, include 2–3 concise definitions in this format:

**What is [Term]?**
[One-sentence definition including what it does and why it matters to enterprises.] [Optional: one sentence on how it differs from alternatives.]

Include definitions for any technical terms central to the article: SkyPilot, FinOps for AI, GPU scheduling, multi-cloud orchestration, hybrid AI deployment, data sovereignty, MLOps, etc. Only define terms that appear in the article AND are load-bearing to its argument (not incidentally mentioned once). If fewer than 2 qualifying terms exist, omit this section entirely rather than including 1 thin definition.>

## Executive Questions Answered

<List exactly 5 specific executive questions this article answers. These should be questions executives actually type into search engines — not generic topic labels.>

- <Question 1>
- <Question 2>
- <Question 3>
- <Question 4>
- <Question 5>

## Key Facts

<Exactly 5 factual statements from the article, each self-contained and citable. Include quantitative data if present in the article. Avoid fabricating numbers.>

- <Fact 1>
- <Fact 2>
- <Fact 3>
- <Fact 4>
- <Fact 5>

## FinOps & Infrastructure Metrics

<For infrastructure, compute, or cost articles: include 3–5 actionable metrics or decision thresholds executives can use. Format as bolded metric name followed by a one-sentence explanation.

**GPU Utilization Target**
[What utilization level signals a scheduling optimization opportunity and why]

**Inference TCO Threshold**
[What monthly inference cost level justifies a FinOps ownership structure]

**Spot vs Reserved Trigger**
[What workload stability profile makes reserved capacity more cost-effective than spot arbitrage]

Skip this section unless the article substantively discusses compute cost, GPU/infrastructure spend, or FinOps as a real theme — not just a passing mention of "cost optimization" as a generic aside.>

## Governance & Compliance Notes

<For articles touching governance, data, regulatory, or compliance topics: identify the 2–3 most relevant regulatory frameworks and what they require from enterprises deploying AI. Format as bolded framework name followed by a one-sentence enterprise obligation.

**EU AI Act**
[What it requires for high-risk AI systems in enterprise contexts]

**HIPAA**
[What it requires for AI processing healthcare data]

**SOC 2 / Data Sovereignty**
[What audit trail and residency controls are required]

Skip this section unless the article substantively engages with a specific regulation, compliance framework, or regulated-industry deployment — not just a generic mention of "governance matters.".>

## Executive Decision Framework

Immediate Priorities (0–30 days)

- <point>
- <point>
- <point>

Medium-term Priorities (30–90 days)

- <point>
- <point>
- <point>

Long-term Competitive Priorities (90 days – 12 months)

- <point>
- <point>
- <point>

## FAQs

### <Question 1 — What changed / specific shift>

<Answer: 2–4 sentences, direct, self-contained, cliché-free>

### <Question 2 — Why does it matter now>

<Answer>

### <Question 3 — What should executives do>

<Answer>

### <Question 4 — Governance or compliance implication>

<Answer>

### <Question 5 — Contrarian question: When does the recommendation NOT apply?>

<Answer>

## AI Overview Summary

<2–3 sentence summary optimized for Google AI Overview extraction. Start with the direct answer to the article's primary question. Include one specific metric or decision criterion if present in the article.>

## Featured Snippet

<40–60 word complete-sentence answer to the article's primary executive question. Must be self-contained — readable as a standalone answer without any surrounding context. Start with the answer, not the question. Suitable for position-zero featured snippet extraction.>

## Schema
<Article schema in JSON-LD format. You MUST use the exact SOURCE URL and PUBLISHED DATE given above for "mainEntityOfPage" and "datePublished" -- never substitute a placeholder like "https://www.example.com" or an invented date. If no source URL or date was provided, omit those two fields from the schema entirely rather than inventing values.>

<FAQPage schema in JSON-LD format using the 5 FAQ questions and answers above>
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": """
You are a senior Enterprise AI Answer Engine Optimization strategist.

Generate premium AEO content for enterprise publications.

Optimize for:

- Google AI Overviews
- ChatGPT Search
- Claude
- Gemini
- Perplexity
- Microsoft Copilot

Prioritize:

- Direct-answer formatting (answer first, then support)
- Concise executive answers extractable by AI systems
- Featured snippet eligibility (40–80 word standalone answers)
- AI Overview summaries (2–3 sentence, complete, self-contained)
- Definition blocks for technical terms (for snippet extraction)
- FinOps metrics and decision thresholds (quantitative where possible)
- Governance and compliance notes for regulated industries
- Executive search intent alignment
- Semantic completeness across infrastructure, FinOps, governance, and platform domains

Avoid repetition.

Every answer should be factual, structured, and easily extractable by AI systems.

Do not invent facts or fabricate statistics.

Do not merely summarize the article — distill the strategic insights into extractable units.

Use precise business language: "GPU idle time" not "underutilized compute"; "spot-instance preemption risk" not "cloud reliability concerns"; "inference TCO" not "AI costs".

Eliminate all banned clichés: "game-changer," "cornerstone," "transformative journey," "ever-evolving market," "unprecedented," "paradigm shift."
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("AEO GENERATED")

    return response.choices[0].message.content
