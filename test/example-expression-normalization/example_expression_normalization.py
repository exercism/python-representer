"""Hanging Module docstring.

 This is to make sure that the Expression changes don't munge things"""


import unittest
import pytest
from dataclass import dataclass
from Enum import Flag


# Examples of "Hanging Expressions (expressions not assigned to a name)"
# These have been barfing in the representer, due to bad refrences when
# checking the cache.

# hanging uninitialized dataclass
@dataclass
class Point:
    """Docstring to test removal."""
    x: int = 0
    y: int = 0


# Hanging try/except
try:
    1/0
except:
    pass


# Random addition
5+6


# Hanging print() (should get removed)
print(5+6)


# Various hanging comprehensions and genexps
(item for item in range(8))
[item for item in range(16)]
{item for item in "a b c d e f g h i".split()}
{key:value for key, value in ((1, "a"),(2, "b"),(3, "c"),(5, "e"))}

# Hanging and not hanging lambdas
lambda : {key:value for key, value in ((1, "a"),(2, "b"),(3, "c"),(5, "e"))}
test_assign_name = lambda : {item for item in "a b c d e f g h i".split()}


# hanging "constants"
-a
THIS_IS_A_CONSTANT = "It would be stupid if this exploded."

"""Random Hanging String"""


# hanging Enum
class Allergene(Flag):
    eggs = auto()
    peanuts = auto()
    shellfish = auto()
    strawberries = auto()
    tomatoes = auto()
    chocolate = auto()
    pollen = auto()
    cats = auto()

# The below is a hanging try/except from Guido's Gorgeous Lasagna exercise.

# For this first exercise, it is really important to be clear about how we are importing names for tests.
# To that end, we are putting a try/catch around imports and throwing specific messages to help students
# decode that they need to create and title their constants and functions in a specific way.
try:
    from lasagna import (EXPECTED_BAKE_TIME,
                         bake_time_remaining,
                         preparation_time_in_minutes,
                         elapsed_time_in_minutes)

# Here, we are separating the constant import errors from the function name import errors
except ImportError as import_fail:
    message = import_fail.args[0].split('(', maxsplit=1)
    item_name = import_fail.args[0].split()[3]

    if 'EXPECTED_BAKE_TIME' in item_name:
        # pylint: disable=raise-missing-from
        raise ImportError(f'\n\nMISSING CONSTANT --> \nWe can not find or import the constant {item_name} in your'
                          " 'lasagna.py' file.\nDid you misname or forget to define it?") from None
    else:
        item_name = item_name[:-1] + "()'"
        # pylint: disable=raise-missing-from
        raise ImportError("\n\nMISSING FUNCTION --> In your 'lasagna.py' file, we can not find or import the"
                          f' function named {item_name}. \nDid you misname or forget to define it?') from None


# The below examples overlap with other tests, but are here to show that
# the docstring removals don't alter other expression-type code.


def slices(series, length):
    """
    Given a string of digits, output all the contiguous substrings of length `n`,
    in that string, in the order that they appear.
    """
    return [
        sub_str
        for i, _ in enumerate(series)
        if len(sub_str := series[i : i + length]) == length
    ]


# yield from and yield examples
from typing import Iterable
def flatten(iterable):
    def go(it):
        for e in it:
            if isinstance(e, Iterable) and not isinstance(e, str):
                yield from go(e)
            else:
                yield e
    return [e for e in go(iterable) if e is not None]



def check_height(grid):
    """check that row count is a multiple of 4"""
    if (height := len(grid)) % 3:
        raise ValueError("grid rows not a multiple of 4")
    return height


def nswe_points(self, point):
    """return a set of four adjacent points"""
    nswe_offsets = set([(1, 0), (-1, 0), (0, -1), (0, 1)])
    return {
        neighbor
        for offset in nswe_offsets
        if self.on_the_board(neighbor := point + offset)
    }


def first_item_greater_than_N(iterable, N):
    if any((item := x) > N for x in iterable):
        return item
    return None


def generate_codes(seat_numbers, flight_id):
    """Generate codes for a ticket.

    :param seat_numbers: list[str] - list of seat numbers.
    :param flight_id: str - string containing the flight identifier.
    :return: generator - generator that yields 12 character long ticket codes.

    """
    return (
        base.ljust(12, "0") for seat in seat_numbers if (base := f"{seat}{flight_id}")
    )
