DUPLICATE_CHECK_RULES = """
DUPLICATE CHECK RULES

Detect:

- Repeated section titles.
- Repeated quotes.
- Duplicate ideas.

STRUCTURAL DUPLICATION (in addition to literal repeats)

FAIL if the article contains two or more "Enterprise Evidence" /
illustrative example blocks that follow the same Challenge → Approach
→ Outcome shape AND rely on substantially the same underlying
mechanism to solve the challenge (e.g. two examples that both resolve
via "tiered routing between an open-source baseline and a premium
model, plus caching, plus a human-in-the-loop approval step") — even
if the company name, industry, and surface wording differ each time.

A second example is only acceptable if it demonstrates a genuinely
different mechanism, constraint, or trade-off than the first — not a
re-skinned version of the same solution.

Return PASS or FAIL. If FAIL due to structural duplication, name the
shared mechanism that caused the fail, not just "duplicate content."
"""