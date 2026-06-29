
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

OBJECTIVE

Generate complete SEO metadata for an Enterprise AI publication.

Focus on:

- AI Agents
- Agentic AI
- Enterprise AI
- AI Employees
- Digital Workers
- Human-AI Collaboration
- Future of Work
- Enterprise Productivity
- Autonomous Operations

OUTPUT ONLY

Slug:
<slug>

SEO Title:
<50-60 characters>

Meta Title:
<50-60 characters>

Meta Description:
<140-160 characters>

Primary Keyword:
<keyword>

Secondary Keywords:

- keyword
- keyword
- keyword
- keyword
- keyword

Semantic Keywords:

- keyword
- keyword
- keyword
- keyword
- keyword

Tags:

- tag
- tag
- tag
- tag
- tag

Related Topics:

- topic
- topic
- topic
- topic
- topic

Internal Linking Suggestions:

- suggestion
- suggestion
- suggestion

Open Graph Title:
<title>

Open Graph Description:
<description>

Twitter Title:
<title>

Twitter Description:
<description>
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
You are a senior Enterprise AI SEO strategist.

Generate professional SEO metadata.

Optimize for:

- Google Search
- Google AI Overviews
- ChatGPT
- Claude
- Gemini
- Perplexity

Use semantic SEO.

Avoid keyword stuffing.

Prioritize enterprise search intent.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=700
    )

    print("SEO GENERATED")

    return response.choices[0].message.content

