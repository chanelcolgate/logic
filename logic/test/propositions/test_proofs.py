"""Tests for the propositions.proofs module."""

from logic.utils.logic_utils import frozendict
from logic.propositions.syntax import *
from logic.propositions.proofs import *


# Tests for InferenceRule
def test_variables(debug=False):
    for assumptions, conclusion, variables in [
        [[], "T", set()],
        [["p", "q"], "r", {"p", "q", "r"}],
        [["(p|q)", "(q|r)", "(r|p)"], "(p->(q&s))", {"p", "q", "r", "s"}],
        [["(x1&x2)", "(x3|x4)"], "(x1->x11)", {"x1", "x2", "x3", "x4", "x11"}],
        [["~z", "~y", "~x"], "(((x|y)|z)|w)", {"z", "y", "x", "w"}],
        [["~~z"], "((~~z->z)|z)", {"z"}],
    ]:
        rule = InferenceRule(
            [Formula.parse(a) for a in assumptions], Formula.parse(conclusion)
        )
        if debug:
            print("Testing variables of the inference rule", rule)
        assert rule.variables() == variables


substitutions = [
    [{}, ["p", "p"], ["(p->q)", "(p->q)"], ["~x", "~x"], ["T", "T"]],
    [
        {"p": "p1"},
        ["p", "p1"],
        ["(p->q)", "(p1->q)"],
        ["~p1", "~p1"],
        ["T", "T"],
        ["(p&p)", "(p1&p1)"],
        ["(p->p1)", "(p1->p1)"],
    ],
    [
        {"p": "(x|y)"},
        ["p", "(x|y)"],
        ["(p->q)", "((x|y)->q)"],
        ["~p", "~(x|y)"],
        ["(T&~p)", "(T&~(x|y))"],
        ["(p&p)", "((x|y)&(x|y))"],
    ],
    [
        {"p": "(x|y)", "q": "~w"},
        ["p", "(x|y)"],
        ["q", "~w"],
        ["z", "z"],
        ["w", "w"],
        ["(p->q)", "((x|y)->~w)"],
        ["~p", "~(x|y)"],
        ["(T&~p)", "(T&~(x|y))"],
        ["(p&p)", "((x|y)&(x|y))"],
        ["((p->q)->(~q->~p))", "(((x|y)->~w)->(~~w->~(x|y)))"],
    ],
    [
        {"x": "F", "y": "~T", "z": "p"},
        ["x", "F"],
        ["((x&x)->y)", "((F&F)->~T)"],
        ["~(z|x)", "~(p|F)"],
        ["((z|x)&~(x->y))", "((p|F)&~(F->~T))"],
    ],
]


def test_specialize(debug=False):
    for t in substitutions:
        d = t[0]
        if debug:
            print("Testing substituion dictionary ", d)
        d = frozendict({k: Formula.parse(d[k]) for k in d})
        cases = [[Formula.parse(c[0]), Formula.parse(c[1])] for c in t[1:]]
        for case in cases:
            if debug:
                print("...checking that ", case[0], " specializes to ", case[1])
            general = InferenceRule([], case[0])
            special = InferenceRule([], case[1])
            assert general.specialize(d) == special, "got " + str(
                general.specialize(d).conclusion
            )

        if debug:
            print("...now checking all together in a single rule")
            general = InferenceRule(
                [case[0] for case in cases[1:]], cases[0][0]
            )
            special = InferenceRule(
                [case[1] for case in cases[1:]], cases[0][1]
            )
            assert general.specialize(d) == special, "got " + str(
                general.specialize(d)
            )
