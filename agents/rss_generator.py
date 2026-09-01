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
    gspread's get_all_records() requires every header in row 1 to be
    unique and non-empty, and raises if it isn't -- which is exactly
    what was crashing this function (two blank-header columns both
    read as ''). get_all_values() has no such restriction, so we build
    the header row ourselves here: blank headers get a placeholder
    name, and any repeated name (blank or not) gets a numeric suffix
    so every key ends up unique.
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

        # Pad short rows so zip doesn't silently drop trailing columns
        padded_row = row + [""] * (len(headers) - len(row))

        records.append(dict(zip(headers, padded_row)))

    return records


def generate_rss():

    sheet = get_sheet()

    records = _get_all_records_safe(sheet)

    Path("outputs").mkdir(exist_ok=True)

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>

<title>AI Insights</title>

<link>{SITE_URL}</link>

<description>
Daily executive insights on Enterprise AI, Agentic AI, AI Employees,
Digital Workers and the Future of Work.
</description>
"""

    latest_records = list(reversed(records[-20:]))

    for index, row in enumerate(latest_records, start=1):

        title = row.get("Title", "")

        date = row.get("Date", "")

        rss += f"""
<item>

<title>{title}</title>

<link>{SITE_URL}/blog/{index}</link>

<pubDate>{date}</pubDate>

</item>
"""

    rss += """
</channel>
</rss>
"""

    output_path = Path("outputs") / "rss.xml"

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(rss)

    print(f"RSS feed generated: {output_path}")


if __name__ == "__main__":

    generate_rss()