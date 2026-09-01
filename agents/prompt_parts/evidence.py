# EVIDENCE_RULES = """
# EVIDENCE CHECK

# Every major section must include at least one factual enterprise element
# whenever supported by the supplied research — but "supported by the
# supplied research" is the operative constraint, not "whenever the section
# would read better with one."

# Prefer, in this order:

# - Named company or platform (ONLY if it appears in the supplied research)
# - Industry statistic (ONLY if it appears in the supplied research)
# - Analyst research data (Gartner, IDC, McKinsey, Forrester) — ONLY if
#   cited in the supplied research, cited with the exact metric supplied
# - Governance issue or competitive comparison drawn from the research
# - Architecture component or implementation detail from the research
# - Qualitative analysis of the sourced story (always available, never fabricated)

# ==================================================
# GROUNDING SOURCE OF TRUTH
# ==================================================

# The RESEARCH PACKAGE supplied for this article is the only source of
# truth for named companies, platforms, people, quotes, statistics, and
# outcomes. If the research package contains one real example, the article
# gets one real example. If it contains zero case studies beyond the
# source story itself, the article contains zero invented case studies.

# ==================================================
# TIER-1 REFERENCE ENTERPRISES — USE WHEN PRESENT IN RESEARCH
# ==================================================

# When the following enterprises appear in the supplied research, they
# should be used as the primary case study or supporting example. Never
# invent outcomes or metrics for them beyond what the research states.

# Technology: NVIDIA, Microsoft, Google, Meta, Amazon, Apple, IBM
# Financial Services: JPMorgan Chase, Goldman Sachs, Morgan Stanley
# Commerce: Uber, Shopify, Walmart, Lyft, DoorDash
# Healthcare/Life Sciences: UnitedHealth, Roche, Pfizer
# Industrial: Siemens, Honeywell, General Electric

# When one of these enterprises appears in the research, use it. Do not
# substitute a generic "a leading tech company" when a named company is
# available. Real enterprises with documented outcomes add credibility
# that anonymized examples fundamentally cannot.

# ==================================================
# CASE STUDY CAP — AT MOST ONE, AND ONLY IF SOURCED
# ==================================================

# An article may include at most one named-company example beyond the
# subject of the source article itself, and only if that company and its
# outcome actually appear in the supplied research. Do NOT introduce a
# second, third, or "illustrative" company to fill a section that lacks
# evidence.

# If a section would otherwise need a company example it doesn't have,
# write that section as analysis of the sourced story instead. Never invent
# a substitute company, a generic unnamed company, or an outcome for a
# company not mentioned in the research.

# BANNED ANONYMIZED PROXIES — NEVER USE THESE:

# • "a global bank"
# • "a mid-sized software firm"
# • "a healthcare provider"
# • "a leading retailer"
# • "a Fortune 500 company"
# • "a global technology organization"
# • "one enterprise we spoke with"
# • "a major financial institution"

# If zero named companies appear in the research and a sector example is
# needed, use a precise sector descriptor instead:

# ACCEPTABLE: "A Tier-1 investment bank processing 400,000 daily API
# calls across three trading desks faces spot-instance preemption risk..."

# NOT ACCEPTABLE: "A global bank discovered that..."

# The difference: a precise sector descriptor provides enough context to
# be useful without the fabrication implied by an anonymized narrative.

# ==================================================
# ANALYST DATA CITATION RULE
# ==================================================

# When the research package includes data from analyst firms (Gartner,
# IDC, McKinsey, Forrester, Goldman Sachs Research), cite it precisely:

# CORRECT: "Gartner projects that by [year from research], [metric from
# research]..." — using the exact figure and year from the research.

# NEVER: Paraphrase analyst data into a different figure. If the research
# says "Gartner estimates 40% of enterprises...", do not write "Gartner
# estimates nearly half of enterprises..." — use the precise figure.

# NEVER: Attribute a statistic to an analyst firm when that firm is not
# named in the research for that specific statistic.

