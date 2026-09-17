# ==================================================
#
#                   NOTIFIER    
#   
#   the notifier does not send emails. it simply decieds
# i.e. the mailer handles actually sending the mail 
#  
# ==================================================

from datetime import datetime, timezone

from src.newswatch.models import AppState, Settings
from src.newswatch.state import now_iso


def should_notify(state: AppState, settings: Settings) -> bool:
    # ========================================================
    # Decide whether an email should be sent right now

    # An email is sent if BOTH:
    #   1. There are new articles since the last email, AND
    #   2. Either:
    #      - we've never sent an email before (first run), OR
    #      - the interval has elapsed since the last email.

    # Args:
    #     state: The job's current AppState.
    #     settings: Global settings (includes interval_days).

    # Returns:
    #     True if the mailer should send an email now.
    # ========================================================
    
    # Rule 1: is there anything to report?
    if not state.new_since_last_send:
        return False

    # Rule 2a: first run — never sent an email before
    if state.last_sent is None:
        return True

    # Rule 2b: has the interval elapsed?
    try:
        last_sent_dt = datetime.fromisoformat(state.last_sent)
    except ValueError:
        # Malformed timestamp in state — treat as first run (send).
        # This is defensive; state should always be valid ISO 8601.
        return True

    now = datetime.now(timezone.utc)
    elapsed_days = (now - last_sent_dt).days

    return elapsed_days >= settings.interval_days


def mark_sent(state: AppState) -> None:
    # ========================================================
    # Update state to reflect that an email was just sent.

    # Modifies `state` in place. Caller is responsible for saving it.
    # ========================================================
    
    state.last_sent = now_iso()
    state.new_since_last_send = False