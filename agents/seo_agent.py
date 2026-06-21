import os
from groq import Groq
from dotenv import load_dotenv

from agents.seo_parts.seo_rules import SEO_RULES
from agents.seo_parts.slug_rules import SLUG_RULES
from agents.seo_parts.summary_rules import SUMMARY_RULES
from agents.seo_parts.tags_rules import TAGS_RULES
from agents.seo_parts.related_topics_rules import RELATED_TOPICS_RULES

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_seo(
    title,
    article
):

    prompt = f"""
TITLE

{title}

ARTICLE

{article}

{SEO_RULES}

{SLUG_RULES}

{SUMMARY_RULES}

{TAGS_RULES}

{RELATED_TOPICS_RULES}

IMPORTANT

Focus on:

- AI Agents
- Agentic AI
- AI Employees
- Enterprise AI
- Digital Workers
- Human + AI Collaboration
- Future of Work

OUTPUT ONLY:

Slug: <slug>

Meta Title: <meta title>

Meta Description: <description>

Keywords:

- keyword1
- keyword2
- keyword3
- keyword4
- keyword5

Related Topics:

- topic1
- topic2
- topic3
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content":
                "You are an SEO strategist for an enterprise AI publication."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=400
    )

    print("SEO GENERATED")

    return response.choices[0].message.content