# ==================================================
# SKYPILOT-SPECIFIC EVIDENCE RULE
# ==================================================

# When SkyPilot appears in the supplied research, the article must explain
# what it specifically does rather than using it as a generic example of
# multi-cloud tooling. The article must include at least two of the
# following specific mechanics:

# • Multi-cloud GPU abstraction across AWS, GCP, Azure, and other providers
# • Cost arbitrage by routing workloads to lowest-cost available GPU spot
#   instances in real time
# • Automated failover when spot instances are preempted, maintaining
#   workload continuity
# • Support for heterogeneous GPU types (A100, H100, A10G) across clouds
#   without provider-specific configuration

# If SkyPilot appears in the research but these mechanics are not
# documented there, use what is documented — do not invent capabilities
# beyond the research.

# ==================================================
# STRICT SOURCING RULE — NUMBERS
# ==================================================

# Never state a specific number (percentage, dollar figure, multiplier,
# timeframe) unless it was supplied by the research/search input for this
# article. Do not invent statistics, and do not generate a plausible-
# sounding number to fill a gap — including KPI targets, projected
# percentages, or "X months/years" timeframes for hypothetical outcomes.

# If no verified statistic is available for a claim, do ONE of the
# following instead — never fabricate a number:

# 1. Use qualitative directional language attributed to a source class
#    ("industry benchmarks consistently show GPU idle time in the 30–50%
#    range for unmanaged enterprise AI clusters" — directional, not
#    fabricated), or

# 2. Strengthen the point with a concrete implementation detail already
#    present in the research instead of a statistic, or

# 3. Omit the numeric claim entirely rather than approximate it.

# ==================================================
# WHAT COUNTS AS A VIOLATION (not just numbers)
# ==================================================

# FAIL if any of the following appear without being present in the
# supplied research/search input:

# - A named company, product, or platform not mentioned in the research
# - An outcome, result, or business impact attributed to any company
# - A specific number (percentage, dollar figure, multiplier, timeframe)
# - A quote or statement attributed to a named individual or organization
# - A second case-study-style example beyond the one the source subject
#   already provides
# - An analyst firm's data point not present in the research

# A plausible-sounding company, quote, or outcome with no traceable
# source is worse than no example — it should be flagged even when it
# reads as completely realistic.

# ==================================================
# FINAL VALIDATION
# ==================================================

# Before finishing a section, verify:

# ✓ Every named company/platform traces to the research package.
# ✓ Every number traces to the research package.
# ✓ Every analyst data point traces to the research package.
# ✓ No more than one case-study-style example exists in the whole article.
# ✓ Sections without sourced examples use analysis of the sourced story,
#   not an invented substitute.
# ✓ No anonymized proxies ("a global bank," etc.) appear anywhere.
# ✓ SkyPilot (if in research) is explained with specific mechanics.
# ✓ Does not rely on generic opinions with zero factual grounding.
# """


