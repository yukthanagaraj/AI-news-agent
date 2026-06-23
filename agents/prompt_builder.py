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
- Use markdown headings.
- Professional tone.
- Avoid hype and clickbait.
- Focus on AI Agents, AI Employees, Enterprise AI and Future of Work.
- Make the article feel like an AI insights publication rather than a news blog.
- Image prompts should describe editorial illustrations.
- Avoid text inside images.

ARTICLE REQUIREMENTS

- Article length should be 1000–1500 words.
- Minimum article length should be 1000 words.
- Every major section should contain 3–4 paragraphs.
- Generate 6–8 meaningful sections.
- Use strategic analysis instead of news summarization.
- Explain enterprise impact and business implications.
- Include actionable insights for executives and organizations.

SEO REQUIREMENTS

- Use SEO keywords naturally throughout the article.
- Include AI Agents throughout the article.
- Include AI Employees throughout the article.
- Include Enterprise AI throughout the article.
- Include Digital Workers throughout the article.
- Include Human AI Collaboration throughout the article.
- Include Future of Work throughout the article.
- Include Autonomous Operations where relevant.
- Include Enterprise Productivity where relevant.
- Use keywords naturally and avoid keyword stuffing.

QUOTE REQUIREMENTS

* Generate exactly one memorable quote.
* Include exactly one markdown blockquote inside the Blog content.
* Use markdown > syntax.
* Place the quote immediately after the second introductory paragraph.
* The quote must appear before the first major section heading.
* The quote must appear only once in the entire article.
* Quote should be short, memorable, and editorial in tone.
* Quote should reinforce the article's central insight.
* Quote should be a single sentence.
* Quote should contain between 8 and 15 words.
* Quote should fit within 1–3 visual lines on desktop screens.
* Use a single markdown blockquote line.
* Do not create multiple blockquotes.
* Do not split the quote into multiple lines.
* Do not insert blank lines inside the quote.
* Do not break the quote into separate paragraphs.
* Do not use lists, headings, or formatting inside the quote.
* Do not place the quote after Key Takeaways.
* Do not place the quote near the Conclusion.
* Avoid generic statements.
* Prefer strategic observations related to AI Agents, AI Employees, Enterprise AI, Digital Workers, Human AI Collaboration, or Future of Work.

VALID EXAMPLE

> AI agents are becoming the execution layer of modern enterprises.

INVALID EXAMPLE

> AI agents are becoming the execution layer

>

> of modern enterprises.


"""