SEO_CHECK_RULES = """
SEO VALIDATION

Verify the article follows ALL SEO best practices.

PRIMARY KEYWORDS

PASS only if the article naturally includes:

- AI Agents
- Enterprise AI
- Agentic AI

SECONDARY KEYWORDS

PASS only if the article naturally includes several of the following:

- AI Employees
- Digital Workers
- Human-AI Collaboration
- Enterprise Automation
- Future of Work
- Enterprise Productivity
- Autonomous Operations
- Operational Intelligence
- Organizational Intelligence
- Business Transformation

KEYWORD USAGE

PASS only if:

- Keywords are naturally integrated.
- Keywords are not stuffed.
- Keywords fit the paragraph context.
- Keywords improve readability.

TITLE SEO

PASS only if:

- Title contains 6 to 8 words.
- Title contains an important enterprise AI keyword.
- No clickbait.
- No unnecessary punctuation.
- No colon.

HEADINGS

PASS only if:

- Section headings are descriptive.
- Headings help search engines understand the article.
- Headings reflect enterprise AI topics.

CONTENT QUALITY

PASS only if:

- Article answers common enterprise AI questions.
- Content is informative.
- Content demonstrates expertise.
- Content is original.

READABILITY

PASS only if:

- Short paragraphs.
- Clear language.
- Executive writing style.
- Easy to scan.

RETURN FORMAT

SEO Check:
PASS or FAIL

If FAIL, briefly explain why.

KEYWORD VALIDATION

Evaluate whether the generated article naturally includes the recommended keywords.

Avoid recommending keywords that are absent from the article.

Prefer keywords already discussed in the article.

Generate keywords that accurately represent the article rather than generic AI terminology.
"""