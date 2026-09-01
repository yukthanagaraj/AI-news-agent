# # quality_parts/article_length.py
# LENGTH_CHECK_RULES = """
# ARTICLE LENGTH CHECK

# Verify the article satisfies ALL of the following rules.

# WORD COUNT

# PASS only if:

# - Article contains between 1000 and 1400 words.
# - Never fewer than 900 words.
# - Never more than 1500 words.

# READING TIME

# PASS only if the estimated reading time is between 8 and 10 minutes.

# CONTENT DEPTH

# PASS only if:

# - Every major section contains detailed analysis.
# - The article develops ideas instead of briefly mentioning them.
# - Every section contributes meaningful enterprise insights.

# PARAGRAPHS

# PASS only if:

# - Every paragraph contains at least 3 complete sentences.
# - Paragraphs are not excessively short.
# - Paragraphs are not repetitive.

# OVERALL DEPTH

# PASS only if:

# - The article feels like an executive intelligence report.
# - Analysis is significantly deeper than the original news.
# - Strategic insights outweigh simple reporting.
# - Insight density matters more than raw length — do not penalize an
#   article near 1000 words if every paragraph teaches something new.

# RETURN FORMAT

# Length Check:
# PASS or FAIL

# If FAIL, briefly explain why.
# """

LENGTH_CHECK_RULES = """
ARTICLE LENGTH CHECK

Verify the article satisfies ALL of the following rules.

WORD COUNT

PASS only if:

- Article contains between 2000 and 2600 words.
- Never fewer than 1800 words.
- Never more than 2800 words.

READING TIME

PASS only if the estimated reading time is between 10 and 13 minutes.

CONTENT DEPTH

PASS only if:

- Every major section contains detailed analysis.
- The article develops ideas instead of briefly mentioning them.
- Every section contributes meaningful enterprise insights.

PARAGRAPHS

PASS only if:

- Every paragraph contains at least 3 complete sentences.
- Paragraphs are not excessively short.
- Paragraphs are not repetitive.
- No section relies on padding to reach length — every paragraph must
  teach something the reader didn't already know from earlier paragraphs.

OVERALL DEPTH

PASS only if:

- The article feels like an executive intelligence report.
- Analysis is significantly deeper than the original news.
- Strategic insights outweigh simple reporting.
- Length comes from genuine additional insight, not repetition or filler.

RETURN FORMAT

Length Check:
PASS or FAIL

If FAIL, briefly explain why.
"""