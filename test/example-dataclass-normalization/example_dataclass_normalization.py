""" Dataclasses:
    Example code, from three exercises, 
    that demonstrates the new `slots` and 
    the `keyword-only` features of dataclasses.

    The slots option is invoked as a parameters to the dataclass decorator.

    Key-words are demonstrated 3 ways: 
       *** as a parameters to @dataclass, 
       *** as a parameters to field(), 
       *** as a sentinel value
"""
from dataclasses import dataclass, field, KW_ONLY



"""
From the `sgf_parsing` exercise
Demonstrates the combined use of slots and kw_only as parameters to @dataclass
"""
@dataclass(frozen=True, slots=True, kw_only=True)   # *** ***
class SgfTree:
    properties: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

def _parse(input):
    properties = input.read_properties()
    children = []
    while input.expect(";"):
        children.append(SgfTree(properties=input.read_properties()))
    while input.expect("(", advance=False):
        children.append(_parse(input))
    return SgfTree(properties=properties, children=children)




"""
From `go_counting` exercise.
Demonstrates the use of slots.

This exercise also demonstrates uninitialized variables.
See x and y.
"""
@dataclass(unsafe_hash=True, slots=True)
class Point:
    x: int
    y: int

    def __add__(self, o):
        return Point(self.x + o.x, self.y + o.y)
    
    def __eq__(self, o):
        if isinstance(o, Point):
            return self.x == o.x and self.y == o.y
        return self.x == o[0] and self.y == o[1]



"""
From the `tree_building` exercise.
The Records() class demonstrates slots and kw_only as a field() parameter.
The Node() class demonstrates use of KW_ONLY sentinel.

Also demonstrates a mix of initialized and uninitialized variables.
See record_id and parent_id.
"""
@dataclass(slots=True)   #***
class Record:
    record_id: int
    parent_id: int = field(kw_only=True)   #***

    def __lt__(self, other):
        return self.record_id < other.record_id

@dataclass
class Node:
    node_id: int
    _: KW_ONLY                                       #***
    children: list = field(default_factory=list)

def BuildTree(records):
    records.sort()

    # initialize one node for every record.
    trees = []
    for record in records:
        trees.append(Node(record.record_id))

    # match children to parents
    for record in records[1:]:
        parent = trees[record.parent_id]
        child = trees[record.record_id]
        parent.children.append(child)

    return trees[0]