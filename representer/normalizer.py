"""
Representer for Python.
"""
import builtins
from itertools import count
from typing import Dict, Optional, overload
from ast import (
    AnnAssign,
    AST,
    Assign,
    AsyncFunctionDef,
    Attribute,
    BinOp,
    BoolOp,
    Call,
    ClassDef,
    Compare,
    Constant,
    DictComp,
    Eq,
    ExceptHandler,
    Expr,
    FunctionDef,
    GeneratorExp,
    Global,
    If,
    Lambda,
    ListComp,
    Load,
    Module,
    Name,
    NodeTransformer,
    Nonlocal,
    SetComp,
    Str,
    Store,
    UnaryOp,
    Yield,
    YieldFrom,
    alias,
    arg,
    get_docstring,
    keyword,
)

from representer import utils

# pylint: disable=too-many-public-methods, invalid-name, no-self-use


class Normalizer(NodeTransformer):
    """
    Visits each node in an AST and normalizes the tree for representation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._no_shadow = set(dir(builtins)).union(["self"])
        self._placeholders = (f"placeholder_{i}" for i in count())
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
        return {value: key for key, value in self._placeholder_cache.items()}

    def register_docstring(self, node: AST) -> None:
        """
        Register the docstring for this node.
        """
        docstring = get_docstring(node, clean=False)
        if docstring:
            self._docstring_cache.add(utils.md5sum(docstring))

    def visit_Module(self, node: Module) -> Module:
        """
        The top level of the module.
        """
        self.register_docstring(node)
        self.generic_visit(node)
        return node

    @overload
    def _visit_definition(self, node: ClassDef) -> ClassDef:
        ...

    @overload
    def _visit_definition(self, node: FunctionDef) -> FunctionDef:
        ...

    @overload
    def _visit_definition(self, node: AsyncFunctionDef) -> AsyncFunctionDef:
        ...

    def _visit_definition(self, node):
        self.register_docstring(node)
        node.name = self.add_placeholder(node.name)
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node: ClassDef) -> ClassDef:
        """
        Any `class name` definition.
        """
        return self._visit_definition(node)

    def visit_FunctionDef(self, node: FunctionDef) -> FunctionDef:
        """
        Any `def name` definition.
        """
        if node.returns:
            node.returns = None
        return self._visit_definition(node)

    def visit_AnnAssign(self, node: AnnAssign) -> Assign:
        """
        Any type-annotated assignment

        Converts type-annotated assignments to regular assignments.
        """
        new_assign = Assign(targets=[node.target],
                            value=node.value,
                            lineno=node.lineno)
        self.generic_visit(new_assign)
        return new_assign

    def visit_AsyncFunctionDef(self, node: AsyncFunctionDef) -> AsyncFunctionDef:
        """
        Any `async def name` definition.
        """
        return self._visit_definition(node)

    def visit_arg(self, node: arg) -> arg:
        """
        Arguments in definition signatures.
        Drops type annotations.
        """
        node.arg = self.add_placeholder(node.arg)
        if node.annotation:
            node.annotation = None
        self.generic_visit(node)
        return node

    def visit_keyword(self, node: keyword) -> keyword:
        """
        Keyword references in call signatures.
        """
        if node.arg:
            node.arg = self.add_placeholder(node.arg)
        self.generic_visit(node)
        return node

    def visit_alias(self, node: alias) -> alias:
        """
        The "as" alias in `import module as name`.
        """
        if node.asname:
            node.asname = self.add_placeholder(node.asname)
        self.generic_visit(node)
        return node

    def visit_ExceptHandler(self, node: ExceptHandler) -> ExceptHandler:
        """
        The "as" alias in `except Exception as name`.
        """
        if node.name:
            node.name = self.add_placeholder(node.name)
        self.generic_visit(node)
        return node

    def visit_Global(self, node: Global) -> Global:
        """
        Any `global name[, name(s)]` statements.
        """
        node.names = [self.add_placeholder(name) for name in node.names]
        self.generic_visit(node)
        return node

    def visit_Nonlocal(self, node: Nonlocal) -> Nonlocal:
        """
        Any `nonlocal name[, name(s)]` statements.
        """
        node.names = [self.get_placeholder(name) for name in node.names]
        self.generic_visit(node)
        return node

    @overload
    def _visit_identifier(self, node: Name) -> Name:
        ...

    @overload
    def _visit_identifier(self, node: Attribute) -> Attribute:
        ...

    def _visit_identifier(self, node):
        attr = "id" if isinstance(node, Name) else "attr"
        value = getattr(node, attr)
        if isinstance(node.ctx, Store):
            setattr(node, attr, self.add_placeholder(value))
        if isinstance(node.ctx, Load):
            setattr(node, attr, self.get_placeholder(value))
        self.generic_visit(node)
        return node

    def visit_Name(self, node: Name) -> Name:
        """
        Any named variable may be loaded, stored, or deleted.
        """
        return self._visit_identifier(node)

    def visit_Attribute(self, node: Attribute) -> Attribute:
        """
        Any named attribute may be loaded, stored, or deleted.
        """
        return self._visit_identifier(node)


    @overload
    def _visit_comprehension(self, node: ListComp) -> ListComp:
        ...

    @overload
    def _visit_comprehension(self, node: SetComp) -> SetComp:
        ...

    @overload
    def _visit_comprehension(self, node: GeneratorExp) -> GeneratorExp:
        ...

    @overload
    def _visit_comprehension(self, node: DictComp) -> DictComp:
        ...

    def _visit_comprehension(self, node):
        self.generic_visit(node)
        if isinstance(node, DictComp):
            self.visit(node.key)
            self.visit(node.value)
        else:
            self.visit(node.elt)
        return node

    def visit_ListComp(self, node: ListComp) -> ListComp:
        """
        A list comprehension.
        """
        return self._visit_comprehension(node)

    def visit_SetComp(self, node: SetComp) -> SetComp:
        """
        A set comprehension.
        """
        return self._visit_comprehension(node)

    def visit_GeneratorExp(self, node: GeneratorExp) -> GeneratorExp:
        """
        A generator comprehension.
        """
        return self._visit_comprehension(node)

    def visit_DictComp(self, node: DictComp) -> DictComp:
        """
        A dict comprehension.
        """
        return self._visit_comprehension(node)

    @overload
    def _visit_If(self, node: If) -> If:
        ...

    def visit_If(self, node: If) -> None:
        """Remove if __name__ == '__main__' nodes.

        Looks for ast.If that includes __name__ == __main__ checks
        and removes the block.
        """
        if isinstance(node.test, Compare):
            if not (isinstance(node.test.left, Name) and node.test.left.id == '__name__'):
                self.generic_visit(node)
                return node
            else:
                if node.test.comparators[0].value == '__main__':
                    return None

        self.generic_visit(node)
        return node

    def visit_Expr(self, node: Expr) -> Optional[Expr]:
        """Expressions not assigned to an identifier.

           Removes print statements and docstrings from
           the representation.
        """

        # Remove print() statements from representation.
        if (isinstance(node.value, Call) and
            isinstance(node.value.func, Name)):
            if node.value.func.id == 'print':
                return None

        if isinstance(node.value, Constant) and not isinstance(node.value, Call):
            # eliminate registered docstrings
            if utils.md5sum(node.value.value) in self._docstring_cache:
                return None

        self.generic_visit(node)
        return node


__all__ = ["Normalizer"]
