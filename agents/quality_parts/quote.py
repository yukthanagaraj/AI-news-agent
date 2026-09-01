QUOTE_CHECK_RULES = """
QUOTE CHECK

PASS only if ALL of the following conditions are satisfied:

• Exactly one markdown blockquote exists.

• The blockquote appears immediately after the second introduction paragraph.

• The quote contains between 12 and 24 words.

• The quote is exactly one sentence.

• The quote uses an executive, strategic tone.

• The quote contains no company names.

• The quote contains no product names.

• The quote is not promotional.

• The quote summarizes a strategic insight rather than the news itself.

Otherwise return FAIL.
"""