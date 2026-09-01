# import re
# from dataclasses import dataclass, field
# from typing import List, Optional

# BLOCKQUOTE_RE = re.compile(r"(?m)^\s*>\s+")
# H2_RE = re.compile(r"(?m)^##\s+(.+)$")
# FAQ_Q_RE = re.compile(r"(?m)^\*\*Q:\s*(.+?)\*\*")
# JSONLD_RE = re.compile(r"<script[^>]*application/ld\+json[^>]*>(.*?)</script>", re.DOTALL | re.IGNORECASE)

# GENERIC_PHRASES = [
#     "ever-evolving landscape",
#     "no longer optional",
#     "critical imperative",
#     "critical determinant of success",
#     "future-ready",
#     "game-changing",
#     "transformative",
#     "crucial for sustainable growth",
# ]

# NUMBER_RE = re.compile(
#     r"""
#     (?<!\w)
#     (
#         \d{1,3}(?:,\d{3})+(?:\.\d+)? |
#         \d+\.\d+ |
#         \d+
#     )
#     (?:\s?%|\s?(?:days?|weeks?|months?|years?|hours?|minutes?|seconds?|times?|x|percent|dollars?|USD|INR|Rs\.?|rupees?))?
#     """,
#     re.IGNORECASE | re.VERBOSE,
# )

# @dataclass
# class ValidationResult:
#     ok: bool
#     hard_failures: List[str] = field(default_factory=list)
#     soft_warnings: List[str] = field(default_factory=list)

# def _count_blockquotes(text: str) -> int:
#     return len(BLOCKQUOTE_RE.findall(text))

# def _extract_h2_sections(text: str):
#     parts = re.split(r"(?m)^##\s+", text)
#     if len(parts) <= 1:
#         return []
#     sections = []
#     for part in parts[1:]:
#         lines = part.splitlines()
#         heading = lines[0].strip() if lines else ""
#         body = "\n".join(lines[1:]).strip()
#         sections.append((heading, body))
#     return sections

# def _count_paragraphs(section_body: str) -> int:
#     paras = [p.strip() for p in re.split(r"\n\s*\n", section_body) if p.strip()]
#     return len(paras)

# def _faq_count(text: str) -> int:
#     return len(FAQ_Q_RE.findall(text))

# def _has_jsonld(text: str) -> bool:
#     return bool(JSONLD_RE.findall(text))

# def _find_numbers(text: str) -> List[str]:
#     return [m.group(0) for m in NUMBER_RE.finditer(text)]

# def _generic_phrase_hits(text: str) -> List[str]:
#     t = text.lower()
#     return [p for p in GENERIC_PHRASES if p in t]

# def validate_article(
#     article: str,
#     research_package: str = "",
#     allowed_numbers: Optional[List[str]] = None,
#     require_faq: bool = True,
#     require_jsonld: bool = True,
#     require_one_quote: bool = True,
#     min_paragraphs_per_section: int = 3,
# ) -> ValidationResult:
#     allowed_numbers = allowed_numbers or []
#     failures = []
#     warnings = []

#     blockquote_count = _count_blockquotes(article)
#     if require_one_quote and blockquote_count != 1:
#         failures.append(f"Exactly one markdown blockquote required; found {blockquote_count}.")

#     sections = _extract_h2_sections(article)
#     if not sections:
#         failures.append("No H2 sections found.")
#     else:
#         for heading, body in sections:
#             pcount = _count_paragraphs(body)
#             if pcount < min_paragraphs_per_section:
#                 failures.append(f"H2 section '{heading}' has fewer than {min_paragraphs_per_section} paragraphs.")

#     faq_count = _faq_count(article)
#     if require_faq and faq_count != 5:
#         failures.append(f"FAQ block must contain exactly 5 Q&A pairs; found {faq_count}.")

#     if require_jsonld and not _has_jsonld(article):
#         failures.append("Missing JSON-LD schema block.")

