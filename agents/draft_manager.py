import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DRAFTS_DIR = BASE_DIR / "drafts"


def save_draft(title, subtitle, blog_content, image_prompt, source_url, related_sources=None):
    """Persist the draft to disk. No validation here — validation belongs
    in check_hard_structural_gate() and quality_check(), which run later
    in the pipeline once all content (including AEO) actually exists."""
    DRAFTS_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = "".join(c if c.isalnum() or c in " -_" else "" for c in title)[:60].strip()
    filename = f"{timestamp}_{safe_title or 'draft'}.json"

    draft = {
        "title": title,
        "subtitle": subtitle,
        "blog_content": blog_content,
        "image_prompt": image_prompt,
        "source_url": source_url,
        "related_sources": related_sources or [],
        "saved_at": datetime.now().isoformat(),
    }

    path = DRAFTS_DIR / filename
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(draft, f, indent=2, ensure_ascii=False)
        print(f"Draft saved: {path}")
        return str(path)
    except Exception as e:
        print(f"Warning: could not save draft: {e}")
        return None