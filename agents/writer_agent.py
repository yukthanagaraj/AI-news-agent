import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_blog(news, previous_titles=None):

    used_titles = "\n".join(previous_titles or [])

    prompt = f"""
You are an enterprise technology analyst writing for a publication similar in style to Luvana AI Insights.

NEWS INPUT

{news}

PREVIOUS TITLES

{used_titles}

Do not generate any title that already exists above.

Avoid similar title structures.

Create a fresh title every time.

OBJECTIVE

Use the news as evidence.

Do not simply summarize the news.

Explain the larger organizational shift behind the news.

The reader should understand:

1. What happened.
2. Why it matters.
3. What changes because of it.

CATEGORY

Choose exactly one:

Future of Organizations
AI Workforce
Digital Labor
Enterprise Intelligence
Human-AI Collaboration
Autonomous Operations
Knowledge Systems
Enterprise Transformation
AI Governance
Operating Models

Generate titles that describe a shift,
an observation,
or a business consequence.

Avoid:
- Imperative
- Revolution
- Transformation
- Future of
- Wins
- Takes Hold

Prefer:
- The Geography of Intelligence
- Access Shapes Advantage
- Work Without Coordination
- Knowledge Without Queues
- Organizations Built for Agents

TITLE RULES

- 3 to 6 words
- No company names
- No colons
- No clickbait
- No headlines
- No em dashes
- Sound like an executive insight

Examples:

The Geography of Intelligence
Knowledge Without Queues
The New Management Layer
Work Without Coordination
Organizations Built for Agents
The Rise of AI Colleagues
The End of Manual Handoffs

ARTICLE RULES

- Write exactly 10 paragraphs
- Use simple language
- Use human writing
- Avoid consultant jargon
- Avoid hype
- Avoid generic AI statements
- Focus on organizations, work, management, operations, and decision making
- Avoid repeating the title inside the article

STRUCTURE

Paragraph 1:
What happened.

Paragraph 2:
Why it matters.

Paragraph 3:
What is changing.

Paragraph 4:
Why old models break.

Paragraph 5:
What replaces them.

Paragraph 6:
Hidden consequence.

Paragraph 7:
Who adapts fastest.

Paragraph 8:
Prediction.

Paragraph 9:
Strategic observation.

Paragraph 10:
Strong closing insight.

IMAGE PROMPT RULES

Create a premium editorial illustration.

The image should visually represent the core insight of the article.

Avoid generic robots.

Avoid people shaking hands.

Avoid company logos.

Use:
- enterprise operations
- digital workers
- knowledge networks
- intelligence infrastructure
- organizational transformation
- autonomous systems
- future workplaces

The image should look like a magazine cover illustration, not stock photography.

Create one detailed sentence.

OUTPUT FORMAT

Category: <category>

Title: <title>

Source URL: <source url>

Image Prompt: <image prompt>

Blog: <article>
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a senior enterprise technology analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=2000
    )

    print("BLOG GENERATED")

    return response.choices[0].message.content








    



