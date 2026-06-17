from agents.sheets_agent import get_sheet


def generate_newsletter():

    sheet = get_sheet()

    records = sheet.get_all_records()

    latest_articles = list(
        reversed(records[-5:])
    )

    newsletter = []

    for i, row in enumerate(
            latest_articles,
            start=1
    ):

        title = row.get(
            "Title",
            ""
        )

        category = row.get(
            "Category",
            ""
        )

        newsletter.append(
            f"{i}. {title} ({category})"
        )

    return "\n".join(newsletter)


if __name__ == "__main__":

    print()

    print("TOP STORIES THIS WEEK")

    print()

    print(
        generate_newsletter()
    )