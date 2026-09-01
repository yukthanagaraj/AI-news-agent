# from agents.llm_client import client, MODEL_NAME
# from agents.text_metrics import (
#     seq_similarity,
#     split_h2_sections,
#     rebuild_from_sections,
#     has_framework,
#     extract_quotes,
#     FRAMEWORK_KEYWORDS,
# )
# from agents.history_manager import (
#     get_used_titles,
#     get_used_section_titles,
#     get_used_frameworks,
#     get_used_opening_styles,
#     get_used_conclusions,
#     get_used_quotes,
#     remember_title,
#     remember_framework,
#     remember_quote,
#     remember_conclusion,
# )

# SIMILARITY_FAIL_THRESHOLD = 0.85
# COMPONENT_FAIL_THRESHOLD = 0.80


# def first_paragraph(article):
#     paragraphs = [p.strip() for p in article.split("\n\n") if p.strip()]
#     return paragraphs[0] if paragraphs else ""


# def last_paragraph(article):
#     paragraphs = [p.strip() for p in article.split("\n\n") if p.strip()]
#     return paragraphs[-1] if paragraphs else ""


# def _max_similarity(candidate, history):
#     if not candidate or not history:
#         return 0.0
#     return max(seq_similarity(candidate, h) for h in history)


# def uniqueness_check(title: str, article: str):
#     sections = split_h2_sections(article)
#     headings = [s["heading"] for s in sections if s["heading"]]

#     framework_heading = has_framework(sections) or ""
#     quotes = extract_quotes(article)
#     quote = quotes[0] if quotes else ""

#     report = {
#         "title_similarity": round(_max_similarity(title, get_used_titles()), 2),
#         "heading_similarity": 0.0,
#         "opening_similarity": round(_max_similarity(first_paragraph(article), get_used_opening_styles()), 2),
#         "framework_similarity": round(_max_similarity(framework_heading, get_used_frameworks()), 2),
#         "conclusion_similarity": round(_max_similarity(last_paragraph(article), get_used_conclusions()), 2),
#         "quote_similarity": round(_max_similarity(quote, get_used_quotes()), 2),
#         "status": "PASS",
#         "weak_components": [],
#     }

#     previous_headings = get_used_section_titles()
#     if headings and previous_headings:
#         scores = [
#             max(seq_similarity(h, prev) for prev in previous_headings)
#             for h in headings
#         ]
#         report["heading_similarity"] = round(sum(scores) / len(scores), 2)

#     report["overall_similarity"] = round(
#         report["title_similarity"] * 0.20 +
#         report["heading_similarity"] * 0.15 +
#         report["opening_similarity"] * 0.15 +
#         report["framework_similarity"] * 0.20 +
#         report["conclusion_similarity"] * 0.15 +
#         report["quote_similarity"] * 0.15,
#         2,
#     )

#     for key in [
#         "title_similarity",
#         "opening_similarity",
#         "framework_similarity",
#         "conclusion_similarity",
#         "quote_similarity",
#     ]:
#         if report[key] >= COMPONENT_FAIL_THRESHOLD:
#             report["weak_components"].append(key.replace("_similarity", ""))

#     if report["overall_similarity"] >= SIMILARITY_FAIL_THRESHOLD or report["weak_components"]:
#         report["status"] = "FAIL"

#     return report


# def _llm_fix(system, user):
#     response = client.chat.completions.create(
#         model=MODEL_NAME,
#         messages=[
#             {"role": "system", "content": system},
#             {"role": "user", "content": user},
#         ],
#     )
#     return response.choices[0].message.content.strip()


# def regenerate_title(thesis_hint, previous_titles):
#     system = (
#         "You write ONE executive article title, exactly 6-8 words, no colon, no quotation marks. "
#         "Return only the title text."
#     )
#     user = (
#         f"Article thesis: {thesis_hint}\n\n"
#         f"Avoid resembling these previous titles:\n" +
#         "\n".join(f"- {t}" for t in previous_titles[-15:])
#     )
#     return _llm_fix(system, user)


# def regenerate_opening(thesis_hint, previous_openings):
#     system = (
#         "You write ONE opening paragraph (60-100 words) for an executive article. "
#         "It must start with the broader enterprise shift, not the company/news event itself. "
#         "Return only the paragraph text."
#     )
#     user = (
#         f"Article thesis: {thesis_hint}\n\n"
#         f"Avoid resembling these previous openings in wording or structure:\n" +
#         "\n".join(f"- {o[:160]}" for o in previous_openings[-10:])
#     )
#     return _llm_fix(system, user)


