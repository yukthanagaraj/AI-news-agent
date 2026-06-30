import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from newspaper import Article

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# ============================================================================
# CONSTANTS
# ============================================================================

ENTERPRISE_AI_QUERY = (
    '"Agentic AI" OR '
    '"AI Agents" OR '
    '"Enterprise AI" OR '
    '"Enterprise Software" OR '
    '"Enterprise Automation" OR '
    '"Autonomous Operations" OR '
    '"Digital Workers" OR '
    '"Future of Work" OR '
    '"Human-AI Collaboration" OR '
    '"AI Coding Agents" OR '
    '"Developer Productivity" OR '
    '"Business Transformation" OR '
    '"Operational Intelligence" OR '
    '"Enterprise Productivity"'
)

TRUSTED_NEWS_SOURCES = [
    "Reuters",
    "TechCrunch",
    "VentureBeat",
    "MIT Technology Review",
    "The Verge",
    "Wired",
    "Forbes",
    "Fast Company",
    "Business Insider",
    "ZDNET",
    "InfoWorld",
    "Computerworld",
    "The Register",
    "CIO",
    "TechRadar",
    "SiliconANGLE",
    "The Decoder",
    "AI Business",
    "Unite.AI",
    "Microsoft",
    "Google Cloud",
    "IBM",
    "AWS",
    "Fortune",
    "The Times of India",
    "InfoQ",
    "Computer Weekly",
    "ZDNet",
    "CIO Dive",
    "Silicon Republic",
    "The New Stack",
    "VentureBeat AI",
    "SiliconANGLE AI",
    "Mozilla",
    "ComputerWeekly",
    "TechRepublic",
    "RedMonk",
    "DevOps.com",
    "SD Times"
]

PREMIUM_SOURCES = {
    "Reuters",
    "TechCrunch",
    "VentureBeat",
    "MIT Technology Review",
    "Business Insider",
    "Forbes",
    "Wired",
    "The Verge",
    "Fast Company",
    "InfoQ",
    "ComputerWeekly",
    "TechRepublic",
}

SECONDARY_SOURCES = {
    "Slashdot",
    "The New Stack",
    "DevOps.com",
    "SD Times",
    "RedMonk",
}

