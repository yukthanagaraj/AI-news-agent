import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from newspaper import Article

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def fetch_ai_news(previous_titles=None, previous_sources=None):

    query = """
(OpenAI OR Anthropic OR Microsoft OR NVIDIA
OR Salesforce OR ServiceNow
OR Workday OR SAP OR Oracle
OR Notion OR Perplexity OR Cursor)

AND

("AI" OR
"AI Agent" OR
"Agentic AI" OR
"Enterprise AI" OR
"Future of Work" OR
"Digital Labor" OR
"Autonomous Operations" OR
"Knowledge Management" OR
"Enterprise Productivity")
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





