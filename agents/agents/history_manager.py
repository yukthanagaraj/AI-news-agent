from pathlib import Path
import json

HISTORY_DIR = Path("output")
HISTORY_FILE = HISTORY_DIR / "history.json"

DEFAULT_DATA = {
    "titles": [],
    "section_titles": [],
    "frameworks": [],
    "opening_styles": [],
    "conclusions": [],
    "quotes": [],
}

_cache = None


def _ensure_loaded():
    global _cache
    if _cache is not None:
        return _cache

    if HISTORY_FILE.exists():
        try:
            _cache = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            _cache = DEFAULT_DATA.copy()
    else:
        _cache = DEFAULT_DATA.copy()

    for key, value in DEFAULT_DATA.items():
        _cache.setdefault(key, list(value))
    return _cache


def _save():
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(
        json.dumps(_ensure_loaded(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def _append_unique(key, value, limit=100):
    value = (value or "").strip()
    if not value:
        return
    data = _ensure_loaded()
    if value not in data[key]:
        data[key].append(value)
        data[key] = data[key][-limit:]
        _save()


def get_used_titles():
    return list(_ensure_loaded()["titles"])


def get_used_section_titles():
    return list(_ensure_loaded()["section_titles"])


def get_used_frameworks():
    return list(_ensure_loaded()["frameworks"])


def get_used_opening_styles():
    return list(_ensure_loaded()["opening_styles"])


def get_used_conclusions():
    return list(_ensure_loaded()["conclusions"])


def get_used_quotes():
    return list(_ensure_loaded()["quotes"])


def remember_title(title):
    _append_unique("titles", title)


def remember_section_title(title):
    _append_unique("section_titles", title)


def remember_framework(framework):
    _append_unique("frameworks", framework)


def remember_opening_style(opening):
    _append_unique("opening_styles", opening)


def remember_conclusion(conclusion):
    _append_unique("conclusions", conclusion)


def remember_quote(quote):
    _append_unique("quotes", quote)