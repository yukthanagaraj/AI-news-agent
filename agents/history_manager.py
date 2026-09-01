# import json
# from pathlib import Path


# BASE_DIR = Path(__file__).resolve().parent.parent

# MEMORY_DIR = BASE_DIR / "memory"


# def load_memory(filename):

#     MEMORY_DIR.mkdir(exist_ok=True)

#     path = MEMORY_DIR / filename

#     if not path.exists():
#         return []

#     try:
#         with open(path, "r", encoding="utf-8") as f:
#             return json.load(f)

#     except Exception:
#         return []


# def save_memory(filename, data):

#     MEMORY_DIR.mkdir(exist_ok=True)

#     path = MEMORY_DIR / filename

#     with open(path, "w", encoding="utf-8") as f:
#         json.dump(
#             data,
#             f,
#             indent=2,
#             ensure_ascii=False
#         )


# def get_used_titles():
#     return load_memory("used_titles.json")


# def get_used_quotes():
#     return load_memory("used_quotes.json")


# def get_used_frameworks():
#     return load_memory("used_frameworks.json")


# def get_used_section_titles():
#     return load_memory("used_section_titles.json")


# def get_used_visual_concepts():
#     return load_memory("used_visual_concepts.json")


# def get_used_categories():
#     return load_memory("used_categories.json")

# def get_used_companies():
#     return load_memory("used_companies.json")


# def get_used_examples():
#     return load_memory("used_examples.json")


# def get_used_case_studies():
#     return load_memory("used_case_studies.json")


# def get_used_technologies():
#     return load_memory("used_technologies.json")

# def get_used_topics():
#     return load_memory("used_topics.json")


# def get_used_industries():
#     return load_memory("used_industries.json")


# def get_used_archetypes():
#     return load_memory("used_archetypes.json")


# def get_used_executive_audiences():
#     return load_memory("used_executive_audiences.json")


# def get_used_business_maturity():
#     return load_memory("used_business_maturity.json")


# def get_used_strategic_themes():
#     return load_memory("used_strategic_themes.json")


# def get_used_opening_styles():
#     return load_memory("used_opening_styles.json")


# def get_used_conclusions():
#     return load_memory("used_conclusions.json")

# def remember_title(title):

#     titles = get_used_titles()

#     if title not in titles:

#         titles.append(title)

#         save_memory(
#             "used_titles.json",
#             titles[-200:]
#         )


# def remember_quote(quote):

#     quotes = get_used_quotes()

#     if quote not in quotes:

#         quotes.append(quote)

#         save_memory(
#             "used_quotes.json",
#             quotes[-200:]
#         )


# def remember_framework(framework):

#     frameworks = get_used_frameworks()

#     if framework not in frameworks:

#         frameworks.append(framework)

#         save_memory(
#             "used_frameworks.json",
#             frameworks[-200:]
#         )


# def remember_section_title(section_title):

#     section_titles = get_used_section_titles()

#     if section_title not in section_titles:

#         section_titles.append(section_title)

#         save_memory(
#             "used_section_titles.json",
#             section_titles[-200:]
#         )


# def remember_visual_concept(concept):

#     visual_concepts = get_used_visual_concepts()

#     if concept not in visual_concepts:

#         visual_concepts.append(concept)

#         save_memory(
#             "used_visual_concepts.json",
#             visual_concepts[-100:]
#         )


# def remember_category(category):

#     categories = get_used_categories()

#     if category not in categories:

#         categories.append(category)

#         save_memory(
#             "used_categories.json",
#             categories[-50:]
#         )

# def remember_company(company):

#     companies = get_used_companies()

#     if company not in companies:

#         companies.append(company)

#         save_memory(
#             "used_companies.json",
#             companies[-200:]
#         )


# def remember_example(example):

#     examples = get_used_examples()

#     if example not in examples:

#         examples.append(example)

#         save_memory(
#             "used_examples.json",
#             examples[-200:]
#         )


# def remember_case_study(case):

#     cases = get_used_case_studies()

#     if case not in cases:

#         cases.append(case)

#         save_memory(
#             "used_case_studies.json",
#             cases[-100:]
#         )


# def remember_technology(technology):

#     technologies = get_used_technologies()

#     if technology not in technologies:

#         technologies.append(technology)

#         save_memory(
#             "used_technologies.json",
#             technologies[-150:]
#         )    

# def remember_topic(topic):

#     topics = get_used_topics()

#     if topic not in topics:

#         topics.append(topic)

#         save_memory(
#             "used_topics.json",
#             topics[-100:]
#         )


# def remember_industry(industry):

#     industries = get_used_industries()

#     if industry not in industries:

#         industries.append(industry)

#         save_memory(
#             "used_industries.json",
#             industries[-100:]
#         )


# def remember_archetype(archetype):

#     archetypes = get_used_archetypes()

#     if archetype not in archetypes:

#         archetypes.append(archetype)

#         save_memory(
#             "used_archetypes.json",
#             archetypes[-100:]
#         )


# def remember_executive_audience(audience):

#     audiences = get_used_executive_audiences()

#     if audience not in audiences:

#         audiences.append(audience)

#         save_memory(
#             "used_executive_audiences.json",
#             audiences[-100:]
#         )


# def remember_business_maturity(level):

#     maturity = get_used_business_maturity()

#     if level not in maturity:

#         maturity.append(level)

#         save_memory(
#             "used_business_maturity.json",
#             maturity[-50:]
#         )


# def remember_strategic_theme(theme):

#     themes = get_used_strategic_themes()

#     if theme not in themes:

#         themes.append(theme)

#         save_memory(
#             "used_strategic_themes.json",
#             themes[-100:]
#         )


