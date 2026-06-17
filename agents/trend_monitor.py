from collections import Counter
from agents.sheets_agent import get_sheet


def top_categories():

    sheet = get_sheet()

    records = sheet.get_all_records()

    categories = [
        row["Category"]
        for row in records
    ]

    counter = Counter(
        categories
    )

    return counter.most_common(
        5
    )


if __name__ == "__main__":

    print(
        top_categories()
    )