import os
from pathlib import Path

from dotenv import load_dotenv

from agents.sheets_agent import get_sheet

load_dotenv()

SITE_URL = os.getenv(
    "SITE_URL",
    "https://your-domain.com"
)


def _dedupe_headers(headers):
    """
    Same fix as rss_generator.py: get_all_records() requires every
    header in row 1 to be unique and non-empty and raises otherwise
    (two blank-header columns both read as ''). get_all_values() has
    no such restriction, so we build the header row ourselves: blank
    headers get a placeholder name, and any repeated name (blank or
    not) gets a numeric suffix so every key ends up unique.
    """
    seen = {}
    deduped = []

    for i, h in enumerate(headers):

        name = h.strip() if h and h.strip() else f"_blank_col_{i + 1}"

        if name in seen:

            seen[name] += 1

            name = f"{name}_{seen[name]}"

        else:

            seen[name] = 0

        deduped.append(name)

    return deduped


def _get_all_records_safe(sheet):
    """
    Drop-in replacement for sheet.get_all_records() that can't be
    broken by blank or duplicate header cells. Returns the same shape:
    a list of dicts, one per data row, keyed by (deduped) header name.
    """
    all_values = sheet.get_all_values()

    if not all_values:
        return []

    headers = _dedupe_headers(all_values[0])
    data_rows = all_values[1:]

    records = []

    for row in data_rows:

        padded_row = row + [""] * (len(headers) - len(row))

        records.append(dict(zip(headers, padded_row)))

    return records


def generate_sitemap():

    sheet = get_sheet()

    records = _get_all_records_safe(sheet)

    Path("outputs").mkdir(exist_ok=True)

    sitemap = """<?xml version="1.0" encoding="UTF-8"?>

<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

    latest_records = list(reversed(records))

    for index, row in enumerate(latest_records, start=1):

        date = row.get("Date", "")

        sitemap += f"""

<url>

<loc>{SITE_URL}/blog/{index}</loc>

<lastmod>{date}</lastmod>

<changefreq>daily</changefreq>

<priority>0.8</priority>

</url>
"""

    sitemap += """

</urlset>
"""

    output_path = Path("outputs") / "sitemap.xml"

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(sitemap)

    print(f"Sitemap generated: {output_path}")


if __name__ == "__main__":

    generate_sitemap()