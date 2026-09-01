from datetime import datetime
import os
import re
from agents.research_agent import fetch_ai_news
from agents.writer_agent import generate_blog
from agents.editor_agent import improve_article, apply_targeted_revision
from agents.image_agent import generate_image
from agents.seo_agent import generate_seo
from agents.aeo_agent import generate_aeo
from agents.quality_agent import (
    quality_check,
    extract_gating_score,
    extract_improvement_suggestions,
    QUALITY_THRESHOLD,
)
from agents.sheets_agent import save_blog, get_sheet
from agents.rss_generator import generate_rss
from agents.sitemap_generator import generate_sitemap
from agents.history_manager import (
    remember_title,
    remember_opening_style,
    remember_conclusion
)
from agents.insight_agent import generate_insight
from agents.uniqueness_agent import uniqueness_check, fix_weak_components
from agents.text_metrics import diagnose_article, strip_leaked_meta_lines, H2_CEILING, rebuild_from_sections
from openai import RateLimitError
from agents.text_metrics import ensure_single_quote
from agents.history_manager import get_used_quotes
from agents.draft_manager import save_draft
from agents.text_metrics import ensure_single_quote, autofix_banned_phrases, autofix_structural_phrases
DAILY_TOKEN_BUDGET_WARNING = 85000
_session_token_estimate = 0

ENABLE_IMAGE_GENERATION = os.getenv("ENABLE_IMAGE_GENERATION", "true").lower() == "true"
FALLBACK_IMAGE_URL = "https://images.unsplash.com/photo-1677442136019-21780ecad995"

EMPTY_HEADER_SKELETON_RE = re.compile(
    r"^\s*Title:\s*\n"
    r"Subtitle:\s*\n"
    r"Source URL:\s*\n"
    r"Image Prompt:\s*\n"
    r"Blog:\s*\n+",
)


def _track_tokens(n):
    global _session_token_estimate
    _session_token_estimate += n
    if _session_token_estimate > DAILY_TOKEN_BUDGET_WARNING:
        print(f"\n⚠ WARNING: estimated {_session_token_estimate} tokens used this run — approaching your OpenAI usage limit.\n")

def get_previous_titles():

    try:

        s = get_sheet()

        records = s.col_values(2)

        titles = [
            t for t in records[1:]
            if t.strip()
        ] if len(records) > 1 else []

        return titles[-20:]

    except Exception as e:

        print(
            f"Warning: Could not fetch previous titles: {e}"
        )

        return []


def get_previous_urls():

    try:

        s = get_sheet()

        records = s.col_values(5)

        urls = [
            u for u in records[1:]
            if u.strip()
        ] if len(records) > 1 else []

        return urls[-50:]

    except Exception as e:

        print(
            f"Warning: Could not fetch previous urls: {e}"
        )

        return []


def get_previous_sources():
    return []

def parse_research_source_url(news_text):

    for line in news_text.split("\n"):

        line = line.strip()

        if line.startswith("Source URL:"):

            return line.replace(
                "Source URL:",
                ""
            ).strip()

    return ""

def log(step):
    print(f"\n{'=' * 70}")
    print(step)
    print(f"{'=' * 70}")

def extract_overall_score(report):
    """Informational only -- the /100 self-reported overall score.
    Not used for the publish/revise decision; see extract_gating_score()
    in quality_agent.py for that."""

    match = re.search(r"Overall Score:\s*(\d+)", report)

    if match:
        return int(match.group(1))

    return 0


def first_paragraph(text):
    """Return the first non-empty paragraph of a blog_content string."""

    parts = [
        p for p in text.split("\n\n")
        if p.strip()
    ]

    return parts[0] if parts else ""


def _strip_empty_header_skeleton(blog):
    while True:
        m = EMPTY_HEADER_SKELETON_RE.match(blog)
        if not m:
            break
        blog = blog[m.end():]
    return blog

def _parse_blog_only(blog_or_content):
    """Best-effort extraction of just the blog body, whether given raw
    'Title: / Blog:' text or already-parsed blog_content."""
    if "Blog:" in blog_or_content:
        try:
            _, _, _, _, content = parse_blog_metadata(blog_or_content)
            return content
        except Exception:
            return blog_or_content
    return blog_or_content

