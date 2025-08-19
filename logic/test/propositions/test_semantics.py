"""Tests for the propositions.semantics module."""

from logic.utils.logic_utils import frozendict
from logic.propositions.syntax import Formula, is_variable
from logic.propositions.semantics import (
    evaluate,
    all_models,
    truth_values,
    print_truth_table,
    is_tautology,
    is_contradiction,
    is_satisfiable,
    synthesize,
    synthesize_cnf,
    evaluate_inference,
)


def test_evaluate(debug=False):
    infix1 = "~(p&q7)"
    models_values1 = [
        ({"p": True, "q7": False}, True),
        ({"p": False, "q7": False}, True),
        ({"p": True, "q7": True}, False),
    ]
    infix2 = "~~~x"
    models_values2 = [({"x": True}, False), ({"x": False}, True)]
    infix3 = "((x->y)&(~x->z))"
    models_values3 = [
        ({"x": True, "y": False, "z": True}, False),
        ({"x": False, "y": False, "z": True}, True),
        ({"x": True, "y": True, "z": False}, True),
    ]
    infix4 = "(T&p)"
    models_values4 = [({"p": True}, True), ({"p": False}, False)]
    infix5 = "(F|p)"
    models_values5 = [({"p": True}, True), ({"p": False}, False)]

    for infix, models_values in [
        [infix1, models_values1],
        [infix2, models_values2],
        [infix3, models_values3],
        [infix4, models_values4],
        [infix5, models_values5],
    ]:
        formula = Formula.parse(infix)
        for model, value in models_values:
            if debug:
                print(
                    "Testing evaluation of formula ",
                    formula,
                    " in model ",
                    model,
                )
            assert evaluate(formula, frozendict(model)) == value


def test_all_models(debug=False):
    variables1 = ("p", "q")
    models1 = [
        {"p": False, "q": False},
        {"p": False, "q": True},
        {"p": True, "q": False},
        {"p": True, "q": True},
    ]
    variables2 = ["x"]
    models2 = [{"x": False}, {"x": True}]
    variables3 = ("q", "p")
    models3 = [
        {"q": False, "p": False},
        {"q": False, "p": True},
        {"q": True, "p": False},
        {"q": True, "p": True},
    ]
    for variables, models in [
        (variables1, models1),
        (variables2, models2),
        (variables3, models3),
    ]:
        if debug:
            print("Testing all models over ", variables)
        assert list(all_models(tuple(variables))) == models


def test_truth_values(debug=False):
    for infix, variables, values in [
        ["~(p&q7)", ("p", "q7"), [True, True, True, False]],
        ["(y|~x)", ("y", "x"), [True, False, True, True]],
        ["~~~p", ("p"), [True, False]],
    ]:
        formula = Formula.parse(infix)
        if debug:
            print(
                "Testing the evaluation of ",
                formula,
                " on all models over its variables",
            )
        tvals = list(truth_values(formula, list(all_models(tuple(variables)))))
        assert tvals == values, (
            "Expected " + str(values) + " ; got " + str(tvals)
        )


def test_print_truth_table(debug=False):
    infix1 = "~r"
    table1 = "| r | ~r |\n" "|---|----|\n" "| F | T  |\n" "| T | F  |\n"

    infix2 = "~(p&q7)"
    table2 = (
        "| p | q7 | ~(p&q7) |\n"
        "|---|----|---------|\n"
        "| F | F  | T       |\n"
        "| F | T  | T       |\n"
        "| T | F  | T       |\n"
        "| T | T  | F       |\n"
    )

    infix3 = "~(q7&p)"
    table3 = (
        "| p | q7 | ~(q7&p) |\n"
        "|---|----|---------|\n"
        "| F | F  | T       |\n"
        "| F | T  | T       |\n"
        "| T | F  | T       |\n"
        "| T | T  | F       |\n"
    )

    infix4 = "(x&(~z|y))"
    table4 = (
        "| x | y | z | (x&(~z|y)) |\n"
        "|---|---|---|------------|\n"
        "| F | F | F | F          |\n"
        "| F | F | T | F          |\n"
        "| F | T | F | F          |\n"
        "| F | T | T | F          |\n"
        "| T | F | F | T          |\n"
        "| T | F | T | F          |\n"
        "| T | T | F | T          |\n"
        "| T | T | T | T          |\n"
    )
    _test_print_truth_table(
        [infix1, infix2, infix3, infix4],
        [table1, table2, table3, table4],
        debug,
    )


