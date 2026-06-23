import os
import random
from dotenv import load_dotenv
from groq import Groq

from agents.templates import TEMPLATES
from agents.prompt_builder import build_prompt

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_blog(news, previous_titles=None):

    template = random.choice(
        TEMPLATES
    )

    prompt = build_prompt(
        news,
        previous_titles,
        template
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
You are a senior enterprise technology analyst.

Write articles similar to Luvana AI Insights.

Rules:

- Professional tone.
- Avoid hype and clickbait.
- No category labels.
- Focus on AI Agents, AI Employees, Enterprise AI and Future of Work.
- Prefer strategic and enterprise perspectives.
- Titles should be short (4–6 words).
- Avoid colons.
- Generate one memorable quote.
- Make articles insightful rather than news summaries.
- Articles must be between 1200 and 1500 words.
- Every major section must contain 3–4 detailed paragraphs.
- Never generate short sections.
- Include SEO keywords naturally throughout the article.
- Include one markdown quote block inside the article.
- Minimum article length is 1200 words.
- Never generate articles below 1200 words.
- Every major section must contain at least 3 detailed paragraphs.
- Do not create sections with only 1 or 2 paragraphs.
- Expand enterprise implications with concrete analysis.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=1.0,
        max_tokens=4000
    )

    print("BLOG GENERATED")

    return response.choices[0].message.content









    



