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
QUOTE RULES

Generate one memorable standalone quote.

Rules:

- Exactly two sentences.
- Each sentence should appear on its own line.
- Leave one blank line between them.
- Editorial tone.
- Thought-provoking.
- Bold statement.
- No company names.
- No hype.
- Maximum 8 words per sentence.
- Suitable for large italic typography.
- Similar to Luvana AI Insights.

Format:

> First sentence.
>
> Second sentence.

Examples:

> Software was billed on availability.
>
> AI Employees will be billed on execution.

> Intelligence is abundant.
>
> Execution is scarce.

> AI agents automate tasks.
>
> AI employees own outcomes.

> Knowledge work becomes programmable.
>
> Outcomes become measurable.

> Trust becomes infrastructure.
>
> Execution becomes leverage.

IMPORTANT

Never output:

> First sentence. Second sentence.

Always output:

> First sentence.
>
> Second sentence.
"""