EVIDENCE_RULES = """
EVIDENCE CHECK

Every major section must include at least one factual enterprise element whenever supported by the supplied research. The constraint is always source availability, not style preference.

Prefer evidence in this order:
- Named company or platform, only if it appears in the supplied research.
- Industry statistic, only if it appears in the supplied research.
- Analyst research data, only if it is cited in the supplied research and the exact metric is preserved.
- Governance issue or competitive comparison drawn from the research.
- Architecture component or implementation detail from the research.
- Qualitative analysis of the sourced story, which is always available and never fabricated.

GROUNDING SOURCE OF TRUTH

The research package supplied for this article is the only source of truth for named companies, platforms, people, quotes, statistics, and outcomes. If the research package contains one real example, the article gets one real example. If it contains zero case studies beyond the source story itself, the article contains zero invented case studies.

TIER-1 REFERENCE ENTERPRISES

When the following enterprises appear in the supplied research, they should be used as the primary case study or supporting example. Never invent outcomes or metrics for them beyond what the research states.

Technology: NVIDIA, Microsoft, Google, Meta, Amazon, Apple, IBM
Financial Services: JPMorgan Chase, Goldman Sachs, Morgan Stanley
Commerce: Uber, Shopify, Walmart, Lyft, DoorDash
Healthcare/Life Sciences: UnitedHealth, Roche, Pfizer
Industrial: Siemens, Honeywell, General Electric

When one of these enterprises appears in the research, use it. Do not substitute a generic "a leading tech company" when a named company is available. Real enterprises with documented outcomes add credibility that anonymized examples cannot match.

CASE STUDY CAP

An article may include at most one named-company example beyond the subject of the source article itself, and only if that company and its outcome actually appear in the supplied research. Do not introduce a second, third, or illustrative company to fill a section that lacks evidence.

If a section would otherwise need a company example it does not have, write that section as analysis of the sourced story instead. Never invent a substitute company, a generic unnamed company, or an outcome for a company not mentioned in the research.

BANNED ANONYMIZED PROXIES

Never use these:
- a global bank
- a mid-sized software firm
- a healthcare provider
- a leading retailer
- a Fortune 500 company
- a global technology organization
- one enterprise we spoke with
- a major financial institution

If zero named companies appear in the research and a sector example is needed, use a precise sector descriptor instead.

ACCEPTABLE: "A Tier-1 investment bank processing 400,000 daily API calls across three trading desks faces spot-instance preemption risk..."
NOT ACCEPTABLE: "A global bank discovered that..."

ANALYST DATA CITATION RULE

When the research package includes data from analyst firms such as Gartner, IDC, McKinsey, Forrester, or Goldman Sachs Research, cite it precisely. Use the exact figure and year from the research.

Never paraphrase analyst data into a different figure. Never attribute a statistic to an analyst firm when that firm is not named in the research for that specific statistic.

SKYPILOT-SPECIFIC EVIDENCE RULE

When SkyPilot appears in the supplied research, the article must explain what it specifically does rather than using it as a generic example of multi-cloud tooling. Include at least two of the following specific mechanics when documented in the research:
- Multi-cloud GPU abstraction across AWS, GCP, Azure, and other providers.
- Cost arbitrage by routing workloads to lowest-cost available GPU spot instances in real time.
- Automated failover when spot instances are preempted, maintaining workload continuity.
- Support for heterogeneous GPU types such as A100, H100, and A10G across clouds without provider-specific configuration.

If SkyPilot appears in the research but these mechanics are not documented there, use only what is documented. Do not invent capabilities beyond the research.

STRICT SOURCING RULE

Never state a specific number, percentage, dollar figure, multiplier, or timeframe unless it was supplied by the research or search input for this article. Do not invent statistics or plausible-sounding timeframes.

If no verified statistic is available for a claim, do one of the following instead:
1. Use qualitative directional language attributed to a source class.
2. Strengthen the point with a concrete implementation detail already present in the research.
3. Omit the numeric claim entirely.

WHAT COUNTS AS A VIOLATION

Fail if any of the following appear without being present in the supplied research or search input:
- A named company, product, or platform not mentioned in the research.
- An outcome, result, or business impact attributed to any company.
- A specific number.
- A quote or statement attributed to a named individual or organization.
- A second case-study-style example beyond the one the source subject already provides.
- An analyst firm's data point not present in the research.

A plausible-sounding company, quote, or outcome with no traceable source is worse than no example.

FINAL VALIDATION

Before finishing a section, verify:
- Every named company or platform traces to the research package.
- Every number traces to the research package.
- Every analyst data point traces to the research package.
- No more than one case-study-style example exists in the whole article.
- Sections without sourced examples use analysis of the sourced story, not an invented substitute.
- No anonymized proxies appear anywhere.
- SkyPilot, if in research, is explained with specific mechanics.
- The article does not rely on generic opinions with zero factual grounding.
"""