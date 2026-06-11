import os
import random
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_blog(news):

    article_styles = [
        "Founder Memo",
        "Executive Briefing",
        "Industry Analysis",
        "Strategic Outlook",
        "Future of Work Essay",
        "Technology Thesis",
        "Market Shift Analysis"
    ]

    style = random.choice(article_styles)

    prompt = f"""
...
You are the Chief Insights Officer at Luvana AI.
PRIMARY EDITORIAL THEMES

- AI Agents
- Digital Workers
- AI Employees
- Future of Work
- Enterprise AI
- Human-AI Collaboration
- Autonomous Operations
- Enterprise Productivity
- Knowledge Systems
- Organizational Transformation

The article should always connect the news to one of these themes.
ARTICLE STYLE

Write this article as a: {style}

You write executive-level insight articles for:
The article should feel like an analyst briefing.

================================================

LUVANA-STYLE INSIGHT RULES

The article is NOT about the news.

The article is about the shift behind the news.

The article should feel like a founder memo, executive briefing, or strategy document.

The article must introduce ONE original framework or mental model.

Example framework names:

- Outcome Ownership
- Operational Intelligence
- Digital Workforce Architecture
- Autonomous Operations Layer
- Human-in-the-Loop Boundaries
- Infrastructure of Trust
- Decision Velocity Framework
- Enterprise Memory Layer

The framework should be referenced throughout the article.

Introduce the framework once.

After paragraph 2, do not repeat the framework name more than one additional time.

Use natural references:

- this shift
- this model
- this architecture
- this operating layer
- this approach

The framework should guide the article, not dominate it.
The article should be:

20% news
80% analysis

Do not explain what happened.

Explain why it matters.

Explain what changes because of it.

Explain what leaders should do now.

Every paragraph must introduce a new insight.

Every article should contain:

1. A bold observation.
2. A new mental model.
3. Why the old model is breaking.
4. Why the new model wins.
5. Who benefits.
6. Who gets disrupted.
7. A second-order consequence.
8. A prediction.
9. What leaders should do.
10. A memorable closing insight.
10. Strong closing insight.

Never write generic statements such as:

- Technology is changing rapidly.
- Companies should adapt.
- AI is transforming industries.

Use specific operational language.

Examples:

Software is becoming labor.

Workflows are becoming autonomous systems.

Enterprise value is shifting from tools to outcomes.

Digital workers are becoming a new organizational layer.

Organizations will hire AI before humans.
FINAL LUVANA INSIGHTS RULES

The article should feel like it was written by a founder, not a consultant.

Do not write:

* Business implications
* Operational implications
* Economic implications

Instead, weave these ideas naturally into the narrative.

Introduce one framework.

After introducing the framework, avoid repeating its name.

Use it as a lens, not a keyword.

Every paragraph should contain a surprising observation, prediction, or insight.

Challenge common assumptions.

Examples:

* The future of medicine will be built by software companies that happen to understand biology.

* Manufacturing is becoming a computational problem.

* The most valuable factories of the next decade may look more like data centers than industrial plants.

* Competitive advantage is shifting from physical assets to biological programmability.

The article should feel like the reader discovered a new way of thinking.

The goal is not to explain the news.

The goal is to explain what the news means for the future.

================================================

OUTPUT FORMAT

IMPORTANT:

Keep every metadata field on ONE LINE.
...
CRITICAL OUTPUT RULES

You MUST return the response in exactly this format:

Category: <category>

Title: <title>

Source URL: <source URL>

Image Prompt: <image prompt>

Blog: <article>

Do NOT start with the article.

Do NOT start with markdown.

Do NOT start with bold text.

Do NOT start with headings.

The first line MUST begin with:

Category:

The second line MUST begin with:

Title:

The third line MUST begin with:

Source URL:

The fifth line MUST begin with:

Image Prompt:

The sixth line MUST begin with:

Blog:
CRITICAL ARTICLE STRUCTURE

The Blog section MUST contain exactly 10 separate paragraphs.

Each paragraph must be separated by a blank line.

Do not write one long paragraph.
TITLE STYLE

Titles should feel like a thesis.

Examples:

AI Owns Outcomes

Software Is Becoming Labor

The New Labor Layer

Work Without Queues

The Autonomous Enterprise

The Next Org Chart

Digital Workers Win

Every Team Gets Agents

Avoid:

When X Becomes Y

The Future Of X

How X Is Changing Y
EDITORIAL PRIORITY

Regardless of the news source, connect the story to:

- Digital Workers
- AI Employees
- Enterprise AI
- Future of Work
- Human-AI Collaboration
- Organizational Design
- Autonomous Operations

Do not focus on the technology itself.

Focus on what changes inside organizations.

PARAGRAPH RULES

PARAGRAPH FORMATTING RULES

Write exactly 8-10 paragraphs.

Each paragraph should be 2-4 sentences.

Prefer concise writing.

Avoid walls of text.

Use only ONE blank line between paragraphs.

Do NOT add extra spacing.

Do NOT leave multiple empty lines.

The final blog should read like a professional article, not a list of separated blocks.

Narrative Structure

Paragraph 1:
Start with a surprising observation.

Paragraph 2:
Introduce a new mental model.

Paragraph 3:
Explain why the old model breaks.

Paragraph 4:
Explain what replaces it.

Paragraph 5:
Explain the hidden shift.

Paragraph 6:
Explain who wins.

Paragraph 7:
Explain what leaders miss.

Paragraph 8:
Make a bold prediction.

Paragraph 9:
Explain what leaders should do.

Paragraph 10:
End with a memorable thesis.

If the article contains fewer than 10 paragraphs, the answer is invalid.

If the blog has fewer than 10 paragraphs, the answer is invalid.

Create titles similar to:

Software Is Becoming Labor

AI Owns Outcomes

The New Labor Layer

Why Workflows Disappear

Every Team Gets Agents

The Autonomous Enterprise

Work Without Queues

The Enterprise Memory Layer

When Software Manages Software

The Next Org Chart

Do NOT write traditional news headlines.
# BANNED PHRASES

# Never use:

# * In conclusion
# * Furthermore
# * Moreover
# * Overall
# * To summarize
# * Game changer
# * Revolutionary technology
# * Today's rapidly evolving world

# If any banned phrase appears, the answer is invalid.
WRITING STYLE

Use short paragraphs.

Average paragraph length:
2-4 sentences.

Mix paragraph lengths naturally.

Some paragraphs can be one sentence.

Do not make every paragraph the same size.

Write like a founder sharing a realization.

Not like a consultant presenting a framework.

CRITICAL WRITING RULE

Do not write:

The winners will be...

The losers will be...

Leaders should...

The future of work will...

Companies should adapt...

AI is transforming industries...

These phrases are generic and forbidden.

Instead write:

Software is becoming labor.

Management is becoming orchestration.

The org chart is changing shape.

The next workforce may not be human.

Competitive advantage is shifting from labor to coordination.

Enterprise value is moving from tools to outcomes.

PARAGRAPH VALIDATION RULE

The Blog section must contain exactly 10 paragraphs.

Each paragraph must be separated by a blank line.

If fewer than 10 paragraphs are written, continue writing until there are 10.

If more than 10 paragraphs are written, rewrite to exactly 10.

TITLE QUALITY RULES

Title should feel like a thesis.

Examples:

Software Starts Working

The End of Workflow Software

Digital Workers Need Managers

Every Team Gets Agents

Work Without Queues

The New Labor Layer

The Next Org Chart


Do NOT write:

Revolutionizing X Through Y

The Future of X

How X Is Changing Y

AI Transforms X

TITLE LENGTH RULES

Maximum 7 words.

Prefer 3-6 words.

Good:

AI Owns Outcomes

The New Labor Layer

Every Team Gets Agents

Work Without Queues

Bad:

How Artificial Intelligence Is Transforming Enterprise Productivity Through Autonomous Agents


Use only the source found in the input news.
FRAMEWORK RULES

Create ONLY ONE original framework.

Give the framework a unique name.

Use the framework throughout the article.

Do NOT introduce multiple frameworks.

The framework should explain the shift behind the news.

Examples:

Outcome Ownership Model

Digital Workforce Architecture

Autonomous Operations Layer

Enterprise Memory Layer

Decision Velocity Framework

Human-AI Coordination Layer

Operational Intelligence Layer

Use only one framework per article.
FRAMEWORK USAGE RULES

Create ONLY ONE framework.

Introduce the framework in paragraph 2.

After introducing it, do NOT repeat the framework name in every paragraph.

Mention it only when necessary.

Use natural writing.

The article should feel written by a human analyst.

Avoid repeating phrases.

Avoid repeating terminology.

Avoid repeating sentence structures.
FRAMEWORK DEPTH RULES

Do not create a framework only as a label.

The framework must explain:

* Why the old model is breaking.
* Why the new model wins.
* What leaders should do differently.
* What becomes possible because of it.

A framework must change how the reader thinks about the problem.


# THOUGHT LEADERSHIP RULES

# Take a strong point of view.

# Make bold predictions.

# Challenge conventional assumptions.

# Do not write like an academic report.

# Do not write like a news summary.

# Write like a founder explaining a major shift in how industries operate.

# The reader should feel they learned a new mental model.

# Focus on:

# * Why the old way no longer works.
# * Why this shift matters now.
# * What leaders are missing.
# * What winners will do differently.
# * What happens over the next 3-5 years.

# Avoid generic observations.

# Avoid obvious statements.

# Avoid repeating industry buzzwords.

# Prefer insights over explanations.

# Prefer predictions over descriptions.

# Prefer strategic thinking over reporting.

# The article should feel like a premium executive briefing.

# The reader should finish the article with a new way of thinking about the problem.

THOUGHT QUALITY RULES

Do not repeat framework names more than twice.

Do not repeat key phrases.

After introducing a framework, refer to it naturally:

* this shift
* this model
* this architecture
* this capability
* this operating layer

Focus on second-order effects.

Do not explain what the technology does.

Explain what changes because the technology exists.

Ask:

* What industries change?
* What business models disappear?
* What new advantages emerge?
* What becomes cheaper?
* What becomes faster?
* What becomes possible?





THOUGHT LEADERSHIP RULES

Take a strong point of view.

Make bold predictions.

Challenge conventional assumptions.

Do not write like an academic report.

Do not write like a news summary.

Write like a founder explaining a major shift in how industries operate.

The reader should feel they learned a new mental model.

Focus on:

* Why the old way no longer works.
* Why this shift matters now.
* What leaders are missing.
* What winners will do differently.
* What happens over the next 3-5 years.

Avoid generic observations.

Avoid obvious statements.

Avoid repeating industry buzzwords.

Prefer insights over explanations.

Prefer predictions over descriptions.

Prefer strategic thinking over reporting.

The article should feel like a premium executive briefing.

The reader should finish the article with a new way of thinking about the problem.

NARRATIVE STRUCTURE RULES

Do not write:

* Business implications
* Operational implications
* Economic implications
* Industry impact
* Leadership takeaway

Do not label ideas.

Instead, build a narrative.

Paragraph 1:
Start with a bold observation.

Paragraph 2:
Introduce the shift.

Paragraph 3:
Explain why the old model is breaking.

Paragraph 4:
Explain the new model.

Paragraph 5:
Describe who wins.

Paragraph 6:
Describe who loses.

Paragraph 7:
Reveal a non-obvious consequence.

Paragraph 8:
Make a bold prediction.

Paragraph 9:
Explain what leaders should do.

Paragraph 10:
End with a memorable insight.

The article should read like a founder memo, not a consulting report.

HUMAN WRITING RULES

After introducing a framework, do not repeat the framework name more than 2 times.

Use natural references such as:

* this model
* this shift
* this architecture
* this approach
* this infrastructure

Avoid keyword repetition.

Write like a human analyst, not an SEO article.

Every paragraph should feel different in tone and structure.

VOICE RULES

Write in short, punchy sentences.

Mix short and long paragraphs.

Occasionally use a one-sentence paragraph for emphasis.

Challenge assumptions.

Prefer strong statements over explanations.

Examples:

* Software is becoming labor.

* Biology is becoming infrastructure.

* The factory is becoming a data center.

* The next workforce may not be human.

The article should feel provocative but believable.

CATEGORY RULES

Category is NOT the article style.

Category must represent the industry or topic.

Examples:
Future of Work
Digital Workers
Enterprise AI
AI Workforce
Autonomous Operations
Human-AI Collaboration
Enterprise Transformation
Operational Intelligence
Digital Labor
AI Infrastructure

Never use:

* Founder Memo
* Executive Briefing
* Industry Analysis
* Strategic Outlook
* Technology Thesis
* Market Shift Analysis

Those are writing styles, not categories.

BANNED PHRASES RULE

If any of these phrases appear,
rewrite the paragraph.

- In conclusion
- Furthermore
- Moreover
- Overall
- To summarize

The answer is invalid if these phrases appear.
{news}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are the Chief Insights Officer at Luvana AI."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5,
        max_tokens=2000
    )

    print("BLOG GENERATED")

    blog_content = response.choices[0].message.content

    return blog_content








    



