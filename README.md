# NewsWatch

Automated news monitoring and alerting.

NewsWatch watches the news for any search query you define, tracks new articles, and sends periodic email digests. It uses Google News RSS, runs on GitHub Actions, and stores everything as plain files — no database required.


## Demo

<!-- <img width="799" height="554" alt="demo" src="https://github.com/user-attachments/assets/18f6abd8-3e78-4781-b9ff-c784e2605179" /> -->
<p align="center">
  <img width="799" height="554" alt="demo" src="https://github.com/user-attachments/assets/18f6abd8-3e78-4781-b9ff-c784e2605179" />
</p>

 
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
    │       ├── articles.md      Generated — human-readable views
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
    ├── main.py              Entry point 
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


## Add Features :

- [ ] Global enrichment setup — store `article_text`, add enrichment step/schema fields, cache models, update email template with fallbacks, process only new articles, truncate text (~5000 chars), and fail soft per feature.
- [ ] AI Summary — generate a max-5-sentence summary with DistilBART/BART/FLAN-T5, store `ai_summary`, and render under the article title.
- [ ] “Why This Matters” — prompt FLAN-T5 for one sentence tied to the user query, store `why_it_matters`, and show under the summary.
- [ ] Sentiment Indicator — run VADER, map compound score to Positive/Neutral/Negative, store label/score, and render a badge without using it as main ranking.
- [ ] Topic / Category Detection — zero-shot classify with BART-MNLI or use embedding similarity, store top topics, render tags, and cache the model.
- [ ] Article Type Badge — start rule-based for News/Analysis/Opinion/Interview/Press release/Research, store `article_type`, and render a badge.
- [ ] Named Entity Recognition — run spaCy `en_core_web_sm`, group PERSON/ORG/GPE entities, store `entities`, and render people/orgs mentioned.
- [ ] Keyword Extraction — use YAKE with `n=2, top=5`, store `keywords`, and render as tags in the email.
- [ ] Duplicate / Near-Duplicate Detection — embed with `all-MiniLM-L6-v2`, compare cosine similarity > 0.85, store group/count/sources, and collapse duplicate cards while keeping all links.
- [ ] Read Time — compute `max(1, round(words / 200))`, store `read_time_minutes`, and render next to article metadata.
- [ ] Daily AI Digest — compute article/publisher/topic/type counts, pick top 3 stories, and insert a concise briefing before the article list.
- [ ] Suggested Implementation Order — do read time, sentiment, keywords, article type, NER, AI summary, why-this-matters, topics, duplicates, then daily digest.
- [ ] GitHub Actions Notes — cache Hugging Face/Torch/spaCy models, prefer small models, set timeout, fail soft, log enrichment errors, truncate inputs, process new articles only, and keep HTML responsive.