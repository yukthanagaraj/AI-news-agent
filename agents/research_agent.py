# from groq import Groq
# from dotenv import load_dotenv
# import os

# load_dotenv()

# client = Groq(
#     api_key=os.getenv("GROQ_API_KEY")
# )

# def fetch_ai_news(previous_titles=None, previous_sources=None):

#     exclusion_block = ""
#     exclusions = []

#     if previous_titles:
#         exclusion_list = "\n".join(
#             f"- {title}" for title in previous_titles
#         )
#         exclusions.append(f"Do NOT repeat any of these previously covered topics:\n{exclusion_list}")

#     if previous_sources:
#         sources_list = ", ".join(previous_sources)
#         exclusions.append(f"Do NOT use any of these recently used news sources to vary the reporting: {sources_list}")

#     if exclusions:
#         joined_exclusions = "\n\n".join(exclusions)
#         exclusion_block = f"""
# IMPORTANT EXCLUSIONS:
# {joined_exclusions}

# Pick a completely different topic and a different source.
# """

#     prompt = f"""
# Fetch ONE latest unique tech, business, SaaS, or scientific news topic (e.g. related to future of work, automation, operations, biotechnology, databases, security, or technology shifts) from the last 24 hours.

# Return ONLY in this format:

# Title: <news title>

# Summary: <short summary>

# Source: <source name>

# Date: <date>

# Image: <image prompt>

# Rules:

# - Make sure the topic is fresh and different from common repeated tech news.
# - The title and topic do NOT always need to focus on or contain the word "AI". Focus on broader technology, software, and operational shifts.
# - Use a REAL source name.
# - Examples: Reuters, Bloomberg, TechCrunch, Wired, MIT Technology Review, The Verge, VentureBeat, Nature, Science Daily, TechSoft, etc.
# - Do NOT always use the same source.
# - Vary the source whenever appropriate.
# - Source must never be empty.
# - Image must never be empty.
# - Keep summary under 100 words.

# {exclusion_block}
# """

#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ],
#         temperature=0.9,
#         max_tokens=500
#     )

#     return response.choices[0].message.content

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def fetch_ai_news(previous_titles=None, previous_sources=None):

    exclusion_block = ""

    exclusions = []

    if previous_titles:

        title_list = "\n".join(
            f"- {title}" for title in previous_titles
        )

        exclusions.append(
            f"""
Do NOT repeat any of these topics:

{title_list}
"""
        )

    if previous_sources:

        source_list = ", ".join(previous_sources)

        exclusions.append(
            f"""
Do NOT use any of these recently used sources:

{source_list}
"""
        )

    if exclusions:

        exclusion_block = f"""

IMPORTANT:

{"".join(exclusions)}

Choose a completely different topic and source.
"""

    prompt = f"""

You are a senior research analyst for a Future of Work and Enterprise AI insights platform.

Your job is to find ONE recent development that signals a larger shift in how organizations, teams, and work itself are changing.

PRIORITY TOPICS

- AI Agents
- Agentic AI
- Digital Workers
- AI Employees
- Future of Work
- Human-AI Collaboration
- Enterprise AI
- Autonomous Operations
- Workforce Transformation
- Enterprise Productivity
- Digital Labor
- Enterprise Automation
- Intelligent Workflows
- Enterprise Knowledge Systems
- Multi-Agent Systems
- AI Infrastructure
- AI Governance
- Organizational Transformation

PRIORITY COMPANIES

- OpenAI
- Anthropic
- Google DeepMind
- Microsoft
- NVIDIA
- Salesforce
- ServiceNow
- Workday
- SAP
- Oracle
- HubSpot
- Notion
- Cursor
- Perplexity

AVOID

- Biotechnology
- Gene Editing
- CRISPR
- Healthcare Research
- Climate Science
- Physics Discoveries
- Space Research
- Consumer Gadgets
- Smartphones
- Gaming

unless directly related to AI workforce transformation.

Return ONLY in this format:

Title: <title>

Summary: <summary under 100 words>

Source: <publication name>

Source URL: <full source url>

Date: <date>

Image Prompt: <detailed editorial illustration prompt>

Rules:

- Focus on enterprise implications.
- Focus on organizational change.
- Focus on future of work.
- Focus on AI employees and digital workers.
- Avoid generic AI news.
- Avoid product launch announcements unless strategically important.
- Prefer stories that change how businesses operate.
- Source URL must never be empty.
- Image Prompt must never be empty.
- Summary must be under 100 words.

{exclusion_block}
"""



    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=1.0,
        max_tokens=600
    )

    return response.choices[0].message.content