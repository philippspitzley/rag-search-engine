#!/usr/bin/env python3

import argparse

from lib.search import build_index, search


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    subparsers.add_parser("build", help="Build Search Index")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            search(args.query)
        case "build":
            print("Building search index...")
            build_index()
            print("Search index succesfully built!")
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
