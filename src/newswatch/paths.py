from pathlib import Path


# Project root: src/newswatch/paths.py → parent.parent.parent
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Directories
ASSETS_DIR = PROJECT_ROOT / "assets"
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"

# Files
LOCALES_CSV = ASSETS_DIR / "locales.csv"
CONFIG_FILE = CONFIG_DIR / "config.json"
ARTICLES_MD = DATA_DIR / "articles.md"
STATE_JSON = DATA_DIR / "state.json"