from collections import Counter
from agents.sheets_agent import get_sheet


def get_analytics():

    sheet = get_sheet()

    records = sheet.get_all_records()

    total_articles = len(records)

    categories = []

    for row in records:

        category = row.get(
            "Category",
            ""
        )

        if category:

            categories.append(category)

    counter = Counter(categories)

    return {
        "total_articles": total_articles,
        "category_counts": counter,
        "top_category": (
            counter.most_common(1)[0][0]
            if counter
            else "None"
        )
    }


if __name__ == "__main__":

    analytics = get_analytics()

    print()

    print("LUVANA AI JOURNAL ANALYTICS")

    print()

    print(
        "Total Articles:",
        analytics["total_articles"]
    )

    print()

    print(
        "Top Category:",
        analytics["top_category"]
    )

    print()

    print("Articles by Category")

    print()

    for category, count in analytics[
        "category_counts"
    ].items():

        print(
            f"{category}: {count}"
        )