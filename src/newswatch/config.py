from pathlib import Path

import yaml

from src.newswatch.models import JobConfig, Config, Settings
from src.newswatch.paths import CONFIG_FILE




def load_config(path: Path = CONFIG_FILE) -> Config:
    # =============================================
    # Load and validate config.yaml.
    #
    #  Raises:
    #     - FileNotFoundError: if the config file doesn't exist.
    #     - ValueError: if validation fails (duplicate names, missing fields, etc.).
    # =============================================


    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open(encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    if not isinstance(raw, dict):
        raise ValueError("config.yaml must be a YAML mapping at the top level.")

    # ================= Settings =================
    settings_raw = raw.get("settings", {})
    if not settings_raw.get("email"):
        raise ValueError("config.yaml is missing 'settings.email'.")

    settings = Settings(
        interval_days=int(settings_raw.get("interval_days", 7)),
        email=settings_raw["email"],
        max_articles=int(settings_raw.get("max_articles", 50)),
    )

    if settings.interval_days < 1:
        raise ValueError("settings.interval_days must be at least 1.")

    if settings.max_articles < 1:
        raise ValueError("settings.max_articles must be at least 1.")

    # ================= Jobs =================
    jobs_raw = raw.get("jobs", [])
    if not jobs_raw:
        raise ValueError("config.yaml must define at least one job.")

    jobs: list[JobConfig] = []
    seen_names: set[str] = set()

    for i, job_raw in enumerate(jobs_raw, start=1):
        name = job_raw.get("name", "").strip()
        if not name:
            raise ValueError(f"Job #{i} is missing 'name'.")

        if name in seen_names:
            raise ValueError(
                f"Duplicate job name: '{name}'. Job names must be unique."
            )
        seen_names.add(name)

        query = job_raw.get("query", "").strip()
        if not query:
            raise ValueError(f"Job '{name}' is missing 'query'.")

        jobs.append(JobConfig(
            name=name,
            query=query,
            exact_match=bool(job_raw.get("exact_match", True)),
            include_site=job_raw.get("include_site") or None,
            locale=job_raw.get("locale", "US:en"),
            time_range=job_raw.get("time_range") or None,
        ))

    return Config(settings=settings, jobs=jobs)