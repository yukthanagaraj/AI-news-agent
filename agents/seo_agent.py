from agents.llm_client import client, MODEL_NAME
from agents.seo_parts.entity_rules import ENTITY_SEO_RULES
from agents.seo_parts.seo_rules import SEO_RULES
from agents.seo_parts.slug_rules import SLUG_RULES
from agents.seo_parts.summary_rules import SUMMARY_RULES
from agents.seo_parts.tags_rules import TAGS_RULES
from agents.seo_parts.related_topics_rules import RELATED_TOPICS_RULES
from agents.seo_parts.eeat_rules import EEAT_RULES
from agents.seo_parts.search_intent import SEARCH_INTENT_RULES


def generate_seo(
    title,
    article
):

    prompt = f"""
TITLE

{title}

ARTICLE

{article}

{SEO_RULES}

{SLUG_RULES}

{SUMMARY_RULES}

{TAGS_RULES}

{RELATED_TOPICS_RULES}

{ENTITY_SEO_RULES}

{EEAT_RULES}

{SEARCH_INTENT_RULES}

OBJECTIVE

Generate premium SEO and AEO metadata for an Enterprise AI publication.

Optimize for:

- Google Search
- Google AI Overviews
- ChatGPT Search
- Claude
- Gemini
- Perplexity

Focus on executive search intent.

Use semantic SEO.

Use natural language suitable for answer engines.

Avoid keyword stuffing.

Focus on:

- AI Agents
- Agentic AI
- Enterprise AI
- AI Employees
- Digital Workers
- Human-AI Collaboration
- Future of Work
- Enterprise Productivity
- Autonomous Operations

EXTRACTION METHOD

Ground every output field in what the article ACTUALLY discusses --
do not generate keywords, tags, or summary language that merely sound
adjacent to the topic. Before finalizing Secondary Keywords, Long-tail
Keywords, and Semantic Keywords, verify each one corresponds to a
concept the article substantively covers (appears in at least one
section's argument, not just a passing word choice). A keyword this
article doesn't actually address will rank for the wrong intent and
increase bounce rate -- precision matters more than volume here.

For Featured Snippet Opportunity and AI Overview Summary, draw from
the article's own H2 section-opening sentences (each section opens
with a direct-answer sentence by convention) rather than synthesizing
new framing from scratch. This keeps the metadata consistent with
what the article itself asserts.

TITLE FIELD DISCIPLINE

The article's H1 Title was already written to be specific and
concrete (a named technology, mechanism, or outcome -- not a generic
template). When generating "SEO Title" and "Meta Title":

- Preserve the H1's specific element (the named technology, company,
  or mechanism) -- do not smooth it back into generic phrasing to fit
  the character limit.
- Make SEO Title and Meta Title MEANINGFULLY DIFFERENT from each
  other, not near-duplicate rewordings. SEO Title should prioritize
  the primary keyword and search intent; Meta Title should prioritize
  what makes a reader click if seen in a social share or browser tab.
  If you cannot make them substantively different, that signals the
  underlying claim needs more specificity, not that duplication is
  acceptable.

OUTPUT ONLY

Slug:
<slug>

SEO Title:
<50–60 characters>

Meta Title:
<50–60 characters>

Meta Description:
<140–160 characters>

Primary Keyword:
<keyword>

Secondary Keywords:

- keyword
- keyword
- keyword
- keyword
- keyword

Long-tail Keywords:

- keyword
- keyword
- keyword
- keyword
- keyword

Semantic Keywords:

- keyword
- keyword
- keyword
- keyword
- keyword

People Also Ask:

- question
- question
- question

Related Searches:

- search
- search
- search

Search Intent:
<Informational / Commercial / Strategic>

Executive Search Queries:

- query
- query
- query

Tags:

- tag
- tag
- tag
- tag
- tag

Related Topics:

- topic
- topic
- topic
- topic
- topic

Internal Linking Suggestions:

- suggestion
- suggestion
- suggestion

Featured Snippet Opportunity:

<one concise paragraph answering the main executive question>

AI Overview Summary:

<2–3 sentence executive summary>

Canonical URL Suggestion:

/blog/<slug>

Open Graph Title:
<title>

Open Graph Description:
<description>

Twitter Title:
<title>

Twitter Description:
<description>
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": """
You are a senior Enterprise AI SEO and AEO strategist.

Generate premium metadata suitable for enterprise publications.

Optimize for:

- Google Search
- Google AI Overviews
- ChatGPT Search
- Claude
- Gemini
- Perplexity

Prioritize:

- semantic SEO
- executive search intent
- answer engine optimization
- featured snippets
- AI Overviews
- natural language retrieval
- experience, expertise, authoritativeness and trustworthiness (E-E-A-T)

Never stuff keywords.

Prefer semantic keyword variations.

Generate metadata that improves discoverability while remaining natural for executive readers.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    print("SEO GENERATED")

    return response.choices[0].message.content

