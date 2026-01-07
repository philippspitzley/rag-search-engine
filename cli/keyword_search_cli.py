#!/usr/bin/env python3
import argparse
import textwrap

from config import BM25_B, BM25_K1, MAX_SEARCH_RESULTS
from lib.search import (
    bm25_search,
    build_index,
    calculate_bm25_idf,
    calculate_bm25_tf,
    calculate_idf,
    calculate_tf,
    calculate_tf_idf,
    search,
)


class _HelpFmt(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter
):
    pass


def cmd_search(args: argparse.Namespace) -> None:
    print(f"Searching for: {args.query}")
    search(args.query)


def cmd_bm25_search(args: argparse.Namespace) -> None:
    print(f"Searching for: {args.query}")
    bm25_search(args.query, args.limit, BM25_K1, BM25_B)


def cmd_build(_: argparse.Namespace) -> None:
    print("Building search index ...")
    build_index()
    print("Search index successfully built!")


def cmd_tf(args: argparse.Namespace) -> None:
    print(f"Calculating occurrences of {args.term} in document {args.doc_id} ...")
    calculate_tf(args.doc_id, args.term)


def cmd_idf(args: argparse.Namespace) -> None:
    print(f"Calculating IDF for {args.term} ...")
    calculate_idf(args.term)


def cmd_tf_idf(args: argparse.Namespace) -> None:
    print(f"Calculating TF-IDF for {args.term} ...")
    calculate_tf_idf(args.doc_id, args.term)


def cmd_bm25_tf(args: argparse.Namespace) -> None:
    print(f"Calculating TF-IDF for {args.term} ...")
    calculate_bm25_tf(args.doc_id, args.term, args.k1, args.b)


def cmd_bm25_idf(args: argparse.Namespace) -> None:
    print(f"Calculation BM25-IDF for {args.term} ...")
    calculate_bm25_idf(args.term)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Keyword search over the movie dataset. Build the index, run BM25 search, and inspect TF/IDF.",
        epilog=textwrap.dedent(
            """\
            Examples:
              keyword_search_cli.py build
              keyword_search_cli.py search "the matrix"
              keyword_search_cli.py tf 42 matrix
              keyword_search_cli.py idf matrix
              keyword_search_cli.py bmidf matrix

            """
        ),
        formatter_class=_HelpFmt,
    )

    parser.add_argument(
        "--version", action="version", version="Keyword Search CLI 1.0.0"
    )

    subparsers = parser.add_subparsers(
        title="commands", dest="command", metavar="<command>", help="Available commands"
    )

    ##########
    # Search
    #######

    search_parser = subparsers.add_parser(
        "search",
        aliases=["s"],
        help="Search the corpus using BM25 ranking",
        description="Search the corpus using BM25 ranking",
        formatter_class=_HelpFmt,
        epilog=textwrap.dedent(
            """\
            Examples:

              keyword_search_cli.py search "matrix"
              keyword_search_cli.py s inception
            """
        ),
    )
    search_parser.add_argument(
        "query",
        type=str,
        help="Free-text query to search for",
    )
    search_parser.set_defaults(func=cmd_search)

    ##########
    # BM25-Search
    #######

    bm25_search_parser = subparsers.add_parser(
        "bm25search",
        aliases=["bms"],
        help="Search movies using full BM25 scoring.",
        description="Search the corpus using full BM25 scoring",
        formatter_class=_HelpFmt,
        epilog=textwrap.dedent(
            """\
             Examples:

               keyword_search_cli.py bm25search "love story"
               keyword_search_cli.py bms "action bear"
             """
        ),
    )
    bm25_search_parser.add_argument(
        "query",
        type=str,
        help="Free-text query to search for",
    )
    bm25_search_parser.add_argument(
        "limit",
        type=int,
        nargs="?",
        default=MAX_SEARCH_RESULTS,
        help="Free-text query to search for",
    )
    bm25_search_parser.set_defaults(func=cmd_bm25_search)

    #########
    # Build
    ######

    build_cmd = subparsers.add_parser(
        "build", aliases=["b"], help="Build the search index", formatter_class=_HelpFmt
    )
    build_cmd.set_defaults(func=cmd_build)

    ######################
    # TF (Term Frequency)
    ####################

    tf_parser = subparsers.add_parser(
        "tf",
        help="Show term frequency (TF) — count occurrences of a term in a single document",
        formatter_class=_HelpFmt,
        epilog=textwrap.dedent(
            """\
            Examples:

              keyword_search_cli.py tf 42 matrix
            """
        ),
    )
    tf_parser.add_argument("doc_id", type=int, help="Document ID")
    tf_parser.add_argument("term", type=str, help="Term to count")
    tf_parser.set_defaults(func=cmd_tf)

    ###################################
    # IDF (Inverse Document Frequency)
    #################################

    idf_parser = subparsers.add_parser(
        "idf",
        help="Show inverse document frequency (IDF) across the corpus",
        formatter_class=_HelpFmt,
        epilog=textwrap.dedent(
            """\
            Examples:

              keyword_search_cli.py idf sience
            """
        ),
    )
    idf_parser.add_argument("term", type=str, help="Term to evaluate")
    idf_parser.set_defaults(func=cmd_idf)

    #######################################################
    # TF-IDF (Term Frequency - Inverse Document Frequency)
    #####################################################

    tfidf_parser = subparsers.add_parser(
        "tfidf",
        help="Show term frequency - inverse document frequency (TF-IDF) across the corpus",
        formatter_class=_HelpFmt,
        epilog=textwrap.dedent(
            """\
            Example:

              keyword_search_cli.py tfidf matrix
            """
        ),
    )
    tfidf_parser.add_argument("doc_id", type=int, help="Document ID")
    tfidf_parser.add_argument("term", type=str, help="Term to evaluate")
    tfidf_parser.set_defaults(func=cmd_tf_idf)

    ################################
    # Bm25-TF (BM25 Term Frequency)
    ##############################

    bm25_tf_parser = subparsers.add_parser(
        "bm25tf",
        help="Show term frequency - inverse document frequency (BM25-TF) across the corpus",
        formatter_class=_HelpFmt,
        epilog=textwrap.dedent(
            """\
            Example:

              keyword_search_cli.py bm25tf inception 23
              keyword_search_cli.py bm25tf inception 12 1.2

            """
        ),
    )
    bm25_tf_parser.add_argument("doc_id", type=int, help="Document ID")
    bm25_tf_parser.add_argument("term", type=str, help="Term to evaluate")
    bm25_tf_parser.add_argument(
        "k1",
        type=float,
        nargs="?",
        default=BM25_K1,
        help="Tunable BM25 K1 parameter to control diminishing return for higher term frequencies",
    )
    bm25_tf_parser.add_argument(
        "b",
        type=float,
        nargs="?",
        default=BM25_B,
        help="Tunable BM25 B parameter to control document length nomalization",
    )
    bm25_tf_parser.set_defaults(func=cmd_bm25_tf)

    #############################################
    # BM25-IDF (BM25 Inverse Document Frequency)
    ###########################################

    bm25_idf_parser = subparsers.add_parser(
        "bm25idf",
        help="Show term frequency - inverse document frequency (BM25-IDF) across the corpus",
        formatter_class=_HelpFmt,
        epilog=textwrap.dedent(
            """\
             Example:

               keyword_search_cli.py bm25idf interstellar
             """
        ),
    )

    bm25_idf_parser.add_argument(
        "term",
        type=str,
        help="Term to evaluate",
    )
    bm25_idf_parser.set_defaults(func=cmd_bm25_idf)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        parser.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()
