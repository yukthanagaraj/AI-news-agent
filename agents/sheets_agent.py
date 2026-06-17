import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os

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

        client = gspread.authorize(
            creds
        )

        sheet_id = os.getenv(
            "GOOGLE_SHEET_ID"
        )

        _sheet = client.open_by_key(
            sheet_id
        ).sheet1

    return _sheet


def save_blog(
    date,
    category,
    title,
    blog_content,
    image_prompt,
    source_url,
    image_url
):

    sheet = get_sheet()

    sheet.append_row(
        [
            date,
            category,
            title,
            blog_content,
            image_prompt,
            source_url,
            image_url
        ]
    )

    print("Blog saved to Google Sheets")