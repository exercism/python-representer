"""
Representer for Python.
"""
from typing import Dict

from . import utils
from .normalizer import Normalizer


class Representer:
    """
    Represent Python code in normalized form.
    """

    def __init__(self, source: str) -> None:
        self._tree = utils.parse(source)
        self._normalizer = Normalizer()

    def normalize(self) -> None:
        """
        Normalize the tree.
        """
        self._tree = self._normalizer.visit(self._tree)

    def dump_tree(self) -> str:
        """
        Dump the current state of the tree for printing.
        """
        return utils.dump_tree(self._tree)

    def dump_code(self, reformat=True) -> str:
        """
        Dump the current tree as generate code.
        """
        code = utils.to_source(self._tree)
        if reformat:
            return utils.reformat(code)
        return code

    @property
    def mapping(self) -> Dict[str, str]:
        """
        Get the placeholder assignments after normalize.
        """
        return self._normalizer.get_placeholders()

    def dump_map(self) -> str:
        """
        Dump the tree's mapping of placeholders.
        """
        return utils.to_json(self.mapping)


def represent(slug: utils.Slug, directory: utils.Directory) -> None:
    """
    Normalize the `directory/slug.py` file representation.
    """
    src = directory.joinpath(slug.replace("-", "_") + ".py")
    out_dst = directory.joinpath("representation.out")
    txt_dst = directory.joinpath("representation.txt")
    map_dst = directory.joinpath("mapping.json")

    # parse the tree from the file contents
    representation = Representer(src.read_text())

    # save dump of the initial tree for debug
    out = ["# BEGIN TREE BEFORE", representation.dump_tree(), ""]

    # normalize the tree
    representation.normalize()

    # save dump of the normalized tree for debug
    out.extend(["# BEGIN TREE AFTER", representation.dump_tree()])

    # dump the representation files
    out_dst.write_text("\n".join(out))
    txt_dst.write_text(representation.dump_code())
    map_dst.write_text(representation.dump_map())
