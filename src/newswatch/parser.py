import hashlib
from src.newswatch.models import Article

def generate_id_from_url(url: str) -> str:
    # ==================================================================
    #  Generate a stable 12-character ID from a URL  
    # ==================================================================
    
    return hashlib.sha1(string=url.encode("utf-8")).hexdigest()[:12]


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
        published=entry.get("published", ""),
    )

    return data