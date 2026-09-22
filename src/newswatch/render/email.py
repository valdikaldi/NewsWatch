# =====================================================================================
#   Render articles as a styled HTML email.
 
# The template (templates/email.html) is pre-compiled from templates/email.mjml
# using the MJML CLI. This module does NOT compile MJML — it only fills in the
# Jinja2 placeholders at runtime.

# ================================================================================= 

 
from src.newswatch.models import Article
from src.newswatch.render._jinja import build_environment, format_date
from src.newswatch.state import now_iso

def render_html_email(job_name: str, articles: list[Article]) -> str:
    #  Render the HTML email for a job.
    # Args:
    #     job_name: The job's name (e.g. "Apple News").
    #     articles: List of Article objects, newest first.
    # Returns:
    #     The complete HTML string, ready to send.
   
    env = build_environment()
    template = env.get_template("email.html")

    return template.render(
        job_name=job_name,
        articles=articles,
        updated=format_date(now_iso()),
    )