# def remember_opening_style(style):

#     styles = get_used_opening_styles()

#     if style not in styles:

#         styles.append(style)

#         save_memory(
#             "used_opening_styles.json",
#             styles[-100:]
#         )


# def remember_conclusion(conclusion):

#     conclusions = get_used_conclusions()

#     if conclusion not in conclusions:

#         conclusions.append(conclusion)

#         save_memory(
#             "used_conclusions.json",
#             conclusions[-100:]
#         )   

# def get_used_clusters(limit=None):
#     clusters = load_memory("used_clusters.json")

#     if limit:
#         return clusters[-limit:]

#     return clusters

# def remember_cluster(cluster):

#     clusters = get_used_clusters()

#     if cluster not in clusters:

#         clusters.append(cluster)

#         save_memory(
#             "used_clusters.json",
#             clusters[-100:]
#         )

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
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def save_memory(filename, data):
    MEMORY_DIR.mkdir(exist_ok=True)
    path = MEMORY_DIR / filename

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


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


def get_used_companies():
    return load_memory("used_companies.json")


def get_used_examples():
    return load_memory("used_examples.json")


def get_used_case_studies():
    return load_memory("used_case_studies.json")


def get_used_technologies():
    return load_memory("used_technologies.json")


def get_used_topics():
    return load_memory("used_topics.json")


def get_used_industries():
    return load_memory("used_industries.json")


def get_used_archetypes():
    return load_memory("used_archetypes.json")


def get_used_executive_audiences():
    return load_memory("used_executive_audiences.json")


def get_used_business_maturity():
    return load_memory("used_business_maturity.json")


def get_used_strategic_themes():
    return load_memory("used_strategic_themes.json")


def get_used_opening_styles():
    return load_memory("used_opening_styles.json")


def get_used_conclusions():
    return load_memory("used_conclusions.json")


def get_used_theses():
    return load_memory("used_theses.json")


def get_used_clusters(limit=None):
    clusters = load_memory("used_clusters.json")
    if limit:
        return clusters[-limit:]
    return clusters


def remember_title(title):
    titles = get_used_titles()
    if title not in titles:
        titles.append(title)
        save_memory("used_titles.json", titles[-200:])


def remember_quote(quote):
    quotes = get_used_quotes()
    if quote not in quotes:
        quotes.append(quote)
        save_memory("used_quotes.json", quotes[-200:])


def remember_framework(framework):
    frameworks = get_used_frameworks()
    if framework not in frameworks:
        frameworks.append(framework)
        save_memory("used_frameworks.json", frameworks[-200:])


def remember_section_title(section_title):
    section_titles = get_used_section_titles()
    if section_title not in section_titles:
        section_titles.append(section_title)
        save_memory("used_section_titles.json", section_titles[-200:])


def remember_visual_concept(concept):
    visual_concepts = get_used_visual_concepts()
    if concept not in visual_concepts:
        visual_concepts.append(concept)
        save_memory("used_visual_concepts.json", visual_concepts[-100:])


def remember_category(category):
    categories = get_used_categories()
    if category not in categories:
        categories.append(category)
        save_memory("used_categories.json", categories[-50:])


def remember_company(company):
    companies = get_used_companies()
    if company not in companies:
        companies.append(company)
        save_memory("used_companies.json", companies[-200:])


def remember_example(example):
    examples = get_used_examples()
    if example not in examples:
        examples.append(example)
        save_memory("used_examples.json", examples[-200:])


def remember_case_study(case):
    cases = get_used_case_studies()
    if case not in cases:
        cases.append(case)
        save_memory("used_case_studies.json", cases[-100:])


def remember_technology(technology):
    technologies = get_used_technologies()
    if technology not in technologies:
        technologies.append(technology)
        save_memory("used_technologies.json", technologies[-150:])


def remember_topic(topic):
    topics = get_used_topics()
    if topic not in topics:
        topics.append(topic)
        save_memory("used_topics.json", topics[-100:])


def remember_industry(industry):
    industries = get_used_industries()
    if industry not in industries:
        industries.append(industry)
        save_memory("used_industries.json", industries[-100:])


def remember_archetype(archetype):
    archetypes = get_used_archetypes()
    if archetype not in archetypes:
        archetypes.append(archetype)
        save_memory("used_archetypes.json", archetypes[-100:])


def remember_executive_audience(audience):
    audiences = get_used_executive_audiences()
    if audience not in audiences:
        audiences.append(audience)
        save_memory("used_executive_audiences.json", audiences[-100:])


def remember_business_maturity(level):
    maturity = get_used_business_maturity()
    if level not in maturity:
        maturity.append(level)
        save_memory("used_business_maturity.json", maturity[-50:])


def remember_strategic_theme(theme):
    themes = get_used_strategic_themes()
    if theme not in themes:
        themes.append(theme)
        save_memory("used_strategic_themes.json", themes[-100:])


def remember_opening_style(style):
    styles = get_used_opening_styles()
    if style not in styles:
        styles.append(style)
        save_memory("used_opening_styles.json", styles[-100:])


def remember_conclusion(conclusion):
    conclusions = get_used_conclusions()
    if conclusion not in conclusions:
        conclusions.append(conclusion)
        save_memory("used_conclusions.json", conclusions[-100:])


def remember_thesis(thesis):
    theses = get_used_theses()
    if thesis not in theses:
        theses.append(thesis)
        save_memory("used_theses.json", theses[-200:])


def remember_cluster(cluster):
    clusters = get_used_clusters()
    if cluster not in clusters:
        clusters.append(cluster)
        save_memory("used_clusters.json", clusters[-100:])