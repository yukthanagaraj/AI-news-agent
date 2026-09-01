# quality_parts/structure.py
STRUCTURE_CHECK_RULES = """
STRUCTURE CHECK

Verify the article follows ALL of these rules. Do NOT check for a fixed
list of section names — different article archetypes (Executive
Briefing, Market Analysis, Governance Deep Dive, Implementation
Playbook, Enterprise Case Study, Future Scenario, etc.) legitimately
use different section names and different numbers of sections. Judge
structure by function, not by matching specific heading text.

INTRODUCTION

PASS only if:

- The article starts with an Introduction (may or may not be labeled
  "Introduction" — the opening content counts even without a heading).
- The Introduction contains exactly 2 paragraphs.
- The Introduction explains the enterprise development.
- The Introduction does not summarize the source article.

QUOTE

PASS only if:

- Exactly ONE markdown blockquote exists.
- The quote appears immediately after the second introduction paragraph.
- The quote contains between 12 and 24 words.
- The quote is a strategic observation.
- The quote is not plain text.

MAIN ANALYSIS

PASS only if:

- The article contains 2-4 H2 sections of substantive analysis
  (beyond the introduction and conclusion), reflecting the article's
  selected archetype.
- No two sections answer the same underlying executive question,
  regardless of how differently their headings are worded.
- Section headings are specific to today's thesis, not generic
  boilerplate like "Enterprise Impact" or "Strategic Recommendations"
  repeated without distinction.

SECTION VALIDATION

PASS only if every major H2 section contains at least 3 paragraphs.

FAIL if any H2 section contains only one or two paragraphs.

FAIL if any required section is missing.

KEY TAKEAWAYS

PASS only if, somewhere in the article:

- A Key Takeaways section (or equivalent bulleted summary section)
  exists with exactly 5 bullet points.
- Every bullet is unique.
- Every bullet provides one executive insight not already stated
  verbatim elsewhere.

STRATEGIC CONCLUSION

PASS only if:

- A concluding section exists (name may vary by archetype).
- Contains exactly 2 paragraphs.
- Ends with a strategic executive observation.
- Introduces a new idea rather than summarizing prior sections.

RETURN FORMAT

Structure Check:
PASS or FAIL

If FAIL, briefly explain why, and specify which functional requirement
(not which heading name) was not met.
"""