from agents.research_agent import fetch_ai_news
from agents.writer_agent import generate_blog
from agents.sheets_agent import save_blog, get_sheet
from agents.image_agent import generate_image

from datetime import datetime


def get_previous_titles():
    try:
        s = get_sheet()

        records = s.col_values(3)

        titles = [
            t for t in records[1:]
            if t.strip()
        ] if len(records) > 1 else []

        return titles[-20:]

    except Exception as e:
        print(f"Warning: Could not fetch previous titles: {e}")
        return []


def get_previous_sources():
    try:
        s = get_sheet()

        records = s.col_values(6)

        sources = [
            src for src in records[1:]
            if src.strip()
        ] if len(records) > 1 else []

        return list(set(sources[-20:]))

    except Exception as e:
        print(f"Warning: Could not fetch previous sources: {e}")
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

    print("Fetching Previous Titles and Sources...")

    previous_titles = get_previous_titles()
    previous_sources = get_previous_sources()

    print(
        f"Found {len(previous_titles)} previous titles and "
        f"{len(previous_sources)} sources to exclude"
    )

    print("Fetching News...")

    news = fetch_ai_news(
        previous_titles,
        previous_sources
    )

    research_source_url = parse_research_source_url(news)

    print(
        "RESEARCH SOURCE URL =",
        research_source_url
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

    category = ""
    title = ""
    image_prompt = ""
    source_url = ""
    blog_content = ""

    current_date = datetime.now().strftime("%Y-%m-%d")

    lines = blog.split("\n")

    capture_blog = False
    metadata_done = False

    blog_lines = []

    for line in lines:

        stripped = line.strip()

        if capture_blog and (
            stripped.startswith("Category:")
            or stripped.startswith("Title:")
            or stripped.startswith("Source URL:")
            or stripped.startswith("Image Prompt:")
        ):
            break

        if capture_blog:
            blog_lines.append(stripped)
            continue

        if stripped.startswith("Category:"):

            category = stripped.replace(
                "Category:",
                ""
            ).strip()

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
                blog_lines.append(blog_inline)

            capture_blog = True

        elif metadata_done and stripped:

            capture_blog = True
            blog_lines.append(stripped)

    blog_content = "\n\n".join(
        [line for line in blog_lines if line.strip()]
    ).strip()

    if not source_url:
        source_url = research_source_url


    print("CATEGORY =", category)
    print("TITLE =", title)

    # Prevent duplicate titles
    if title.lower() in [t.lower() for t in previous_titles]:

        print("Duplicate title detected:", title)

        title = f"{title} Strategy"

        print("Using alternative title:", title)

    print("IMAGE PROMPT =", image_prompt)
    print("SOURCE URL =", source_url)

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
        category,
        title,
        blog_content,
        image_prompt,
        source_url,
        image_url
    )

    print("Saved Successfully")
    print("Pipeline Completed")




if __name__ == "__main__":
    run_pipeline()