def parse_blog_metadata(blog):
    """Extract title, subtitle, source_url, image_prompt, and blog_content from
    the writer/editor agent's raw text output."""

    blog = _strip_empty_header_skeleton(blog)

    title = ""
    subtitle = ""
    image_prompt = ""
    source_url = ""

    lines = blog.split("\n")

    capture_blog = False
    metadata_done = False

    blog_lines = []

    def _demark(s):
        # Tolerate bold-markdown header lines like "**Title:**" in
        # addition to plain "Title:" -- the writer/editor LLM emits
        # either format inconsistently.
        return re.sub(r"\*{1,2}", "", s).strip()

    for line in lines:

        stripped = line.strip()
        match_line = _demark(stripped)

        if capture_blog and (
            match_line.startswith("Title:")
            or match_line.startswith("Subtitle:")
            or match_line.startswith("Source URL:")
            or match_line.startswith("Image Prompt:")
        ):
            break

        if capture_blog:

            blog_lines.append(
                stripped
            )

            continue

        elif match_line.startswith("Title:"):

            title = match_line.replace(
                "Title:",
                ""
            ).strip()
        elif match_line.startswith("Subtitle:"):
            subtitle = match_line.replace(
                "Subtitle:",
                ""
            ).strip()
        elif match_line.startswith("Source URL:"):
            source_url = match_line.replace(
                "Source URL:",
                ""
            ).strip()
        elif match_line.startswith("Image Prompt:"):
            image_prompt = match_line.replace(
                "Image Prompt:",
                ""
            ).strip()
            metadata_done = True
        elif match_line.startswith("Blog:"):
            blog_inline = match_line.replace(
                "Blog:",
                ""
            ).strip()
            if blog_inline:
                blog_lines.append(
                    blog_inline
                )
            capture_blog = True
        elif metadata_done and stripped:
            capture_blog = True
            blog_lines.append(
                stripped
            )

    blog_content = "\n\n".join(
        [
            line
            for line in blog_lines
            if line.strip()
        ]
    ).strip()

    blog_content = strip_leaked_meta_lines(blog_content)

    print("\n========== PARSED OUTPUT ==========\n")
    print("TITLE:", title)
    print("SUBTITLE:", subtitle)
    print("SOURCE URL:", source_url)
    print("IMAGE PROMPT:", image_prompt)
    print("BLOG PREVIEW:\n")
    print(blog_content[:500])
    print("\n===================================\n")

    if not blog_content.strip():

        raise ValueError(
            "Editor output parsing failed. Blog content is empty."
        )

    return title, subtitle, source_url, image_prompt, blog_content


def check_hard_structural_gate(blog_content):
    """
    Deterministic, non-negotiable checks. Runs BEFORE SEO/AEO/quality
    generation so a structurally broken article is caught before
    burning tokens on metadata nobody will use.
    """
    report = diagnose_article(blog_content)
    reasons = []

    if report["has_duplicate_frameworks"]:
        frameworks_found = report.get("all_framework_headings", []) + report.get("named_framework_mentions", [])
        reasons.append(
            f"Duplicate frameworks still present: {frameworks_found}"
        )

    if report["has_duplicate_case_studies"]:
        reasons.append(
            f"Duplicate case studies still present: {report['all_case_study_headings']}"
        )

    if report["exceeds_h2_ceiling"]:
        reasons.append(
            f"Article has {report['total_h2_count']} H2 sections (ceiling is {H2_CEILING})."
        )

    if report["takeaways_needs_bullet_fix"]:
        reasons.append("Key Takeaways is not formatted as 5 bullet points.")

    if report["quote_count"] != 1:
        reasons.append(
            f"Article has {report['quote_count']} blockquotes (must be exactly 1)."
        )

    if report["banned_phrases"]:
        reasons.append(
            f"Banned generic phrases found: {report['banned_phrases']}"
        )

    if report["has_excess_unsourced_examples"]:
        reasons.append(
            f"Too many unsourced example patterns found "
            f"({len(report['unsourced_example_markers'])}): "
            f"{report['unsourced_example_markers']}"
        )

    if report["has_repeated_closers"]:
        reasons.append(
        "Three or more sections end on the same rhetorical closer "
        "(e.g. repeated 'winners vs laggards' formula)."
    )

    if not report["conclusion_ends_cleanly"]:
        reasons.append(
            "Conclusion ends on a dangling/incomplete fragment rather than a full sentence."
        )

    if len(report["ai_filler_transitions"]) >= 3:
        reasons.append(
            f"Excessive AI-prose filler transitions found: {report['ai_filler_transitions']}"
        )

    if report["has_excess_skeleton_repetition"]:
        reasons.append(
            f"Same sentence template repeated {len(report['repeated_sentence_skeletons'])}x "
            f"across sections: {report['repeated_sentence_skeletons']}"
        )

    return (len(reasons) == 0, reasons)


