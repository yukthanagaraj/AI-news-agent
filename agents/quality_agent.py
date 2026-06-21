import os
from dotenv import load_dotenv
from groq import Groq

from agents.quality_parts.title import TITLE_CHECK_RULES
from agents.quality_parts.quote import QUOTE_CHECK_RULES
from agents.quality_parts.faq import FAQ_CHECK_RULES
from agents.quality_parts.duplicate import DUPLICATE_CHECK_RULES

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

{FAQ_CHECK_RULES}

{DUPLICATE_CHECK_RULES}

OUTPUT ONLY:

Title Check:
PASS or FAIL

Quote Check:
PASS or FAIL

FAQ Check:
PASS or FAIL

Duplicate Check:
PASS or FAIL

Overall:
PASS or FAIL
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content":
                "You are an editorial quality reviewer for an enterprise AI publication."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
        max_tokens=300
    )

    print("QUALITY CHECK COMPLETE")

    return response.choices[0].message.content