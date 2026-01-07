#!/usr/bin/env python3
import argparse
import textwrap

from config import TRANSFORMER_MODEL
from lib.semantic_search import embed_text, verify_model


class _HelpFmt(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter
):
    pass


def cmd_verify_model(args: argparse.Namespace) -> None:
    print("Verify transformer model ...")
    verify_model(TRANSFORMER_MODEL)


def cmd_embed_text(args: argparse.Namespace) -> None:
    print("Embedding text ...")
    embed_text(args.text)


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

    ###############
    # Verify Model
    ############

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

    #############
    # Embed Text
    ##########

    embed_text_parser = subparsers.add_parser(
        "embed_text",
        aliases=["et"],
        help="Embed text.",
        description="embed text",
        formatter_class=_HelpFmt,
        epilog=textwrap.dedent(
            """\
            Examples:

              keyword_search_cli.py search "matrix"
              keyword_search_cli.py s inception
            """
        ),
    )

    embed_text_parser.add_argument(
        "text",
        type=str,
        help="text to embed",
    )

    embed_text_parser.set_defaults(func=cmd_embed_text)
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
