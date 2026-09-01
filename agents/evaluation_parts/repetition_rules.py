REPETITION_RULES = """
REPETITION RULES

Use deterministic signals from text_metrics as primary evidence.

Penalize heavily when:
- paragraph repetition pairs are detected
- section topic overlap is high
- multiple framework names appear
- multiple case studies appear
- the conclusion overlaps too much with prior sections
- key takeaways are written as prose instead of bullets

The evaluator should trust the diagnostic report over vague model impressions.
"""