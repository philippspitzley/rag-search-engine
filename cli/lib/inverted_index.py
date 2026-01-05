import pickle
from collections import defaultdict

from config import CACHE_DIR, CACHE_DOCMAP_PKL, CACHE_INDEX_PKL
from lib.tokenize import tokenize_str
from lib.utils import load_movies


class InvertedIndex:
    def __init__(self) -> None:
        self.index: dict[str, set[int]] = defaultdict(set)
        self.docmap: dict[int, dict] = {}

    def __add_document(self, doc_id: int, text: str) -> None:
        tokens = tokenize_str(text)

        for token in tokens:
            self.index[token].add(doc_id)

    def get_documents(self, term: str) -> list[int]:
        documents_set: set[int] = set()
        query_tokens = tokenize_str(term)

        for token in query_tokens:
            documents_set |= self.index.get(token, set())

        return sorted(documents_set)

    def build(self) -> None:
        for movie in load_movies():
            key = f"{movie['title']} {movie['description']}"
            self.__add_document(movie["id"], key)
            self.docmap[movie["id"]] = movie

    def save(self) -> None:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        with open(CACHE_INDEX_PKL, "wb") as f:
            pickle.dump(dict(self.index), f)  # convert default dict to nomal dict

        with open(CACHE_DOCMAP_PKL, "wb") as f:
            pickle.dump(self.docmap, f)

    def load(self) -> None:
        if not CACHE_INDEX_PKL.exists() or not CACHE_DOCMAP_PKL.exists():
            raise FileNotFoundError(
                f"Files not found: {CACHE_INDEX_PKL}, {CACHE_DOCMAP_PKL}"
            )

        with open(CACHE_INDEX_PKL, "rb") as f:
            data = pickle.load(f)
            self.index = defaultdict(set, data)  # reconvert dict back to default dict

        with open(CACHE_DOCMAP_PKL, "rb") as f:
            self.docmap = pickle.load(f)
