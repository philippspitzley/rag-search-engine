from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

# Data Files
DATA_DIR = PROJECT_ROOT / "data"
MOVIES_JSON = DATA_DIR / "movies.json"
STOPWORDS_TXT = DATA_DIR / "stopwords.txt"

# Cache Files
CACHE_DIR = PROJECT_ROOT / "cache"
CACHE_INDEX_FILE = CACHE_DIR / "index.pkl"
CACHE_DOCMAP_FILE = CACHE_DIR / "docmap.pkl"
CACHE_TF_FILE = CACHE_DIR / "term_frequencies.pkl"
CACHE_DOC_LENGTH_FILE = CACHE_DIR / "doc_lengths.pkl"

# Search Settings
MAX_SEARCH_RESULTS = 5
BM25_K1 = 1.5
BM25_B = 0.75

# Semantic Search Settings
TRANSFORMER_MODEL = "all-MiniLM-L6-v2"
