import os
from dotenv import load_dotenv
from groq import Groq

from agents.evaluation_parts.content_quality import CONTENT_QUALITY_RULES
from agents.evaluation_parts.uniqueness_rules import UNIQUENESS_RULES
from agents.evaluation_parts.readability_rules import READABILITY_RULES
from agents.evaluation_parts.repetition_rules import REPETITION_RULES

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def evaluate_article(article):

    prompt = f"""
ARTICLE

{article}

{CONTENT_QUALITY_RULES}

{UNIQUENESS_RULES}

{READABILITY_RULES}

{REPETITION_RULES}

Give:

Content Quality:
Originality Score:
Readability Score:
Repetition Score:

Overall Score:

Short explanation.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=300
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    sample_article = """
    AI agents are becoming an important layer of enterprise intelligence.
    Organizations are increasingly using autonomous systems to improve
    productivity and decision-making.
    """

    print()
    print("ARTICLE EVALUATION")
    print()

    result = evaluate_article(sample_article)

    print(result)