SEO_CHECK_RULES = """
SEO VALIDATION

Verify the article follows ALL SEO best practices.

PRIMARY KEYWORDS

PASS only if the article naturally includes "Enterprise AI" or a close synonym (enterprise artificial intelligence, enterprise-grade AI), AND at least one of the following that is topically relevant to what the article actually covers:

- AI Agents / Agentic AI (if the article discusses autonomous or agentic systems)
- The specific named technology, model, or program the article is about (e.g. "Qwen3.8-Max", "Xcelerate", the actual subject)
- A close domain-relevant term if neither of the above naturally fits the article's actual subject matter (e.g. "AI infrastructure investment", "AI governance", "enterprise technology strategy")

Do not fail an article solely for omitting the literal phrase "AI Agents" when the article's actual subject is a different but still legitimate enterprise-AI topic.

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

TLE SEO

PASS only if:

- Title contains 6 to 12 words.
- Title contains an important enterprise AI keyword or names the specific technology/company/mechanism the article is about.
- No clickbait (no vague curiosity-gap phrasing like "You Won't Believe...").
- A single colon separating a hook from a specific claim is acceptable Luvana house style (e.g. "Navigating the Open-Weight AI Landscape: Alibaba's Challenge to American Firms") -- flag only titles with 2+ colons or excessive punctuation stacking.
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