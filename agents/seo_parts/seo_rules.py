SEO_RULES = """
SEO RULES

Generate:

- SEO Title
- Meta Title

Meta title:

- 50-60 characters.
- Reflects the article title's strategic thesis (does not need to be
  word-for-word identical to the article title).
- No clickbait.
- No colons.

GROUNDING REQUIREMENT:

Both SEO Title and Meta Title must preserve at least ONE concrete,
specific element from the article -- a named company, named
technology, or named mechanism the article actually discusses (e.g.
if the article discusses HSBC's AI center of excellence, at least one
of the two titles should reference "in-house AI" or "banking AI
talent," not just generic phrases like "AI Transformation" or
"Enterprise Success"). Do not smooth a specific article title back
into generic language to fit the character count -- trim length by
cutting filler words, not by removing the specific element.

SEO Title and Meta Title must be MEANINGFULLY DIFFERENT from each
other in wording, not near-duplicate rewordings of the same sentence
with one swapped synonym.

Meta description is generated separately — see SUMMARY RULES.

Avoid hype.
"""