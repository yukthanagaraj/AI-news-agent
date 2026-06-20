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
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.9,
        max_tokens=2000
    )

    print("BLOG GENERATED")

    return response.choices[0].message.content









    



