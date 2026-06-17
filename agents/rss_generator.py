from agents.sheets_agent import get_sheet


def generate_rss():

    sheet = get_sheet()

    records = sheet.get_all_records()

    rss = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>

<title>Luvana AI Journal</title>

<link>https://your-domain.com</link>

<description>
Daily insights on AI, digital labor, and enterprise intelligence.
</description>
"""

    for row in reversed(records[-20:]):

        title = row.get("Title", "")
        article_id = row.get("ID", "")
        date = row.get("Date", "")

        rss += f"""
<item>

<title>{title}</title>

<link>
https://your-domain.com/blog/{article_id}
</link>

<pubDate>{date}</pubDate>

</item>
"""

    rss += """
</channel>
</rss>
"""

    with open(
        "outputs/rss.xml",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(rss)

    print("RSS feed generated")


if __name__ == "__main__":

    generate_rss()