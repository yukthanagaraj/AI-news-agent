import json
import re
import sys

def normalize(name):
    name = name.lower().strip()
    name = re.sub(r'^the\s+', '', name)
    name = re.sub(r'\s+(framework|model|maturity)\s*$', '', name).strip()
    return name

def find_frameworks(text):
    lines = text.split('\n')
    frameworks = []
    current_heading = None
    current_stages = []

    heading_pattern = re.compile(r'^#{2,3}\s*(.+)$')
    stage_pattern = re.compile(r'^#{2,3}\s*(Stage\s*\d+[:\-]?\s*.+)$', re.IGNORECASE)

    for line in lines:
        stage_match = stage_pattern.match(line.strip())
        heading_match = heading_pattern.match(line.strip())

        if stage_match and current_heading:
            current_stages.append(stage_match.group(1).strip())
        elif heading_match:
            title = heading_match.group(1).strip()
            if 'maturity' in title.lower() or 'framework' in title.lower():
                if current_heading:
                    frameworks.append((current_heading, current_stages))
                current_heading = title
                current_stages = []

    if current_heading:
        frameworks.append((current_heading, current_stages))

    return frameworks

def check_drift(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    body = data.get('blog_content', '')

    inline_matches = re.findall(
        r'(stages?\s+(?:such as|including|comprise[sd]?)\s+)([^.]+)\.',
        body, re.IGNORECASE
    )

    frameworks = find_frameworks(body)

    print("=== Named framework sections found ===")
    seen = {}
    for heading, stages in frameworks:
        key = normalize(heading)
        print(f"\nHeading: {heading!r}")
        print(f"  Normalized key: {key!r}")
        print(f"  Stages: {stages}")
        if key in seen and seen[key] != stages:
            print("  !! DRIFT: same framework name, DIFFERENT stage list elsewhere !!")
        seen[key] = stages

    print("\n=== Inline stage-list mentions (not under a heading) ===")
    for prefix, stagelist in inline_matches:
        print(f"  '{prefix}{stagelist}.'")
        mentioned_stages = [s.strip() for s in re.split(r',| and ', stagelist) if s.strip()]
        for heading, stages in frameworks:
            named_stage_words = ' '.join(stages).lower()
            overlap = any(m.split()[0].lower() in named_stage_words for m in mentioned_stages if m)
            if not overlap and stages:
                print(f"    !! Possible drift vs '{heading}': inline stages don't match named framework's stages !!")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python check_framework_drift.py <path-to-draft.json>")
        sys.exit(1)
    check_drift(sys.argv[1])
