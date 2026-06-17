from agents.vector_memory import (
    retrieve_similar_articles
)


def recommend_articles(
        article_content
):

    results = retrieve_similar_articles(
        article_content
    )

    return results


if __name__ == "__main__":

    result = recommend_articles(
        "AI agents improve enterprise intelligence."
    )

    print(result)