BAD_DOMAINS = [
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

PACKAGE_PATTERNS = [
    "added to pypi",
    ".dev",
    "rc",
    "alpha",
    "beta",
    "release candidate",
    "v0.",
    "v1.0",
    "version",
    "0.1.0",
    "1.2.3"
]

HIGH_PRIORITY_KEYWORDS = [
    "agentic ai",
    "ai agent",
    "ai agents",
    "enterprise ai",
    "enterprise automation",
    "ai employees",
    "digital workers",
    "autonomous enterprise",
    "autonomous operations",
    "multi-agent systems",
    "ai orchestration",
    "human ai collaboration",
    "enterprise productivity",
    "future of work",
    "ai coding agents",
    "developer productivity",
    "enterprise development",
    "software engineering",
    "software development",
    "developer workflow",
    "intelligent automation",
    "ai security",
    "enterprise platform",
    "enterprise transformation"
]

MEDIUM_PRIORITY_KEYWORDS = [
    "workflow",
    "workflow automation",
    "automation",
    "enterprise software",
    "enterprise platform",
    "knowledge worker",
    "reasoning model",
    "reasoning",
    "decision making",
    "business process",
    "copilot",
    "enterprise copilot",
    "digital transformation",
    "productivity",
    "ai assistant",
    "autonomous workflow",
    "orchestration",
    "business automation",
    "enterprise workflow",
    "workforce",
    "developer",
    "coding assistant",
    "software teams",
    "engineering productivity",
    "application modernization",
    "enterprise applications",
    "workflow intelligence",
    "business operations",
    "software lifecycle"
]

LOW_PRIORITY_KEYWORDS = [
    "llm",
    "language model",
    "generative ai",
    "machine learning"
]

UNWANTED_KEYWORDS = [
    # Consumer Tech
    "iphone",
    "android",
    "camera",
    "smartphone",
    # Hardware
    "gpu",
    "graphics card",
    "chip",
    "processor",
    # Gaming
    "gaming",
    "playstation",
    "xbox",
    # Crypto
    "bitcoin",
    "ethereum",
    "token",
    # Politics
    "election",
    "campaign",
    # Reviews
    "benchmark",
    "hands-on",
    "review",
    # Academic
    "arxiv",
    "paper",
    "research paper"
]

TOPIC_CLASSIFICATION = {
    "Agentic AI": [
        "agentic ai",
        "multi-agent",
        "reasoning"
    ],
    "AI Agents": [
        "ai agent",
        "ai agents",
        "autonomous agent"
    ],
    "Enterprise AI": [
        "enterprise ai",
        "enterprise automation",
        "business process"
    ],
    "AI Employees": [
        "ai employee",
        "digital worker"
    ],
    "Future of Work": [
        "future of work",
        "knowledge worker",
        "workforce"
    ],
    "Human-AI Collaboration": [
        "human ai collaboration",
        "copilot"
    ],
    "Developer Productivity": [
        "developer productivity",
        "ai coding agents",
        "software engineering"
    ],
    "Enterprise Transformation": [
        "enterprise transformation",
        "digital transformation",
        "business operations"
    ]
}

# ============================================================================
# FUNCTIONS
# ============================================================================

def classify_topic(text: str):
    """
    Classify text into predefined topics based on keywords.
    
    Args:
        text (str): Input text to classify
        
    Returns:
        str: Topic with highest keyword match score
    """
    text = text.lower()
    scores = {}

    for topic, keywords in TOPIC_CLASSIFICATION.items():
        score = 0
        for keyword in keywords:
            if keyword in text:
                score += 1
        scores[topic] = score

    best_topic = max(scores, key=scores.get)

    if scores[best_topic] == 0:
        return "Enterprise AI"

    return best_topic


def normalize_title(title: str) -> str:
    """
    Normalize title for better duplicate detection.
    
    Removes punctuation and extra spaces for comparison.
    
    Args:
        title (str): Title to normalize
        
    Returns:
        str: Normalized title
    """
    normalized = (
    title.lower()
    .replace(":", "")
    .replace("-", " ")
    .replace("'", "")
    .replace('"', "")
    .replace(",", "")
    .replace("(", "")
    .replace(")", "")
    .replace(".", "")
    .replace("!", "")
    .replace("?", "")
    .strip()
)
    # Remove extra whitespace
    normalized = " ".join(normalized.split())
    return normalized


def is_package_release(title: str, url: str) -> bool:
    """
    Detect if article is about a package/library release.
    
    Args:
        title (str): Article title
        url (str): Article URL
        
    Returns:
        bool: True if this is a package release announcement
    """
    content_to_check = f"{title} {url}".lower()
    return any(pattern in content_to_check for pattern in PACKAGE_PATTERNS)


def fetch_ai_news(
    previous_titles=None,
    previous_sources=None,
    previous_urls=None
):
    """
    Fetch and filter AI news articles from NewsAPI.
    
    Implements multiple filtering layers:
    - Keyword-based relevance filtering with confidence scoring
    - Tiered trusted news source bonuses (Premium vs Secondary)
    - Freshness bonus for recent articles
    - Short title penalty
    - Duplicate detection with normalization
    - Bad domain blocking
    - Package release detection
    - Article extraction with fallback
    - Minimum content length validation
    
    Args:
        previous_titles (list, optional): List of previously used article titles
        previous_sources (list, optional): List of previously used article sources
        previous_urls (list, optional): List of previously used article URLs
    
    Returns:
        str: Formatted article with metadata and context, or None if no suitable article found
    """
    articles = []

    # Try multiple time windows to find fresh articles
    for hours in [24, 48, 72]:
        cutoff = (
            datetime.utcnow() - timedelta(hours=hours)
        ).strftime("%Y-%m-%dT%H:%M:%SZ")

        print(f"Trying {hours}-hour news window")

        try:
            response = requests.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q": ENTERPRISE_AI_QUERY.strip(),
                    "from": cutoff,
                    "sortBy": "publishedAt",
                    "language": "en",
                    "pageSize": 100,
                    "apiKey": NEWS_API_KEY,
                },
                timeout=20,
            )

        except requests.exceptions.RequestException as e:
            print(f"NewsAPI request failed: {e}")
            continue

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

    # Process and filter articles
    for article in articles:
        title = article.get("title", "")
        source = article.get("source", {}).get("name", "")
        url = article.get("url", "")
        description = article.get("description") or ""
        published = article.get("publishedAt", "")

        # FILTER 1: Skip press releases
        if "business wire" in source.lower():
            print("Skipping press release")
            continue

        if "press release" in title.lower():
            print("Skipping press release")
            continue

        # FILTER 2: Skip package releases with improved detection
        if is_package_release(title, url):
            print("Skipping package release")
            continue

        content_to_check = f"{title} {description}".lower()

        # FILTER 3: Check for required keywords with improved scoring
        high_matches = sum(
            keyword in content_to_check
            for keyword in HIGH_PRIORITY_KEYWORDS
        )

        medium_matches = sum(
            keyword in content_to_check
            for keyword in MEDIUM_PRIORITY_KEYWORDS
        )

        low_matches = sum(
            keyword in content_to_check
            for keyword in LOW_PRIORITY_KEYWORDS
        )

        # FILTER 4: Apply tiered source bonus (Premium vs Secondary)
        source_bonus = 0

        if any(s.lower() in source.lower() for s in PREMIUM_SOURCES):
            source_bonus = 3

        elif any(s.lower() in source.lower() for s in SECONDARY_SOURCES):
            source_bonus = 1
        
        base_score = (
            high_matches * 4
            + medium_matches * 2
            + low_matches
        )
        
        total_score = base_score + source_bonus

        # Apply short title penalty
        if len(title.split()) < 5:
            total_score -= 2

        # Apply freshness bonus
        if published:
            try:
                age_hours = (
                    datetime.utcnow() -
                    datetime.fromisoformat(
                        published.replace("Z", "+00:00")
                    ).replace(tzinfo=None)
                ).total_seconds() / 3600

                if age_hours <= 12:
                    total_score += 2

                elif age_hours <= 24:
                    total_score += 1
            except Exception as e:
                print(f"Could not parse publish date: {e}")
        
        print(f"TITLE: {title}")
        print(f"Score: {total_score} (High: {high_matches}, Medium: {medium_matches}, Low: {low_matches}, Source Bonus: {source_bonus})")
        print("-" * 60)

        # IMPROVED SCORING THRESHOLD: Relaxed from 6 to 5
        if total_score < 5:
            print("Skipping low relevance article")
            continue

        # FILTER 5: Skip if URL already used
        if previous_urls and url in previous_urls:
            print("Skipping used URL")
            continue

        # FILTER 6: Skip if title already used - with improved normalization for duplicates
        if previous_titles:
            normalized_title = normalize_title(title)
            previous_normalized = [
                normalize_title(t)
                for t in previous_titles
            ]
            if normalized_title in previous_normalized:
                print("Skipping duplicate title")
                continue

        # FILTER 7: Skip articles with unwanted keywords
        if any(word in title.lower() for word in UNWANTED_KEYWORDS):
            print("Skipping unwanted article")
            continue

        # FILTER 8: Skip articles from bad domains
        if any(domain in url for domain in BAD_DOMAINS):
            print("Skipping bad source")
            continue

        print("TITLE =", title)
        print("SOURCE =", source)
        print("URL =", url)
        print("-" * 80)

        full_text = ""

        # EXTRACTION STEP 1: Try newspaper3k extraction
        try:
            article_obj = Article(url)
            article_obj.download()
            article_obj.parse()
            full_text = article_obj.text
            full_text = " ".join(full_text.split())
            full_text = full_text[:15000]
            print("ARTICLE EXTRACTED")
            print("Using extracted content for analysis.")

        # EXTRACTION STEP 2: Fallback to API content
        except Exception as e:
            print("ARTICLE EXTRACTION FAILED:", e)
            description = article.get("description") or ""
            content = article.get("content") or ""
            full_text = f"""
{description}

{content}
""".strip()
            print("Using NewsAPI fallback content.")

        # FILTER 9: Ensure minimum content length
        if len(full_text.strip()) < 120:
            print("Description too short. Skipping article.")
            continue

        # Classify article topic
        topic = classify_topic(
            f"{title} {description} {full_text[:2000]}"
        )

        # RETURN FORMATTED ARTICLE
        return f"""
Title: {title}

Topic: {topic}

Summary:
{article.get('description', '')}

Source:
{source}

Source URL:
{url}

Published Date:
{article.get('publishedAt', '')}

Article Text:
{full_text}

Business Context:

Treat the supplied article only as supporting evidence.

Explain:

• enterprise strategy

• operational redesign

• organizational capability

• competitive positioning

• executive decision making

• future operating models

Avoid summarizing the article.

Focus on why the enterprise landscape is changing.

Image Prompt:
Enterprise AI agents collaborating with human professionals, digital workers, intelligent automation, enterprise dashboards, modern business operations, futuristic corporate environment.
"""

    print("No suitable article found")
    return None