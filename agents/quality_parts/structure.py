STRUCTURE_CHECK_RULES = """
STRUCTURE CHECK

Verify the article follows ALL of these rules.

INTRODUCTION

PASS only if:

- The article starts with an Introduction.
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

SECTION ORDER

Verify the following sections exist in this exact order:

1. Introduction
2. Why This Matters
3. Enterprise Impact
4. AI Agents Perspective
5. Human-AI Collaboration
6. Future of Work
7. Strategic Recommendations
8. Key Takeaways
9. Strategic Conclusion

SECTION VALIDATION

PASS only if every major section contains at least 2 paragraphs.

FAIL if any section contains only one paragraph.

FAIL if any required section is missing.

KEY TAKEAWAYS

PASS only if:

- Exactly 5 bullet points exist.
- Every bullet is unique.
- Every bullet provides one executive insight.

STRATEGIC CONCLUSION

PASS only if:

- Strategic Conclusion exists.
- Contains exactly 2 paragraphs.
- Ends with a strategic executive observation.
- Does not summarize the article.

RETURN FORMAT

Structure Check:
PASS or FAIL

If FAIL, briefly explain why.
"""