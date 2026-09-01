# import re
# from agents.llm_client import client, MODEL_NAME
# from agents.evaluation_parts.content_quality import CONTENT_QUALITY_RULES
# from agents.evaluation_parts.uniqueness_rules import UNIQUENESS_RULES
# from agents.evaluation_parts.readability_rules import READABILITY_RULES
# from agents.evaluation_parts.repetition_rules import REPETITION_RULES
# from agents.publish_guard import validate_article
# from agents.text_metrics import diagnose_article


# def _extract_blog_body(article):
#     m = re.search(r"Blog:\s*(.*)", article, re.DOTALL)
#     return m.group(1).strip() if m else article


# def _build_diagnostic_block(article):
#     d = diagnose_article(_extract_blog_body(article))
#     return "\n".join([
#         f"- Sections with fewer than 3 paragraphs: {', '.join(d['thin_sections']) if d['thin_sections'] else 'none'}",
#         f"- Paragraph pairs teaching the same idea: {d['repetitive_paragraph_pairs'] if d['repetitive_paragraph_pairs'] else 'none'}",
#         f"- Section pairs with overlapping topics: {d['section_overlaps'] if d['section_overlaps'] else 'none'}",
#         f"- Blockquotes found: {d['quote_count']} (should be exactly 1)",
#         f"- Enterprise framework present: {'yes — ' + d['framework_heading'] if d['has_framework'] else 'NO'}",
#         f"- Duplicate framework mentions: {d['named_framework_mentions'] if d['named_framework_mentions'] else 'none'}",
#         f"- Enterprise case study present: {'yes — ' + d['case_study_heading'] if d['has_case_study'] else 'NO'}",
#         f"- Duplicate case studies: {d['duplicate_case_study_pairs'] if d['duplicate_case_study_pairs'] else 'none'}",
#         f"- Executive trade-off present: {'yes — ' + d['tradeoff_heading'] if d['has_tradeoff'] else 'NO'}",
#         f"- Conclusion vocabulary overlap with rest of article: {d['conclusion_overlap']} (>0.30 suggests it summarizes rather than teaches something new)",
#         f"- Banned phrases found: {d['banned_phrases'] if d['banned_phrases'] else 'none'}",
#         f"- Unsourced numeric claims: {d['unsourced_numeric_claims'] if d['unsourced_numeric_claims'] else 'none'}",
#         f"- Unsourced example markers: {d['unsourced_example_markers'] if d['unsourced_example_markers'] else 'none'}",
#         f"- AI filler transitions: {d['ai_filler_transitions'] if d['ai_filler_transitions'] else 'none'}",
#         f"- Repeated sentence skeletons: {d['repeated_sentence_skeletons'] if d['repeated_sentence_skeletons'] else 'none'}",
#         f"- Conclusion ends cleanly: {'yes' if d['conclusion_ends_cleanly'] else 'NO'}",
#         f"- Total H2 sections: {d['total_h2_count']}",
#     ])


# def evaluate_article(article, research_package=""):
#     guard = validate_article(article, research_package=research_package)

#     if not guard.ok:
#         return f"""
# Overall Score: 0/10

# Overall Editorial Decision:
# Reject

# Major Strengths

# - None.

# Major Weaknesses

# - {'; '.join(guard.hard_failures)}

# Top Three Improvements

# - Fix all blocking validation failures.
# - Regenerate unsupported sections with evidence.
# - Add required structure, quote, and framework controls.
# """.strip()

#     diagnostic_block = _build_diagnostic_block(article)

#     prompt = f"""
# You are a senior editorial evaluator for Luvana AI Journal, a premium Enterprise AI publication.

# Evaluate this article as if you are a strict editorial board member comparing it against Harvard Business Review, MIT Technology Review, and The Information.

# Hard rules:
# - Be objective and critical.
# - Do not inflate scores.
# - Treat the diagnostic report as ground truth.
# - Penalize generic AI writing heavily.
# - Penalize broad-topic drift heavily.
# - Reward originality, framework depth, enterprise usefulness, and agentic AI specificity.
# - The article must feel like a Luvana perspective, not a recycled AI-generated enterprise piece.

