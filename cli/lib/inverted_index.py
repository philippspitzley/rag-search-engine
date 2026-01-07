import math
import pickle
from collections import Counter, defaultdict

from config import (
    CACHE_DIR,
    CACHE_DOC_LENGTH_FILE,
    CACHE_DOCMAP_FILE,
    CACHE_INDEX_FILE,
    CACHE_TF_FILE,
)
from lib.tokenize import tokenize_single_str, tokenize_str
from lib.utils import load_movies


class InvertedIndex:
    def __init__(self) -> None:
        self.index: dict[str, set[int]] = defaultdict(set)
        self.docmap: dict[int, dict] = {}
        self.term_frequencies: dict[int, Counter[str]] = defaultdict(Counter)
        self.doc_length: dict[int, int] = {}

    def __add_document(self, doc_id: int, text: str) -> None:
        tokens = tokenize_str(text)
        self.doc_length[doc_id] = len(tokens)

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

    def get_bm25_tf(self, doc_id: int, term: str, k1: float, b: float) -> float:
        tf = self.get_tf(doc_id, term)

        doc_len = self.doc_length.get(doc_id, 0)
        avg_doc_len = self.__get_avg_doc_length()
        len_norm = 1 - b + b * (doc_len / avg_doc_len)

        # BM25 Algorithm:
        # tf -> total number of terms in doc
        # k1 -> constant that controls diminishing returns for documents with higher term frequency; default=1.5
        # b -> constat that controls length nomalization strength; b=0 -> no normalization; b=1 -> full normalization; default=0.75
        # len_norm -> normalization factor
        # (tf * (k1 + 1)) / (tf + k1 * len_norm)

        return (tf * (k1 + 1)) / (tf + k1 * len_norm)

    def get_bm25_idf(self, term: str) -> float:
        token = tokenize_single_str(term)
        total_doc_count = len(self.docmap)
        term_match_doc_count = len(self.index[token])

        # BM25 Algorithm:
        # N -> total number of docs
        # df -> docs with the term
        # (N - df) -> docs without term
        # 0.5 -> laplace smoothing
        # 1 -> ensures idf is always positve; handles edge cases
        # log((N - df + 0.5) / (df + 0.5) + 1)

        return math.log(
            (total_doc_count - term_match_doc_count + 0.5)
            / (term_match_doc_count + 0.5)
            + 1
        )

    def get_bm25_score(self, doc_id: int, term: str, k1: float, b: float) -> float:
        tf = self.get_bm25_tf(doc_id, term, k1, b)
        idf = self.get_bm25_idf(term)
        return tf * idf

    def bm25_search(
        self, query: str, limit: int, k1: float, b: float
    ) -> dict[int, float]:
        tokens = tokenize_str(query)

        # calculate bm25 scores for each token and each document
        scores: dict[int, float] = defaultdict(float)

        for token in tokens:
            
            for doc_id in self.index.get(token, []):
                scores[doc_id] += self.get_bm25_score(doc_id, token, k1, b)

        # sort values of dict in descending order
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

        return dict(sorted_scores[:limit])

    def __get_avg_doc_length(self) -> float:
        if not self.doc_length:
            return 0

        return sum(self.doc_length.values()) / len(self.doc_length)

    def build(self) -> None:
        for movie in load_movies():
            key = f"{movie['title']} {movie['description']}"
            self.__add_document(movie["id"], key)
            self.docmap[movie["id"]] = movie

    def save(self) -> None:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        with open(CACHE_INDEX_FILE, "wb") as f:
            pickle.dump(dict(self.index), f)  # convert default dict to nomal dict

        with open(CACHE_DOCMAP_FILE, "wb") as f:
            pickle.dump(self.docmap, f)

        with open(CACHE_TF_FILE, "wb") as f:
            pickle.dump(
                dict(self.term_frequencies), f
            )  # convert default dict to nomal dict

        with open(CACHE_DOC_LENGTH_FILE, "wb") as f:
            pickle.dump(self.doc_length, f)

    def load(self) -> None:
        if not CACHE_INDEX_FILE.exists() or not CACHE_DOCMAP_FILE.exists():
            raise FileNotFoundError(
                f"Files not found: {CACHE_INDEX_FILE}, {CACHE_DOCMAP_FILE}"
            )

        with open(CACHE_INDEX_FILE, "rb") as f:
            data = pickle.load(f)
            self.index = defaultdict(set, data)  # reconvert dict back to default dict

        with open(CACHE_DOCMAP_FILE, "rb") as f:
            self.docmap = pickle.load(f)

        with open(CACHE_TF_FILE, "rb") as f:
            data = pickle.load(f)
            self.term_frequencies = defaultdict(
                Counter, data
            )  # reconvert dict back to default dict

        with open(CACHE_DOC_LENGTH_FILE, "rb") as f:
            self.doc_length = pickle.load(f)
