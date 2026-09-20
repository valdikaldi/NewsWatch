# =====================================================================================
# Render articles as a styled HTML email.

# The template (templates/email.html) is pre-compiled from templates/email.mjml
# using the MJML CLI. This module does NOT compile MJML — it only fills in the
# Jinja2 placeholders at runtime.
# ================================================================================= 


from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from src.newswatch.models import Article
from src.newswatch.paths import PROJECT_ROOT
from src.newswatch.state import now_iso

 

# Where the email template lives
TEMPLATES_DIR = PROJECT_ROOT / "templates"





def format_date(iso_string: str) -> str:
    # Convert an ISO 8601 timestamp to a human-readable string.
    # Example:
    #     "2026-09-20T08:00:00+00:00"  ->  "20 Sep 2026, 08:00 UTC"

    # Returns the input unchanged if it can't be parsed.

    if not iso_string:
        return ""

    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%d %b %Y, %H:%M UTC")
    except ValueError:
        return iso_string




def _build_environment() -> Environment:
    # Build a Jinja2 environment that loads templates from TEMPLATES_DIR.
    # Registers the custom `format_date` filter so templates can use
    # `{{ some_iso_date | format_date }}`.

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=True,
    )
    env.filters["format_date"] = format_date
    return env





def render_html_email(job_name: str, articles: list[Article]) -> str:
    #  Render the HTML email for a job.
    # Args:
    #     job_name: The job's name (e.g. "Apple News").
    #     articles: List of Article objects, newest first.
    # Returns:
    #     The complete HTML string, ready to send.
   
    env = _build_environment()
    template = env.get_template("email.html")

    return template.render(
        job_name=job_name,
        articles=articles,
        updated=format_date(now_iso()),
    )