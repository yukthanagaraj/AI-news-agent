from datetime import datetime

from agents.research_agent import fetch_ai_news
from agents.writer_agent import generate_blog
from agents.image_agent import generate_image
from agents.seo_agent import generate_seo
from agents.aeo_agent import generate_aeo
from agents.quality_agent import quality_check
from agents.sheets_agent import save_blog, get_sheet
from agents.rss_generator import generate_rss
from agents.sitemap_generator import generate_sitemap
from agents.history_manager import remember_title


def get_previous_titles():

    try:

        s = get_sheet()

        records = s.col_values(2)

        titles = [
            t for t in records[1:]
            if t.strip()
        ] if len(records) > 1 else []

        return titles[-20:]

    except Exception as e:

        print(
            f"Warning: Could not fetch previous titles: {e}"
        )

        return []


def get_previous_urls():

    try:

        s = get_sheet()

        records = s.col_values(5)

        urls = [
            u for u in records[1:]
            if u.strip()
        ] if len(records) > 1 else []

        return urls[-50:]

    except Exception as e:

        print(
            f"Warning: Could not fetch previous urls: {e}"
        )

        return []


def get_previous_sources():
    return []


def parse_research_source_url(news_text):

    for line in news_text.split("\n"):

        line = line.strip()

        if line.startswith("Source URL:"):

            return line.replace(
                "Source URL:",
                ""
            ).strip()

    return ""


def run_pipeline():

    print("Fetching Previous Titles...")

    previous_titles = get_previous_titles()
    previous_sources = get_previous_sources()
    previous_urls = get_previous_urls()

    print(
        f"Found {len(previous_titles)} previous titles"
    )

    print("Fetching News...")

    news = fetch_ai_news(
        previous_titles,
        previous_sources,
        previous_urls
    )

    if not news:

        print("No suitable news article found")

        return

    research_source_url = parse_research_source_url(
        news
    )

    blog = generate_blog(
        news,
        previous_titles
    )

    if not blog:

        print(
            "ERROR: Writer Agent returned empty response"
        )

        return

    print("BLOG GENERATED")

    title = ""
    image_prompt = ""
    source_url = ""

    current_date = datetime.now().strftime(
        "%Y-%m-%d"
    )

    lines = blog.split("\n")

    capture_blog = False
    metadata_done = False

    blog_lines = []

    for line in lines:

        stripped = line.strip()

        if capture_blog and (
            stripped.startswith("Title:")
            or stripped.startswith("Source URL:")
            or stripped.startswith("Image Prompt:")
        ):
            break

        if capture_blog:

            blog_lines.append(
                stripped
            )

            continue

        elif stripped.startswith("Title:"):

            title = stripped.replace(
                "Title:",
                ""
            ).strip()

        elif stripped.startswith("Source URL:"):

            source_url = stripped.replace(
                "Source URL:",
                ""
            ).strip()

        elif stripped.startswith("Image Prompt:"):

            image_prompt = stripped.replace(
                "Image Prompt:",
                ""
            ).strip()

            metadata_done = True

        elif stripped.startswith("Blog:"):

            blog_inline = stripped.replace(
                "Blog:",
                ""
            ).strip()

            if blog_inline:

                blog_lines.append(
                    blog_inline
                )

            capture_blog = True

        elif metadata_done and stripped:

            capture_blog = True

            blog_lines.append(
                stripped
            )

    blog_content = "\n\n".join(
        [
            line
            for line in blog_lines
            if line.strip()
        ]
    ).strip()

    print()
    print("BLOG CONTENT")
    print("--------------------------------")
    print(blog_content)
    print("--------------------------------")
    print()

    print("Generating SEO...")

    seo_data = generate_seo(
        title,
        blog_content
    )

    print(seo_data)

    print("Generating AEO...")

    aeo_data = generate_aeo(
        title,
        blog_content
    )

    print(aeo_data)

    print("Running Quality Checks...")

    combined_content = (
        blog_content
        + "\n\n"
        + aeo_data
    )

    quality_data = quality_check(
        title,
        combined_content
    )

    if "Overall: FAIL" in quality_data:

     print(
        "WARNING: Quality issues detected."
    )

    print(
        "Continuing pipeline..."
    )



    if not source_url:

        source_url = research_source_url

    print("TITLE =", title)

    if title.lower() in [
        t.lower()
        for t in previous_titles
    ]:

        print(
            "Duplicate title detected:",
            title
        )

        title = f"{title} Strategy"

        print(
            "Using alternative title:",
            title
        )

    print(
        "IMAGE PROMPT =",
        image_prompt
    )

    print(
        "SOURCE URL =",
        source_url
    )

    print("Generating Image...")

    try:

        image_url = generate_image(
            image_prompt
        )

        print(
            "IMAGE URL =",
            image_url
        )

    except Exception as e:

        print(
            "Image Generation Failed:",
            e
        )

        image_url = (
            "https://images.unsplash.com/photo-1677442136019-21780ecad995"
        )

        print(
            "Using fallback image:",
            image_url
        )

    print("Saving Blog...")

    save_blog(
        current_date,
        title,
        blog_content,
        image_prompt,
        source_url,
        image_url
    )

    remember_title(
        title
    )

    print("Saved Successfully")

    print("Updating RSS feed...")

    generate_rss()

    print("Updating sitemap...")

    generate_sitemap()

    print("Pipeline Completed")

if __name__ == "__main__":
    run_pipeline()