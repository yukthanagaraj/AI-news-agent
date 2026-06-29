
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

OBJECTIVE

Generate complete Answer Engine Optimization (AEO) content for an Enterprise AI publication.

Optimize for:

- Google AI Overviews
- ChatGPT
- Claude
- Gemini
- Perplexity
- Microsoft Copilot

OUTPUT ONLY

## Executive Summary

<2-3 sentence summary>

## Quick Answer

<40-80 word answer>

## Key Facts

- Fact 1
- Fact 2
- Fact 3
- Fact 4
- Fact 5

## FAQs

### Question 1

Answer

### Question 2

Answer

### Question 3

Answer

### Question 4

Answer

### Question 5

Answer

## AI Overview Summary

<Short summary suitable for AI-generated answers>

## Schema

<Article schema>

<FAQPage schema>
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
You are a senior Answer Engine Optimization strategist for an Enterprise AI publication.

Generate structured answers optimized for AI search systems.

Prioritize:

- Clear answers
- Executive summaries
- High-quality FAQs
- Structured information
- AI readability

Avoid unnecessary repetition.

Produce factual, concise and well-organized content.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=900
    )

    print("AEO GENERATED")

    return response.choices[0].message.content

