# ====================================
# # Render the GitHub Pages dashboard.
# Takes a list of jobs (each with a JobConfig and a list of Article objects)
# and produces a complete HTML page with CSS inlined.
# ====================================

from datetime import datetime, timedelta, timezone

from src.newswatch.models import Article, JobConfig
from src.newswatch.render._jinja import (
    TEMPLATES_DIR,
    build_environment,
    format_date,
)
from src.newswatch.state import now_iso


ACCENT_PALETTE = [
    "#2563eb",
    "#0891b2",
    "#7c3aed",
    "#dc2626",
    "#d97706",
]


# Human-readable descriptions for time_range codes
TIME_RANGE_LABELS = {
    "1h": "Past hour",
    "1d": "Past day",
    "7d": "Past week",
    "1m": "Past month",
    "1y": "Past year",
}


def _compute_stats(articles: list[Article]) -> dict[str, int]:
    # ====================================
    #  Count how many articles fall into each recency bucket.
    # ====================================
    
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today_start - timedelta(days=1)
    week_start = today_start - timedelta(days=7)

    stats = {"today": 0, "yesterday": 0, "week": 0, "older": 0}

    for article in articles:
        if not article.published:
            stats["older"] += 1
            continue
        try:
            dt = datetime.fromisoformat(article.published)
        except ValueError:
            stats["older"] += 1
            continue

        if dt >= today_start:
            stats["today"] += 1
        elif dt >= yesterday_start:
            stats["yesterday"] += 1
        elif dt >= week_start:
            stats["week"] += 1
        else:
            stats["older"] += 1

    return stats


def _describe_search(job: JobConfig) -> dict[str, str]:
    # ====================================
    # Turn a JobConfig into human-readable display strings for the template.
    # ====================================
    match_display = "Exact phrase" if job.exact_match else "Loose match"

    site_display = f"site:{job.include_site}" if job.include_site else ""

    range_display = TIME_RANGE_LABELS.get(job.time_range or "", "All time")

    return {
        "display_query": f'"{job.query}"',
        "match_display": match_display,
        "site_display": site_display,
        "locale_display": job.locale,
        "range_display": range_display,
    }


def render_dashboard(jobs: list[dict]) -> str:
    # ====================================
    # Render the dashboard HTML for all jobs.
    # Args:
    #     jobs: List of dicts, each with:
    #           - "config": JobConfig
    #           - "articles": list[Article] — newest first
    # Returns:   The complete HTML string, CSS inlined.
    # ====================================
    env = build_environment()
    template = env.get_template("dashboard.html")

    css_path = TEMPLATES_DIR / "dashboard.css"
    inline_css = css_path.read_text(encoding="utf-8")

    enriched_jobs = []
    for index, job in enumerate(jobs):
        config: JobConfig = job["config"]
        articles: list[Article] = job["articles"]

        display = _describe_search(config)
        stats = _compute_stats(articles)

        enriched_jobs.append({
            "name": config.name,
            "articles": articles,
            "accent": ACCENT_PALETTE[index % len(ACCENT_PALETTE)],
            "updated": format_date(articles[0].published) if articles else "",
            "stats": stats,
            **display,
        })

    return template.render(
        jobs=enriched_jobs,
        inline_css=inline_css,
        updated=format_date(now_iso()),
    )