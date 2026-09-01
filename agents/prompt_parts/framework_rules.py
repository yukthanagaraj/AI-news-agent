FRAMEWORK_RULES = """
FRAMEWORK OBJECTIVE

When the article discusses enterprise transformation, AI infrastructure,
AI platform engineering, operational change, or business strategy,
organize complex ideas into clear executive frameworks.

Frameworks should improve readability and deliver a unique analytical
tool the reader can apply to their own organization.

Never interrupt the flow of the article.

Use frameworks only when they genuinely help explain the topic.

==================================================
WHEN TO USE
==================================================

Use a framework when the article explains:

• Enterprise transformation or organizational redesign
• AI infrastructure strategy (cloud, hybrid, on-prem trade-offs)
• AI platform engineering (MLOps, orchestration, model serving)
• Competitive positioning or market dynamics
• Governance, compliance, or risk management
• Human–AI collaboration or workforce redesign
• FinOps for AI workloads
• Enterprise automation maturity
• Digital workforce evolution
• GPU scheduling or compute strategy

Do NOT force a framework into every article.

==================================================
FRAMEWORK CAP — ONE PER ARTICLE
==================================================

An article may introduce AT MOST ONE named/acronym framework.

If a framework is introduced, do NOT introduce a second, competing,
or overlapping framework elsewhere in the same article — including
in the Strategic Recommendations or Enterprise Evidence sections.
Fold any additional structural ideas into the single framework's
capability blocks instead of naming them separately.

If the article does not need a named framework, use plain capability
blocks (see FRAMEWORK STYLE below) with no name at all. Naming a
framework is optional; running two is never acceptable.

==================================================
FRAMEWORK OPTIONS — CHOOSE THE BEST FIT
==================================================

Option A: MATURITY MODEL

Best for: infrastructure readiness, governance maturity, AI adoption
stages, organizational capability development.

Format: 4–5 stages with a unique name for the overall model and a
one-sentence description of each stage. Name the stages with
enterprise-relevant labels, not generic "Level 1 / Level 2" labels.

Example structure (derive a unique name for the article's specific thesis):

The [Unique Model Name]:

Stage 1 — [Stage Name]
[One sentence: what characterizes this stage and what it costs the enterprise]

Stage 2 — [Stage Name]
[One sentence: what changes and what capability is gained]

Stage 3 — [Stage Name]
[One sentence: the inflection point where competitive advantage begins]

Stage 4 — [Stage Name]
[One sentence: the target state and what it enables]

Stage 5 (optional) — [Stage Name]
[One sentence: the autonomous/optimized end state]

Do NOT name the model "AI Maturity Model" — make it specific to the
article's thesis (e.g., "AI Infrastructure Readiness Maturity Model,"
"GPU Scheduling Discipline Framework," "Enterprise AI Governance
Maturity Curve").

Option B: DECISION MATRIX (PROSE FORMAT)

Best for: infrastructure trade-offs (cloud vs hybrid vs on-prem),
tool comparisons (SkyPilot vs Ray vs Kubernetes-native), or
procurement decisions (reserved vs spot GPU capacity).

Format: compare 3–4 options across 4 dimensions — Cost Profile,
Latency Implications, Operational Complexity, and Vendor Lock-in
Exposure. Present as prose capability blocks, NOT as a markdown table.

Example structure:

**[Option A — e.g., On-Premises GPU Clusters]**
Cost Profile: [sentence]. Latency Implications: [sentence].
Operational Complexity: [sentence]. Vendor Lock-in: [sentence].

**[Option B — e.g., Public Cloud Managed AI]**
...

**[Option C — e.g., Multi-Cloud Orchestration via SkyPilot]**
...

Executive Recommendation: [one sentence on when each option makes sense]

Option C: PHASED IMPLEMENTATION FRAMEWORK

Best for: implementation playbooks, rollout strategies, adoption
roadmaps, platform engineering plans.

Format: 3–5 phases with a unique framework name and one sentence per
phase covering what is done, what is measured, and what signals
readiness to move to the next phase.

Example structure:

The [Framework Name]:

Phase 1 — [Phase Name] (0–30 days)
[What teams do, what they measure, what signals completion]

Phase 2 — [Phase Name] (30–90 days)
[What teams do, what they measure, what signals completion]

Phase 3 — [Phase Name] (90–180 days)
[...]

Option D: CAPABILITY BLOCKS (NO NAMED FRAMEWORK)

Best for: when the article does not need a named framework but does
need to organize 3–5 distinct enterprise capabilities, leadership
priorities, or strategic implications.

Format: Bold heading + 2–4 sentence explanation per block.

Example:

**Decision Intelligence**
AI agents accelerate enterprise decision-making by continuously
analyzing operational data and recommending actions within defined
governance boundaries.

**GPU Scheduling Discipline**
Enterprises that actively manage GPU allocation — setting utilization
targets, automating spot-instance failovers, and tracking idle
capacity — consistently outperform peers on inference TCO.

==================================================
FRAMEWORK RULES (ALL TYPES)
==================================================

Each capability or stage:

• 1 short heading or label
• 2–4 sentences
• Executive language, not engineering jargon
• Business-focused outcome, not technical implementation detail

Do NOT use:

• Markdown tables  (EXCEPT for multi-stage/maturity models — see FRAMEWORK STYLE above)
• Numbered lists for framework stages (use bold labels)
• Long paragraphs
• Vendor product names as stage labels

==================================================
FRAMEWORK STYLE
==================================================

Introduce the framework naturally.
Use a short introduction.
Then present 3–6 concise capability blocks.

EXCEPTION — MULTI-STAGE MODELS:
If the framework represents a sequential maturity model, stage
progression, or process pipeline (e.g. "Stage 1 → Stage 2 → Stage 3"),
present it as a Markdown table instead of prose blocks, with columns:
Stage | Characteristics | Governance/Owner | KPI | Primary Risk.
This is the one case where a table is required, not optional — AEO
and answer engines extract staged models far better from tables than
from narrative paragraphs.

For non-sequential capability frameworks (e.g. "four pillars of X"),
continue using capability blocks, no table.

==================================================
SKYPILOT-SPECIFIC RULE
==================================================

When SkyPilot appears in the article research or archetype, the
framework or analysis MUST explain what SkyPilot specifically does:

• Multi-cloud GPU abstraction: SkyPilot abstracts the underlying
  cloud provider, allowing workloads to run on AWS, GCP, Azure, or
  Lambda Labs without provider-specific orchestration code.

• Cost arbitrage via spot instances: SkyPilot continuously monitors
  spot GPU pricing across providers and migrates workloads to lower-
  cost instances, typically reducing training and inference costs
  substantially versus on-demand pricing.

• Automated failover: when a spot instance is preempted, SkyPilot
  automatically relaunches the workload on the next available instance,
  making preemption a managed operational event rather than an outage.

Do NOT use SkyPilot as a springboard for generic multi-cloud
discussion. If it appears in the research, it must be explained with
these specific mechanics.

==================================================
AEO OPTIMIZATION
==================================================

Frameworks should naturally answer questions such as:

What is the AI Infrastructure Readiness Maturity Model?

How does multi-cloud AI orchestration reduce inference costs?

What are the stages of GPU scheduling maturity?

How should enterprises choose between cloud and on-premises AI?

What is the difference between SkyPilot, Ray, and Kubernetes for AI?

==================================================
SEO OPTIMIZATION
==================================================

Use semantic enterprise keywords naturally within framework context:

AI Infrastructure Readiness
GPU Scheduling Maturity
Multi-Cloud AI Orchestration
FinOps for AI Workloads
Hybrid AI Deployment
AI Platform Engineering
MLOps Maturity
Enterprise AI Governance
On-Premises vs Cloud AI Trade-off
SkyPilot Multi-Cloud Abstraction

==================================================
FINAL VALIDATION
==================================================

Before generating a framework verify:

✓ It improves understanding of the article's specific thesis.

✓ It is business-focused, not engineering-documentation.

✓ It contains 3–6 capability blocks or stages.

✓ Each block introduces one unique idea.

✓ No repetition between blocks.

✓ Executive tone throughout.

✓ No markdown tables.

✓ SkyPilot explained with specific mechanics if present in research.

✓ Framework name is unique to this article's thesis.

✓ Only ONE framework exists in the article.
"""