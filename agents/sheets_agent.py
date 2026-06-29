import os
from datetime import datetime

import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

_sheet = None


def get_sheet():

    global _sheet

    if _sheet is None:

        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "credentials/service_account.json",
            scope
        )

        client = gspread.authorize(creds)

        sheet_id = os.getenv("GOOGLE_SHEET_ID")

        _sheet = client.open_by_key(sheet_id).sheet1

    return _sheet


def format_date(date):

    if not date:
        return datetime.now().strftime("%d %B, %Y")

    try:
        # NewsAPI format
        return datetime.strptime(
            date,
            "%Y-%m-%dT%H:%M:%SZ"
        ).strftime("%d %B, %Y")
    except ValueError:
        pass

    try:
        # YYYY-MM-DD format
        return datetime.strptime(
            date,
            "%Y-%m-%d"
        ).strftime("%d %B, %Y")
    except ValueError:
        pass

    return date


def save_blog(
    date,
    title,
    blog_content,
    image_prompt,
    source_url,
    image_url
):

    sheet = get_sheet()

    formatted_date = format_date(date)

    sheet.append_row(
        [
            formatted_date,
            title,
            blog_content,
            image_prompt,
            source_url,
            image_url
        ]
    )

    print("Blog saved to Google Sheets")