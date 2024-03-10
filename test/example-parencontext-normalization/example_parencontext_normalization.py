"""Examples of Parenthesized Context Managers. New feature in Python 3.10"""


#!/usr/bin/python3
"""convert json to jsonl"""

from argparse import ArgumentParser
import json

def main():
    args = parse_args()

    # Context Mgrs
    with (
        open(args.in_filename) as in_file,
        open(args.out_filename, mode="wt") as out_file,
    ):
        records = json.load(in_file)
        for record in records:
            out_file.write(json.dumps(record) + "\n")


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("in_filename")
    parser.add_argument("out_filename")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()





# Examples from python docs
# https://docs.python.org/3/whatsnew/3.10.html#parenthesized-context-managers

    def CtxManager(): pass
    def CtxManager1(): pass
    def CtxManager2(): pass
    def CtxManager3(): pass

    with (CtxManager() as example):
        ...

    with (
        CtxManager1(),
        CtxManager2()
    ):
        ...

    with (CtxManager1() as example,
        CtxManager2()):
        ...

    with (CtxManager1(),
        CtxManager2() as example):
        ...

    with (
        CtxManager1() as example1,
        CtxManager2() as example2
    ):
        ...
    with (
        CtxManager1() as example1,
        CtxManager2() as example2,
        CtxManager3() as example3,
    ):
        ...