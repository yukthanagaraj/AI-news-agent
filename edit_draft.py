import json
import sys

def main(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    body = data.get('blog_content', '')
    original = body

    # Edit 1: remove the redundant duplicate H3 heading right under the H2
    old1 = "## The Multicloud Security Maturity Framework\n\n### The Multicloud Security Maturity Framework\n\n### Stage 1: Initial Awareness"
    new1 = "## The Multicloud Security Maturity Framework\n\n### Stage 1: Initial Awareness"

    if old1 in body:
        body = body.replace(old1, new1)
        print("Edit 1 applied: removed duplicate heading.")
    else:
        print("Edit 1 SKIPPED: exact text not found (check for whitespace differences).")

    # Edit 2: fix the earlier inline mention that invents a conflicting 4-stage model
    old2 = "Organizations should develop a multicloud security maturity framework that guides their security strategy across varied environments. this framework should comprise stages such as Reactive Measures, Integrated Security Protocols, AI-Driven Adaptation, and Proactive Threat Mitigation."
    new2 = "Organizations should develop a multicloud security maturity framework that guides their security strategy across varied environments, progressing through defined stages as outlined in the Multicloud Security Maturity Framework below."

    if old2 in body:
        body = body.replace(old2, new2)
        print("Edit 2 applied: fixed conflicting inline stage list.")
    else:
        print("Edit 2 SKIPPED: exact text not found (check for whitespace differences).")

    if body != original:
        data['blog_content'] = body
        # also clear the NEEDS REVIEW flag from the title if present
        if data.get('title', '').startswith('[NEEDS REVIEW] '):
            data['title'] = data['title'][len('[NEEDS REVIEW] '):]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\nSaved changes to: {filepath}")
    else:
        print("\nNo changes made to file.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python edit_draft.py <path-to-draft.json>")
        sys.exit(1)
    main(sys.argv[1])
