"""
Representer for Python.
"""
import ast
import builtins
from itertools import count
from typing import Dict, Optional

import astor

from representer import utils


class Normalizer(ast.NodeTransformer):
    """
    Visits each node in an ast.AST and normalizes the tree for representation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._no_shadow = set(dir(builtins)).union(["self"])
        self._placeholders = (f"PLACEHOLDER_{i}" for i in count())
        self._placeholder_cache = {}
        self._docstring_cache = set()

    def add_placeholder(self, name: str) -> str:
        """
        Add an identifier name to the placeholder cache.
        """
        if name in self._no_shadow:
            return name
        if name not in self._placeholder_cache:
            self._placeholder_cache[name] = next(self._placeholders)
        return self._placeholder_cache[name]

    def get_placeholder(self, name: str) -> str:
        """
        Get the placeholder name from the cache.
        """
        return self._placeholder_cache.get(name, name)

    def get_placeholders(self) -> Dict[str, str]:
        """
        Get the placeholder assignments after walking the tree.
        """
        return {v: k for k, v in self._placeholder_cache.items()}

    def register_docstring(self, node: ast.AST) -> None:
        """
        Register the docstring for this node.
        """
        docstring = ast.get_docstring(node, clean=False)
        if docstring:
            self._docstring_cache.add(utils.md5sum(docstring))

    def visit_Module(self, node: ast.Module) -> ast.Module:
        """
        The top level of the module.
        """
        self.register_docstring(node)
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        """
        Any `class name` definition.
        """
        self.register_docstring(node)
        node.name = self.add_placeholder(node.name)
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """
        Any `def name` definition.
        """
        self.register_docstring(node)
        node.name = self.add_placeholder(node.name)
        self.generic_visit(node)
        return node

    def visit_AsyncFunctionDef(
        self, node: ast.AsyncFunctionDef
    ) -> ast.AsyncFunctionDef:
        """
        Any `async def name` definition.
        """
        self.register_docstring(node)
        node.name = self.add_placeholder(node.name)
        self.generic_visit(node)
        return node

    def visit_arg(self, node: ast.arg) -> ast.arg:
        """
        Arguments in definition signatures.
        """
        node.arg = self.add_placeholder(node.arg)
        if node.annotation:
            node.annotation = None
        self.generic_visit(node)
        return node

    def visit_keyword(self, node: ast.keyword) -> ast.keyword:
        """
        Keyword references in call signatures.
        """
        node.arg = self.add_placeholder(node.arg)
        self.generic_visit(node)
        return node

    def visit_alias(self, node: ast.alias) -> ast.alias:
        """
        The "as" alias in `import module as name`.
        """
        if node.asname:
            node.asname = self.add_placeholder(node.asname)
        self.generic_visit(node)
        return node

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> ast.ExceptHandler:
        """
        The "as" alias in `except Exception as name`.
        """
        if node.name:
            node.name = self.add_placeholder(node.name)
        self.generic_visit(node)
        return node

    def visit_Global(self, node: ast.Global) -> ast.Global:
        """
        Any `global name[, name(s)]` statements.
        """
        node.names = [self.add_placeholder(name) for name in node.names]
        self.generic_visit(node)
        return node

    def visit_Nonlocal(self, node: ast.Nonlocal) -> ast.Nonlocal:
        """
        Any `nonlocal name[, name(s)]` statements.
        """
        node.names = [self.get_placeholder(name) for name in node.names]
        self.generic_visit(node)
        return node

    def visit_Name(self, node: ast.Name) -> ast.Name:
        """
        Any named variable may be loaded, stored, or deleted.
        """
        if isinstance(node.ctx, ast.Store):
            node.id = self.add_placeholder(node.id)
        if isinstance(node.ctx, ast.Load):
            node.id = self.get_placeholder(node.id)
        self.generic_visit(node)
        return node

    def visit_ListComp(self, node: ast.ListComp) -> ast.ListComp:
        """
        A list comprehension.
        """
        self.generic_visit(node)
        node.elt = self.generic_visit(node.elt)
        return node

    def visit_SetComp(self, node: ast.SetComp) -> ast.SetComp:
        """
        A set comprehension.
        """
        self.generic_visit(node)
        node.elt = self.generic_visit(node.elt)
        return node

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> ast.GeneratorExp:
        """
        A generator comprehension.
        """
        self.generic_visit(node)
        node.elt = self.generic_visit(node.elt)
        return node

    def visit_DictComp(self, node: ast.DictComp) -> ast.DictComp:
        """
        A dict comprehension.
        """
        self.generic_visit(node)
        node.key = self.visit(node.key)
        node.value = self.visit(node.value)
        return node

    def visit_Attribute(self, node: ast.Attribute) -> ast.Attribute:
        """
        Direct name.attribute references.
        """
        if isinstance(node.ctx, ast.Store):
            node.attr = self.add_placeholder(node.attr)
        if isinstance(node.ctx, ast.Load):
            node.attr = self.get_placeholder(node.attr)
        self.generic_visit(node)
        return node

    def visit_Expr(self, node: ast.Expr) -> Optional[ast.Expr]:
        """
        Expressions not assigned to an identifier.
        """
        if isinstance(node.value, ast.Constant):
            # eliminate registered docstrings
            if utils.md5sum(node.value.value) in self._docstring_cache:
                return None
        self.generic_visit(node)
        return node