# def regenerate_quote(thesis, previous_quotes):
#     system = (
#         "You write exactly one short, original executive quote in markdown blockquote form "
#         "(starting with '> '). No company names. One sentence, 12-24 words. Never generic."
#     )
#     user = (
#         f"Article thesis: {thesis}\n\n"
#         f"These quotes were already used -- do not repeat their idea or wording:\n" +
#         "\n".join(f"- {q}" for q in previous_quotes[-15:]) +
#         "\n\nReturn only the new blockquote line."
#     )
#     return _llm_fix(system, user)


# def regenerate_framework_name(thesis, previous_frameworks):
#     system = (
#         "You name one short, memorable enterprise framework (2-5 words, Title Case). "
#         "No explanation, return only the name."
#     )
#     user = (
#         f"Article thesis: {thesis}\n\n"
#         f"These framework names already exist -- the new name must be clearly different in wording and concept:\n" +
#         "\n".join(f"- {f}" for f in previous_frameworks[-20:])
#     )
#     return _llm_fix(system, user)


# def regenerate_conclusion(article_summary, previous_conclusions):
#     system = (
#         "You write ONE closing paragraph (80-120 words) for an executive article. "
#         "It must introduce a new insight (a prediction, a competitive implication, or a leadership observation) "
#         "and must NOT summarize the article."
#     )
#     user = (
#         f"What the article already covered (do not repeat): {article_summary}\n\n"
#         f"Avoid resembling these previous conclusions:\n" +
#         "\n".join(f"- {c[:160]}" for c in previous_conclusions[-10:])
#     )
#     return _llm_fix(system, user)


# def fix_weak_components(title, blog_content, report, thesis_hint):
#     weak = report.get("weak_components", [])
#     sections = split_h2_sections(blog_content)

#     if "title" in weak:
#         new_title = regenerate_title(thesis_hint, get_used_titles())
#         title = new_title.strip().strip('"')
#         remember_title(title)

#     if "opening" in weak:
#         new_opening = regenerate_opening(thesis_hint, get_used_opening_styles())
#         old_opening = first_paragraph(blog_content)
#         blog_content = blog_content.replace(old_opening, new_opening, 1)
#         sections = split_h2_sections(blog_content)

#     if "framework" in weak:
#         framework_heading = None
#         for s in sections:
#             if s["heading"] and any(k in s["heading"].lower() for k in FRAMEWORK_KEYWORDS):
#                 framework_heading = s["heading"]
#                 break
#         if framework_heading:
#             new_name = regenerate_framework_name(thesis_hint, get_used_frameworks())
#             for s in sections:
#                 if s["heading"] == framework_heading:
#                     s["heading"] = new_name
#                     break
#             remember_framework(new_name)

#     if "quote" in weak:
#         blog_content = rebuild_from_sections(sections)
#         quotes = extract_quotes(blog_content)
#         old_quote_line = f"> {quotes[0]}" if quotes else None
#         new_quote = regenerate_quote(thesis_hint, get_used_quotes())
#         new_line = new_quote if new_quote.startswith(">") else f"> {new_quote}"
#         if old_quote_line and old_quote_line in blog_content:
#             blog_content = blog_content.replace(old_quote_line, new_line, 1)
#         else:
#             blog_content += f"\n\n{new_line}"
#         remember_quote(new_quote)
#         sections = split_h2_sections(blog_content)

#     if "conclusion" in weak:
#         real = [s for s in sections if s["heading"]]
#         if real:
#             covered = "; ".join(s["heading"] for s in real[:-1])
#             new_conclusion = regenerate_conclusion(covered, get_used_conclusions())
#             real[-1]["body"] = new_conclusion
#             remember_conclusion(new_conclusion)

#     blog_content = rebuild_from_sections(sections)
#     return title, blog_content


# if __name__ == "__main__":
#     sample_title = "Beyond Automation Toward Autonomous Decisions"
#     sample_article = """
# ## Governance Challenge

# Enterprise AI governance is becoming essential.

# ## Governance Roadmap

# Organizations need better oversight.

# ## Executive Conclusion

# Competitive advantage will depend on governance.
# """
#     print(uniqueness_check(sample_title, sample_article))

from agents.llm_client import client, MODEL_NAME
from agents.text_metrics import (
    seq_similarity,
    split_h2_sections,
    rebuild_from_sections,
    has_framework,
    extract_quotes,
    FRAMEWORK_KEYWORDS,
    diagnose_article,
)
from agents.history_manager import (
    get_used_titles,
    get_used_section_titles,
    get_used_frameworks,
    get_used_opening_styles,
    get_used_conclusions,
    get_used_quotes,
    remember_title,
    remember_framework,
    remember_quote,
    remember_conclusion,
)

