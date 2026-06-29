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

Evaluate the article using the following criteria.

Content Quality

- Score out of 10
- Brief explanation

Originality

- Score out of 10
- Brief explanation

Readability

- Score out of 10
- Brief explanation

Repetition

- Score out of 10
- Brief explanation

SEO Score

- Score out of 10
- Consider keyword usage, title quality, headings and semantic relevance.

AEO Score

- Score out of 10
- Consider answer quality, article structure and executive questions.

Enterprise Insight Score

- Score out of 10
- Evaluate strategic thinking, enterprise relevance and business value.

Executive Editorial Score

- Score out of 10
- Evaluate writing quality, professionalism and executive tone.

Overall Score

- Score out of 10

Finally provide a short overall evaluation in 2-3 sentences.

Return ONLY the evaluation.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
You are a senior editorial evaluator for an Enterprise AI publication.

Evaluate articles as if reviewing them before publication.

Be objective.

Reward:

- Original insights
- Executive writing
- Strong enterprise analysis
- High readability
- Excellent SEO
- Excellent AEO

Penalize:

- Repetition
- Weak analysis
- Generic AI explanations
- Poor structure
- News summarization
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=700
    )

    print("ARTICLE EVALUATION COMPLETE")

    return response.choices[0].message.content


if __name__ == "__main__":

    sample_article = """
AI agents are becoming an important layer of enterprise intelligence.
Organizations are increasingly using autonomous systems to improve
productivity, decision-making and enterprise execution.
"""

    print("=" * 80)
    print("ARTICLE EVALUATION")
    print("=" * 80)

    result = evaluate_article(sample_article)

    print(result)