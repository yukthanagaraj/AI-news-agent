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

QUOTE_RULES = """
QUOTE OBJECTIVE

Generate EXACTLY ONE memorable executive quote.

The quote should represent the single strongest strategic insight from the article.

The quote MUST appear immediately after the second introduction paragraph.

Output ONLY as a markdown blockquote.

Correct Example:

> AI agents amplify execution before they replace effort.

Incorrect:

AI agents amplify execution before they replace effort.

Incorrect:

> AI agents amplify execution

>

> before they replace effort.

==================================================
QUOTE LENGTH
============

* One sentence only.
* Between 12 and 24 words.
* Never exceed 24 words.
* No quotation marks.

==================================================
WRITING STYLE
=============

The quote should sound like an observation from an enterprise strategist.

It should feel timeless rather than tied to today's news.

Write with confidence.

Keep it concise.

Professional editorial tone.

==================================================
FOCUS
=====

The quote should naturally relate to one of these themes:

* Agentic AI
* AI Agents
* Enterprise AI
* AI Employees
* Digital Workers
* Enterprise Automation
* Human-AI Collaboration
* Operational Intelligence
* Enterprise Productivity
* Decision Making
* Organizational Learning
* Competitive Advantage

==================================================
AVOID
=====

Do NOT:

* Mention company names.
* Mention CEOs.
* Mention products.
* Mention model names.
* Mention funding.
* Mention statistics.
* Mention dates.
* Mention news events.
* Summarize the article.
* Use marketing language.
* Use clichés.
* Generate motivational quotes.

==================================================
GOOD EXAMPLES
=============

> Software no longer creates value; intelligent execution does.

> Intelligence compounds when execution becomes autonomous.

> AI agents amplify execution before they replace effort.

> Enterprises compete through coordination before computation.

> Every intelligent workflow becomes a competitive asset.

> Competitive advantage increasingly belongs to operational intelligence.

> Organizations that coordinate intelligence outperform those that simply deploy AI.

> Business value emerges when intelligence becomes operational.

==================================================
BAD EXAMPLES
============

OpenAI launched another powerful AI model.

AI is changing everything.

This technology will revolutionize business.

AI Agents are the future.

The enterprise world is evolving rapidly.

==================================================
FINAL VALIDATION
================

Before returning the quote verify:

* Exactly one markdown blockquote.
* One sentence.
* Between 12 and 24 words.
* Executive tone.
* Strategic insight.
* No company names.
* No product names.
* No hype.
* No repetition.
* Suitable as the article's featured quote.

Never generate more than ONE quote.
"""