#     generic_hits = _generic_phrase_hits(article)
#     if generic_hits:
#         warnings.append("Generic AI/consulting phrases detected: " + ", ".join(generic_hits))

#     article_numbers = _find_numbers(article)
#     research_numbers = set(_find_numbers(research_package))

#     for n in article_numbers:
#         if n not in research_numbers and n not in allowed_numbers:
#             failures.append(f"Unsupported number in article: {n}")

#     if "enterprise" not in article.lower() and "enterprise ai" not in article.lower():
#         warnings.append("Weak enterprise grounding detected.")

#     ok = len(failures) == 0
#     return ValidationResult(ok=ok, hard_failures=failures, soft_warnings=warnings)

import re
from dataclasses import dataclass, field
from typing import List, Optional

from agents.text_metrics import diagnose_article, find_banned_phrases


BLOCKQUOTE_RE = re.compile(r"(?m)^\s*>\s+")
FAQ_Q_RE = re.compile(r"(?m)^\*\*Q:\s*(.+?)\*\*")
JSONLD_RE = re.compile(
    r"<script[^>]*application/ld\+json[^>]*>(.*?)</script>",
    re.DOTALL | re.IGNORECASE
)

AGENTIC_TERMS = [
    "agentic ai",
    "ai agents",
    "agent",
    "autonomous",
    "orchestration",
    "tool calling",
    "runtime",
    "guardrails",
    "workflow",
    "context",
    "constraints",
    "consequences",
    "production",
    "governance",
    "risk",
    "trust",
]

GENERIC_PHRASES = [
    "ever-evolving landscape",
    "no longer optional",
    "critical imperative",
    "critical determinant of success",
    "future-ready",
    "game-changing",
    "transformative",
    "crucial for sustainable growth",
    "transformative shift",
    "unlock value",
    "rapidly evolving",
    "strategic imperative",
    "business landscape",
    "more important than ever",
]

NUMBER_RE = re.compile(
    r"""
    (?<!\w)
    (
        \d{1,3}(?:,\d{3})+(?:\.\d+)? |
        \d+\.\d+ |
        \d+
    )
    (?:\s?%|\s?(?:days?|weeks?|months?|years?|hours?|minutes?|seconds?|times?|x|percent|dollars?|USD|INR|Rs\.?|rupees?))?
    """,
    re.IGNORECASE | re.VERBOSE,
)


@dataclass
class ValidationResult:
    ok: bool
    hard_failures: List[str] = field(default_factory=list)
    soft_warnings: List[str] = field(default_factory=list)


def _count_blockquotes(text: str) -> int:
    return len(BLOCKQUOTE_RE.findall(text))


def _count_paragraphs(section_body: str) -> int:
    paras = [p.strip() for p in re.split(r"\n\s*\n", section_body) if p.strip()]
    return len(paras)


def _faq_count(text: str) -> int:
    return len(FAQ_Q_RE.findall(text))


def _has_jsonld(text: str) -> bool:
    return bool(JSONLD_RE.findall(text))


def _find_numbers(text: str) -> List[str]:
    return [m.group(0) for m in NUMBER_RE.finditer(text)]


def _generic_phrase_hits(text: str) -> List[str]:
    t = text.lower()
    return [p for p in GENERIC_PHRASES if p in t]


def _has_agentic_scope(text: str) -> bool:
    t = text.lower()
    return "agentic ai" in t or ("agent" in t and "enterprise" in t)


def _has_framework(report) -> bool:
    return bool(report.get("has_framework"))


def _has_case_study(report) -> bool:
    return bool(report.get("has_case_study"))


def _has_tradeoff(report) -> bool:
    return bool(report.get("has_tradeoff"))


def _has_quick_answers_or_faq(text: str) -> bool:
    t = text.lower()
    return "## quick answers" in t or "## faq" in t or "## executive q&a" in t


def _lead_has_direct_answer(report) -> bool:
    return bool(report.get("has_direct_answer_lead"))


