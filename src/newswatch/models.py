from dataclasses import dataclass, field



# ==================================================================
#  NEWS ARTICLES
# ==================================================================
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







# ==================================================================
#  CONFIG FILE DATA CLASSES
# ---- what the user defines in config.yaml - ---
# ==================================================================

@dataclass
class JobConfig:
    # ===========================
    # One monitoring job
    # ===========================

    name: str
    query: str
    exact_match: bool = True
    include_site: str | None = None
    locale: str = "US:en"
    time_range: str | None = "7d"


@dataclass
class Settings:
    # ===========================
    # Global settings shared across all jobs 
    # ===========================
    
    interval_days: int = 7
    email: str = ""
    max_articles: int = 50


@dataclass
class Config:
    # ===========================
    # The full configuration
    # ===========================
    settings: Settings
    jobs: list[JobConfig] = field(default_factory=list)




# ==================================================================
#  STATE - last rss fetch , state of processed articles
# --- what the program remembers between runs----
# ==================================================================

@dataclass
class AppState:
    last_run: str | None = None 
    last_sent: str | None = None 
    new_since_last_send: bool = False
    seen_ids: list[str] = field(default_factory=list)