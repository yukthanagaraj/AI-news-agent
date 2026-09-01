EVIDENCE_CHECK_RULES = """
EVIDENCE CHECK

Verify every major section contains at least one of the following whenever appropriate:

- Named enterprise company (ONLY if it appears in the supplied research)
- Enterprise platform (ONLY if it appears in the supplied research)
- Enterprise example grounded in the supplied research
- Industry statistic (ONLY if it appears in the supplied research)
- Governance discussion
- Implementation detail from the supplied research
- Business outcome (ONLY if it appears in the supplied research)

FAIL if the article relies mostly on generic opinions.

==================================================
ANTI-FABRICATION CHECK — NUMBERS
==================================================

FAIL if any specific number (percentage, dollar figure, multiplier,
timeframe) appears in the article without having been present in the
supplied research/search input for this article. A specific-sounding
number with no traceable source is worse than no number — flag it
even if it reads as plausible.

==================================================
ANTI-FABRICATION CHECK — COMPANIES, EXAMPLES, AND QUOTES
==================================================

FAIL if any of the following appear without being present in the
supplied research/search input for this article:

- A named company, product, or platform not mentioned in the research
  (e.g. "TechSolutions Inc.", "a global healthcare provider implemented...",
  "Microsoft's AI ethics board" — none of these are violations if and
  only if the named company/example genuinely appears in the research
  package; otherwise they are fabrications regardless of how plausible
  or "illustrative" they sound)
- An outcome, result, or business impact attributed to any company,
  named or unnamed, that does not appear in the supplied research
- A quote or statement attributed to a named individual, role, or
  organization not present in the supplied research
- A generic unnamed "case study" standing in for a real one
  ("a mid-sized software firm...", "a leading logistics company...")
  when the research package contains no such example

A fabricated company or outcome is a FAIL even when no fabricated
number accompanies it. Do not require a number to be present before
flagging a fabricated example — the company/outcome itself is the
violation.

==================================================
CASE STUDY CAP
==================================================

FAIL if the article contains more than one case-study-style example
(an example with a named or implied company, a challenge, an approach,
and an outcome) beyond the subject of the source article itself — even
if every individual example in isolation looks well-sourced. Multiple
examples across different sections (e.g. one in "Key Takeaways," another
in "Enterprise Leverage," a third in a Q&A) count as duplicates and FAIL
the check, regardless of section placement.

==================================================
PASS CONDITION
==================================================

PASS only if:
- Evidence is naturally distributed throughout the article
- Every specific number in the article is traceable to supplied research
- Every named company, platform, outcome, and quote in the article is
  traceable to supplied research
- No more than one case-study-style example exists in the entire article
"""