# ARTICLE

# {article}

# ==================================================
# ALGORITHMIC STRUCTURE REPORT (computed, not your judgment — treat as ground truth)
# ==================================================

# {diagnostic_block}

# Use this report as ground truth for:
# - Editorial Structure
# - Enterprise Framework
# - Enterprise Case Study
# - Editorial Quote
# - Repetition
# - Conclusion quality
# - Structural completeness

# Reference rules:
# {CONTENT_QUALITY_RULES}

# {UNIQUENESS_RULES}

# {READABILITY_RULES}

# {REPETITION_RULES}

# Scoring criteria:
# 1. SEO
# 2. AEO
# 3. Executive Editorial Quality
# 4. Originality
# 5. Readability
# 6. Enterprise Insight
# 7. Evidence & Examples
# 8. Evidence Credibility
# 9. Strategic Depth
# 10. Information Density
# 11. Editorial Structure
# 12. Enterprise Framework
# 13. Enterprise Case Study
# 14. Editorial Quote
# 15. Executive Conclusion
# 16. Publication Readiness
# 17. Enterprise AI Relevance
# 18. Search Engine Readiness

# For every score provide:
# - Score
# - Why the score was given
# - One improvement

# Output format:

# Overall Score: X/10

# Overall Editorial Decision:
# Publish
# OR
# Publish with Minor Revisions
# OR
# Major Revision Required
# OR
# Reject

# Major Strengths

# - point
# - point
# - point

# Major Weaknesses

# - point
# - point
# - point

# Top Three Improvements

# - point
# - point
# - point

# Return ONLY the evaluation.
# """

#     response = client.chat.completions.create(
#         model=MODEL_NAME,
#         messages=[
#             {
#                 "role": "system",
#                 "content": """
# You are a senior editorial evaluator for an Enterprise AI publication.
# You evaluate articles before publication.
# You are strict, original, and unsparing.
# Never inflate scores.
# """
#             },
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ]
#     )

#     print("ARTICLE EVALUATION COMPLETE")
#     return response.choices[0].message.content

import re

from agents.llm_client import client, MODEL_NAME
from agents.evaluation_parts.content_quality import CONTENT_QUALITY_RULES
from agents.evaluation_parts.uniqueness_rules import UNIQUENESS_RULES
from agents.evaluation_parts.readability_rules import READABILITY_RULES
from agents.evaluation_parts.repetition_rules import REPETITION_RULES
from agents.publish_guard import validate_article
from agents.text_metrics import diagnose_article


def _extract_blog_body(article):
    m = re.search(r"Blog:\s*(.*)", article, re.DOTALL)
    return m.group(1).strip() if m else article


def _build_diagnostic_block(article):
    d = diagnose_article(_extract_blog_body(article))
    return "\n".join([
        f"- Sections with fewer than 3 paragraphs: {', '.join(d['thin_sections']) if d['thin_sections'] else 'none'}",
        f"- Paragraph pairs teaching the same idea: {d['repetitive_paragraph_pairs'] if d['repetitive_paragraph_pairs'] else 'none'}",
        f"- Section pairs with overlapping topics: {d['section_overlaps'] if d['section_overlaps'] else 'none'}",
        f"- Blockquotes found: {d['quote_count']} (should be exactly 1)",
        f"- Direct-answer lead present: {'yes' if d.get('has_direct_answer_lead') else 'NO'}",
        f"- Question headings found: {d.get('question_headings') if d.get('question_headings') else 'none'}",
        f"- Quick Answers present: {'yes' if d.get('has_quick_answers') else 'no'}",
        f"- Executive summary present: {'yes' if d.get('has_executive_summary') else 'no'}",
        f"- Enterprise framework present: {'yes — ' + d['framework_heading'] if d['has_framework'] else 'NO'}",
        f"- Duplicate framework mentions: {d['named_framework_mentions'] if d['named_framework_mentions'] else 'none'}",
        f"- Enterprise case study present: {'yes — ' + d['case_study_heading'] if d['has_case_study'] else 'NO'}",
        f"- Duplicate case studies: {d['duplicate_case_study_pairs'] if d['duplicate_case_study_pairs'] else 'none'}",
        f"- Executive trade-off present: {'yes — ' + d['tradeoff_heading'] if d['has_tradeoff'] else 'NO'}",
        f"- Conclusion vocabulary overlap with rest of article: {d['conclusion_overlap']} (>0.30 suggests it summarizes rather than teaches something new)",
        f"- Banned phrases found: {d['banned_phrases'] if d['banned_phrases'] else 'none'}",
        f"- Unsourced numeric claims: {d['unsourced_numeric_claims'] if d['unsourced_numeric_claims'] else 'none'}",
        f"- Unsourced example markers: {d['unsourced_example_markers'] if d['unsourced_example_markers'] else 'none'}",
        f"- AI filler transitions: {d['ai_filler_transitions'] if d['ai_filler_transitions'] else 'none'}",
        f"- Repeated sentence skeletons: {d['repeated_sentence_skeletons'] if d['repeated_sentence_skeletons'] else 'none'}",
        f"- Conclusion ends cleanly: {'yes' if d['conclusion_ends_cleanly'] else 'NO'}",
        f"- Total H2 sections: {d['total_h2_count']}",
    ])


