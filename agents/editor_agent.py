from agents.quality_evaluator import (
    evaluate_article
)


def approve_article(
        article
):

    report = evaluate_article(
        article
    )

    return report