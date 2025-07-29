"""Semantic analysis of propositional-logic constructs."""

from typing import AbstractSet, Iterable, Iterator, Mapping, Sequence, Tuple
from itertools import product

from logic.propositions.syntax import (
    is_variable,
    Formula,
    is_constant,
    is_binary,
    is_unary,
)

#: A model for propositional-logic formulas, a mapping from variable names to
#: truth values
Model = Mapping[str, bool]


def is_model(model: Model) -> bool:
    """Checks if the given dictionary is a model over some set of variable
    names.

    Parameters:
        model: dictionary to check.

    Returns:
        ```True``` if the given dictionary is a model over some set of variable
        names, `False` otherwise.
    """
    for key in model:
        if not is_variable(key):
            return False
    return True


def variables(model: Model) -> AbstractSet[str]:
    """Finds all variable names over which the given model is defined.

    Parameters:
        model: model to check.

    Returns:
        A set of all variable names over which the given model is defined.
    """
    assert is_model(model)
    return model.keys()


def evaluate(formula: Formula, model: Model) -> bool:
    """Calculates the truth value of the given formula in the given model.

    Parameters:
        formula: formula to calculate the truth value of.
        model: model over (possibly a superset of) the variable names of the
        given formula, to calculate the truth value in.

    Returns:
        The truth value of the given formula in the given model.

    Examples:
        >>> evaluate(Formula.parse('~(p&q76)'), {'p': True, 'q76': False})
        True

        >>> evaluate(Formula.parse('~(p&q76)'), {'p': True, 'q76': True})
        False
    """
    assert is_model(model)
    assert formula.variables().issubset(variables(model))
    # TODO: Task 2.1
    root = formula.root
    if is_constant(root):
        return formula.root == "T"
    elif is_variable(root):
        return model[root]
    elif is_unary(root):
        return not evaluate(formula.first, model)
    elif is_binary(root):
        if root == "&":
            return evaluate(formula.first, model) and evaluate(
                formula.second, model
            )
        elif root == "|":
            return evaluate(formula.first, model) or evaluate(
                formula.second, model
            )
        elif root == "->":
            return not evaluate(formula.first, model) or evaluate(
                formula.second, model
            )
        elif root == "-&":
            return not (
                evaluate(formula.first, model)
                and evaluate(formula.second, model)
            )
        elif root == "-|":
            return not (
                evaluate(formula.first, model)
                or evaluate(formula.second, model)
            )
        elif root == "+":
            return evaluate(formula.first, model) != evaluate(
                formula.second, model
            )
        elif root == "<->":
            return evaluate(formula.first, model) == evaluate(
                formula.second, model
            )


def all_models(variables: Sequence[str]) -> Iterable[Model]:
    """Calculates all possbile models over the given variable names.

    Parameters:
        variables: variable names over which to calculate the models.

    Returns:
        An iterable over all possible models over the given variable names. The
        order of the models is lexicographic according to the order of the given
        variable names, where False precedes True.

    Examples:
        >>> list(all_models(['p', 'q']))
        [{'p': False, 'q': False}, {'p': False, 'q': True},
         {'p': True, 'q': False}, {'p': True, 'q': True}]

        >>> list(all_models(['q', 'p']))
        [{'q': False, 'p': False}, {'q': False, 'p': True},
         {'q': True, 'p': False}, {'q': True, 'p': True}]
    """
    for v in variables:
        assert is_variable(v)
    # TODO: Task 2.2
    return (
        ({tuple(variables)[j]: i[j] for j in range(len(i))})
        for i in product({False, True}, repeat=len(variables))
    )


def truth_values(formula: Formula, models: Iterable[Model]) -> Iterable[bool]:
    """Calculates the truth value of the given formula in each of the given
    models.

    Parameters:
        formula: formula to calculate the truth value of.
        models: iterable over models to  calculate the truth value in.

    Returns:
        An iterable over the respective truth values of the given formula in
        each of the given models, in the order the given models.

    Examples:
        >>> list(truth_values(Formula.parse('~(p&q76)'),
                              all_models(['p', 'q76'])))
        [True, True, True, False]
    """
    # TODO: Task 2.3
    return (evaluate(formula, model) for model in models)


def print_truth_table(formula: Formula) -> None:
    """Prints the truth table of the given formula, with variable-name columns
    sorted alphabetically.

    Parameters:
        formula: formula to print the truth table of.

    Examples:
        >>> print_truth_table(Formula.parse('~(p&q76)'))
                | p | q76 | ~(p&q76) |
                |---|-----|----------|
                | F | F   | T        |
                | F | T   | T        |
                | T | F   | T        |
                | T | T   | F        |
    """

    # TODO: Task 2.4
    def bool_to_str(value):
        assert type(value) == bool
        return "T" if value else "F"

    variables = sorted(formula.variables())
    print(
        "| " + " | ".join([i for i in variables]) + " | " + str(formula) + " |"
    )
    print(
        "|-"
        + "-|-".join(["-" * len(i) for i in variables])
        + "-|-"
        + "-" * len(str(formula))
        + "-|"
    )
    for i in all_models(variables):
        print(
            "| "
            + " | ".join(
                [bool_to_str(i[j]) + " " * (len(j) - 1) for j in variables]
            )
            + " | "
            + bool_to_str(evaluate(formula, i))
            + " " * len(str(formula))
            + "|"
        )


def is_tautology(formula: Formula) -> bool:
    """Checks if the given formula is a tautology.

    Parameters:
        formula: formula to check.

    Returns:
        `True` if the given formula is a tautology, `False` otherwise.
    """
    # TODO: Task 2.5a
    return all(truth_values(formula, all_models(Formula.variables(formula))))


def is_contradiction(formula: Formula) -> bool:
    """Checks if the given formula is a contradiction.

    Parameters:
        formula: formula to check.

    Returns:
        `True` if the given formula is a contradiction, `False` otherwise.
    """
    # TODO: Task 2.5b
    return not any(
        truth_values(formula, all_models(Formula.variables(formula)))
    )


def is_satisfiable(formula: Formula) -> bool:
    """Checks if the given formula is satisfiable.

    Parameters:
        formula: formula to check.

    Returns:
        `True` if the given formula is satisfiable, `False` otherwise.
    """
    # TODO: Task 2.5c
    return any(truth_values(formula, all_models(Formula.variables(formula))))


def _synthesize_for_model(model: Model) -> Formula:
    """Synthesizes a propositional formula in the form of a single conjunctive
    clause that evaluates to `True` in the given model, and to `False` in
    any other model over the same variable names.

    Parameters:
        model: model over a nonempty set of variable names, in which the
            synthesized formula is to hold.

    Returns:
        The synthesized formula.
    """
    assert is_model(model)
    assert len(model.keys()) > 0
    # TODO: Task 2.6
    variables = list(model.keys())

    if not (model[variables[0]]):
        formula = Formula("~", Formula(variables.pop(0)))
    else:
        formula = Formula(variables.pop(0))

    while variables:
        if not (model[variables[0]]):
            second = Formula("~", Formula(variables.pop(0)))
        else:
            second = Formula(variables.pop(0))

        formula = Formula("&", formula, second)
    return formula