def _test_print_truth_table(infixes, tables, debug):
    from io import StringIO
    import sys

    class PrintCapturer:
        """A helper class for capturing text printed to the standard output."""

        def __enter__(self):
            """Saves the standdard and replace it with a mock."""
            self._stdout = sys.stdout
            sys.stdout = self._stringio = StringIO()
            return self

        def __exit__(self, *args):
            """Stores the captured text, and restore the original standard
            output."""
            self.captured = self._stringio.getvalue()
            sys.stdout = self._stdout

    capturer = PrintCapturer()
    for infix, table in zip(infixes, tables):
        formula = Formula.parse(infix)
        if debug:
            print("Testing truth table of ", formula)
        with capturer as output:
            print_truth_table(formula)
        if debug:
            print("Printed:\n" + capturer.captured)
            print("Expected:\n" + table)
        import re

        assert re.sub("[ -]+", " ", capturer.captured) == re.sub(
            "[ -]+", " ", table
        )


def test_is_tautology(debug=False):
    for infix, answer in [
        ["~(p&q7)", False],
        ["(x|~x)", True],
        ["(p->q)", False],
        ["(p->p)", True],
        ["(F|T)", True],
        ["((y1|~y1)&T)", True],
        ["((T&T)|F)", True],
        ["F", False],
        ["x", False],
        ["~y", False],
        ["((x->y)&((y->z)&(x&~z)))", False],
        ["~((x->y)&((y->z)&(x&~z)))", True],
    ]:
        formula = Formula.parse(infix)
        if debug:
            print("Testing whether ", formula, " is a tatology")
        assert is_tautology(formula) == answer


def test_is_contradiction(debug=False):
    for infix, answer in [
        ["~(p&q7)", False],
        ["~(x|~x)", True],
        ["(T->F)", True],
        ["((y1|~y1)&T)", False],
        ["((T&T)|F)", False],
        ["F", True],
        ["x", False],
        ["~y", False],
        ["((x->y)&((y->z)&(x&~z)))", True],
    ]:
        formula = Formula.parse(infix)
        if debug:
            print("Testing whether ", formula, " is a contradiction")
        assert is_contradiction(formula) == answer


def test_is_satisfiable(debug=False):
    for infix, answer in [
        ["~(p&q7)", True],
        ["~(x|~x)", False],
        ["(T->F)", False],
        ["((y1|~y1)&T)", True],
        ["((T&T)|F)", True],
        ["F", False],
        ["x", True],
        ["~y", True],
        ["((x->y)&((y->z)&(x&~z)))", False],
    ]:
        formula = Formula.parse(infix)
        if debug:
            print("Testing whether ", formula, " is a satisfiable")
        assert is_satisfiable(formula) == answer


def test_synthesize_for_model(debug=False):
    from logic.propositions.semantics import _synthesize_for_model

    _test_synthesize_clause(_synthesize_for_model, True, debug)


def _test_synthesize_clause(clause_synthesizer, for_model, debug):
    all_models1 = [{"x": False}, {"x": True}]
    all_models2 = [
        {"p": False, "q": False},
        {"p": False, "q": True},
        {"p": True, "q": False},
        {"p": True, "q": True},
    ]
    all_models3 = [
        {"r1": False, "r12": False, "p37": False},
        {"r1": False, "r12": False, "p37": True},
        {"r1": False, "r12": True, "p37": False},
        {"r1": False, "r12": True, "p37": True},
        {"r1": True, "r12": False, "p37": False},
        {"r1": True, "r12": False, "p37": True},
        {"r1": True, "r12": True, "p37": False},
        {"r1": True, "r12": True, "p37": True},
    ]

    for all_models in [all_models1, all_models2, all_models3]:
        for idx in range(len(all_models)):
            if debug:
                print(
                    "Testing ",
                    clause_synthesizer.__qualname__,
                    " for model ",
                    all_models[idx],
                )
            f = clause_synthesizer(frozendict(all_models[idx]))
            assert type(f) is Formula, "Expected a formula, got " + str(f)
            if for_model:
                assert is_conjunctive_clause(f), (
                    str(f) + " should be a conjunctive clause"
                )
                all_values = [False] * len(all_models)
                all_values[idx] = True
            else:
                assert is_disjunctive_clause(f), (
                    str(f) + " should be a disjunctive clause"
                )
                all_values = [True] * len(all_models)
                all_values[idx] = False
            for model, value in zip(all_models, all_values):
                assert evaluate(f, frozendict(model)) == value


def is_conjunctive_clause(f):
    if is_variable(f.root) or (f.root == "~" and is_variable(f.first.root)):
        return True
    return (
        f.root == "&"
        and is_conjunctive_clause(f.first)
        and is_conjunctive_clause(f.second)
    )


