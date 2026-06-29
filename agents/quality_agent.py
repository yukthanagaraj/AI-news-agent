import os
from dotenv import load_dotenv
from groq import Groq

from agents.quality_parts.title import TITLE_CHECK_RULES
from agents.quality_parts.quote import QUOTE_CHECK_RULES
from agents.quality_parts.faq import FAQ_CHECK_RULES
from agents.quality_parts.duplicate import DUPLICATE_CHECK_RULES
from agents.quality_parts.structure import STRUCTURE_CHECK_RULES
from agents.quality_parts.article_length import LENGTH_CHECK_RULES
from agents.quality_parts.seo_rules import SEO_CHECK_RULES
from agents.quality_parts.aeo_rules import AEO_CHECK_RULES

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def quality_check(
    title,
    article
):

    prompt = f"""
TITLE

{title}

ARTICLE

{article}

{TITLE_CHECK_RULES}

{QUOTE_CHECK_RULES}

{STRUCTURE_CHECK_RULES}

{LENGTH_CHECK_RULES}

{SEO_CHECK_RULES}

{AEO_CHECK_RULES}

{FAQ_CHECK_RULES}

{DUPLICATE_CHECK_RULES}


OUTPUT ONLY

Title Check:
PASS or FAIL

Quote Check:
PASS or FAIL

Structure Check:
PASS or FAIL

Length Check:
PASS or FAIL

SEO Check:
PASS or FAIL

AEO Check:
PASS or FAIL

FAQ Check:
PASS or FAIL

Duplicate Check:
PASS or FAIL

Overall:
PASS or FAIL

If any section fails, briefly explain why.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
You are a senior editorial quality reviewer for an Enterprise AI publication.

Your responsibility is to verify that every article satisfies all editorial standards.

Evaluate:

- Structure
- Editorial quality
- SEO
- AEO
- Enterprise writing style
- Quote placement
- Readability
- Executive writing quality

Do not rewrite the article.

Only evaluate it.

Return PASS or FAIL exactly as requested.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
        max_tokens=600
    )

    print("QUALITY CHECK COMPLETE")

    return response.choices[0].message.content