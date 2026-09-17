import hashlib
from src.newswatch.models import Article
from datetime import timezone
from email.utils import parsedate_to_datetime




def generate_id_from_url(url: str) -> str:
    # ==================================================================
    #  Generate a stable 12-character ID from a URL  
    # ==================================================================
    
    return hashlib.sha1(string=url.encode("utf-8")).hexdigest()[:12]


def normalize_published(raw:str) -> str:
    # ==================================================================
    # Convert an RSS date sting (rfc 822) to a ISO 8601 UTC string 
    # 
    # e.g. "Mon, 08 Jan 2026 09:12:00 GMT"  -> "2026-01-08T09:12:00+00:00"
    # 
    # Returns "" if the input is empty or cannot be parsed.
    # ==================================================================

    if not raw:
        return ""

    try:
        dt = parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        return ""

    # if parsed datetime has no timezone assume UTC 
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)


    # convert To UTC so alll timestamps are directly comparable 
    dt = dt.astimezone(timezone.utc)

    return dt.isoformat() #retuzrn the date time as  ISO 8601 string 


def parse_entry(entry) -> Article:
    # ==================================================================
    # Convert a single feedparser entry into an Article object
    # ==================================================================

    url = entry.get("link", "")

    data = Article(
        id=generate_id_from_url(url),
        title=entry.get("title", "").strip(),
        url=url,
        source=entry.get("source", {}).get("title", "Unknown"),
        published=normalize_published(entry.get("published", "")),
        # published=entry.get("published", ""),
    )

    return data