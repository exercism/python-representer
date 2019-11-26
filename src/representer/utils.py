"""
Representer for Python.
"""
import ast
import astor
import errno
import json
import os
import re
from hashlib import md5
from functools import lru_cache
from pathlib import Path
from typing import NewType

import black


Slug = NewType("Slug", str)

SLUG_RE = re.compile(r"^[a-z]+(-[a-z]+)*$")


def slug(string: str) -> Slug:
    """
    Check if the given arg is a valid exercise slug.
    """
    if not SLUG_RE.match(string):
        raise ValueError(f"Does not match {SLUG_RE.pattern!r}: {string!r}")
    return Slug(string)


Directory = NewType("Directory", Path)


def directory(string: str) -> Directory:
    """
    Check if the given arg is a readable / writeable directory.
    """
    path = Path(string)
    if not path.is_dir():
        err = errno.ENOENT
        msg = os.strerror(err)
        raise FileNotFoundError(err, f"{msg}: {string!r}")
    if not os.access(path, os.R_OK | os.W_OK):
        err = errno.EACCES
        msg = os.strerror(err)
        raise PermissionError(err, f"{msg}: {string!r}")
    return Directory(path)


@lru_cache()
def md5sum(data: str) -> str:
    """
    Return the md5 sum of the given string.
    """
    return md5(data.encode("utf-8")).hexdigest()


def single_space(text: str) -> str:
    """
    Remove any blank lines in the text.
    """
    return re.sub(r"^\n{2,}", "\n", text)


def reformat(text: str) -> str:
    """
    Reformat a Python string with Black.
    """
    return black.format_str(single_space(text), mode=black.FileMode())


def to_json(data: dict) -> str:
    """
    Reformat to pretty-print JSON for writing to disk.
    """
    return json.dumps(data, indent=4, sort_keys=False)


def parse(source: str) -> ast.AST:
    """
    Wrapper around ast.parse.
    """
    return ast.parse(source)


def dump_tree(tree: ast.AST) -> str:
    """
    Dump a formatted string of the AST.
    """
    return astor.dump_tree(tree, indentation="  ", maxline=88)


def to_source(tree: ast.AST) -> str:
    """
    Dump the AST to generated source doe.
    """
    return astor.to_source(tree)
