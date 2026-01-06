from config import MAX_SEARCH_RESULTS
from lib.inverted_index import InvertedIndex

from .utils import print_search_results

search_index = InvertedIndex()
index_is_loaded = False


def search(query: str) -> None:
    search_results = index_search(query)
    if not search_results:
        print("Nothing found")
    else:
        print_search_results(search_results)


def build_index() -> None:
    search_index.build()
    search_index.save()

    global index_is_loaded
    index_is_loaded = False


def count_term(doc_id: int, term: str) -> None:
    if not index_is_loaded:
        load_index()

    count = search_index.get_tf(doc_id, term)
    print(f"Found {count} occurences for {term} in document {doc_id}!")


def index_search(query: str) -> list[str] | None:
    if not index_is_loaded:
        load_index()

    results = []
    index_results = search_index.get_documents(query)
    for index in index_results[:MAX_SEARCH_RESULTS]:
        results.append(search_index.docmap[index]["title"])

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
