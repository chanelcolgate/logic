from logic.propositions.syntax import Formula
from logic.propositions.semantics import *


def to_not_and_or(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond `'~'`, `'&'`, and `'|'`

    Parameters:
        formula: formula to convert

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond `'~'`, `'&'` and `'|'`
    """
    # TODO: Task 3.5


def to_not_and(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond '~' and '&'

    Parameters:
        formula: formula to convert

    Returns:
         A formula thas has the same truth table as the given formula, but
         contains no constants or operators beyond '~' and '&'
    """
    # TODO: Task 3.6a


def to_nand(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond '-&'.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond '-&'.
    """
    # TODO: Task 3.6b


def to_implies_not(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond '->' and '~'.

    Parameters:
        formula: formula to convert

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond '->' and '~'
    """
    # TODO: Task 3.6c


def to_implies_false(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    constains no constants or operators beyond '->' and 'F'.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond '->' and 'F'.
    """
    # TODO: Task 3.6d
