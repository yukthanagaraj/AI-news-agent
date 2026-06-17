from agents.sheets_agent import get_sheet


def search_articles(
        query,
        limit=10
):

    try:

        sheet = get_sheet()

        records = sheet.get_all_records()

        query = query.lower()

        results = []

        for row in records:

            title = row.get(
                "Title",
                ""
            ).lower()

            category = row.get(
                "Category",
                ""
            ).lower()

            content = row.get(
                "Content",
                ""
            ).lower()

            if (
                query in title
                or query in category
                or query in content
            ):

                results.append(
                    {
                        "title": row.get(
                            "Title",
                            ""
                        ),

                        "category": row.get(
                            "Category",
                            ""
                        )
                    }
                )

        return results[:limit]

    except Exception as e:

        print(
            "Search error:",
            e
        )

        return []


if __name__ == "__main__":

    results = search_articles(
        "enterprise"
    )

    print()

    print("SEARCH RESULTS")

    print()

    if len(results) == 0:

        print("No matching articles found.")

    else:

        for article in results:

            print(
                f"- {article['title']} ({article['category']})"
            )