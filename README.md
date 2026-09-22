<div align="center">

# 📰 NewsWatch

### Automated news monitoring and alerting

Watches the news for any search query you define, tracks new articles,<br>
and sends periodic email digests — powered by Google News RSS and GitHub Actions.

<br>

<a href="https://valdikaldi.github.io/NewsWatch/">
  <img src="https://img.shields.io/badge/🌐_Live_Dashboard-valdikaldi.github.io-2563eb?style=for-the-badge" alt="Live Dashboard">
</a>

<br><br>

<img width="799" alt="demo" src="https://github.com/user-attachments/assets/18f6abd8-3e78-4781-b9ff-c784e2605179" />

</div>

---

## ✨ What It Does

- Monitors **multiple search queries** (called *jobs*) independently
- Fetches articles from Google News RSS, filtered by locale, site, and recency
- Deduplicates by URL hash and publication date
- Keeps the newest 50 articles per job (configurable)
- Sends styled HTML email digests on a schedule you control
- Only emails when there's actually something new
- Publishes a public dashboard to GitHub Pages

---

## 🌐 Live Dashboard

Every monitored query appears on a public page, updated automatically whenever new data arrives:

**https://valdikaldi.github.io/NewsWatch/**

 

## 📁 Project Structure

 
```
newswatch/
├── .github/workflows/
│   ├── newswatch.yml          Daily cron: collect + email
│   └── deploy-pages.yml       On push: rebuild the dashboard
├── assets/
│   ├── locales.csv            Google News locale codes (ceid, hl, gl)
│   └── README.md              Source attribution
├── config/
│   └── config.yaml            User settings: jobs, interval, email
├── data/
│   └── <job-slug>/            One folder per job
│       ├── articles.json      Source of truth — structured article data
│       ├── articles.md        Generated — human-readable view
│       └── state.json         Program memory (last run, last sent)
├── templates/
│   ├── email.mjml             Email design (source)
│   ├── email.html             Email design (compiled)
│   ├── dashboard.html         Dashboard markup
│   └── dashboard.css          Dashboard styles
├── src/newswatch/
│   ├── models.py              Dataclasses
│   ├── paths.py               Filesystem paths
│   ├── config.py              Loads and validates config.yaml
│   ├── state.py               Loads/saves state.json + dedupe rule
│   ├── store.py               Loads/saves articles.json + trim
│   ├── rss_builder.py         Builds Google News RSS URLs
│   ├── rss_fetcher.py         Fetches RSS feeds
│   ├── parser.py              Converts feed entries to Article objects
│   ├── collector.py           Orchestrates fetch → dedupe → save per job
│   ├── notifier.py            Decides whether to send an email
│   ├── mailer.py              Sends email via SMTP
│   └── render/
│       ├── _jinja.py          Shared Jinja2 setup
│       ├── markdown.py        Renders articles as markdown
│       ├── email_html.py      Renders the HTML email
│       └── dashboard.py       Renders the dashboard
├── main.py                    Entry point: collect → notify → email
├── generate_site.py           Entry point: build the dashboard
├── pyproject.toml
├── uv.lock
└── TODO.md
```

---

## ⚙️ Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

---

## 🚀 Running Locally

Modules are run as packages (src-layout):

```bash
uv run python -m main                          # collect + email
uv run python -m generate_site                 # build the dashboard
```

> Do **not** run scripts directly (e.g. `uv run src/newswatch/rss_builder.py`) — the src-layout requires module-style invocation.

## 🔧 Configuration

Edit `config/config.yaml`:

```yaml
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

  - name: "Microsoft News"
    query: "Microsoft"
    exact_match: false
    include_site: null
    locale: "US:en"
    time_range: "7d"
```

**Settings**

| Field | Description |
|---|---|
| `interval_days` | How often to email. The collector runs daily regardless — this controls notification frequency only. |
| `email` | Where digests are sent. |
| `max_articles` | Maximum articles kept per job. Oldest are dropped when exceeded. |

**Job fields**

| Field | Description |
|---|---|
| `name` | Unique label. Used for the dashboard card and the `data/<slug>/` folder. |
| `query` | Search term sent to Google News. |
| `exact_match` | `true` wraps the query in quotes for phrase matching. |
| `include_site` | Restrict results to a domain (e.g. `"bbc.com"`), or `null` for all sites. |
| `locale` | A `ceid` from `assets/locales.csv` (e.g. `"US:en"`, `"GB:en"`, `"DE:de"`). |
| `time_range` | Google News `when:` filter — `"1h"`, `"1d"`, `"7d"`, `"1m"`, `"1y"`, or `null` for all time. |

Job names must be unique. Each job gets its own folder under `data/`.

Credentials (`MAIL_USERNAME`, `MAIL_PASSWORD`) live in `.env` locally and in **GitHub repository secrets** when deployed.

---

## 🛠 Tech

Python · [uv](https://docs.astral.sh/uv/) · [feedparser](https://github.com/kurtmckee/feedparser) · [Jinja2](https://jinja.palletsprojects.com/) · [MJML](https://mjml.io/) · GitHub Actions · GitHub Pages



---
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