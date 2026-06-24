# QUOTE_RULES = """
# One section should contain a memorable standalone quote.

# Rules:

# - One or two lines.
# - Editorial.
# - Thought-provoking.
# - Memorable.
# - Suitable for italic formatting.
# - Avoid generic statements.
# - No company names.
# - Sound like an executive insight.

# Examples:

# > Software was billed on availability.
# AI Employees will be billed on execution.

# > Intelligence is abundant.
# Execution is scarce.

# > Trust becomes infrastructure.

# > Decision speed becomes a competitive advantage.

# > Organizations will compete on autonomy.

# > Digital labor scales differently than software.

# > Human capability expands through autonomous systems.

# > Knowledge work is becoming programmable.
# """

QUOTE_CHECK_RULES = """
QUOTE CHECK

PASS if:

* The article contains exactly one markdown blockquote.
* The quote uses markdown > syntax.
* The quote appears inside the Blog content.
* The quote appears near the introduction.
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
  """
