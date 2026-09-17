from src.newswatch.models import AppState, Article
from src.newswatch.state import is_new_article, load_state, save_state, now_iso


def make_article(id_: str, published: str) -> Article:
     return Article(
        id=id_,
        title=f"Article {id_}",
        url=f"https://example.com/{id_}",
        source="Test Source",
        published=published,
    )


def check(label: str, result: bool, expected: bool) -> None:
    """Print a pass/fail line."""
    mark = "BINGO" if result == expected else "ERROR"
    print(f"  {mark} {label}: got {result}, expected {expected}")


def main() -> None:
    print("=== Dedupe rule tests ===\n")

    # ==== Case 1: First run, article with valid date ====
    state = AppState()
    article = make_article("aaa", "2026-09-17T10:00:00+00:00")
    check("First run, valid date",
          is_new_article(article, state), True)



    # ==== Case 2: First run, article with no date ====
    article_no_date = make_article("bbb", "")
    check("First run, no date",
          is_new_article(article_no_date, state), False)

    

    # ==== Case 3: Article ID already in seen_ids ====
    state_with_seen = AppState(seen_ids=["ccc"])
    article_seen = make_article("ccc", "2026-09-17T10:00:00+00:00")
    check("Already seen",
          is_new_article(article_seen, state_with_seen), False)

    

    # ==== Case 4: Old article (published before last_run) ====
    state_old = AppState(last_run="2026-09-17T12:00:00+00:00")
    article_old = make_article("ddd", "2026-09-17T11:00:00+00:00")
    check("Published before last_run",
          is_new_article(article_old, state_old), False)



    # ==== Case 5: Fresh article (published after last_run) ====
    article_new = make_article("eee", "2026-09-17T13:00:00+00:00")
    check("Published after last_run",
          is_new_article(article_new, state_old), True)



    # ==== Case 6: Exactly at last_run (boundary) ====
    article_boundary = make_article("fff", "2026-09-17T12:00:00+00:00")
    check("Published exactly at last_run",
          is_new_article(article_boundary, state_old), False)






    print("\n=== Save/load round-trip ===\n")

    job = "Dedupe Test Job"

    # Clean slate
    from src.newswatch.paths import job_data_dir
    import shutil
    folder = job_data_dir(job)
    if folder.exists():
        shutil.rmtree(folder)

    # Load on empty
    empty_state = load_state(job)
    print(f"  Empty load: {empty_state}")

    # Modify and save
    empty_state.last_run = now_iso()
    empty_state.seen_ids = ["a1b2c3d4e5f6", "7890abcdef12"]
    save_state(job, empty_state)
    print(f"  Saved with {len(empty_state.seen_ids)} seen_ids")

    # Reload
    reloaded = load_state(job)
    if reloaded == empty_state:
        print("   BINGO ---- Round-trip succeeded")
    else:
        print("  ERROR --- Mismatch")

    # Clean up
    shutil.rmtree(folder)
    print(f"  Cleaned up {folder.name}/")


if __name__ == "__main__":
    main()