from src.newswatch.parser import normalize_published, parse_entry


def main() -> None:
    print("=== 1. Date normalization ===")
    examples = [
        "Mon, 08 Jan 2026 09:12:00 GMT",
        "Tue, 17 Sep 2026 14:30:00 +0200",
        "Wed, 01 Jan 2025 00:00:00 -0500",
        "",                                  # empty
        "not a date at all",                 # malformed
    ]

    for raw in examples:
        result = normalize_published(raw)
        print(f"  {raw!r:45} -> {result!r}")

    print()




    print("=== 2. parse_entry with a real feed entry ===")

    from src.newswatch.rss_builder import build_feed_url
    from src.newswatch.rss_fetcher import fetch_feed

    url = build_feed_url("Apple Inc", time_range="1d")
    feed = fetch_feed(url)

    if not feed.entries:
        print("  No entries returned from feed.")
        return

    entry = feed.entries[0]
    print(f"  Raw entry.published:    {entry.get('published', 'N/A')!r}")

    article = parse_entry(entry)
    print(f"  Article.published:      {article.published!r}")
    print(f"  Article.title:          {article.title!r}")
    print(f"  Article.id:             {article.id!r}")


if __name__ == "__main__":
    main()