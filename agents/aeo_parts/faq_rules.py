FAQ_RULES = """
FAQ RULES

Generate EXACTLY 5 question-and-answer pairs, derived from THIS
article's specific thesis and news — never generic definitional
questions like "What are AI agents?" or "What is cloud computing?".
Each question must be answerable only by having read this specific
article, not by general AI knowledge.


QUESTION ANGLES — ROTATE ACROSS ALL FIVE

Each answer should follow one of these five angles, varied across
the 5 questions so they don't all repeat the same lens:

1. What changed? (the specific shift this article covers)
2. Why does it matter now? (the business consequence and timing)
3. What should executives do? (a concrete, non-generic action)
4. What is the governance or compliance implication?
5. What is the contrarian or counter-intuitive view?

One of the five questions MUST be explicitly contrarian — challenging
the article's primary recommendation with a legitimate counter-argument.
Example contrarian question register:
"Is multi-cloud AI orchestration always worth the added complexity?"
"Does automated GPU scheduling actually reduce costs for stable workloads?"
"When does prioritizing AI governance slow competitive advantage?"


INFRASTRUCTURE & FINOPS FAQ ANGLES

For infrastructure, platform, or cost-related articles, include at
least one FAQ that directly answers a FinOps or infrastructure question
executives actually search for. Examples of the required register:

"How does automated cloud orchestration lower AI training TCO?"
"What GPU utilization rate signals a need for orchestration investment?"
"When does on-premises AI infrastructure outperform public cloud?"
"How does SkyPilot reduce spot-instance preemption risk?"
"What is the real cost of GPU idle time at LLM inference scale?"

These questions align with high-value long-tail search queries that
drive executive traffic. Use this angle when the article covers
compute, cost, or infrastructure topics.

GOVERNANCE & REGULATORY FAQ ANGLES

For articles covering governance, compliance, data platform, or
deployment strategy, include at least one FAQ addressing:

"How does multi-cloud AI deployment comply with data sovereignty laws?"
"What does the EU AI Act require from enterprises running LLM workloads?"
"How should enterprises handle HIPAA compliance for AI in healthcare?"
"What data residency controls are required for AI workloads in the EU?"
"How does automated infrastructure orchestration affect SOC 2 compliance?"


DEFINITION BLOCKS — REQUIRED FOR TECHNICAL ARTICLES

For articles covering infrastructure, platform engineering, MLOps,
or AI tooling (especially when SkyPilot, Ray, Kubernetes, FinOps,
or similar technical terms appear), include 2–3 concise definition
blocks formatted for Google featured snippet extraction. These appear
as a separate mini-section BEFORE or WITHIN the FAQ section.

Format:

**What is [Term]?**
[Term] is [one-sentence definition including what it does and why it matters
to enterprises]. [Optional: one sentence on how it differs from alternatives.]

Example:

**What is SkyPilot?**
SkyPilot is an open-source multi-cloud orchestration framework that
abstracts GPU provisioning across AWS, GCP, Azure, and other providers,
allowing AI workloads to run on the lowest-cost available spot instance
without provider-specific configuration. Unlike Kubernetes-native
solutions, SkyPilot automates cross-cloud failover when spot instances
are preempted.

**What is FinOps for AI?**
FinOps for AI is the practice of applying financial accountability
disciplines — chargeback models, utilization tracking, budget alerts,
and cost-per-query measurement — to AI infrastructure spending.
Unlike general cloud FinOps, AI FinOps must account for GPU spot
pricing volatility, inference cost spikes, and model iteration cycles.

Derive definitions from the article topic. Do not copy these examples.


QUESTION DERIVATION RULES

Generate questions that:

- Are answerable only from this article
- A CFO, CIO, or CTO would actually type into a search engine
- Are specific enough to drive featured snippet extraction
- Cover the article's main thesis plus governance/FinOps angles

Example pattern (do not reuse this wording — derive fresh questions):

### What does [today's specific development] change for enterprise infrastructure?
### Why does [the specific shift] matter now rather than in two years?
### What should CIOs prioritize to [achieve the article's core recommendation]?
### What risk does [the article's primary trend] create if ignored?
### When does [the article's recommendation] NOT apply?


ANSWER FORMAT RULES
Answers should be:

- Short (2–4 sentences)
- Analytical and self-contained — understandable without reading the full article
- Direct: state the answer first, then support it
- Formatted for AI engine extraction (ChatGPT, Gemini, Perplexity, Claude)
- Free of banned clichés and vague enterprise language

Avoid questions that name specific companies unless the company is
central to the article's thesis.

Avoid answers that require the reader to have read the full article
to understand — each answer must stand alone.
"""