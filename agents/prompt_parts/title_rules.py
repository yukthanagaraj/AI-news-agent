# TITLE_RULES = """
# ==================================================
# TITLE OBJECTIVE
# ==================================================

# Generate ONE premium executive editorial title.

# The title must be sharpened around a SINGLE CLEAR SEARCH INTENT —
# it should feel like the answer to one specific executive question that
# a decision-maker types into a search engine or asks an AI assistant.

# The title communicates the article's strategic business insight,
# not the news event that prompted it.

# Use the Editorial Insight and suggested title ideas as the primary source.

# Prefer selecting one of the five suggested titles.
# Only create a new title if all suggested titles are weak or repetitive.

# ==================================================
# LENGTH
# ==================================================

# - Exactly 6–8 words.
# - Validate the word count before returning.

# ==================================================
# EDITORIAL STYLE
# ==================================================

# Write like the front page of a premium Enterprise AI journal.

# The title should communicate one of these:

# - Business transformation consequence
# - Infrastructure or platform decision
# - Governance or compliance imperative
# - Competitive positioning shift
# - Operating model evolution
# - Leadership decision at an inflection point
# - Cost or economics insight
# - Strategic execution discipline

# Create curiosity through business implications rather than technology
# announcements. The title teaches a claim, not a topic.

# STRONG TITLE REGISTER EXAMPLES (derive fresh ones, do not reuse):

# "Why GPU Scheduling Determines AI Competitive Advantage"
# "Rethinking AI Infrastructure Before the Next Cost Crisis"
# "Inside Multi-Cloud AI Orchestration at Enterprise Scale"
# "Building the Platform Layer That Outlasts Model Generations"
# "Governing AI Infrastructure Across Regulatory Boundaries"
# "When FinOps Becomes the AI Department's Survival Skill"
# "Preparing Enterprises for Autonomous Compute Provisioning"

# ==================================================
# SEO — SINGLE SEARCH INTENT
# ==================================================

# Every title should be optimized for ONE primary search intent from
# the following domains. Select the most relevant:

# INFRASTRUCTURE & COMPUTE:
# • "AI infrastructure cost" / "AI infrastructure TCO"
# • "GPU scheduling enterprise" / "GPU utilization AI"
# • "multi-cloud AI orchestration" / "SkyPilot vs Kubernetes"
# • "hybrid AI deployment strategy" / "on-premises AI vs cloud"
# • "AI training cost optimization" / "LLM inference cost"

# FINOPS & ECONOMICS:
# • "FinOps for AI workloads" / "AI budget governance"
# • "AI infrastructure ROI" / "AI cost per query"
# • "enterprise AI economics" / "GPU cost optimization"

# GOVERNANCE & COMPLIANCE:
# • "AI governance enterprise" / "EU AI Act compliance"
# • "data sovereignty AI" / "HIPAA AI compliance"
# • "enterprise AI risk management" / "AI audit trail"

# PLATFORM ENGINEERING:
# • "MLOps enterprise" / "AI platform engineering"
# • "AI observability" / "model serving enterprise"
# • "AI pipeline orchestration" / "AI platform strategy"

# Use ONE high-value keyword naturally when appropriate.
# Avoid keyword stuffing.

# ==================================================
# VARIETY
# ==================================================

# Rotate title openings naturally.

# Avoid repeatedly starting with:

# - Enterprise
# - AI
# - Future
# - Operational
# - Intelligent
# - Digital

# Prefer varied openings such as:

# - Why
# - Beyond
# - Inside
# - Building
# - Rethinking
# - Governing
# - Scaling
# - Managing
# - Designing
# - Preparing
# - When
# - Lessons From
# - The Cost of

# Do not repeat the same sentence pattern across articles.

# ==================================================
# AVOID
# ==================================================

# Do NOT use:

# - Clickbait
# - Questions in the H1 (questions go in H2 section headings)
# - Colons in the H1 (subtitle carries the concrete detail)
# - Quotation marks
# - Marketing language
# - Product names as the headline subject
# - CEO names
# - Funding announcements
# - Generic openings: "The Future of..." / "Why [Topic] Matters..."
# - Gerund-plus-colon trend templates: "[Word]ing [Noun]: The Rise of
#   [Topic] in [Domain]" (e.g. "Powering Transformation: The Rise of
#   Strategic Partnerships in Enterprise AI"). This already violates the
#   no-colon-in-H1 rule above, but is called out explicitly because it
#   keeps recurring — verify the title has no colon before returning it.

