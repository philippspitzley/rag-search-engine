from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

# Data Files
DATA_DIR = PROJECT_ROOT / "data"
MOVIES_JSON = DATA_DIR / "movies.json"
STOPWORDS_TXT = DATA_DIR / "stopwords.txt"

# Cache Files
CACHE_DIR = PROJECT_ROOT / "cache"
CACHE_INDEX_PKL = CACHE_DIR / "index.pkl"
CACHE_DOCMAP_PKL = CACHE_DIR / "docmap.pkl"
CACHE_TERM_FREQUENCIES = CACHE_DIR / "term_frequencies.pkl"

# Search Settings
MAX_SEARCH_RESULTS = 5

# file_paths = [MOVIES_JSON, STOPWORDS_TXT, CACHE_INDEX_PKL, CACHE_DOCMAP_PKL]

# for file in file_paths:
#     if not file.exists():
#         raise FileNotFoundError(f"Data directory not found: {file}")
