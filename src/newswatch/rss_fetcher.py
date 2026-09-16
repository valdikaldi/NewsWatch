import feedparser

def fetch_feed(url: str):
    """
    Download and parse an RSS feed.
    """
    feed = feedparser.parse(url)
    return feed