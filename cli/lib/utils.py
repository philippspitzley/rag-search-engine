import json

from config import MOVIES_JSON, STOPWORDS_TXT


def load_movies() -> list[dict]:
    with open(MOVIES_JSON, "r") as f:
        data = json.load(f)

    return data["movies"]


def load_stopwords() -> list[str]:
    with open(STOPWORDS_TXT, "r") as f:
        stop_words = f.read().splitlines()

    return stop_words


def print_search_results(
    movies: list[str] | list[tuple[str, int]], bm25: bool = False
) -> None:
    if bm25:
        for i, (doc_id, movie, score) in enumerate(movies, 1):
            print(f"{i}. ({doc_id}) {movie} - Score: {score:.2f}")
    else:
        for i, movie in enumerate(movies, 1):
            print(f"{i}. ({movie})")
