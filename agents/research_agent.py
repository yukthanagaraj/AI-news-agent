import os
import random
import re
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from difflib import SequenceMatcher
from newspaper import Article

from agents.history_manager import (
    get_used_topics,
    remember_topic,
    get_used_clusters,
    remember_cluster,
)

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

import requests as _requests_lib
from bs4 import BeautifulSoup




# ============================================================================
# CONSTANTS
# ============================================================================

TOPIC_CLUSTERS = {

    "AI Agents":
        (
            '"AI Agents" OR '
            '"Agentic AI" OR '
            '"Multi-Agent Systems" OR '
            '"Autonomous AI"'
        ),

    "Enterprise AI":
        (
            '"Enterprise AI" OR '
            '"Enterprise Automation" OR '
            '"Enterprise Software" OR '
            '"Business AI"'
        ),

    "AI Economics":
        (
            '"AI ROI" OR '
            '"Enterprise Productivity" OR '
            '"AI Investment" OR '
            '"Business Value of AI" OR '
            '"AI Adoption" OR '
            '"Enterprise Automation"'
        ),

    "AI Governance":
        (
            '"AI Governance" OR '
            '"Responsible AI" OR '
            '"AI Compliance" OR '
            '"AI Risk"'
        ),

    "Enterprise Infrastructure":
        (
            '"AI Infrastructure" OR '
            '"Enterprise AI Platform" OR '
            '"Retrieval Augmented Generation" OR '
            '"Model Context Protocol" OR '
            '"Enterprise Vector Database"'
        ),

    "Digital Workers":
        (
            '"Digital Workers" OR '
            '"AI Employees" OR '
            '"Autonomous Workforce"'
        ),

    "Future of Work":
        (
            '"Future of Work" OR '
            '"Knowledge Workers" OR '
            '"Human AI Collaboration"'
        ),

    "Enterprise Strategy":
        (
            '"Enterprise Strategy" OR '
            '"Enterprise Transformation" OR '
            '"Digital Transformation" OR '
            '"Business Strategy" OR '
            '"AI Strategy"'
        ),
}

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
    "SD Times",
    "SiliconANGLE News",
    "ComputerWeekly.com",
    "Microsoft.com",
    "Fortinet.com",
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

    "ZDNet",
    "Computer Weekly",
    "ComputerWeekly",
    "InfoQ",
    "TechRepublic",
    "CIO",
    "InfoWorld",
    "Computerworld",
    "The Register",
    "SiliconANGLE",
    "The Decoder",
    "Help Net Security",
    "The Next Web",
    "Search Engine Journal",
    "Fortinet",
    "Forrester",
    "BusinessLine",
    "The Economic Times",
    "Economic Times",
    "Mint",
    "Fortune",
    "Bloomberg",
    "CNBC",
}
  
SECONDARY_SOURCES = {

    "Slashdot",
    "The New Stack",
    "DevOps.com",
    "SD Times",
    "RedMonk",

    "TechRadar",
    "Silicon Republic",
    "CIO Dive",
    "AI Business",
    "Unite.AI",
    "Tech Times",
    "Stack Overflow Blog",
    "JetBrains",
    "CNX Software",

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
    "marketscreener.com",
    "itsfoss.com",
    "freerepublic.com",
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
    "enterprise transformation",
    "agentic",
    "autonomous",
    "enterprise operations",
    "enterprise workflow",
    "enterprise execution",
    "operational intelligence",
    "ai observability",
    "production ai",
    "ai governance",
    "enterprise security",
    "ai infrastructure",
    "intelligent operations",
    "enterprise software",
    "business operations",
    "shadow ai",
    "ai spend",
    "ai investment",
    "ai budget",
    "ai talent",
    "ai roi",
    "ai strategy",
]

MEDIUM_PRIORITY_KEYWORDS = [
    
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
    "software lifecycle",
    "operations",
"production",
"observability",
"governance",
"workflow",
"platform",
"infrastructure",
"enterprise",
"business",
"deployment",
"implementation",
"adoption",
"security",
"productivity",
]

LOW_PRIORITY_KEYWORDS = [
    "llm",
    "language model",
    "large language model",
    "foundation model",
    "reasoning model",
    "generative ai",
    "machine learning"
]

