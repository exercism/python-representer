"""Module-level docstring.

   Multi-line docstring style comment at
   the module level.
"""


import re
import operator


# Module-leve comment
# Second line of comment
# Third line of comment

operations = {
    'plus': operator.add,
    'minus': operator.sub,
    'multiplied by': operator.mul,
    'divided by': operator.floordiv
}

regex = {
    'number': re.compile(r'-?\d+'),
    'operator': re.compile(f'(?:{"|".join(operations.keys())})\\b') # In-line comment
}

def get_number(question):
    # Comment after function def

    m = regex['number'].match(question)
    if not m:
        raise ValueError("syntax error")
    return [question.removeprefix(m.group(0)).lstrip(), int(m.group(0))]

def get_operation(question):
    """Docstring style comment (should be removed)."""

    # Hash-style comment
    m = regex['operator'].match(question)
    if not m:
        raise ValueError("unknown operation") # Another in-line comment
    return [question.removeprefix(m.group(0)).lstrip(), operations[m.group(0)]]

def prepare_question(question):
    """Mulit-line docstring.

        This is a multi-line comment in the style of a
        docstring. It should get removed in the representation.
    """

    # Comment above statement.
    q = question.lower().strip().removesuffix("?")

    # Every valid question starts with "What is"
    prefix = "what is"
    if not q.startswith(prefix):
        raise ValueError("unknown operation") # In-line comment.
    return q.removeprefix(prefix).lstrip()

def answer(question):

    q = prepare_question(question)

    # the question should start with a number
    q, result = get_number(q)
    while len(q) > 0:
        # can't have a number followed by a number
        # Second line of comment
        # Third line of comment
        if regex['number'].match(q):
            raise ValueError("syntax error")
        q, operation = get_operation(q) # And another in-line comment.
        q, num = get_number(q)
        result = operation(result, num)
    return result