# Use company names only if they are essential to understanding the
# strategic shift.

# ==================================================
# SUBTITLE / DEK
# ==================================================

# After finalizing the H1 title, generate ONE separate subtitle line.

# The subtitle is a SEPARATE FIELD returned alongside the title — never
# merge it into the H1 with a colon. The H1 stays exactly as validated
# above; the subtitle renders underneath it as a smaller dek line.

# Purpose: the H1 is intentionally abstract and editorial. The subtitle
# carries the ONE concrete, searchable detail the H1 deliberately
# avoided — a named audience, a named tool or mechanism, or a named
# outcome.

# Requirements:

# - 6–14 words.
# - Written in plain language, not editorial/aphoristic style — this
#   is the opposite register from the H1.
# - Must include at least one concrete element the H1 lacks: a named
#   role (CIOs, CFOs, ML platform teams), a named mechanism (SkyPilot,
#   spot-instance arbitrage, token pricing, GPU scheduling), a named
#   outcome (cost reduction, vendor lock-in avoidance, compliance speed).
# - Do not repeat any word already used in the H1.
# - No colon within the subtitle itself.
# - No company names unless essential.
# - Reads as a natural expansion of the title, not a second headline
#   competing with it.

# Example pairings:

# H1: "Governing AI at Enterprise Scale"
# Subtitle: "How CIOs should price tokens, compute, and energy across the organization"

# H1: "Rethinking AI Infrastructure Before the Next Cost Crisis"
# Subtitle: "GPU idle time, spot preemption, and the FinOps controls that prevent overruns"

# H1: "Building the Platform Layer That Outlasts Model Generations"
# Subtitle: "Why ML platform teams are investing in orchestration over model selection"

# ==================================================
# OUTPUT FORMAT
# ==================================================

# Return two distinct fields:

# Title: <the H1, 6-8 words>
# Subtitle: <the dek, 6-14 words>

# ==================================================
# FINAL VALIDATION
# ==================================================

# Before returning the title verify:

# ✓ 6–8 words

# ✓ Editorial rather than news headline

# ✓ Sharpened around ONE clear search intent

# ✓ Describes a strategic enterprise shift or decision

# ✓ Matches the article thesis

# ✓ SEO friendly — contains a keyword from the relevant domain

# ✓ Executive tone

# ✓ Different from recent titles

# ✓ No colon in H1

# ✓ Suitable for a premium Enterprise AI publication

# Before returning the subtitle verify:

# ✓ 6–14 words

# ✓ Contains a concrete detail (tool, role, mechanism, or outcome) the H1 omits

# ✓ No word overlap with the H1

# ✓ No colon within the subtitle

# ✓ Reads naturally as a dek line under the title

# BANNED TITLE PATTERN
# Never use the template "[Gerund word]: The Rise of [Topic] in [Domain]"
# (e.g. "Powering Transformation: The Rise of Strategic Partnerships in
# Enterprise AI"). This pattern reads as templated/AI-generated and is
# penalized by search and answer engines. Titles must state a concrete
# claim, differentiator, or finding — not a generic trend label.
# """

