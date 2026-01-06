#!/usr/bin/env python3
import argparse

from lib.search import build_index, calculate_idf, count_term, search


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Search
    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    # Build
    subparsers.add_parser("build", help="Build Search Index")

    # Frequencies
    freq_parser = subparsers.add_parser(
        "tf", help="Show count of matches for a documents search term. "
    )
    freq_parser.add_argument("freq_doc_id", type=int, help="Document id")
    freq_parser.add_argument("freq_term", type=str, help="Search term")

    # Inverse Document Frequency (IDF)
    idf_parser = subparsers.add_parser(
        "idf", help="Calculate inverse document frequency"
    )
    idf_parser.add_argument("idf_term", type=str, help="Search term")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            search(args.query)
        case "build":
            print("Building search index ...")
            build_index()
            print("Search index succesfully built!")
        case "tf":
            print(
                f"Calculating occurences of {args.freq_term} in document {args.freq_doc_id} ..."
            )
            count_term(args.freq_doc_id, args.freq_term)
        case "idf":
            print(f"Calculating IDF for {args.idf_term} ...")
            calculate_idf(args.idf_term)
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
