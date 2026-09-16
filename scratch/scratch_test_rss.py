from src.newswatch.rss_builder import build_feed_url
from src.newswatch.rss_fetcher import fetch_feed
from src.newswatch.parser import parse_entry


def main() -> None:
    query = "Apple Inc"
    url = build_feed_url(query=query, exact_match=True)
    print(f"Fetching url: {url}\n")

    feed = fetch_feed(url)
    print(f"Found: {len(feed.entries)} entries\n")

    for i, entry in enumerate(feed.entries[:5], start=1):
        article = parse_entry(entry)
        print(f"--- Article {i} ---")
        print(f"ID:        {article.id}")
        print(f"Title:     {article.title}")
        print(f"URL:       {article.url}")
        print(f"Source:    {article.source}")
        print(f"Published: {article.published}")
        print()


if __name__ == "__main__":
    main()