def _question_sections_answer_first(report) -> bool:
    if not report.get("has_question_headings"):
        return True
    return True if not report.get("lead_needs_rewrite") else False


def validate_article(
    article: str,
    research_package: str = "",
    allowed_numbers: Optional[List[str]] = None,
    require_faq: bool = False,
    require_jsonld: bool = False,
    require_one_quote: bool = True,
    min_paragraphs_per_section: int = 3,
    require_quick_answers: bool = True,
    require_tradeoff: bool = True,
    require_agentic_only: bool = True,
) -> ValidationResult:
    allowed_numbers = allowed_numbers or []
    failures = []
    warnings = []

    report = diagnose_article(article)

    blockquote_count = _count_blockquotes(article)
    if require_one_quote and blockquote_count != 1:
        failures.append(f"Exactly one markdown blockquote required; found {blockquote_count}.")

    if not report.get("has_direct_answer_lead"):
        failures.append("Missing direct-answer lead under the title.")

    if report.get("has_question_headings") and not report.get("has_direct_answer_lead"):
        failures.append("Question-headed sections must answer first.")

    sections = report.get("sections", [])
    if not sections:
        failures.append("No H2 sections found.")
    else:
        for section in sections:
            heading = section["heading"]
            body = section["body"]
            if not heading:
                continue
            if heading.lower() in {"quick answers", "faq", "executive q&a"}:
                continue
            pcount = _count_paragraphs(body)
            if pcount < min_paragraphs_per_section:
                failures.append(f"H2 section '{heading}' has fewer than {min_paragraphs_per_section} paragraphs.")

    if require_quick_answers and not _has_quick_answers_or_faq(article):
        warnings.append("Missing Quick Answers / FAQ section.")

    if require_faq:
        faq_count = _faq_count(article)
        if faq_count != 5:
            failures.append(f"FAQ block must contain exactly 5 Q&A pairs; found {faq_count}.")

    if require_jsonld and not _has_jsonld(article):
        failures.append("Missing JSON-LD schema block.")

    if require_agentic_only and not _has_agentic_scope(article):
        failures.append("Article is not clearly focused on agentic AI.")

    if not _has_framework(report):
        failures.append("Missing enterprise framework.")

    if not _has_case_study(report):
        failures.append("Missing enterprise case study.")

    if require_tradeoff and not _has_tradeoff(report):
        failures.append("Missing executive trade-off section.")

    generic_hits = _generic_phrase_hits(article)
    if generic_hits:
        warnings.append("Generic AI/consulting phrases detected: " + ", ".join(generic_hits))

    banned_hits = find_banned_phrases(article)
    if banned_hits:
        warnings.append("Banned phrases detected: " + ", ".join(banned_hits))

    article_numbers = _find_numbers(article)
    research_numbers = set(_find_numbers(research_package))

    for n in article_numbers:
        if n not in research_numbers and n not in allowed_numbers:
            failures.append(f"Unsupported number in article: {n}")

    if "enterprise" not in article.lower() and "enterprise ai" not in article.lower():
        warnings.append("Weak enterprise grounding detected.")

    if "luvana" not in article.lower():
        warnings.append("Luvana perspective may be too weak or missing.")

    if report.get("has_duplicate_frameworks"):
        failures.append("Duplicate framework mentions detected.")

    if report.get("has_duplicate_case_studies"):
        failures.append("Duplicate case studies detected.")

    if report.get("conclusion_needs_rewrite"):
        warnings.append("Conclusion appears repetitive or summary-like.")

    if report.get("has_excess_unsourced_examples"):
        failures.append("Too many unsourced example markers detected.")

    if report.get("has_excess_skeleton_repetition"):
        warnings.append("Repeated sentence skeletons detected.")

    if report.get("exceeds_h2_ceiling"):
        failures.append(f"Too many H2 sections; found {report.get('total_h2_count')}.")

    ok = len(failures) == 0
    return ValidationResult(ok=ok, hard_failures=failures, soft_warnings=warnings)