#  ==========================================================
# 
#                       Collector
#    
#   Fetches, dedupe (deduplicates) , save s articles for
#   each configured job 
#  ==========================================================


from src.newswatch.state import is_new_article, load_state, now_iso, save_state
from src.newswatch.store import load_articles, save_articles
from src.newswatch.rss_builder import build_feed_url
from src.newswatch.rss_fetcher import fetch_feed
from src.newswatch.parser import parse_entry
from src.newswatch.render import save_markdown
from src.newswatch.models import Config, JobConfig, Settings


 

def collect_job(job: JobConfig, settings: Settings) -> int:
    # =========================
    # Run one job   
    #   - fetch the feed
    #   - dedupe
    #   - save articles and state
    # =========================


    # grab the run time BEFORE fetching so any article published during the fetch
    # window is still considered "new" on the next run 
    run_started = now_iso()

    # ==================> Load current memory 
    state = load_state(job_name= job.name)
    existing = load_articles(job_name= job.name)
    seen_ids = {a.id for a in existing}

    # ==================> Fetch news feed 

    url = build_feed_url(
        query= job.query,
        exact_match= job.exact_match,
        include_site= job.include_site,
        locale=job.locale,
        time_range=job.time_range,
    )

    feed = fetch_feed(url= url)

    # ==================> parse and filter 
    # de duplicate twice agains existin seen_ids and within the given fetch 
    # new_ids -  the same url can appear twice in one feed 

    new_articles: list = []
    new_ids: set[str] = set()

    for entry in feed.entries: 
        article = parse_entry(entry)

        if article.id in new_ids:
            continue

        if not is_new_article(article, state, seen_ids):
            continue

        new_articles.append(article)
        new_ids.add(article.id)

    # ==================> Merge trim and save 
    combined = new_articles + existing
    trimmed = save_articles(job.name, combined, settings.max_articles)
    save_markdown(job.name, trimmed)

    # ==================> Update state 
    state.last_run = run_started
    if new_articles:
        state.new_since_last_send = True
    save_state(job.name, state)

    return len(new_articles)

    # # ==================>
    # # ==================>

    # pass


def collect_all_jobs(config: Config) -> dict[str, str]:
    # =========================
    # Run every conrfigured job 
    #   0   
    #   - returns a dict mapping job name to the number of new articles added
    # =========================

    results: dict[str, int] = {}

    for job in config.jobs:
        results[job.name] = collect_job(job, config.settings)


    