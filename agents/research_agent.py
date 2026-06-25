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
("AI Agents" OR
"Agentic AI" OR
"AI Employees" OR
"Digital Workers" OR
"Enterprise AI" OR
"Autonomous Operations" OR
"Human AI Collaboration" OR
"Future of Work" OR
"Enterprise Productivity")
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
        "tomshardware.com",
        "anandtech.com",
        "gsmarena.com",
        "financialpost.com",
        "businesswire.com",
        "prnewswire.com",
        "globenewswire.com",
        "benzinga.com",
        "einnews.com",
        "yahoo.com",
        "finance.yahoo.com",
        "seekingalpha.com",
        "fool.com",
        "marketscreener.com"
    ]

    required_keywords = [
        "ai agent",
        "ai agents",
        "agentic ai",
        "enterprise ai",
        "ai employee",
        "ai employees",
        "digital worker",
        "digital workers",
        "autonomous operations",
        "future of work",
        "human ai collaboration",
        "enterprise productivity"
    ]

    trusted_sources = [
        "Reuters",
        "VentureBeat",
        "TechCrunch",
        "The Verge",
        "Wired",
        "MIT Technology Review",
        "Forbes",
        "Fast Company",
        "Business Insider",
        "ComputerWeekly.com",
        "ZDNet",
        "InfoWorld"
    ]

    unwanted_keywords = [
        # Hardware
        "gpu",
        "graphics card",
        "cpu",
        "chip",
        "hardware",
        "device",

        # Robotics
        "robot",
        "robots",
        "robotics",
        "drone",
        "drones",
        "vlc",

        # Libraries
        "framework",
        "library",
        "sdk",
        "release",
        "version",

        # Development
        "frontend",
        "backend",
        "github",
        "python",

        # Consumer
        "smartphone",
        "camera",
        "iphone",
        "android",

        # Crypto
        "bitcoin",
        "crypto",
        "ethereum",
        "token",

        # Benchmarks
        "benchmark",
        "review",

        # Politics
        "election",
        "political",
        "campaign"
    ]

    articles = []

    for hours in [24, 48, 72]:

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

        print(
            f"Found {len(articles)} articles in {hours}-hour window"
        )

        if articles:
            break

    if not articles:
        print("No articles found")
        return None

    for article in articles:

        title = article.get("title", "")
        source = article.get("source", {}).get("name", "")

        if source not in trusted_sources:
            print("Skipping low-quality source")
            continue

        if "business wire" in source.lower():
            print("Skipping press release")
            continue

        if "press release" in title.lower():
            print("Skipping press release")
            continue

        url = article.get("url", "")

        content_to_check = (
            title + " " +
            article.get("description", "")
        ).lower()

        # Check for required keywords
        if not any(
            keyword in content_to_check
            for keyword in required_keywords
        ):
            print("Skipping non-agentic article")
            continue

        # Skip if URL already used
        if previous_urls and url in previous_urls:
            print("Skipping used URL")
            continue

        # Skip if title already used
        if previous_titles and title in previous_titles:
            print("Skipping used title")
            continue

        # Skip community sources
        if source.lower() in [
            "reddit",
            "hacker news",
            "the next web"
        ]:
            print("Skipping community source")
            continue

        # Skip articles with unwanted keywords
        if any(word in title.lower() for word in unwanted_keywords):
            print("Skipping unwanted article")
            continue

        # Skip articles from bad domains
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

        if len(full_text.strip()) < 120:
            print("Description too short. Skipping article.")
            continue

        print("Using NewsAPI description as fallback.")

        return f"""
Title: {title}

Summary: {article.get('description', '')}

Source: {source}

Source URL: {url}

Date: {article.get('publishedAt', '')}

Article Text:
{full_text}

Image Prompt:
Futuristic enterprise workforce with AI employees, digital workers, human AI collaboration, autonomous workflows and enterprise productivity dashboards.
"""

    print("No suitable article found")

    return None