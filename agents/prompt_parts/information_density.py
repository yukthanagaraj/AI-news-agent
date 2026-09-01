# INFORMATION_DENSITY = """
# ==================================================
# SECTION DEPTH
# ==================================================

# Every major H2 section MUST contain 2–4 paragraphs. This is not optional.

# Each paragraph must introduce a different executive insight — never restate
# the paragraph before it in different words.

# Required progression:

# Paragraph 1
# - Explain the strategic shift.

# Paragraph 2
# - Explain the enterprise consequence.

# Paragraph 3
# - Explain implementation, governance, leadership, or organizational implications.

# Paragraph 4 (optional)
# - Provide a realistic enterprise example, case study, comparison, or executive trade-off.

# ==================================================
# EXECUTIVE THINKING
# ==================================================

# Every section must answer a DIFFERENT executive question than every other
# section. Before writing a section, check the other section headings — if
# the question you're about to answer is already answered elsewhere, pick a
# different question:

# - Why does this matter?
# - What changes operationally?
# - Who is affected?
# - What should leaders prioritize?
# - What competitive advantage emerges?
# - What governance implication follows?

# ==================================================
# MANDATORY ELEMENTS (exactly one each, article-wide — not per section)
# ==================================================

# The article MUST contain, somewhere across its sections:

# 1. ONE enterprise example, grounded in a plausible industry (Banking,
#    Healthcare, Manufacturing, Retail, Logistics, Cloud, Cybersecurity,
#    Software Engineering). Never invent statistics — use plausible
#    operational outcomes only.

# 2. ONE memorable strategic framework (unique name, 3–5 stages, each
#    stage explained in one sentence). Do not reuse a generic name like
#    "AI Maturity Model" — make it specific to today's thesis.

# 3. ONE executive trade-off (e.g. Speed vs Governance, Automation vs
#    Accountability, Innovation vs Compliance, Cost vs Resilience,
#    Autonomy vs Human Oversight), explained as: why the tension exists,
#    the business consequence, and an executive recommendation.

# Do not place all three in the same section — spread them across
# different H2s so no single section is overloaded while others are thin.

# ==================================================
# TRANSITIONS
# ==================================================

# Use natural executive transitions: Strategically, Operationally,
# Meanwhile, Consequently, In practice, As organizations mature, From a
# leadership perspective.

# ==================================================
# ARTICLE DEPTH
# ==================================================

# Target 140–220 words per major H2 section.

# The article should read like an executive journal, not a blog post.
# No filler. Every paragraph teaches something new.
# """

INFORMATION_DENSITY = """
==================================================
SECTION DEPTH
==================================================

Every major H2 section MUST contain 3–5 paragraphs. This is not optional.

Each paragraph must introduce a different executive insight — never restate the paragraph before it in different words.

Required progression:

Paragraph 1
- Explain the strategic shift. State the claim first.

Paragraph 2
- Explain the enterprise consequence. Who is affected and how?

Paragraph 3
- Explain implementation, governance, leadership, or organizational implications. Be specific — name the team, decision, or trade-off.

Paragraph 4
- Provide a realistic enterprise example, case study, comparison, or executive trade-off. If a named company exists in the research, use it. If not, use a sector-grounded directional example — never "a global bank."

Paragraph 5 (optional)
- Add a second-order consequence, a competitive angle, or a contrarian counterpoint the section hasn't covered yet. Do not restate Paragraph 1.

==================================================
EXECUTIVE THINKING
==================================================

Every section must answer a DIFFERENT executive question than every other section. Before writing a section, check the other section headings — if the question you're about to answer is already answered elsewhere, pick a different question:

- Why does this matter?
- What changes operationally?
- Who is affected and what decision do they face?
- What should leaders prioritize and by when?
- What competitive advantage emerges for early movers?
- What governance or compliance implication follows?
- What is the FinOps or cost-management consequence?
- What infrastructure or architectural decision is forced?

==================================================
MANDATORY ELEMENTS (exactly one each, article-wide — not per section)
==================================================

The article MUST contain, somewhere across its sections:

1. ONE enterprise case study, grounded in a named or sector-specific example from the research. Named enterprises from the research are strongly preferred over generic sector descriptions. Never invent statistics — use sourced metrics or directional language only.

2. ONE memorable strategic framework — a unique name with 3–5 stages.
   Options:
   - A maturity model (e.g., "AI Infrastructure Readiness Maturity Model" with stages: Ad Hoc → Provisioned → Orchestrated → Optimized → Autonomous)
   - A decision matrix comparing options across Cost, Latency, Complexity, and Vendor Lock-in (presented as prose blocks, not a markdown table)
   - A phased implementation framework (e.g., Assess → Architect → Automate → Observe → Optimize)
   Do not reuse a previously used framework name. Make it specific to today's thesis.

3. ONE executive trade-off (e.g., GPU Reserved Capacity vs Spot Arbitrage, Multi-Cloud Complexity vs Cost Savings, Governance Speed vs Compliance Rigor), explained as: why the tension exists, the business consequence of choosing wrong, and one executive recommendation with a measurable trigger if possible.

Do not place all three in the same section — spread them across different H2s so no single section is overloaded while others are thin.

==================================================
FINOPS & QUANTITATIVE EVIDENCE
==================================================

When the article covers AI infrastructure cost, compute economics, GPU utilization, or inference scaling, apply these rules:

SOURCED METRICS: If the research package contains quantitative data (GPU utilization %, TCO figures, cost-per-query benchmarks, latency SLAs), cite them precisely. Do not paraphrase into a different number.

DIRECTIONAL LANGUAGE (when no metric is sourced): Use qualitative directional language that conveys magnitude without fabricating figures.

DECISION CRITERIA: Include at least one measurable threshold or decision trigger that executives can apply:
- A utilization target that triggers a procurement or orchestration decision.
- A monthly cost threshold that justifies a FinOps ownership structure.
- A latency SLA threshold that determines on-prem vs cloud placement.

==================================================
CLOUD-NATIVE ANTI-REPETITION RULE
==================================================

When a section has already established a "cloud-native" or "cloud-first" premise, subsequent paragraphs in that section MUST pivot to a different domain rather than restating the cloud benefit in different words. Pivot to one of:

- Governance and security implications of cloud placement.
- FinOps and cost optimization within the cloud model.
- Data sovereignty and residency constraints that limit cloud use.
- Hybrid deployment as the operational reality for regulated workloads.
- Observability and monitoring gaps specific to managed cloud AI services.
- The on-premises vs cloud trade-off for stable, high-volume workloads.

Never write a second paragraph that makes the same point as the first with different vocabulary.

==================================================
TRANSITIONS
==================================================

Use natural executive transitions: Strategically, Operationally, Meanwhile, Consequently, In practice, As organizations mature, From a governance perspective, From a cost perspective, At the infrastructure layer.

==================================================
ARTICLE DEPTH
==================================================

Target 220–320 words per major H2 section.

The article should read like an executive journal, not a blog post.
No filler. Every paragraph teaches something new. Do not pad a section to reach the paragraph count — if a fifth paragraph would only restate earlier points, stop at four.
"""