# NewsWatch

Automated news monitoring and alerting. Define a search query, and NewsWatch
fetches matching articles from Google News RSS daily, tracks new ones in a
markdown file, and emails you a digest on your chosen interval.

## How it works

1. You set a query (e.g. `"Apple Inc"`) and an interval (e.g. every 7 days).
2. A GitHub Action runs daily and collects new articles into `data/articles.md`.
3. On the interval boundary, NewsWatch emails you the updated digest.
4. Duplicates are avoided using URL-based IDs.

## Status

🚧 MVP in progress.

## Stack

- Python 3.12
- [feedparser](https://pypi.org/project/feedparser/) for RSS
- GitHub Actions for scheduling
- Markdown as the database (max 50 articles)

## Setup

_TBD — coming as the project takes shape._



## License

MIT
