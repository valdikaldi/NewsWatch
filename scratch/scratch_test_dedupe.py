from src.newswatch.models import AppState, Article
from src.newswatch.state import is_new_article, load_state, save_state, now_iso
# copy paste
#  ✅
#   ❌

def make_article(id_: str, published: str) -> Article:
    """Helper to make a minimal Article for testing."""
    return Article(
        id=id_,
        title=f"Article {id_}",
        url=f"https://example.com/{id_}",
        source="Test Source",
        published=published,
    )


def check(label: str, result: bool, expected: bool) -> None:
    mark = "✅" if result == expected else "❌"
    print(f"  {mark} {label}: got {result}, expected {expected}")


def main() -> None:
    print("=== Dedupe rule tests ===\n")

    # ==== Case 1: First run, article with valid date ====
    state = AppState()
    article = make_article("aaa", "2026-09-17T10:00:00+00:00")
    check("First run, valid date",
          is_new_article(article, state, seen_ids=set()), True)



    # ==== Case 2: First run, article with no date ====
    article_no_date = make_article("bbb", "")
    check("First run, no date",
          is_new_article(article_no_date, state, seen_ids=set()), False)




    # ==== Case 3: Article ID already in seen_ids ====
    article_seen = make_article("ccc", "2026-09-17T10:00:00+00:00")
    check("Already seen",
          is_new_article(article_seen, state, seen_ids={"ccc"}), False)



    # ==== Case 4: Old article (published before last_run) ====
    state_old = AppState(last_run="2026-09-17T12:00:00+00:00")
    article_old = make_article("ddd", "2026-09-17T11:00:00+00:00")
    check("Published before last_run",
          is_new_article(article_old, state_old, seen_ids=set()), False)



    # ==== Case 5: Fresh article (published after last_run) ====
    article_new = make_article("eee", "2026-09-17T13:00:00+00:00")
    check("Published after last_run",
          is_new_article(article_new, state_old, seen_ids=set()), True)




    # ==== Case 6: Exactly at last_run (boundary) ====
    article_boundary = make_article("fff", "2026-09-17T12:00:00+00:00")
    check("Published exactly at last_run",
          is_new_article(article_boundary, state_old, seen_ids=set()), False)







    print("\n=== Save/load round-trip ===\n")

    job = "Dedupe Test Job"

    from src.newswatch.paths import job_data_dir
    import shutil
    folder = job_data_dir(job)
    if folder.exists():
        shutil.rmtree(folder)

    empty_state = load_state(job)
    print(f"  Empty load: {empty_state}")

    empty_state.last_run = now_iso()
    empty_state.new_since_last_send = True
    save_state(job, empty_state)
    print(f"  Saved state")

    reloaded = load_state(job)
    if reloaded == empty_state:
        print("  ✅ Round-trip succeeded")
    else:
        print(f"  ❌ Mismatch")
        print(f"     Original: {empty_state}")
        print(f"     Reloaded: {reloaded}")

    shutil.rmtree(folder)
    print(f"  Cleaned up {folder.name}/")


if __name__ == "__main__":
    main()