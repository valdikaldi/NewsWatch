import re
from pathlib import Path



# Project root: src/newswatch/paths.py → parent.parent.parent
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Directories
ASSETS_DIR = PROJECT_ROOT / "assets"
CONFIG_DIR = PROJECT_ROOT / "config"

DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Fixed files
LOCALES_CSV = ASSETS_DIR / "locales.csv"
CONFIG_FILE = CONFIG_DIR / "config.yaml"





def slugify(name: str) -> str:
    # ==================================
    # Convert a job name into a safe folder slug.
    #
    # 'Apple News'  -> 'apple-news'
    # 'MSFT / Bing' -> 'msft-bing'
    # '  Apple  '   -> 'apple'
    # ==================================
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug



def job_data_dir(job_name: str) -> Path:
    # ==================================
    # Return the data folder for a given job name
    # ==================================
    return DATA_DIR / slugify(job_name)




def job_articles_path(job_name: str) -> Path:
    # ==================================
    # Return the articles.md path for a given job
    # ==================================
    return job_data_dir(job_name) / "articles.md"




def job_state_path(job_name: str) -> Path:
    # ==================================
    # Return the state.json path for a given job
    # ==================================
    return job_data_dir(job_name) / "state.json"