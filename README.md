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


newswatch/
│
├── .github/
│   └── workflows/
│       └── newswatch.yml          ← GitHub runs this daily
│
├── config/
│   └── config.json                ← your settings (query, interval, email)
│
├── data/
│   ├── articles.md                ← the news output (human-readable)
│   └── state.json                 ← program memory (seen IDs, last run)
│
├── src/
│   ├── __init__.py
│   ├── models.py                  ← what an Article looks like
│   ├── config.py                  ← reads config.json
│   ├── state.py                   ← reads/writes state.json
│   ├── rss_builder.py             ← query → Google News RSS URL
│   ├── fetcher.py                 ← downloads the RSS feed
│   ├── parser.py                  ← RSS entry → Article object
│   ├── store.py                   ← reads/writes articles.md
│   ├── collector.py               ← orchestrates fetch→parse→dedupe→save
│   ├── notifier.py                ← decides: should we email?
│   └── mailer.py                  ← sends the email
│
├── tests/                         ← automated checks
│   └── fixtures/                  ← sample RSS data for tests
│
├── scripts/                       ← dev-only helpers (optional, later)
│
├── main.py                        ← the entry point: runs collector then notifier
├── pyproject.toml                 ← uv reads this (project metadata + dependencies)
├── uv.lock                        ← uv generates this (exact versions)
├── .python-version                ← uv generates this (Python version pin)
├── .gitignore
├── LICENSE
└── README.md

## License

MIT
