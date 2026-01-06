import math
import pickle
from collections import Counter, defaultdict

from config import CACHE_DIR, CACHE_DOCMAP_PKL, CACHE_INDEX_PKL, CACHE_TERM_FREQUENCIES
from lib.tokenize import tokenize_single_str, tokenize_str
from lib.utils import load_movies


class InvertedIndex:
    def __init__(self) -> None:
        self.index: dict[str, set[int]] = defaultdict(set)
        self.docmap: dict[int, dict] = {}
        self.term_frequencies: dict[int, Counter[str]] = defaultdict(Counter)

    def __add_document(self, doc_id: int, text: str) -> None:
        tokens = tokenize_str(text)

        for token in tokens:
            self.term_frequencies[doc_id][token] += 1
            self.index[token].add(doc_id)

    def get_documents(self, term: str) -> list[int]:
        documents_set: set[int] = set()
        query_tokens = tokenize_str(term)

        for token in set(query_tokens):
            documents_set |= self.index.get(token, set())

        return sorted(documents_set)

    def get_tf(self, doc_id: int, term: str) -> int:
        token = tokenize_single_str(term)
        document_counters = self.term_frequencies.get(doc_id)

        if document_counters is None:
            return 0

        return document_counters.get(token, 0)

    def get_idf(self, term: str) -> float:
        token = tokenize_single_str(term)
        total_doc_count = len(self.docmap)
        term_match_doc_count = len(self.index[token])

        return math.log((total_doc_count + 1) / (term_match_doc_count + 1))

    def get_tf_idf(self, doc_id: int, term: str) -> float:
        tf = self.get_tf(doc_id, term)
        idf = self.get_idf(term)

        return tf * idf

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

        with open(CACHE_TERM_FREQUENCIES, "wb") as f:
            pickle.dump(
                dict(self.term_frequencies), f
            )  # convert default dict to nomal dict

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

        with open(CACHE_TERM_FREQUENCIES, "rb") as f:
            data = pickle.load(f)
            self.term_frequencies = defaultdict(
                Counter, data
            )  # reconvert dict back to default dict
