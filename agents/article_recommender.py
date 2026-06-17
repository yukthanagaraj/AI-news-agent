from agents.sheets_agent import get_sheet


def get_article_recommendations(
    current_title,
    current_category=None,
    limit=3
):

    try:

        sheet = get_sheet()

        records = sheet.get_all_records()

        recommendations = []

        # newest articles first
        for row in reversed(records):

            title = row.get(
                "Title",
                ""
            ).strip()

            category = row.get(
                "Category",
                ""
            ).strip()

            # skip empty titles
            if not title:
                continue

            # skip current article
            if title.lower() == current_title.lower():
                continue

            # same category only
            if (
                current_category
                and category.lower() != current_category.lower()
            ):
                continue

            recommendations.append(
                {
                    "title": title,
                    "category": category
                }
            )

            if len(recommendations) >= limit:
                break

        return recommendations

    except Exception as e:

        print(
            "Article recommendation error:",
            e
        )

        return []


if __name__ == "__main__":

    articles = get_article_recommendations(
        current_title="Decision Infrastructure Evolves",
        current_category="Enterprise Transformation"
    )

    print()
    print("More from Luvana AI Journal")
    print()

    if len(articles) == 0:

        print("No related articles found")

    else:

        for article in articles:

            print(
                f"- {article['title']} ({article['category']})"
            )