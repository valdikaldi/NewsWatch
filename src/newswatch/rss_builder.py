
import csv 
from pathlib import Path
from urllib.parse import quote_plus
from src.newswatch.paths import LOCALES_CSV

def load_locales() -> dict[str, dict[str,str]]:
    # ===================================================
    # Load locales.csv file and return a dict keyed by ceid
    # ===================================================

    locales: dict[str, dict[str,str]] = {}

    with LOCALES_CSV.open(mode="r", encoding="utf-8") as file: 
        reader = csv.DictReader(file)
        for row in reader:
            locales[row["ceid"]] = {
                "hl": row["hl"],
                "gl": row["gl"],
                "country": row["country"]
            }

        return locales

# read the csv file
LOCALES = load_locales()



def build_feed_url(query:str, exact_match: bool = True, include_site: str | None = None, locale:str = "US:en", time_range: str | None = "1d",) -> str:
    # =========================================================
    # Build a google news rss search url for a given query 
    # =========================================================
    
    # Check locale
    if locale not in LOCALES:
        raise ValueError(
            f"Unknown locale '{locale}'. "
            f"Pick a CEID from assets/locales.csv (e.g. 'US:en', 'GB:en', 'DE:de')."
        )

    # setup exact match if needed
    term = f'"{query}"' if exact_match else query

    # setup site filter if included
    if include_site:
        term = f"site:{include_site} {term}"

    # settup time range filter if included
    if time_range:
        term = f"{term} when:{time_range}"    

    # Create the rss url     
    encoded = quote_plus(term)
    locale_data = LOCALES[locale]
    hl = locale_data["hl"]
    gl = locale_data["gl"].upper()

    url = (
        "https://news.google.com/rss/search"
        f"?q={encoded}&hl={hl}&gl={gl}&ceid={locale}"
    )

    return url


if __name__ == "__main__":
    print("Basic (US):  ", build_feed_url("Apple Inc"))
    print("UK:          ", build_feed_url("Apple Inc", locale="GB:en"))
    print("Germany:     ", build_feed_url("Apple Inc", locale="DE:de"))
    print("BBC only:    ", build_feed_url("Apple Inc", include_site="bbc.com"))
    print("Not exact:   ", build_feed_url("Apple Inc", exact_match=False))
    