def evaluate_article(article, research_package=""):
    guard = validate_article(article, research_package=research_package)

    if not guard.ok:
        return f"""
Overall Score: 0/10


Overall Editorial Decision:
Reject


Major Strengths


- None.


Major Weaknesses


- {'; '.join(guard.hard_failures)}


Top Three Improvements


- Fix all blocking validation failures.
- Regenerate unsupported sections with evidence.
- Add required structure, quote, and framework controls.
""".strip()

    diagnostic_block = _build_diagnostic_block(article)

    prompt = f"""
You are a senior editorial evaluator for Luvana AI Journal, a premium Enterprise AI publication.

Evaluate this article as if you were a strict editorial board member comparing it against Harvard Business Review, MIT Technology Review, and The Information.

Hard rules:
- Be objective and critical.
- Do not inflate scores.
- Treat the diagnostic report as ground truth.
- Penalize generic AI writing heavily.
- Penalize broad-topic drift heavily.
- Penalize missing direct-answer lead behavior.
- Penalize question-headed sections that do not answer first.
- Reward originality, framework depth, enterprise usefulness, and agentic AI specificity.
- The article must feel like a Luvana perspective, not a recycled AI-generated enterprise piece.

ARTICLE

{article}

==================================================
ALGORITHMIC STRUCTURE REPORT (computed, not your judgment — treat as ground truth)
==================================================

{diagnostic_block}

Use this report as ground truth for:
- Editorial Structure
- Enterprise Framework
- Enterprise Case Study
- Editorial Quote
- Repetition
- Conclusion quality
- Structural completeness
- Lead quality
- AEO readiness

Reference rules:
{CONTENT_QUALITY_RULES}

{UNIQUENESS_RULES}

{READABILITY_RULES}

{REPETITION_RULES}

Scoring criteria:
1. SEO
2. AEO
3. Executive Editorial Quality
4. Originality
5. Readability
6. Enterprise Insight
7. Evidence & Examples
8. Evidence Credibility
9. Strategic Depth
10. Information Density
11. Editorial Structure
12. Enterprise Framework
13. Enterprise Case Study
14. Editorial Quote
15. Executive Conclusion
16. Publication Readiness
17. Enterprise AI Relevance
18. Search Engine Readiness

For every score provide:
- Score
- Why the score was given
- One improvement

Output format:

Overall Score: X/10

Overall Editorial Decision:
Publish
OR
Publish with Minor Revisions
OR
Major Revision Required
OR
Reject

Major Strengths

- point
- point
- point

Major Weaknesses

- point
- point
- point

Top Three Improvements

- point
- point
- point

Return ONLY the evaluation.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": """
You are a senior editorial evaluator for an Enterprise AI publication.
You evaluate articles before publication.
You are strict, original, and unsparing.
Never inflate scores.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content