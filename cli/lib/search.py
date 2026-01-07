from config import MAX_SEARCH_RESULTS
from lib.inverted_index import InvertedIndex

from .utils import print_search_results

search_index = InvertedIndex()
index_is_loaded = False


def search(query: str) -> None:
    if not index_is_loaded:
        load_index()

    search_results = []
    index_results = search_index.get_documents(query)
    for doc_id in index_results[:MAX_SEARCH_RESULTS]:
        search_results.append(search_index.docmap[doc_id]["title"])

    if not search_results:
        print("Nothing found")
    else:
        print_search_results(search_results)


def bm25_search(query: str, limit: int, k1: float, b: float) -> None:
    if not index_is_loaded:
        load_index()

    search_results: list[tuple[int, str, float]] = []
    index_results = search_index.bm25_search(query, limit, k1, b)
    for doc_id, bm25_score in index_results.items():
        search_results.append(
            (doc_id, search_index.docmap[doc_id]["title"], bm25_score)
        )

    if not search_results:
        print("Nothing found")
    else:
        print_search_results(search_results[:MAX_SEARCH_RESULTS], bm25=True)


def build_index() -> None:
    search_index.build()
    search_index.save()

    global index_is_loaded
    index_is_loaded = False


def calculate_tf(doc_id: int, term: str) -> None:
    if not index_is_loaded:
        load_index()

    count = search_index.get_tf(doc_id, term)
    print(f"Found {count} occurences for {term} in document {doc_id}!")


def calculate_idf(term: str) -> None:
    if not index_is_loaded:
        load_index()

    idf = search_index.get_idf(term)
    print(f"Inverse document frequency of '{term}': {idf:.2f}")


def calculate_tf_idf(doc_id: int, term: str) -> None:
    if not index_is_loaded:
        load_index()

    tf_idf = search_index.get_tf_idf(doc_id, term)
    print(f"TF-IDF score of '{term}' in document '{doc_id}': {tf_idf:.2f}")


def calculate_bm25_tf(doc_id: int, term: str, k1: float, b: float) -> None:
    if not index_is_loaded:
        load_index()

    bm25_tf = search_index.get_bm25_tf(doc_id, term, k1, b)
    print(f"BM25 TF score of '{term}' in document '{doc_id}': {bm25_tf:.2f}")


def calculate_bm25_idf(term: str) -> None:
    if not index_is_loaded:
        load_index()

    bm25_idf = search_index.get_bm25_idf(term)
    print(f"BM25 IDF score of '{term}': {bm25_idf:.2f}")


def index_search(query: str) -> list[str] | None:
    if not index_is_loaded:
        load_index()

    results = []
    index_results = search_index.get_documents(query)
    for doc_id in index_results[:MAX_SEARCH_RESULTS]:
        results.append(search_index.docmap[doc_id]["title"])

    return results


def load_index() -> bool:
    global index_is_loaded
    try:
        search_index.load()
        index_is_loaded = True
    except FileNotFoundError as err:
        print(err)
        return False

    return True


# def simple_keyword_search(query: str) -> list[str]:
#     results: list[str] = []
#     movies = load_movies()
#     query_tokens = tokenize_str(query)

#     for movie in movies:
#         movie_tokens = tokenize_str(movie["title"])

#         for query_token in query_tokens:
#             if has_substring(query_token, movie_tokens):
#                 results.append(movie["title"])
#                 break

#     return results


# def has_substring(query_token: str, movie_tokens: set) -> bool:
#     for movie_token in movie_tokens:
#         if query_token in movie_token:
#             return True
#     return False
