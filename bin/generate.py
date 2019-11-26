#! /usr/bin/env python3
"""
CLI for the representer for the Python track on Exercism.io.
"""
from argparse import ArgumentParser, ArgumentTypeError

import representer


def _slug(arg):
    try:
        return representer.utils.slug(arg)
    except ValueError as err:
        raise ArgumentTypeError(str(err))


def _directory(arg):
    try:
        return representer.utils.directory(arg)
    except (FileNotFoundError, PermissionError) as err:
        raise ArgumentTypeError(str(err))


def main():
    """
    Parse CLI arguments and create a representation.txt.
    """
    parser = ArgumentParser(
        description="Produce a normalized representation of a Python exercise."
    )

    parser.add_argument(
        "slug", metavar="SLUG", type=_slug, help="name of the exercise to process",
    )

    parser.add_argument(
        "directory",
        metavar="DIR",
        type=_directory,
        help="directory where the [EXERCISE.py] file is located",
    )

    args = parser.parse_args()
    representer.represent(args.slug, args.directory)


if __name__ == "__main__":
    main()
