import os
from groq import Groq
from dotenv import load_dotenv

from agents.aeo_parts.answer import QUICK_ANSWER_RULES
from agents.aeo_parts.faq_rules import FAQ_RULES
from agents.aeo_parts.schema_rules import SCHEMA_RULES

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_aeo(
    title,
    article
):

    prompt = f"""
TITLE

{title}

ARTICLE

{article}

{QUICK_ANSWER_RULES}

{FAQ_RULES}

{SCHEMA_RULES}

OUTPUT ONLY:

## Quick Answer

<answer>

## FAQs

### Question 1

Answer

### Question 2

Answer

### Question 3

Answer

## Schema

<Article schema>

<FAQPage schema>
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content":
                "You are an Answer Engine Optimization strategist for an enterprise AI publication."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=700
    )

    print("AEO GENERATED")

    return response.choices[0].message.content