import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def fetch_ai_news(previous_titles=None, previous_sources=None):

    cutoff = (
        datetime.utcnow() - timedelta(hours=48)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")

    query = """
    (OpenAI OR Anthropic OR Microsoft OR NVIDIA
    OR Salesforce OR ServiceNow)
    AND
    ("AI Agent" OR "Agentic AI"
    OR "Enterprise AI"
    OR "Future of Work")
    """

    allowed_sources = [
        "TechCrunch",
        "VentureBeat",
        "Reuters",
        "MIT Technology Review",
        "The Verge",
        "Wired",
        "Fast Company",
        "Forbes",
        "Business Insider"
    ]

    bad_domains = [
        "pypi.org",
        "github.com",
        "npmjs.com",
        "medium.com"
    ]

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
        return None

    data = response.json()

    articles = data.get("articles", [])

    if not articles:
        print("No articles found")
        return None

    for article in articles:

        title = article.get("title", "")
        source = article.get("source", {}).get("name", "")
        url = article.get("url", "")

        print("TITLE =", title)
        print("SOURCE =", source)
        print("URL =", url)
        print("-" * 80)

        if previous_titles and title in previous_titles:
            continue

        if previous_sources and source in previous_sources:
            continue

        if source not in allowed_sources:
            continue

        if any(domain in url for domain in bad_domains):
            continue

        print(f"RESEARCH SOURCE URL = {url}")

        return f"""
Title: {title}

Summary: {article.get('description', '')}

Source: {source}

Source URL: {url}

Date: {article.get('publishedAt', '')}

Image Prompt: Futuristic enterprise workforce with digital workers collaborating with humans, autonomous workflows, enterprise productivity dashboards.
"""

    print("No suitable article found")
    return None






