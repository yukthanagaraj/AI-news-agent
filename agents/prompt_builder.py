from agents.prompt_parts.title_rules import TITLE_RULES
from agents.prompt_parts.article_style import ARTICLE_STYLE
from agents.prompt_parts.article_structure import ARTICLE_STRUCTURE
from agents.prompt_parts.framework_rules import FRAMEWORK_RULES
from agents.prompt_parts.image_rules import IMAGE_RULES
from agents.prompt_parts.quote_rules import QUOTE_RULES
from agents.prompt_parts.section_titles import SECTION_TITLES

from agents.history_manager import (
    get_used_titles,
    get_used_quotes,
    get_used_frameworks,
    get_used_section_titles,
    get_used_visual_concepts
)


def build_prompt(news, previous_titles, template):

    used_titles = "\n".join(previous_titles or [])

    memory_titles = "\n".join(get_used_titles())
    memory_quotes = "\n".join(get_used_quotes())
    memory_frameworks = "\n".join(get_used_frameworks())
    memory_sections = "\n".join(get_used_section_titles())
    memory_visuals = "\n".join(get_used_visual_concepts())

    return f"""
You are a senior enterprise technology analyst writing for Luvana AI Journal.


NEWS INPUT

{news}


PREVIOUS TITLES

{used_titles}


LONG TERM MEMORY

USED TITLES

{memory_titles}


USED QUOTES

{memory_quotes}


USED FRAMEWORKS

{memory_frameworks}


USED SECTION TITLES

{memory_sections}


USED VISUAL CONCEPTS

{memory_visuals}


Never generate titles similar to those stored above.

Avoid repeating:

- titles
- quotes
- frameworks
- section names
- visual concepts

Create variety over time.


ARTICLE TEMPLATE

Use this template:

{template}

Every template should have a different flow.

Never make articles feel identical.


OBJECTIVE

Use the news as supporting evidence.

Do not simply summarize the news.

Explain:

- Why the development matters.
- How enterprises will be affected.
- What larger industry shift is occurring.
- How AI agents and AI employees are changing work.
- What executives and organizations should pay attention to.

Focus on strategic insights rather than reporting.


{TITLE_RULES}

{ARTICLE_STYLE}

{SECTION_TITLES}

{QUOTE_RULES}

{ARTICLE_STRUCTURE}

{FRAMEWORK_RULES}

{IMAGE_RULES}


IMPORTANT

Output ONLY in the following format:

Title: <title>

Quote: <quote>

Source URL: <source url>

Image Prompt: <detailed image prompt>

Blog:

<markdown article>


RULES

- No category labels.
- Do not generate image URLs.
- Generate only the image prompt.
- Title should be 4–6 words.
- Avoid colons in titles.
- Generate one memorable quote.
- Quote should be maximum two lines.
- Use markdown headings.
- Professional tone.
- Avoid hype and clickbait.
- Focus on AI Agents, AI Employees, Enterprise AI and Future of Work.
- Make the article feel like an AI insights publication rather than a news blog.
- Image prompts should describe editorial illustrations.
- Avoid text inside images.
RULES

- No category labels.
- Do not generate image URLs.
- Generate only the image prompt.
- Title should be 4–6 words.
- Avoid colons in titles.
- Generate one memorable quote.
- Quote should be maximum two lines.
- Use markdown headings.
- Professional tone.
- Avoid hype and clickbait.
- Focus on AI Agents, AI Employees, Enterprise AI and Future of Work.
- Make the article feel like an AI insights publication rather than a news blog.
- Image prompts should describe editorial illustrations.
- Avoid text inside images.
- Article length should be 1000–1500 words.
- Every section should contain 3–4 paragraphs.
- Use SEO keywords naturally throughout the article.
- Include AI Agents, AI Employees, Enterprise AI, Digital Workers, Human AI Collaboration, and Future of Work throughout the article.
- Include one markdown blockquote inside the Blog content.
- Use > syntax for the quote.
- Place the quote after the Introduction section.
- Quote may be one or two lines.
- Quote should reinforce the article's main insight.

"""