def is_disjunctive_clause(f):
    if is_variable(f.root) or (f.root == "~" and is_variable(f.first.root)):
        return True
    return (
        f.root == "|"
        and is_disjunctive_clause(f.first)
        and is_disjunctive_clause(f.second)
    )


def test_synthesize(debug=False):
    __test_synthesize(synthesize, True, debug)


def test_sythesize_cnf(debug=False):
    __test_synthesize(synthesize_cnf, False, debug)


def __test_synthesize(synthesizer, dnf, debug):
    all_variables1 = ["p"]
    all_models1 = [{"p": False}, {"p": True}]
    value_lists1 = [(False, False), (False, True), (True, False), (True, True)]

    all_variables2 = ["p", "q"]
    all_models2 = [
        {"p": False, "q": False},
        {"p": False, "q": True},
        {"p": True, "q": False},
        {"p": True, "q": True},
    ]
    value_lists2 = [
        (True, False, False, True),
        (True, True, True, True),
        (False, False, False, False),
    ]

    all_variables3 = ["r1", "r12", "p37"]
    all_models3 = [
        {"r1": False, "r12": False, "p37": False},
        {"r1": False, "r12": False, "p37": True},
        {"r1": False, "r12": True, "p37": False},
        {"r1": False, "r12": True, "p37": True},
        {"r1": True, "r12": False, "p37": False},
        {"r1": True, "r12": False, "p37": True},
        {"r1": True, "r12": True, "p37": False},
        {"r1": True, "r12": True, "p37": True},
    ]
    value_lists3 = [
        (True, False, True, True, False, True, False, True),
        (True, True, True, True, True, True, True, True),
        (False, False, False, False, False, False, False),
    ]

    for all_variables, all_models, value_lists in [
        [all_variables1, all_models1, value_lists1],
        [all_variables2, all_models2, value_lists2],
        [all_variables3, all_models3, value_lists3],
    ]:
        for all_values in value_lists:
            if debug:
                print(
                    "Testing",
                    synthesizer.__qualname__,
                    "for variables",
                    all_variables,
                    "and model-values",
                    all_values,
                )
                formula = synthesize(tuple(all_variables), all_values)
                assert (
                    type(formula) is Formula
                ), "Expected a formula, got " + str(formula)
                if dnf:
                    assert is_dnf(formula), str(formula) + " should be a DNF"
                else:
                    assert is_cnf(formula), str(formula) + " should be a CNF"
                assert formula.variables().issubset(set(all_variables))
                for model, value in zip(all_models, all_values):
                    assert evaluate(formula, frozendict(model)) == value, (
                        str(formula)
                        + " does not evaluate to "
                        + str(value)
                        + " on "
                        + str(model)
                    )


def is_dnf(formula):
    return is_conjunctive_clause(formula) or (
        formula.root == "|" and is_dnf(formula.first) and is_dnf(formula.second)
    )


def is_cnf(formula):
    return is_disjunctive_clause(formula) or (
        formula.root == "&" and is_cnf(formula.first) and is_cnf(formula.second)
    )


def test_evaluate_inference(debug=False):
    from logic.propositions.proofs import InferenceRule

    # Test 1
    rule1 = InferenceRule(
        [Formula.parse("p"), Formula.parse("q")], Formula.parse("r")
    )
    for model in all_models(["p", "q", "r"]):
        if debug:
            print(
                "Testing evaluation of inference rule ",
                rule1,
                " in model ",
                model,
            )
        assert (
            evaluate_inference(rule1, frozendict(model)) == (not model["p"])
            or (not model["q"])
            or model["r"]
        )

    # Test 2
    rule2 = InferenceRule([Formula.parse("(x|y)")], Formula.parse("x"))
    for model in all_models(["x", "y"]):
        if debug:
            print(
                "Testing evaluation of inference rule ",
                rule2,
                " in model ",
                model,
            )
        assert (
            evaluate_inference(rule2, frozendict(model)) == (not model["y"])
            or model["x"]
        )

    # Test 3
    rule3 = InferenceRule(
        [Formula.parse(s) for s in ["(p->q)", "(q->r)"]], Formula.parse("r")
    )
    for model in all_models(["p", "q", "r"]):
        if debug:
            print(
                "Testing evaluation of inference rule ",
                rule3,
                " in model ",
                model,
            )
        assert (
            evaluate_inference(rule3, frozendict(model))
            == (model["p"] and not model["q"])
            or (model["q"] and not model["r"])
            or model["r"]
        )
