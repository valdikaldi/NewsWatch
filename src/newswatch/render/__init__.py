# =========================================================
#   Render layer — produces output in different formats.
# 
#   Public API:
#     render_markdown(job_name, articles)  -> str    (markdown text)
#     save_markdown(job_name, articles)    -> None   (writes articles.md)
#     render_html_email(job_name, articles) -> str   (styled HTML email)
#     render_dashboard(jobs)                  -> str    (dashboard HTML page)
# =====================================================

from src.newswatch.render.dashboard import render_dashboard
from src.newswatch.render.email_html import render_html_email
from src.newswatch.render.markdown import render_markdown, save_markdown

__all__ = [
    "render_markdown",
    "save_markdown",
    "render_html_email",
    "render_dashboard",
]