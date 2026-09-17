
# ========================================
# Here we make sure that we track article  
# state so that we dont add duplicates 
## and simply notify the same articles to user 
# ========================================


import json 
from dataclasses import asdict
from datetime import datetime, timezone

from src.newswatch.models import AppState, Article
from src.newswatch.paths import ensure_job_dir, job_state_path



# ============================================================
# Time helpers
# ===========================================================

def now_iso() -> str:
    # ============================================================
    #  return current UTC time as an ISO 8061 string
    # ===========================================================

    return datetime.now(timezone.utc).isoformat()




# ============================================================
# Persistence
# ============================================================

def load_state(job_name: str) -> AppState:

    # ============================================================
    #  load the state for a job
    # if the state file does NOT exist (first run) returns a fresh 
    # AppState 
    # ============================================================


    path = job_state_path(job_name= job_name)

    if not path.exists():
        return AppState()

    data = json.loads(path.read_text(encoding="utf-8"))

    return AppState(**data)


def save_state(job_name: str, state: AppState) -> None:
    # ============================================================
    # save the state for a job, creates a job folder if needed
    # ============================================================

    ensure_job_dir(job_name) # make sure folder exists for job

    path = job_state_path(job_name=job_name)
    path.write_text(json.dumps(asdict(state), indent=2), encoding="utf-8")




# ============================================================
# Duplicated ARticles 
# ============================================================


def is_new_article(article: Article, state: AppState) -> bool:

    # ============================================================
    # Decide whether an article should be added to the job's markdown.

    # An article is new if:
    #   1. Its ID is not already in state.seen_ids, AND
    #   2. It has a valid published date, AND
    #   3. last_run is None — first run accepts everything with a date
    #   4. Its published date is after state.last_run
    # ============================================================


    # RULE 1 : already in markdown 
    if article.id in state.seen_ids:
        return False

    
    # RULE 2 : date is missing or unparseable then  discard  
    if not article.published:
        return False

    # RULE 3 : first run then accept everything with a valid date   
    if state.last_run is None:
        return True


    # RULE 4: only accept articles if they are newer than our last check 
    try: 
        article_dt = datetime.fromisoformat(article.published)
        last_run_dt = datetime.fromisoformat(state.last_run)

    except ValueError:
        # one of the time stamps was malformed, treat as not new 

        return False

    return article_dt > last_run_dt 
        

        





