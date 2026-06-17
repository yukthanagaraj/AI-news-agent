from agents.sheets_agent import get_sheet


def generate_sitemap():

    sheet = get_sheet()

    records = sheet.get_all_records()

    sitemap = """<?xml version="1.0" encoding="UTF-8"?>

<urlset
xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

    for row in records:

        article_id = row.get("ID", "")

        sitemap += f"""
<url>

<loc>
https://your-domain.com/blog/{article_id}
</loc>

</url>
"""

    sitemap += """
</urlset>
"""

    with open(
        "outputs/sitemap.xml",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(sitemap)

    print("Sitemap generated")


if __name__ == "__main__":

    generate_sitemap()