SIMILARITY_FAIL_THRESHOLD = 0.85
COMPONENT_FAIL_THRESHOLD = 0.80


def first_paragraph(article):
    paragraphs = [p.strip() for p in article.split("\n\n") if p.strip()]
    return paragraphs[0] if paragraphs else ""


def last_paragraph(article):
    paragraphs = [p.strip() for p in article.split("\n\n") if p.strip()]
    return paragraphs[-1] if paragraphs else ""


def _max_similarity(candidate, history):
    if not candidate or not history:
        return 0.0
    return max(seq_similarity(candidate, h) for h in history)


def uniqueness_check(title: str, article: str):
    sections = split_h2_sections(article)
    headings = [s["heading"] for s in sections if s["heading"]]
    report = diagnose_article(article)

    framework_heading = has_framework(sections) or ""
    quotes = extract_quotes(article)
    quote = quotes[0] if quotes else ""

    report_out = {
        "title_similarity": round(_max_similarity(title, get_used_titles()), 2),
        "heading_similarity": 0.0,
        "opening_similarity": round(_max_similarity(first_paragraph(article), get_used_opening_styles()), 2),
        "framework_similarity": round(_max_similarity(framework_heading, get_used_frameworks()), 2),
        "conclusion_similarity": round(_max_similarity(last_paragraph(article), get_used_conclusions()), 2),
        "quote_similarity": round(_max_similarity(quote, get_used_quotes()), 2),
        "lead_similarity": 0.0,
        "status": "PASS",
        "weak_components": [],
    }

    previous_headings = get_used_section_titles()
    if headings and previous_headings:
        scores = [
            max(seq_similarity(h, prev) for prev in previous_headings)
            for h in headings
        ]
        report_out["heading_similarity"] = round(sum(scores) / len(scores), 2)

    lead = report["sections"][0]["body"] if report.get("sections") else ""
    if lead:
        report_out["lead_similarity"] = round(_max_similarity(lead, get_used_opening_styles()), 2)

    report_out["overall_similarity"] = round(
        report_out["title_similarity"] * 0.18 +
        report_out["heading_similarity"] * 0.14 +
        report_out["opening_similarity"] * 0.14 +
        report_out["lead_similarity"] * 0.14 +
        report_out["framework_similarity"] * 0.16 +
        report_out["conclusion_similarity"] * 0.14 +
        report_out["quote_similarity"] * 0.10,
        2,
    )

    for key in [
        "title_similarity",
        "opening_similarity",
        "lead_similarity",
        "framework_similarity",
        "conclusion_similarity",
        "quote_similarity",
    ]:
        if report_out[key] >= COMPONENT_FAIL_THRESHOLD:
            report_out["weak_components"].append(key.replace("_similarity", ""))

    if report_out["overall_similarity"] >= SIMILARITY_FAIL_THRESHOLD or report_out["weak_components"]:
        report_out["status"] = "FAIL"

    return report_out


def _llm_fix(system, user):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return response.choices[0].message.content.strip()


def regenerate_title(thesis_hint, previous_titles):
    system = (
        "You write one premium enterprise article title in a Luvana editorial voice. "
        "Keep it specific, agentic-AI focused, and distinct from the previous titles. "
        "Use 6-10 words. No colon. No quotation marks. Return only the title."
    )
    user = (
        f"Article thesis: {thesis_hint}\n\n"
        f"Avoid resembling these previous titles:\n" +
        "\n".join(f"- {t}" for t in previous_titles[-15:])
    )
    return _llm_fix(system, user)


def regenerate_opening(thesis_hint, previous_openings):
    system = (
        "You write one opening paragraph (60-110 words) for a Luvana enterprise article. "
        "It must open with the strategic shift, not the company or event. "
        "The tone should be opinionated, executive, and specific to agentic AI. "
        "Avoid generic AI prose. Return only the paragraph."
    )
    user = (
        f"Article thesis: {thesis_hint}\n\n"
        f"Avoid resembling these previous openings in wording or structure:\n" +
        "\n".join(f"- {o[:180]}" for o in previous_openings[-10:])
    )
    return _llm_fix(system, user)


