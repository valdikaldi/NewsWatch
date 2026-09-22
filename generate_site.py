# ====================================
# generate_site.py — build the GitHub Pages dashboard.
#
# Reads all job data from data/, renders templates/dashboard.html,
# and writes the result to _site/index.html.
# ====================================

import sys

from src.newswatch.config import load_config
from src.newswatch.paths import PROJECT_ROOT
from src.newswatch.render import render_dashboard
from src.newswatch.store import load_articles


OUTPUT_DIR = PROJECT_ROOT / "_site"
OUTPUT_FILE = OUTPUT_DIR / "index.html"


def main() -> int:
    # ====================================
    # Build the dashboard. Returns 0 on success, 1 on error
    # # ====================================
    print("NewsWatch dashboard — building site\n")

    try:
        config = load_config()
    except (FileNotFoundError, ValueError) as e:
        print(f"❌ Config error: {e}")
        return 1

    # Collect articles for each job
    jobs: list[dict] = []
 
    for job in config.jobs:
        articles = load_articles(job.name)
        jobs.append({"config": job, "articles": articles})
        print(f"  {job.name}: {len(articles)} articles")

    # Render
    html = render_dashboard(jobs)

    # Write
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(html, encoding="utf-8")

    print(f"\n✅ Wrote {OUTPUT_FILE.relative_to(PROJECT_ROOT)}")
    print(f"   Size: {len(html):,} characters")
    return 0


if __name__ == "__main__":
    sys.exit(main())