def _run_pipeline_inner():

    log("FETCHING PREVIOUS TITLES")

    previous_titles = get_previous_titles()
    previous_sources = get_previous_sources()
    previous_urls = get_previous_urls()

    print(
        f"Found {len(previous_titles)} previous titles"
    )

    log("FETCHING NEWS")

    news, related_sources = fetch_ai_news(
        previous_titles,
        previous_sources,
        previous_urls
    )

    if not news:

        print("No suitable news article found")

        return

    print("=" * 80)
    print("NEWS SENT TO WRITER")
    print(news[:1500])
    print("=" * 80)

    print("RELATED SOURCES FOUND:", len(related_sources))
    for rs in related_sources:
        print(f"  - {rs['source']}: {rs['url']}")

    research_source_url = parse_research_source_url(
        news
    )

    log("WRITING ARTICLE")

    print("Generating editorial insight...")

    insight = generate_insight(news)

    print("\n========== INSIGHT ==========\n")
    print(insight)
    print("\n=============================\n")
    blog = generate_blog(
        news,
        insight,
        previous_titles
    )

    if not blog:

        print(
            "ERROR: Writer Agent returned empty response"
        )

        return

    log("EDITOR REVIEW")
    writer_blog = blog

    try:

        blog = improve_article(writer_blog)

        print("EDITOR AGENT COMPLETE")

    except Exception as e:

        import traceback

        print("EDITOR AGENT FAILED:")
        traceback.print_exc()

        print("Using Writer Agent output with minimal structural safety net.")

        # The except-path previously fell back to the completely unedited
        # writer draft with ZERO structural enforcement -- this is how an
        # 8-H2-section article reached the hard gate. At minimum, enforce
        # the H2 ceiling deterministically before this draft goes anywhere
        # near save_draft() / check_hard_structural_gate().
        from agents.editor_agent import _enforce_h2_ceiling

        fallback_report = diagnose_article(writer_blog)
        if fallback_report["exceeds_h2_ceiling"]:
            print(
                f"Writer draft has {fallback_report['total_h2_count']} H2 sections "
                f"(ceiling is {H2_CEILING}). Applying deterministic merge before fallback."
            )
            safe_sections = _enforce_h2_ceiling(fallback_report["sections"], ceiling=H2_CEILING)
            writer_blog = rebuild_from_sections(safe_sections)

        blog = writer_blog

        print("\n========== EDITOR OUTPUT ==========\n")
    print(blog)
    print("\n===================================\n")

    # DEBUG: show the header that parse_blog_metadata will see
    print("DEBUG: RAW BLOG HEADER (first 20 lines)")
    print("\n".join(blog.split("\n")[:20]))

    current_date = datetime.now().strftime(
        "%Y-%m-%d"
    )

    title, subtitle, source_url, image_prompt, blog_content = parse_blog_metadata(blog)
    blog_content = ensure_single_quote(blog_content, used_quotes=get_used_quotes())
    blog_content = autofix_banned_phrases(blog_content)
    blog_content = autofix_structural_phrases(blog_content)
    if not title.strip():
       raise ValueError("Title parsing failed.")

    if not source_url.strip():
       print("Warning: Source URL missing. Will use research URL.")

    if not image_prompt.strip():
       print("Warning: Image prompt missing. Using fallback.")

    if not image_prompt.strip():

        print("Image prompt missing. Generating fallback...")

        image_prompt = (
            f"Editorial illustration of {title}, "
            "showing enterprise executives collaborating with AI agents, "
            "digital workflows, operational dashboards, "
            "modern corporate environment, blue and orange color palette, "
            "minimalist isometric style, premium technology magazine artwork, "
            "no text."
        )

    print()
    print("BLOG CONTENT")
    print("--------------------------------")
    print(blog_content)
    print("--------------------------------")
    print()

    save_draft(
        title=title,
        subtitle=subtitle,
        blog_content=blog_content,
        image_prompt=image_prompt,
        source_url=source_url,
        related_sources=related_sources,
    )

    log("HARD STRUCTURAL GATE")

    gate_passed, gate_reasons = check_hard_structural_gate(blog_content)

    if not gate_passed:

        print("\n" + "!" * 70)
        print("HARD GATE FAILED — ARTICLE WILL NOT BE PUBLISHED")
        print("!" * 70)
        for reason in gate_reasons:
            print(f"  - {reason}")
        print(
            "\nThe fully-written article is already saved to /drafts "
            "(from the save_draft() call earlier in this run). Review "
            "and fix manually, or fix the underlying prompt/editor rule "
            "that let this pattern through, then re-run the pipeline.\n"
        )

        save_draft(
            title=f"[NEEDS REVIEW] {title}",
            subtitle=subtitle,
            blog_content=blog_content,
            image_prompt=image_prompt,
            source_url=source_url,
            related_sources=related_sources,
        )

        return

    print("Hard structural gate PASSED. Proceeding to SEO/AEO/quality generation.")

    log("SEO GENERATION")

    seo_data = generate_seo(
        title,
        blog_content
    )

    print(seo_data)

    log("AEO GENERATION")

    aeo_data = generate_aeo(
        title,
        blog_content,
        source_url=source_url,
        published_date=current_date,
    )

    print(aeo_data)

    log("QUALITY REVIEW")

    combined_content = (
        blog_content
        + "\n\n"
        + seo_data
        + "\n\n"
        + aeo_data
      )

    MAX_RETRY = 1

    quality_passed = False

    for attempt in range(MAX_RETRY + 1):

        print(f"Quality Check Attempt {attempt + 1}")

        quality_data = quality_check(
            title,
            combined_content
        )

        print(quality_data)

        overall_score_100 = extract_overall_score(quality_data)
        gating_score, gating_breakdown = extract_gating_score(quality_data)

        print(f"\nSelf-reported Overall Score (informational): {overall_score_100}/100")
        print(f"Computed Gating Score (Originality / Exec Insight / SEO-AEO / Evidence / Actionability): {gating_score}/10")
        print(f"Gating breakdown: {gating_breakdown}\n")

        if gating_score >= QUALITY_THRESHOLD:

            quality_passed = True
            break
        if attempt < MAX_RETRY:

            log("EDITOR RETRY")
            print(f"Gating score {gating_score}/10 below threshold {QUALITY_THRESHOLD}/10. Running one targeted revision pass.")

            # Snapshot everything from the pre-retry attempt, in case the
            # revision pass makes things worse -- we compare scores after
            # and keep whichever version actually scored higher.
            pre_retry_blog = blog
            pre_retry_title = title
            pre_retry_subtitle = subtitle
            pre_retry_source_url = source_url
            pre_retry_image_prompt = image_prompt
            pre_retry_blog_content = blog_content
            pre_retry_gating_score = gating_score
            pre_retry_quality_data = quality_data

            suggestions = extract_improvement_suggestions(quality_data)
            print(f"Improvement suggestions being applied: {suggestions}")

            blog = apply_targeted_revision(blog, gating_breakdown, suggestions, title)
            blog = improve_article(blog)  # structural safety net, in case content rewrite shifted anything

            # Safety check: if the revision dropped a required structural
            # element the pre-retry version had (Quick Answers, quote,
            # framework), don't even bother scoring it -- revert immediately.
            pre_retry_diag = diagnose_article(pre_retry_blog_content)
            post_retry_diag_check = diagnose_article(_parse_blog_only(blog))
            structure_regressed = (
                (pre_retry_diag.get("has_quick_answers") and not post_retry_diag_check.get("has_quick_answers"))
                or (pre_retry_diag.get("quote_count", 0) >= 1 and post_retry_diag_check.get("quote_count", 0) == 0)
                or (pre_retry_diag.get("has_framework") and not post_retry_diag_check.get("has_framework"))
            )
            if structure_regressed:
                print("Targeted revision dropped a required section (Quick Answers/quote/framework). Reverting to pre-retry version, skipping re-score.")
                blog = pre_retry_blog
                title = pre_retry_title
                subtitle = pre_retry_subtitle
                source_url = pre_retry_source_url
                image_prompt = pre_retry_image_prompt
                blog_content = pre_retry_blog_content
                quality_data = pre_retry_quality_data
                gating_score = pre_retry_gating_score
                gating_breakdown = extract_gating_score(pre_retry_quality_data)[1]
                continue

            new_title, new_subtitle, new_source_url, new_image_prompt, blog_content = (
                parse_blog_metadata(blog)
            )
            blog_content = ensure_single_quote(blog_content, used_quotes=get_used_quotes())
            blog_content = autofix_banned_phrases(blog_content)

            if new_title.strip():
                title = new_title

            if new_subtitle.strip():
                subtitle = new_subtitle

            if new_source_url.strip():
                source_url = new_source_url

            if new_image_prompt.strip():
                image_prompt = new_image_prompt

            gate_passed, gate_reasons = check_hard_structural_gate(blog_content)
            if not gate_passed:
                print("\n" + "!" * 70)
                print("HARD GATE FAILED AFTER RETRY — ARTICLE WILL NOT BE PUBLISHED")
                print("!" * 70)
                for reason in gate_reasons:
                    print(f"  - {reason}")
                save_draft(
                    title=f"[NEEDS REVIEW] {title}",
                    subtitle=subtitle,
                    blog_content=blog_content,
                    image_prompt=image_prompt,
                    source_url=source_url,
                    related_sources=related_sources,
                )
                return

            log("REGENERATING SEO")

            seo_data = generate_seo(
            title,
            blog_content
             )

            log("REGENERATING AEO")

            aeo_data = generate_aeo(
                title,
                blog_content,
                source_url=source_url,
                published_date=current_date,
            )

            combined_content = (
                blog_content
                + "\n\n"
                + seo_data
                + "\n\n"
                + aeo_data
            )

        if not quality_passed:
         if 'pre_retry_gating_score' in dir() and 'gating_score' in dir():
            pass  # comparison below handles this safely regardless

        if not quality_passed and 'pre_retry_blog_content' in locals() and gating_score < pre_retry_gating_score:
          print(f"\nRetry scored lower ({gating_score}/10) than the pre-retry version ({pre_retry_gating_score}/10). Keeping the pre-retry version instead.\n")
        blog = pre_retry_blog
        title = pre_retry_title
        subtitle = pre_retry_subtitle
        source_url = pre_retry_source_url
        image_prompt = pre_retry_image_prompt
        blog_content = pre_retry_blog_content
        gating_score = pre_retry_gating_score

    if not quality_passed:
        print("\nWARNING: Gating score still below threshold after one revision pass.")
        print(f"Publishing the better-scoring version ({gating_score}/10) based on structural soundness.\n")

    if not source_url:

        source_url = research_source_url

    print("TITLE =", title)

    if title.lower() in [
        t.lower()
        for t in previous_titles
    ]:

        print(
            "Duplicate title detected:",
            title
        )

        title = f"{title} Strategy"

        print(
            "Using alternative title:",
            title
        )

    print(
        "IMAGE PROMPT =",
        image_prompt
    )

    print(
        "SOURCE URL =",
        source_url
    )

    log("IMAGE GENERATION")

    if ENABLE_IMAGE_GENERATION:

        try:

            image_url = generate_image(
                image_prompt
            )

            print(
                "IMAGE URL =",
                image_url
            )

        except Exception as e:

            print(
                "Image Generation Failed:",
                e
            )

            image_url = FALLBACK_IMAGE_URL

            print(
                "Using fallback image:",
                image_url
            )

    else:

        print("Image generation disabled via ENABLE_IMAGE_GENERATION=false.")

        image_url = FALLBACK_IMAGE_URL

        print("Using fallback image:", image_url)

    log("SAVING ARTICLE")

    report = uniqueness_check(
        title,
        blog_content
    )

    print(report)

    print()
    print("Similarity Score:", report["overall_similarity"])
    print("Status:", report["status"])
    print()

    if report["status"] == "FAIL":

        print("Similarity too high.")
        print("Regenerating ONLY the flagged components (single pass, no re-check to save tokens)...")

        thesis_hint = insight.get("thesis", "")[:200] if isinstance(insight, dict) else str(insight)[:200]

        title, blog_content = fix_weak_components(
            title,
            blog_content,
            report,
            thesis_hint
        )

        print("Weak components regenerated. Proceeding to save without a second similarity check.")

    save_blog(
        current_date,
        title,
        subtitle,
        blog_content,
        image_prompt,
        source_url,
        image_url,
        related_sources,
    )


# UPDATE MEMORY
    remember_title(title)

    remember_opening_style(
        first_paragraph(blog_content)
    )

    remember_conclusion(
        blog_content.split("\n\n")[-1]
    )

    print("Memory Updated")
    print("Saved Successfully")

    log("UPDATING RSS")

    generate_rss()

    log("UPDATING SITEMAP")

    generate_sitemap()

    log("PIPELINE COMPLETED")

def run_pipeline():
    try:
        _run_pipeline_inner()
    except RateLimitError as e:
        print("\n" + "=" * 70)
        print("OPENAI RATE LIMIT OR QUOTA REACHED — stopping pipeline cleanly.")
        print(f"Details: {e}")
        print("If the article had already been written, a draft was saved to /drafts.")
        print("Check your OpenAI usage, billing, or wait before retrying.")
        print("=" * 70)
        return
if __name__ == "__main__":
    run_pipeline()