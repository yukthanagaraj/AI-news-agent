QUOTE_CHECK_RULES = """
QUOTE CHECK

PASS if:

* The article contains exactly one markdown blockquote.
* The quote uses markdown > syntax.
* The quote appears inside the Blog content.
* The quote appears after the introduction.
* The quote appears before the first major section heading.
* The quote is a single sentence.
* The quote contains between 8 and 20 words.
* The quote reinforces the article's main insight.
* The quote sounds editorial and memorable.

FAIL if:

* No quote exists.
* More than one quote exists.
* The quote is repeated.
* The quote appears inside Key Takeaways.
* The quote appears inside the Conclusion.
* The quote is longer than 20 words.
* The quote is generic or unrelated to the article.

Return PASS or FAIL.
"""