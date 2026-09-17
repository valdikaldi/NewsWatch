import json
from dataclasses import asdict
from pathlib import Path

from src.newswatch.models import Article
from src.newswatch.paths import (
    ensure_job_dir,
    job_articles_json_path,
)


def trim(articles: list[Article], max_articles: int) -> list[Article]:
    # ========================================================================
    #      Sort articles newest-first and keep at most max_articles.
    # ========================================================================
    
    sorted_articles = sorted(articles, key=lambda a: a.published, reverse=True)
    return sorted_articles[:max_articles]


def load_articles(job_name: str) -> list[Article]:
    # ========================================================================
    
    # Load articles from a job's articles.json.

    # Returns an empty list if the file doesn't exist (first run).
    
    # ========================================================================
    
    path = job_articles_json_path(job_name)
    if not path.exists():
        return []

    raw = json.loads(path.read_text(encoding="utf-8"))
    return [Article(**item) for item in raw]


def save_articles( job_name: str, articles: list[Article], max_articles: int) -> list[Article]:
    # ========================================================================

    # Trim, serialize, and save articles to a job's articles.json.

    # Returns the trimmed list (what was actually saved).

    # ========================================================================

    trimmed = trim(articles, max_articles)
    ensure_job_dir(job_name)
    path = job_articles_json_path(job_name)
    payload = [asdict(a) for a in trimmed]
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return trimmed