def regenerate_quote(thesis, previous_quotes):
    system = (
        "You write one short, original executive quote in markdown blockquote form "
        "(starting with '> '). No company names. One sentence. 12-22 words. "
        "It must sound like a Luvana editorial line, not a slogan."
    )
    user = (
        f"Article thesis: {thesis}\n\n"
        f"These quotes were already used -- do not repeat their idea or wording:\n" +
        "\n".join(f"- {q}" for q in previous_quotes[-15:]) +
        "\n\nReturn only the new blockquote line."
    )
    return _llm_fix(system, user)


def regenerate_framework_name(thesis, previous_frameworks):
    system = (
        "You name one short, memorable enterprise framework in Title Case. "
        "Keep it tied to agentic AI and the article thesis. "
        "Use 2-5 words. No explanation. Return only the name."
    )
    user = (
        f"Article thesis: {thesis}\n\n"
        f"These framework names already exist -- the new name must be clearly different in wording and concept:\n" +
        "\n".join(f"- {f}" for f in previous_frameworks[-20:])
    )
    return _llm_fix(system, user)


def regenerate_conclusion(article_summary, previous_conclusions):
    system = (
        "You write one closing paragraph (80-130 words) for a Luvana enterprise article. "
        "It must introduce a new insight such as a prediction, competitive implication, or leadership observation. "
        "Do not summarize the article. Keep it decisive, specific, and executive-oriented. "
        "End with a complete sentence."
    )
    user = (
        f"Sections already covered in this article: {article_summary}\n\n"
        f"Avoid resembling these previous conclusions in wording or structure:\n" +
        "\n".join(f"- {c[:180]}" for c in previous_conclusions[-10:])
    )
    return _llm_fix(system, user)


def regenerate_thesis(context_hint, previous_theses):
    """Used by insight_agent.py when a freshly generated brief's thesis is
    too similar to a recently used one. Must produce a genuinely different
    angle, not a reworded version of the same idea."""
    system = (
        "You write one executive-level thesis paragraph (3-5 sentences) for a premium enterprise AI publication. "
        "It must state a specific, opinionated point of view about an enterprise transformation -- not a generic "
        "AI observation and not a restatement of the news. It must be conceptually distinct from the previous "
        "theses listed below, not just reworded with different vocabulary. Return only the thesis paragraph."
    )
    user = (
        f"Context to stay grounded in (topic/research summary):\n{context_hint}\n\n"
        f"These theses were already used -- the new thesis must take a genuinely different angle or claim:\n" +
        "\n".join(f"- {t[:220]}" for t in previous_theses[-15:])
    )
    return _llm_fix(system, user)


def fix_weak_components(title, blog_content, report, thesis_hint):
    weak = report.get("weak_components", [])
    sections = split_h2_sections(blog_content)

    if "title" in weak:
        new_title = regenerate_title(thesis_hint, get_used_titles())
        title = new_title.strip().strip('"')
        remember_title(title)

    if "opening" in weak:
        new_opening = regenerate_opening(thesis_hint, get_used_opening_styles())
        old_opening = first_paragraph(blog_content)
        blog_content = blog_content.replace(old_opening, new_opening, 1)
        sections = split_h2_sections(blog_content)

    if "framework" in weak:
        framework_heading = None
        for s in sections:
            if s["heading"] and any(k in s["heading"].lower() for k in FRAMEWORK_KEYWORDS):
                framework_heading = s["heading"]
                break
        if framework_heading:
            new_name = regenerate_framework_name(thesis_hint, get_used_frameworks())
            for s in sections:
                if s["heading"] == framework_heading:
                    s["heading"] = new_name
                    break
            remember_framework(new_name)

    if "quote" in weak:
        blog_content = rebuild_from_sections(sections)
        quotes = extract_quotes(blog_content)
        old_quote_line = f"> {quotes[0]}" if quotes else None
        new_quote = regenerate_quote(thesis_hint, get_used_quotes())
        new_line = new_quote if new_quote.startswith(">") else f"> {new_quote}"
        if old_quote_line and old_quote_line in blog_content:
            blog_content = blog_content.replace(old_quote_line, new_line, 1)
        else:
            blog_content += f"\n\n{new_line}"
        remember_quote(new_quote)
        sections = split_h2_sections(blog_content)

    if "conclusion" in weak:
        real = [s for s in sections if s["heading"]]
        if real:
            covered = "; ".join(s["heading"] for s in real[:-1])
            new_conclusion = regenerate_conclusion(covered, get_used_conclusions())
            real[-1]["body"] = new_conclusion
            remember_conclusion(new_conclusion)

    blog_content = rebuild_from_sections(sections)
    return title, blog_content