TITLE_RULES = """
==================================================
TITLE OBJECTIVE
==================================================

Generate ONE premium Luvana AI Journal editorial title.

The title must be sharpened around a SINGLE CLEAR SEARCH INTENT inside agentic AI.
It should feel like the answer to one specific executive question that a decision-maker types into a search engine or asks an AI assistant.

The title communicates the article’s strategic business insight, not the news event that prompted it.

Use the Editorial Insight and suggested title ideas as the primary source.
Prefer selecting one of the five suggested titles.
Only create a new title if all suggested titles are weak or repetitive.


==================================================
LENGTH
==================================================

- Exactly 6–8 words.
- Validate the word count before returning.


==================================================
EDITORIAL STYLE
==================================================

Write like the front page of a premium Luvana AI Journal.

The title should communicate one of these:

- Agentic AI governance imperative
- Agentic AI infrastructure decision
- Agentic AI economics insight
- Agentic AI operating model shift
- Agentic AI platform strategy
- Leadership decision at an inflection point
- Cost, control, or resilience insight
- Strategic execution discipline for autonomous systems

Create curiosity through business implications rather than technology announcements.
The title teaches a claim, not a topic.


STRONG TITLE REGISTER EXAMPLES (derive fresh ones, do not reuse):

- Why GPU Scheduling Determines AI Competitive Advantage
- Rethinking AI Infrastructure Before the Next Cost Crisis
- Inside Multi-Cloud AI Orchestration at Enterprise Scale
- Building the Platform Layer That Outlasts Model Generations
- Governing AI Infrastructure Across Regulatory Boundaries
- When FinOps Becomes the AI Department’s Survival Skill
- Preparing Enterprises for Autonomous Compute Provisioning
- Governing Agentic AI Before It Reaches Production


==================================================
SEO — SINGLE SEARCH INTENT
==================================================

Every title should be optimized for ONE primary search intent from the following agentic AI domains. Select the most relevant:

AGENTIC AI GOVERNANCE:
• agentic AI governance enterprise
• AI governance for agents
• agentic AI risk management
• AI audit trail for agents

AGENTIC AI ECONOMICS:
• agentic AI cost optimization
• AI infrastructure TCO
• AI cost per query
• FinOps for agentic AI

AGENTIC AI INFRASTRUCTURE:
• agentic AI infrastructure
• GPU scheduling enterprise
• AI platform engineering
• model serving enterprise
• AI pipeline orchestration

AGENTIC AI OPERATING MODEL:
• agentic AI operating model
• autonomous workflow governance
• enterprise AI agent control
• runtime guardrails for AI agents

Use ONE high-value keyword naturally when appropriate.
Avoid keyword stuffing.


==================================================
VARIETY
==================================================

Rotate title openings naturally.

Avoid repeatedly starting with:

- Enterprise
- AI
- Future
- Operational
- Intelligent
- Digital

Prefer varied openings such as:

- Why
- Beyond
- Inside
- Building
- Rethinking
- Governing
- Scaling
- Managing
- Designing
- Preparing
- When
- Lessons From
- The Cost of

Do not repeat the same sentence pattern across articles.


==================================================
AVOID
==================================================

Do NOT use:

- Clickbait
- Questions in the H1
- Colons in the H1
- Quotation marks
- Marketing language
- Product names as the headline subject
- CEO names
- Funding announcements
- Generic openings: "The Future of..." / "Why [Topic] Matters..."
- Gerund-plus-colon trend templates

Use company names only if they are essential to understanding the strategic shift.


==================================================
SUBTITLE / DEK
==================================================

After finalizing the H1 title, generate ONE separate subtitle line.

The subtitle is a SEPARATE FIELD returned alongside the title — never merge it into the H1 with a colon.

Purpose: the H1 is intentionally abstract and editorial. The subtitle carries the ONE concrete, searchable detail the H1 deliberately avoided — a named audience, a named tool or mechanism, or a named outcome.

Requirements:

- 6–14 words.
- Written in plain language, not editorial or aphoristic style.
- Must include at least one concrete element the H1 lacks: a named role, a named mechanism, or a named outcome.
- Do not repeat any word already used in the H1.
- No colon within the subtitle itself.
- No company names unless essential.
- Reads as a natural expansion of the title, not a second headline competing with it.


Example pairings:

H1: "Governing AI at Enterprise Scale"
Subtitle: "How CIOs should price tokens, compute, and energy across the organization"

H1: "Rethinking AI Infrastructure Before the Next Cost Crisis"
Subtitle: "GPU idle time, spot preemption, and the FinOps controls that prevent overruns"

H1: "Building the Platform Layer That Outlasts Model Generations"
Subtitle: "Why ML platform teams are investing in orchestration over model selection"


==================================================
OUTPUT FORMAT
==================================================

Return two distinct fields:

Title: <the H1, 6-8 words>
Subtitle: <the dek, 6-14 words>


==================================================
FINAL VALIDATION
==================================================

Before returning the title verify:

✓ 6–8 words
✓ Editorial rather than news headline
✓ Sharpened around ONE clear search intent
✓ Describes a strategic enterprise shift or decision
✓ Matches the article thesis
✓ SEO friendly — contains a keyword from the relevant domain
✓ Executive tone
✓ Different from recent titles
✓ No colon in H1
✓ Suitable for a premium Luvana AI publication

Before returning the subtitle verify:

✓ 6–14 words
✓ Contains a concrete detail (tool, role, mechanism, or outcome) the H1 omits
✓ No word overlap with the H1
✓ No colon within the subtitle
✓ Reads naturally as a dek line under the title


BANNED TITLE PATTERN
Never use the template "[Gerund word]: The Rise of [Topic] in [Domain]".
Titles must state a concrete claim, differentiator, or finding — not a generic trend label.
"""