UNWANTED_KEYWORDS = [
    "iphone",
    "android",
    "camera",
    "smartphone",
    "gpu",
    "graphics card",
    "chip",
    "processor",
    "gaming",
    "playstation",
    "xbox",
    "bitcoin",
    "ethereum",
    "token",
    "election",
    "campaign",
    "benchmark",
    "hands-on",
    "review",
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

INDUSTRY_CLASSIFICATION = {
    "Healthcare": [
        "healthcare", "hospital", "clinical", "patient", "health system"
    ],
    "Finance": [
        "bank", "banking", "finance", "fintech", "insurance", "payments"
    ],
    "Retail": [
        "retail", "e-commerce", "ecommerce", "consumer goods", "merchandising"
    ],
    "Manufacturing": [
        "manufacturing", "factory", "supply chain", "industrial", "plant"
    ],
    "Cloud": [
        "cloud", "aws", "azure", "google cloud", "saas", "hyperscaler"
    ],
    "Security": [
        "cybersecurity", "security breach", "threat detection", "soc", "cyberattack"
    ],
    "Software": [
        "software company", "developer tools", "engineering team", "devops", "saas platform"
    ],
    "Government": [
        "government", "public sector", "federal agency", "regulator", "policy maker"
    ],
    "Education": [
        "education", "university", "school district", "edtech", "higher education"
    ],
}

AUDIENCE_CLASSIFICATION = {
    "CISO": [
        "security", "governance", "risk", "compliance", "breach", "threat"
    ],
    "CTO": [
        "architecture", "infrastructure", "technical stack", "engineering platform", "system design"
    ],
    "CIO": [
        "it operations", "enterprise software", "digital transformation", "technology strategy", "legacy systems"
    ],
    "COO": [
        "operations", "workforce", "productivity", "process", "supply chain", "execution"
    ],
    "CEO": [
        "strategy", "market", "competitive", "investment", "business model", "growth"
    ],
}

TOPIC_DIVERSITY_LOOKBACK = 5
CLUSTER_DIVERSITY_LOOKBACK = 5

RELEVANCE_THRESHOLD = 3

# ============================================================================
# HELPERS
# ============================================================================

BARE_AI_RE = re.compile(r"\bai\b", re.IGNORECASE)


def _has_bare_ai_mention(text: str) -> bool:
    return bool(BARE_AI_RE.search(text))


def normalize_url(url: str) -> str:
    return url.split("?")[0].rstrip("/").lower()


def classify_topic(text: str):
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


def classify_industry(text: str):
    text = text.lower()
    scores = {}

    for industry, keywords in INDUSTRY_CLASSIFICATION.items():
        score = sum(keyword in text for keyword in keywords)
        scores[industry] = score

    best_industry = max(scores, key=scores.get)

    if scores[best_industry] == 0:
        return "Cross-Industry"

    return best_industry


def classify_audience(text: str):
    text = text.lower()
    scores = {}

    for audience, keywords in AUDIENCE_CLASSIFICATION.items():
        score = sum(keyword in text for keyword in keywords)
        scores[audience] = score

    best_audience = max(scores, key=scores.get)

    if scores[best_audience] == 0:
        return "CIO"

    return best_audience


def topic_penalty(topic: str, recent_topics) -> int:
    if topic in recent_topics:
        return 4
    return 0


def select_topic_cluster(exclude=None):
    exclude = set(exclude or [])

    recent_clusters = get_used_clusters(limit=CLUSTER_DIVERSITY_LOOKBACK)

    excluded = set(recent_clusters) | exclude

    available = [
        name for name in TOPIC_CLUSTERS
        if name not in excluded
    ]

    if not available:
        available = [
            name for name in TOPIC_CLUSTERS
            if name not in exclude
        ]

    if not available:
        available = list(TOPIC_CLUSTERS.keys())

    chosen = random.choice(available)

    return chosen, TOPIC_CLUSTERS[chosen]


def _fetch_via_requests_fallback(url, timeout=15):
    """
    Second-chance extraction when newspaper3k's download() is blocked
    (403/anti-bot). Uses a browser-like User-Agent, which newspaper3k
    does not set by default and which is why sites like SiliconANGLE
    return 403 to it specifically. Falls back to paragraph-tag text
    extraction via BeautifulSoup -- cruder than newspaper3k's article
    parser, but still far more real content than NewsAPI's truncated
    description/content snippet.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }
    try:
        resp = _requests_lib.get(url, headers=headers, timeout=timeout)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, "html.parser")
        paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
        text = " ".join(p for p in paragraphs if len(p.split()) > 4)
        text = " ".join(text.split())
        return text if len(text) > 200 else None
    except Exception:
        return None

def normalize_title(title: str) -> str:
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
    normalized = " ".join(normalized.split())
    return normalized


def is_package_release(title: str, url: str) -> bool:
    content_to_check = f"{title} {url}".lower()
    return any(pattern in content_to_check for pattern in PACKAGE_PATTERNS)


def _title_similarity(a, b):
    """
    Ratio-based title similarity used to identify when two different
    outlets are covering the same underlying story.
    """
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_related_coverage(primary_title, primary_url, primary_source, published, max_results=4):
    """
    Finds OTHER trusted outlets covering the same story as the selected
    article, so the blog page can list multiple sources line by line
    instead of one 'View Original Source' link. NewsAPI has no story
    clustering, so this approximates it via title-similarity matching
    within a tight time window around the original publish date.
    """
    all_trusted_lower = {s.lower() for s in (PREMIUM_SOURCES | SECONDARY_SOURCES)}

    related = [{
        "source": primary_source,
        "url": primary_url,
        "primary": True,
    }]

    keywords = " ".join(re.findall(r"[A-Za-z]{4,}", primary_title)[:8])
    if not keywords.strip():
        return related

    params = {
        "q": keywords,
        "sortBy": "relevancy",
        "language": "en",
        "pageSize": 20,
        "excludeDomains": ",".join(BAD_DOMAINS),
        "apiKey": NEWS_API_KEY,
    }

    if published:
        try:
            pub_dt = datetime.fromisoformat(published.replace("Z", "+00:00")).replace(tzinfo=None)
            params["from"] = (pub_dt - timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
            params["to"] = (pub_dt + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            pass

    try:
        response = requests.get("https://newsapi.org/v2/everything", params=params, timeout=20)
        if response.status_code != 200:
            return related
        articles = response.json().get("articles", [])
    except requests.exceptions.RequestException:
        return related

    seen_urls = {normalize_url(primary_url)}
    candidates = []

    for a in articles:
        a_title = a.get("title", "")
        a_source = a.get("source", {}).get("name", "")
        a_url = a.get("url", "").strip()

        if not a_title or not a_url:
            continue
        if normalize_url(a_url) in seen_urls:
            continue
        if not any(trusted in a_source.lower() for trusted in all_trusted_lower):
            continue
        if any(domain in a_url for domain in BAD_DOMAINS):
            continue

        similarity = _title_similarity(a_title, primary_title)
        if similarity < 0.45:
            continue

        seen_urls.add(normalize_url(a_url))
        candidates.append({"source": a_source, "url": a_url, "primary": False, "_score": similarity})

    candidates.sort(key=lambda c: c["_score"], reverse=True)

    for c in candidates[:max_results]:
        c.pop("_score", None)
        related.append(c)

    return related


# ============================================================================
# MAIN FETCH FUNCTION
# ============================================================================

def fetch_ai_news(
    previous_titles=None,
    previous_sources=None,
    previous_urls=None
):
    """
    Fetch and filter AI news articles from NewsAPI.

    Returns a tuple: (research_package: str | None, related_sources: list)
    related_sources is always a list (empty if none found or on early exit).
    """
    all_trusted_sources = PREMIUM_SOURCES | SECONDARY_SOURCES
    trusted_sources = {s.lower() for s in all_trusted_sources}

    recent_topics = get_used_topics()[-TOPIC_DIVERSITY_LOOKBACK:]

    candidates = []
    soft_pool = []
    cluster_name = None
    tried_clusters_this_run = set()

    for cluster_attempt in range(3):

        cluster_name, cluster_query = select_topic_cluster(
            exclude=tried_clusters_this_run
        )
        tried_clusters_this_run.add(cluster_name)

        print(f"\nTrying Topic Cluster {cluster_attempt + 1}/3")
        print(f"Using topic cluster: {cluster_name}")
        print(f"Using query: {cluster_query}")

        articles = []

        for hours in [24, 48, 72, 168, 336]:

            cutoff = (
                datetime.utcnow() - timedelta(hours=hours)
            ).strftime("%Y-%m-%dT%H:%M:%SZ")

            print(f"Trying {hours}-hour news window")

            try:
                response = requests.get(
                    "https://newsapi.org/v2/everything",
                    params={
                        "q": cluster_query.strip(),
                        "from": cutoff,
                        "sortBy": "publishedAt",
                        "language": "en",
                        "pageSize": 100,
                        "excludeDomains": ",".join(BAD_DOMAINS),
                        "apiKey": NEWS_API_KEY,
                    },
                    timeout=20,
                )
            except requests.exceptions.RequestException as e:
                print(f"NewsAPI request failed: {e}")
                continue

            if response.status_code != 200:
                print("NEWS API ERROR")
                continue

            data = response.json()
            articles = data.get("articles", [])
            print(f"Found {len(articles)} articles")

            if len(articles) >= 5:
                break

        if not articles:
            print("Not enough raw articles. Trying another cluster...")
            continue

        cluster_candidates = []

        for article in articles:
            title = article.get("title", "")
            source = article.get("source", {}).get("name", "")
            url = article.get("url", "").strip()
            description = article.get("description") or ""
            published = article.get("publishedAt", "")

            if not any(trusted in source.lower() for trusted in trusted_sources):
                print(f"Skipping untrusted source: {source}")
                continue

            if "business wire" in source.lower():
                print("Skipping press release")
                continue

            if "press release" in title.lower():
                print("Skipping press release")
                continue

            if is_package_release(title, url):
                print("Skipping package release")
                continue

            if previous_urls:
                normalized_previous_urls = {normalize_url(u) for u in previous_urls}
                if normalize_url(url) in normalized_previous_urls:
                    print("Skipping used URL")
                    continue

            if previous_titles:
                normalized_title = normalize_title(title)
                previous_normalized = [normalize_title(t) for t in previous_titles]
                if normalized_title in previous_normalized:
                    print("Skipping duplicate title")
                    continue

            if any(word in title.lower() for word in UNWANTED_KEYWORDS):
                print("Skipping unwanted article")
                continue

            if any(domain in url for domain in BAD_DOMAINS):
                print("Skipping bad source")
                continue

            content_to_check = f"{title} {description}".lower()

            high_matches = sum(k in content_to_check for k in HIGH_PRIORITY_KEYWORDS)
            medium_matches = sum(k in content_to_check for k in MEDIUM_PRIORITY_KEYWORDS)
            low_matches = sum(k in content_to_check for k in LOW_PRIORITY_KEYWORDS)

            source_bonus = 0
            if any(s.lower() in source.lower() for s in PREMIUM_SOURCES):
                source_bonus = 3
            elif any(s.lower() in source.lower() for s in SECONDARY_SOURCES):
                source_bonus = 1

            base_score = high_matches * 5 + medium_matches * 2 + low_matches

            title_lower = title.lower()
            if any(k in title_lower for k in HIGH_PRIORITY_KEYWORDS):
                base_score += 3
            elif any(k in title_lower for k in MEDIUM_PRIORITY_KEYWORDS):
                base_score += 2

            description_lower = description.lower()
            if any(k in description_lower for k in HIGH_PRIORITY_KEYWORDS):
                base_score += 2
            elif any(k in description_lower for k in MEDIUM_PRIORITY_KEYWORDS):
                base_score += 1

            used_fallback_signal = False
            if base_score == 0 and source_bonus > 0 and _has_bare_ai_mention(content_to_check):
                base_score += 4
                used_fallback_signal = True

            topic = classify_topic(f"{title} {description}")

            pre_penalty_score = base_score + source_bonus

            if len(title.split()) < 5:
                pre_penalty_score -= 2

            if published:
                try:
                    age_hours = (
                        datetime.utcnow() -
                        datetime.fromisoformat(published.replace("Z", "+00:00")).replace(tzinfo=None)
                    ).total_seconds() / 3600
                    if age_hours <= 6:
                        pre_penalty_score += 3
                    elif age_hours <= 12:
                        pre_penalty_score += 2
                    elif age_hours <= 24:
                        pre_penalty_score += 1
                except Exception as e:
                    print(f"Could not parse publish date: {e}")

            penalty = topic_penalty(topic, recent_topics)
            total_score = pre_penalty_score - penalty if penalty else pre_penalty_score

            if penalty:
                print(f"Topic '{topic}' used recently. Applying diversity penalty (-{penalty}).")

            print(f"TITLE: {title}")
            print(
                f"Score: {total_score} (pre-penalty: {pre_penalty_score}, "
                f"High: {high_matches}, Medium: {medium_matches}, Low: {low_matches}, "
                f"Source Bonus: {source_bonus}, Topic: {topic}"
                + (", fallback AI signal used" if used_fallback_signal else "")
                + ")"
            )
            print("-" * 60)

            record = {
                "score": total_score,
                "pre_penalty_score": pre_penalty_score,
                "title": title,
                "source": source,
                "url": url,
                "description": description,
                "published": published,
                "article": article,
            }

            if pre_penalty_score >= RELEVANCE_THRESHOLD:
                soft_pool.append(record)

            if total_score < RELEVANCE_THRESHOLD:
                print("Skipping low relevance article (hard threshold)")
                continue

            print("TITLE =", title)
            print("SOURCE =", source)
            print("URL =", url)
            print("-" * 80)

            cluster_candidates.append(record)

        print(f"\nCluster '{cluster_name}' qualified candidates: {len(cluster_candidates)}")

        if cluster_candidates:
            candidates = cluster_candidates
            print(f"Using cluster: {cluster_name}")
            break

        print("This cluster produced 0 qualified candidates. Trying another cluster...")

    if not candidates:
        if soft_pool:
            print(
                f"\nNo cluster produced a hard-qualified candidate, but "
                f"{len(soft_pool)} article(s) cleared relevance without "
                f"the topic-diversity penalty. Using relaxed threshold "
                f"as a fallback so the pipeline doesn't stall on a slow "
                f"news day."
            )
            candidates = sorted(soft_pool, key=lambda x: x["pre_penalty_score"], reverse=True)
        else:
            print("No suitable article found after trying all clusters")
            return None, []

    candidates.sort(key=lambda x: x["score"], reverse=True)
    top_candidates = candidates[:10]

    print("\nTop Candidates:")
    for candidate in top_candidates:
        print(f"{candidate['score']} - {candidate['title']}")
    print()

    remaining = top_candidates.copy()
    selected = None
    full_text = None
    title = source = url = description = published = article = None

    while remaining:
        min_score = min(c["score"] for c in remaining)
        shift = abs(min_score) + 1 if min_score <= 0 else 0
        weights = [(c["score"] + shift) ** 2 for c in remaining]

        choice = random.choices(remaining, weights=weights, k=1)[0]
        remaining.remove(choice)

        title = choice["title"]
        source = choice["source"]
        url = choice["url"]
        description = choice["description"]
        published = choice["published"]
        article = choice["article"]

        print(f"Selected candidate (Score {choice['score']})")
        print("TITLE =", title)
        print("SOURCE =", source)
        print("URL =", url)
        print("-" * 80)

        try:
            article_obj = Article(url)
            article_obj.download()
            article_obj.parse()
            full_text = " ".join(article_obj.text.split())
            full_text = full_text[:4000]
            print("ARTICLE EXTRACTED")
            print(f"Extracted {len(full_text)} characters for analysis.")
        except Exception as e:
            print("ARTICLE EXTRACTION FAILED (newspaper3k):", e)
            print("Trying fallback scraper with browser headers...")

            fallback_text = _fetch_via_requests_fallback(url)

            if fallback_text:
                full_text = fallback_text[:4000]
                print("FALLBACK SCRAPE SUCCEEDED")
                print(f"Extracted {len(full_text)} characters for analysis.")
            else:
                print("FALLBACK SCRAPE ALSO FAILED. Using NewsAPI snippet as last resort.")
                fallback_description = article.get("description") or ""
                fallback_content = article.get("content") or ""
                full_text = f"{fallback_description}\n\n{fallback_content}".strip()
                print(f"NewsAPI snippet length: {len(full_text)} characters (likely thin).")

        if len(full_text.strip()) < 120:
            print("Article too short, trying next candidate.")
            continue

        selected = choice
        break

    if not selected:
        print("No suitable article found after trying all candidates.")
        return None, []

    topic = classify_topic(f"{title} {description}")
    industry = classify_industry(f"{title} {description}")
    audience = classify_audience(f"{title} {description}")

    remember_topic(topic)
    remember_cluster(cluster_name)

    related_sources = find_related_coverage(
        primary_title=title,
        primary_url=url,
        primary_source=source,
        published=published,
    )
    source_material_is_thin = len(full_text.strip()) < 800

    research_package = f"""

# RESEARCH PACKAGE

## HEADLINE
{title}

## TOPIC
{topic}

## INDUSTRY
{industry}

## PRIMARY AUDIENCE
{audience}

## SOURCE
{source}

## PUBLISHED
{published}

## URL
{url}

## EXECUTIVE SUMMARY

{description}

## ARTICLE SUMMARY

{full_text[:3800]}

## ARTICLE SUMMARY

{full_text[:3800]}

{"## SOURCE MATERIAL NOTICE\n\nThe extracted source content for this article is limited (full-text extraction was blocked by the source site). Do not manufacture named companies, statistics, or specific details beyond what is stated above. Where the article calls for a named example and none exists in this research package, use a generic sector descriptor rather than inventing specificity." if source_material_is_thin else ""}

--------------------------------------------------

# RESEARCH TASK

You are a Senior Enterprise AI Research Analyst.

Do NOT summarize the article.

Extract structured research that helps an executive writer produce an original editorial.



==================================================
EXECUTIVE RESEARCH
==================================================

Return ONLY the following sections.

## Companies
List companies explicitly mentioned.

## Technologies
List AI technologies, platforms, standards, or architectures mentioned.

## Industry
Identify the primary industry.

## Strategic Theme
Choose ONE:

- Infrastructure
- Governance
- Security
- AI Economics
- Enterprise Productivity
- Digital Workers
- AI Agents
- Customer Experience
- Software Engineering
- Enterprise Strategy

## Enterprise Maturity

Choose ONE:

- Early Adoption
- Growth
- Mainstream
- Mature

## Primary Executive Audience

Choose ONE:

- CEO
- CIO
- CTO
- COO
- CISO
- Chief Data Officer

## Enterprise Use Cases

List practical enterprise use cases supported by the article.

## Implementation Challenges

List implementation obstacles explicitly supported by the article.

## Enterprise Risks

List operational, governance, security, compliance, or organizational risks.

## Competitive Landscape

List major competitors and explain their strategic position.

## Business Opportunities

Identify opportunities created for enterprises.

## Counterarguments

Explain one realistic limitation or opposing viewpoint.

## Enterprise Evidence

Extract, in this priority order:

1. Any NAMED company, organization, or named individual explicitly
   mentioned in the source article (even a passing mention) — quote
   the name exactly as it appears. This is the single most valuable
   extraction for the writer; do not summarize it into a generic
   category if a real name is available.
2. Named products, platforms, or initiatives mentioned.
3. Only if no named entities exist in the source material, extract
   generic implementation/governance examples described in the
   article (industry type, company size, sector — without inventing
   a name).

Do not invent examples or names not present in the source article.
If the source contains real names, the writer should be told to use
them; if it doesn't, say so explicitly rather than leaving this
section vague.

## Executive Insights

Generate EXACTLY five strategic observations.

Each should explain a different business implication.

## Executive Questions

Generate EXACTLY five questions that a CEO, CIO, CTO, or COO would ask after reading this news.

## Key Facts

Extract the five most important factual statements.

Do not infer.

## SEO Keywords

Generate:

- 5 Primary Keywords

- 5 Long-tail Keywords

- 10 Semantic Keywords

The article's PRIMARY AUDIENCE is {audience}. Tailor strategic
recommendations and business consequences to what a {audience} specifically
cares about and is accountable for, rather than generic "leaders."

The article's INDUSTRY context is {industry}. Where the industry is not
"Cross-Industry," ground at least one example or implication in that
specific vertical rather than defaulting to generic enterprise language.

Do not summarize the news.

Use the news as evidence for strategic analysis.
"""

    return research_package, related_sources