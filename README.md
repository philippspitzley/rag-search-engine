# RAG Search Engine

A simple keyword-based search engine for movie data using an inverted index with tokenization, stopword removal, and stemming (PorterStemmer).

## Features
- Build and persist an inverted index over movie titles and descriptions
- Tokenization pipeline: punctuation removal, stopword filtering, and stemming
- Fast keyword search over indexed data
- Configurable result limits

## Requirements
- Python 3.13+
- Dependencies: `nltk==3.9.1`

> [!IMPORTANT]  
> This repository is in early development; the instructions below may be outdated and will be updated as the project evolves.


## Quick Start
1. Install dependencies:
   - Using `uv`:
     - `uv sync` (or `uv pip install -r pyproject.toml`)
   - Using `pip`:
     - `pip install -r requirements.txt` (alternatively `pip install nltk==3.9.1`)

2. Prepare data files in `data/`:
   - `movies.json` with a `{"movies": [...]}` array of movie objects containing at least `id`, `title`, `description`
   - `stopwords.txt` (newline-separated stop words)

3. Build the search index:
   - `python cli/keyword_search_cli.py build`

4. Run a search:
   - `python cli/keyword_search_cli.py search "your query"`

## Commands
- `build`: Build and cache the inverted index and document map
- `search "<query>"`: Search for matching movies and print top results

## Configuration
- See `cli/config.py` for paths and settings:
  - Data: `data/movies.json`, `data/stopwords.txt`
  - Cache: `cache/index.pkl`, `cache/docmap.pkl`
  - `MAX_SEARCH_RESULTS`: limit returned results (default: 5)

## Project Structure
- `cli/keyword_search_cli.py`: CLI entrypoint
- `cli/lib/inverted_index.py`: Inverted index build/load/save and lookup
- `cli/lib/tokenize.py`: Tokenization utilities (punctuation removal, stopwords, stemming)
- `cli/lib/utils.py`: Data loading and output formatting
- `cli/config.py`: Project paths and settings

## Notes
- Ensure data files exist before running `build`
- The index must be built before running `search`
