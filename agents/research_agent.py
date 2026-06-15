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

import os
import random
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from newspaper import Article

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def fetch_ai_news(
    previous_titles=None,
    previous_sources=None,
    previous_urls=None
):

    query = """
(OpenAI OR Anthropic OR Microsoft
OR Salesforce OR ServiceNow
OR Workday OR SAP OR Oracle
OR Notion OR Perplexity)

AND

("AI Agent" OR
"Agentic AI" OR
"Enterprise AI" OR
"Digital Labor" OR
"Future of Work" OR
"Autonomous Operations" OR
"Enterprise Productivity" OR
"Enterprise Software" OR
"Workplace Automation" OR
"Knowledge Work")
"""

    bad_domains = [
        "pypi.org",
        "github.com",
        "npmjs.com",
        "medium.com",
        "springer.com",
        "arxiv.org",
        "researchgate.net",
        "naturalnews.com",
        "biztoc.com",
        "cnx-software.com",
        "tomshardware.com",
        "anandtech.com"
    ]

    articles = []

    for hours in [24, 48]:

        cutoff = (
            datetime.utcnow() - timedelta(hours=hours)
        ).strftime("%Y-%m-%dT%H:%M:%SZ")

        print(f"Trying {hours}-hour news window")

        response = requests.get(
            "https://newsapi.org/v2/everything",
            params={
                "q": query,
                "from": cutoff,
                "sortBy": "publishedAt",
                "language": "en",
                "pageSize": 50,
                "apiKey": NEWS_API_KEY
            }
        )

        if response.status_code != 200:
            print("NEWS API ERROR")
            print(response.text)
            continue

        data = response.json()

        articles = data.get("articles", [])

        random.shuffle(articles)

        print(f"Found {len(articles)} articles in {hours}-hour window")

        if articles:
            break

    if not articles:
        print("No articles found")
        return None

    for article in articles:

        title = article.get("title", "")
        source = article.get("source", {}).get("name", "")
        url = article.get("url", "")

        if previous_urls and url in previous_urls:
            print("Skipping used URL")
            continue

        if previous_titles and title in previous_titles:
            print("Skipping used title")
            continue

        if source.lower() in [
            "hacker news",
            "reddit"
        ]:
            print("Skipping community source")
            continue

        if any(word in title.lower() for word in [
            "bitcoin",
            "crypto",
            "cryptocurrency",
            "ethereum",
            "token",
            "rust",
            "frontend",
            "backend",
            "github",
            "framework",
            "library",
            "review",
            "benchmark",
            "pypi",
            "release",
            "version",
            "gpu",
            "graphics card",
            "smartphone",
            "motherboard",
            "camera"
        ]):
            print("Skipping unwanted article")
            continue

        if any(domain in url for domain in bad_domains):
            print("Skipping bad source")
            continue

        print("TITLE =", title)
        print("SOURCE =", source)
        print("URL =", url)
        print("-" * 80)

        full_text = ""

        try:

            article_obj = Article(url)

            article_obj.download()
            article_obj.parse()

            full_text = article_obj.text[:8000]

            print("ARTICLE EXTRACTED")

        except Exception as e:

            print("ARTICLE EXTRACTION FAILED:", e)

            full_text = article.get("description", "")

        print("RESEARCH SOURCE URL =", url)

        return f"""
Title: {title}

Summary: {article.get('description', '')}

Source: {source}

Source URL: {url}

Date: {article.get('publishedAt', '')}

Article Text:
{full_text}

Image Prompt: Futuristic enterprise workforce with digital workers collaborating with humans, autonomous workflows, enterprise productivity dashboards.
"""

    print("No suitable article found")
    return None