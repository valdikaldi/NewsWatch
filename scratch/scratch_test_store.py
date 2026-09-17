import shutil
from datetime import datetime, timedelta, timezone

from src.newswatch.models import Article
from src.newswatch.paths import (
    job_articles_json_path,
    job_articles_path,
    job_data_dir,
)
from src.newswatch.store import load_articles, save_articles
from src.newswatch.render import save_markdown

# copy paste
#  ✅
#   ❌

JOB = "Store Test Job"


def make_article(n: int, days_ago: int = 0) -> Article:
    published = (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()
    return Article(
        id=f"id{n:04d}",
        title=f"Article number {n}",
        url=f"https://example.com/article-{n}",
        source="Test Source",
        published=published,
    )


def clean() -> None:
    folder = job_data_dir(JOB)
    if folder.exists():
        shutil.rmtree(folder)


#  ======================================================================================================


def main() -> None:
    clean()

    #=> 1. Round-trip with 5 articles 
    print("=== 1. Save and reload 5 articles (JSON) ===")
    original = [make_article(i, days_ago=i) for i in range(1, 6)]
    saved = save_articles(JOB, original, max_articles=50)

    reloaded = load_articles(JOB)
    print(f"  Original count: {len(original)}")
    print(f"  Saved count:    {len(saved)}")
    print(f"  Reloaded count: {len(reloaded)}")

    if {a.url for a in original} == {a.url for a in reloaded}:
        print("  ✅ All URLs match after round-trip")
    else:
        print("  ❌ URL mismatch")




    #=> 2. Trim behavior: 60 -> 50 
    print("\n=== 2. Trim to 50 from 60 ===")
    clean()

    many = [make_article(i, days_ago=i) for i in range(1, 61)]
    saved = save_articles(JOB, many, max_articles=50)
    print(f"  Input: {len(many)} articles")
    print(f"  Saved: {len(saved)} articles")

    expected_ids = {f"id{i:04d}" for i in range(1, 51)}
    if {a.id for a in saved} == expected_ids:
        print("  ✅ Kept the 50 newest")
    else:
        print("  ❌ Wrong subset kept")

    reloaded = load_articles(JOB)
    if {a.id for a in reloaded} == expected_ids:
        print("  ✅ Persisted file matches trimmed list")







    #=> 3. Render markdown from trimmed JSON 
    print("\n=== 3. Render markdown ===")
    save_markdown(JOB, reloaded)
    md_path = job_articles_path(JOB)
    if md_path.exists():
        md_text = md_path.read_text(encoding="utf-8")
        print(f"  ✅ articles.md written ({len(md_text)} chars)")
        print(f"  First 200 chars:")
        print("  " + md_text[:200].replace("\n", "\n  "))
    else:
        print("  ❌ articles.md not created")




    #=> 4. Show file paths 
    print("\n=== 4. Files created ===")
    print(f"  {job_articles_json_path(JOB)}")
    print(f"  {job_articles_path(JOB)}")





    #=> 5. First-run behavior 
    print("\n=== 5. Load when no file exists ===")
    # clean()
    empty = load_articles(JOB)
    if empty == []:
        print("  ✅ Returns empty list")

    # clean()
    # print("\nDone.")


if __name__ == "__main__":
    main()