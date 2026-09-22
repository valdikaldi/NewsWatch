#=======================================================
# Shared Jinja2 setup for all renderers.

# This module is internal to the render package. Do not import from it
# outside `src/newswatch/render/`.
#=======================================================




from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from src.newswatch.paths import PROJECT_ROOT


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




def build_environment() -> Environment:
    # Build a Jinja2 environment that loads templates from TEMPLATES_DIR.
    # Registers the custom `format_date` filter so templates can use
    # `{{ some_iso_date | format_date }}`.

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=True,
    )
    env.filters["format_date"] = format_date
    return env


