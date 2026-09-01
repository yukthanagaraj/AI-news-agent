AEO_CHECK_RULES = """
AEO VALIDATION

Verify the article is optimized for Answer Engine Optimization (AEO).

EXECUTIVE QUESTIONS

PASS only if the article clearly answers the following questions:

- Why does this development matter?
- What changes for enterprises?
- How do AI Agents improve execution?
- How will Human-AI Collaboration evolve?
- What is the future impact on organizations?
- What should enterprise leaders do next?

ANSWER QUALITY

PASS only if:

- Every section directly answers a meaningful executive question.
- Answers are complete and easy to understand.
- Answers are supported with strategic analysis.
- Answers avoid vague or generic statements.

ARTICLE STRUCTURE

PASS only if:

- Introduction clearly establishes the topic.
- Each section focuses on one major idea.
- Ideas flow logically from one section to another.
- The conclusion reinforces the strategic insight.

SCANNABILITY

PASS only if:

- Clear headings are used.
- Key Takeaways section exists.
- Bullet points summarize important ideas.
- Information is easy for AI systems to extract.


ENTERPRISE FOCUS

PASS only if:

- Enterprise AI remains the central topic.
- AI Agents are discussed from a business perspective.
- Human-AI Collaboration is explained.
- Strategic Recommendations are included.

AI SEARCH OPTIMIZATION

PASS only if:

- Content provides direct answers.
- Information is factual.
- Sections are well organized.
- Important concepts are easy to identify.
- The article is suitable for AI-powered search engines and assistants.

RETURN FORMAT

AEO Check:
PASS or FAIL

If FAIL, briefly explain why.

AEO VALIDATION

The Quick Answer, FAQs and Schema should be derived from the article.

Do not invent new concepts.

Questions should already be answered somewhere inside the article.

The AEO output should summarize the strongest answers already written.
"""