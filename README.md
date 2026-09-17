# NewsWatch

Automated news monitoring and alerting.

NewsWatch watches the news for any search query you define, tracks new articles, and sends periodic email digests. It uses Google News RSS, runs on GitHub Actions, and stores everything as plain files — no database required.

## What It Does

- Monitors **multiple search queries** (called *jobs*) independently
- Fetches articles from Google News RSS, filtered by locale, site, and recency
- Deduplicates by URL hash and publication date
- Keeps the newest 50 articles per job (configurable)
- Sends email digests on a schedule you control (per day, week, or month)
- Only emails when there's actually something new

## Project Structure

    newswatch/
    ├── assets/              Static resources
    │   ├── locales.csv      Google News locale codes (ceid, hl, gl)
    │   └── README.md        Source attribution for locales.csv
    ├── config/
    │   └── config.yaml      User settings: jobs, interval, email
    ├── data/                Runtime data (one folder per job)
    │   └── <job-slug>/
    │       ├── articles.json    Source of truth — structured article data
    │       ├── articles.md      Generated — human-readable view
    │       └── state.json       Program memory (last run, last sent)
    ├── scratch/             Throwaway test scripts (not shipped)
    ├── src/newswatch/       Application code
    │   ├── models.py            Dataclasses (Article, AppState, JobConfig, ...)
    │   ├── paths.py             All filesystem paths
    │   ├── config.py            Loads and validates config.yaml
    │   ├── state.py             Loads/saves state.json + dedupe rule
    │   ├── store.py             Loads/saves articles.json + trim
    │   ├── render.py            Renders articles as markdown
    │   ├── rss_builder.py       Builds Google News RSS URLs
    │   ├── rss_fetcher.py       Fetches RSS feeds
    │   ├── parser.py            Converts feed entries to Article objects
    │   └── collector.py         Orchestrates fetch → dedupe → save per job
    ├── main.py              Entry point (wired in Step 7)
    ├── pyproject.toml       Project metadata and dependencies
    ├── uv.lock              Locked dependency versions
    └── TODO.md              Project roadmap

## Setup

Requires [uv](https://docs.astral.sh/uv/).

    uv sync

## Running Locally

The project uses the src-layout, so modules are run as packages:

    uv run python -m src.newswatch.rss_builder
    uv run python -m scratch.scratch_test_collector

Do **not** run scripts directly (e.g. `uv run src/newswatch/rss_builder.py`) —
the src-layout requires module-style invocation.

## Configuration

Edit `config/config.yaml`:

    settings:
      interval_days: 7
      email: "you@example.com"
      max_articles: 50

    jobs:
      - name: "Apple News"
        query: "Apple Inc"
        exact_match: true
        include_site: null
        locale: "US:en"
        time_range: "7d"

Job names must be unique. Each job gets its own folder under `data/`.

## Status

Work in progress....