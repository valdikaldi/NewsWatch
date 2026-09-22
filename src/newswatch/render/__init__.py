# =========================================================
#   Render layer — produces output in different formats.
# 
#   Public API:
#     render_markdown(job_name, articles)  -> str    (markdown text)
#     save_markdown(job_name, articles)    -> None   (writes articles.md)
#     render_html_email(job_name, articles) -> str   (styled HTML email)
# =====================================================

from src.newswatch.render.email import render_html_email
from src.newswatch.render.markdown import render_markdown, save_markdown

__all__ = [
    "render_markdown",
    "save_markdown",
    "render_html_email",
]