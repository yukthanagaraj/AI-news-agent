# quality_parts/title.py
TITLE_CHECK_RULES = """
TITLE CHECK RULES

MAIN TITLE (H1)

- Contain exactly 6-8 words.
- Contain no colon.
- Contain no quotation marks.
- Contain no company names, unless essential to the strategic shift.
- Sound like an executive insight, not a news headline.
- Avoid clickbait and questions.

FAIL if word count is outside 6-8 words.

SUBTITLE / DEK (optional, separate field — not part of the H1)

If a subtitle is generated, it must:

- Appear on its own line directly under the title, never merged
  into the title itself via a colon.
- Contain 6-14 words.
- Contain at least one concrete, searchable phrase the H1 is too
  abstract to carry (e.g. a named audience, a named mechanism, or a
  named outcome — "How CIOs Should Govern the New AI P&L").
- Not repeat words already used in the H1.
- Read as a plain-language expansion, not a second headline.

Return PASS or FAIL. If a subtitle is present, validate it as a
separate check line: "Subtitle Check: PASS/FAIL".
"""