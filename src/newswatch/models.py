from dataclasses import dataclass


@dataclass
class Article:
    # ==================================================================
    #  A single News Article 
    #
    # 'id' is a stable 12-char hash of the url ; used for deduplication
    # ==================================================================

    id: str
    title: str
    url: str
    source: str
    published: str

    # ---------- future extention - adding ai models
    # summary: str | None = None
    # sentiment: float | None = None
    # category: str | None = None
