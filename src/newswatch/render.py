from datetime import datetime, timezone

from src.newswatch.models import Article
from src.newswatch.paths import ensure_job_dir, job_articles_path


def render_markdown(job_name: str, articles: list[Article]) -> str:
    # ========================================================================
    #  # Render a list of articles as a markdown document.
    # 
    # This is a pure function — it produces a string but writes nothing.
    # ========================================================================

    updated = datetime.now(timezone.utc).isoformat()

    lines = [
        f"# NewsWatch — {job_name}",
        "",
        f"_Last updated: {updated} · {len(articles)} articles_",
        "",
        "---",
        "",
    ]

    for article in articles:
        lines.append(f"## {article.title}")
        lines.append("")
        lines.append(f"- **URL:** {article.url}")
        lines.append(f"- **Source:** {article.source}")
        lines.append(f"- **Published:** {article.published}")
        lines.append("")

    return "\n".join(lines)


def save_markdown(job_name: str, articles: list[Article]) -> None:
    # ========================================================================
    #
    # # Render articles as markdown and write to the job's articles.md.
    #
    # Creates the job folder if needed.
    # ========================================================================

    ensure_job_dir(job_name)
    content = render_markdown(job_name, articles)
    job_articles_path(job_name).write_text(content, encoding="utf-8")