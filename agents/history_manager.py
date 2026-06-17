import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

MEMORY_DIR = BASE_DIR / "memory"


def load_memory(filename):

    MEMORY_DIR.mkdir(exist_ok=True)

    path = MEMORY_DIR / filename

    if not path.exists():
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return []


def save_memory(filename, data):

    MEMORY_DIR.mkdir(exist_ok=True)

    path = MEMORY_DIR / filename

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


def get_used_titles():
    return load_memory("used_titles.json")


def get_used_quotes():
    return load_memory("used_quotes.json")


def get_used_frameworks():
    return load_memory("used_frameworks.json")


def get_used_section_titles():
    return load_memory("used_section_titles.json")


def get_used_visual_concepts():
    return load_memory("used_visual_concepts.json")


def get_used_categories():
    return load_memory("used_categories.json")


def remember_title(title):

    titles = get_used_titles()

    if title not in titles:

        titles.append(title)

        save_memory(
            "used_titles.json",
            titles[-200:]
        )


def remember_quote(quote):

    quotes = get_used_quotes()

    if quote not in quotes:

        quotes.append(quote)

        save_memory(
            "used_quotes.json",
            quotes[-200:]
        )


def remember_framework(framework):

    frameworks = get_used_frameworks()

    if framework not in frameworks:

        frameworks.append(framework)

        save_memory(
            "used_frameworks.json",
            frameworks[-200:]
        )


def remember_section_title(section_title):

    section_titles = get_used_section_titles()

    if section_title not in section_titles:

        section_titles.append(section_title)

        save_memory(
            "used_section_titles.json",
            section_titles[-200:]
        )


def remember_visual_concept(concept):

    visual_concepts = get_used_visual_concepts()

    if concept not in visual_concepts:

        visual_concepts.append(concept)

        save_memory(
            "used_visual_concepts.json",
            visual_concepts[-100:]
        )


def remember_category(category):

    categories = get_used_categories()

    if category not in categories:

        categories.append(category)

        save_memory(
            "used_categories.json",
            categories[-50:]
        )