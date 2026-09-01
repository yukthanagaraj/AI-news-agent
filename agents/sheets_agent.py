import os
import json
from datetime import datetime
from pathlib import Path

import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

DISABLE_SHEETS = os.getenv("DISABLE_SHEETS", "false").lower() == "true"
LOCAL_BLOGS_FILE = Path("output") / "blogs.json"
LOCAL_BLOGS_FILE.parent.mkdir(parents=True, exist_ok=True)

_sheet = None


def get_sheet():
    global _sheet

    if DISABLE_SHEETS:
        return None

    if _sheet is None:
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                "credentials/service_account.json",
                scope,
            )
            client = gspread.authorize(creds)
            sheet_id = os.getenv("GOOGLE_SHEET_ID")
            _sheet = client.open_by_key(sheet_id).sheet1
        except Exception as e:
            print(f"Warning: Could not initialize Google Sheet: {e}")
            return None

    return _sheet


def format_date(date):
    if not date:
        return datetime.now().strftime("%d %B, %Y")

    try:
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").strftime("%d %B, %Y")
    except ValueError:
        pass

    try:
        return datetime.strptime(date, "%Y-%m-%d").strftime("%d %B, %Y")
    except ValueError:
        pass

    return date


def article_exists(title):
    title = title.strip()

    if DISABLE_SHEETS:
        if not LOCAL_BLOGS_FILE.exists():
            return False
        try:
            data = json.loads(LOCAL_BLOGS_FILE.read_text(encoding="utf-8"))
            if not isinstance(data, list):
                return False
            return any(
                isinstance(item, dict)
                and item.get("title", "").strip().lower() == title.lower()
                for item in data
            )
        except Exception:
            return False

    try:
        sheet = get_sheet()
        if sheet is None:
            return False
        titles = sheet.col_values(2)
        return any(
            t.strip().lower() == title.lower()
            for t in titles[1:]
        )
    except Exception:
        return False


def save_blog(
    date,
    title,
    subtitle,
    blog_content,
    image_prompt,
    source_url,
    image_url,
    related_sources=None,
):
    """
    Column layout:
    1 Date | 2 Title | 3 Blog | 4 Image Prompt | 5 Source URL
    | 6 Image URL | 7 Subtitle | 8 Related Sources (JSON string)
    """
    title = title.strip()
    subtitle = (subtitle or "").strip()
    blog_content = blog_content.strip()
    image_prompt = image_prompt.strip()
    source_url = source_url.strip()
    image_url = image_url.strip()
    related_sources_json = json.dumps(related_sources or [], ensure_ascii=False)

    if article_exists(title):
        print("Duplicate article detected. Skipping save.")
        return

    formatted_date = format_date(date)

    if DISABLE_SHEETS:
        entry = {
            "date": formatted_date,
            "title": title,
            "subtitle": subtitle,
            "blog_content": blog_content,
            "image_prompt": image_prompt,
            "source_url": source_url,
            "image_url": image_url,
            "related_sources": related_sources or [],
            "related_sources_json": related_sources_json,
        }

        try:
            if LOCAL_BLOGS_FILE.exists():
                data = json.loads(LOCAL_BLOGS_FILE.read_text(encoding="utf-8"))
                if not isinstance(data, list):
                    data = []
            else:
                data = []

            data.append(entry)
            LOCAL_BLOGS_FILE.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            print("Blog saved locally to output/blogs.json")
        except Exception as e:
            print(f"Warning: could not save blog locally: {e}")
        return

    sheet = get_sheet()
    if sheet is None:
        print("Warning: Google Sheet unavailable. Skipping save.")
        return

    try:
        sheet.append_row(
            [
                formatted_date,
                title,
                blog_content,
                image_prompt,
                source_url,
                image_url,
                subtitle,
                related_sources_json,
            ]
        )
        print("Blog saved to Google Sheets")
    except Exception as e:
        print(f"Warning: could not save blog to sheet: {e}")