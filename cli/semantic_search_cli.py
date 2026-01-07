#!/usr/bin/env python3
import argparse
import textwrap

from config import TRANSFORMER_MODEL
from lib.semantic_search import verify_model


class _HelpFmt(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter
):
    pass


def cmd_verify_model(args: argparse.Namespace) -> None:
    print("Verify transformer model ...")
    verify_model(TRANSFORMER_MODEL)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Semantic Search CLI",
        epilog=textwrap.dedent(
            """\
            Examples:
                semantic_search thriller
            """
        ),
        formatter_class=_HelpFmt,
    )

    parser.add_argument(
        "--version", action="version", version="Semantic Search CLI 1.0.0"
    )

    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        metavar="<command>",
        help="Available commands",
    )

    ##########
    # Semantic-Search
    #######

    semantic_search_parser = subparsers.add_parser(
        "verify",
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

    semantic_search_parser.set_defaults(func=cmd_verify_model)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        parser.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()
