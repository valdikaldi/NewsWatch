from src.newswatch.config import load_config


def main() -> None:
    config = load_config()

    print("=== Settings ===")
    print(f"Interval:      {config.settings.interval_days} days")
    print(f"Email:         {config.settings.email}")
    print(f"Max articles:  {config.settings.max_articles}")

    print(f"\n=== Jobs ({len(config.jobs)}) ===")
    for job in config.jobs:
        print(f"  [{job.name}]")
        print(f"    query:       {job.query}")
        print(f"    exact_match: {job.exact_match}")
        print(f"    site:        {job.include_site}")
        print(f"    locale:      {job.locale}")
        print(f"    time_range:  {job.time_range}")


if __name__ == "__main__":
    main()