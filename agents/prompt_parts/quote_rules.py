QUOTE_RULES = """
==================================================
EDITORIAL QUOTE
==================================================

QUOTE OBJECTIVE

Generate EXACTLY ONE memorable executive quote.

The quote should represent the strongest strategic insight from the article.

It should feel like a premium editorial pull quote from publications such as Stripe, Anthropic, or Linear.

Output ONLY as a markdown blockquote.

Correct Example:

> AI agents are becoming the execution layer of modern enterprises.

Incorrect:

AI agents are becoming the execution layer of modern enterprises.

Incorrect:

> AI agents are becoming
>
> the execution layer of modern enterprises.

==================================================
QUOTE LENGTH
==================================================

- Exactly ONE sentence.
- Between 8 and 12 words.
- Never exceed 12 words.
- Maximum 70 characters preferred.
- No quotation marks.
- No commas unless absolutely necessary.
- No semicolons.
- No colons.
- No parentheses.

The quote should naturally wrap into 2–3 lines on desktop.

==================================================
WRITING STYLE
==================================================

The quote should sound like a timeless executive observation.

Keep it bold.

Keep it simple.

Keep it memorable.

Avoid complicated sentence structures.

Every word should add meaning.

==================================================
FOCUS
==================================================

The quote should naturally relate to one of these themes:

- AI Agents
- Enterprise AI
- Agentic Execution
- Enterprise Intelligence
- Governance
- Operational Intelligence
- Enterprise Productivity
- Human-AI Collaboration
- Decision Making
- Competitive Advantage

==================================================
AVOID
==================================================

Do NOT:

- Mention company names.
- Mention CEOs.
- Mention products.
- Mention model names.
- Mention funding.
- Mention statistics.
- Mention dates.
- Mention news events.
- Mention technical jargon.
- Mention infrastructure components.
- Use long lists.
- Use multiple clauses.
- Explain the article.
- Summarize the article.
- Use clichés.
- Generate motivational quotes.

Never write long quotes like:

> Performance shifts from infrastructure placement, interconnects, and power where intelligence actually executes.

==================================================
GOOD EXAMPLES
==================================================

> AI agents are becoming the execution layer of modern enterprises.

> Governance determines enterprise AI success.

> Intelligence becomes valuable through disciplined execution.

> Enterprises compete through operational intelligence.

> Execution is replacing automation as the competitive advantage.

> Enterprise value begins where intelligent execution scales.

> Governance transforms intelligence into enterprise capability.

> Competitive advantage now belongs to operational intelligence.

==================================================
BAD EXAMPLES
==================================================

> Performance shifts from infrastructure placement, interconnects, and power where intelligence actually executes.

> OpenAI launched another powerful model.

> AI is changing everything.

> Enterprise AI changes every business forever.

> This technology will revolutionize organizations.

==================================================
PLACEMENT
==================================================

The quote MUST appear immediately after the second introduction paragraph.

The article must contain exactly ONE markdown blockquote.

No additional blockquotes are allowed.

Never split the quote across multiple markdown blockquote lines.

Always output as:

> Your single sentence here.

==================================================
FINAL VALIDATION
==================================================

Before returning the quote verify:

✓ Exactly one markdown blockquote.
✓ Exactly one sentence.
✓ Between 8 and 12 words.
✓ Maximum 12 words.
✓ Premium editorial tone.
✓ Strategic insight.
✓ No company names.
✓ No products.
✓ No hype.
✓ No repetition.
✓ Reads naturally in 2–3 wrapped lines on desktop.
"""