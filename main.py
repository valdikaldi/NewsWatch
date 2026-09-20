"""
NewsWatch — main entry point.

Runs the full pipeline for each configured job:
  1. Collect (fetch, dedupe, save articles + state)
  2. Decide whether to notify
  3. If yes: render markdown, send email, mark as sent
"""

import sys

from dotenv import load_dotenv

from src.newswatch.collector import collect_job
from src.newswatch.config import load_config
from src.newswatch.mailer import send_email
from src.newswatch.notifier import mark_sent, should_notify
from src.newswatch.render import render_markdown
from src.newswatch.state import load_state, save_state
from src.newswatch.store import load_articles

from src.newswatch.render_email import render_html_email



def process_job(job, settings) -> dict:
    # ===============================================================
    # Run one job through the full pipeline.
    #
    # Returns a summary dict:
    #     {"job": str, "new_articles": int, "notified": bool}
    # ===============================================================


    # =====>  1. Collect 
    new_count = collect_job(job, settings)

    # =====>  2. Decide whether to notify 
    state = load_state(job.name)
    notify = should_notify(state, settings)

    result = {"job": job.name, "new_articles": new_count, "notified": False}

    if not notify:
        return result

    # =====>  3. Load articles and render email body 
    articles = load_articles(job.name)
    plain_body = render_markdown(job.name, articles)
    html_body = render_html_email(job.name, articles)
    subject = f"NewsWatch: {job.name} ({len(articles)} articles)"

    # =====>  4. Send 
    send_email(
        to=settings.email,
        subject=subject,
        body=plain_body,
        html_body=html_body,
    )

    # =====>  5. Mark as sent and persist state 
    mark_sent(state)
    save_state(job.name, state)

    result["notified"] = True
    return result


def main() -> int:
    # ===============================================================
    # Entry point. Returns a process exit code (0 = success, 1 = error).
    # ===============================================================
    
    load_dotenv()  # no-op if .env doesn't exist

    print("NewsWatch — starting run\n")

    try:
        config = load_config()
    except (FileNotFoundError, ValueError) as e:
        print(f"    --- Config error: {e}")
        return 1

    print(f"Loaded {len(config.jobs)} job(s)\n")

    summaries: list[dict] = []
    errors = 0

    for job in config.jobs:
        print(f" {job.name} ")
        try:
            result = process_job(job, config.settings)
            summaries.append(result)
            email_status = "sent" if result["notified"] else "not sent"
            print(f"   New articles: {result['new_articles']}  |  Email: {email_status}\n")
        except Exception as e:
            errors += 1
            print(f"   ---- Error: {e}\n")

    # =====>  Summary 
    print("=== Summary ===")
    for r in summaries:
        status = "sent" if r["notified"] else "not sent"
        print(f"  {r['job']}: {r['new_articles']} new, email {status}")

    if errors:
        print(f"\n{errors} job(s) failed.")
        return 1

    print("\n -> Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())