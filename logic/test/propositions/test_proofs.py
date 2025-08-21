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


def test_merge_specialization_maps(debug=False):
    for d1, d2, d in [
        ({}, {}, {}),
        ({}, None, None),
        (None, {}, None),
        (None, None, None),
        ({"p": "q"}, {"r": "s"}, {"p": "q", "r": "s"}),
        ({"p": "q"}, {}, {"p": "q"}),
        ({}, {"p": "q"}, {"p": "q"}),
        ({"p": "q"}, {"p": "r"}, None),
        ({"p": "q"}, None, None),
        (None, {"p": "q"}, None),
        (
            {"x": "p1", "y": "p2"},
            {"x": "p1", "z": "p3"},
            {"x": "p1", "y": "p2", "z": "p3"},
        ),
        ({"x": "p1", "y": "p2"}, {"x": "p1", "y": "p3"}, None),
        (
            {"x": "p1", "y": "p2"},
            {"x": "p1", "y": "p2", "z": "p3"},
            {"x": "p1", "y": "p2", "z": "p3"},
        ),
        (
            {"x": "p1", "y": "p2", "z": "p3"},
            {"x": "p1", "y": "p2"},
            {"x": "p1", "y": "p2", "z": "p3"},
        ),
    ]:
        if debug:
            print("Testing merging of dictionaries", d1, d2)
        dd = InferenceRule._merge_specialization_maps(
            (
                frozendict({v: Formula.parse(d1[v]) for v in d1})
                if d1 is not None
                else None
            ),
            (
                frozendict({v: Formula.parse(d2[v]) for v in d2})
                if d2 is not None
                else None
            ),
        )
        assert dd == (
            {v: Formula.parse(d[v]) for v in d} if d is not None else None
        ), ("got " + dd)


specializations = [
    ["p", "p", {"p": "p"}],
    ["(p->q)", "(p->q)", {"p": "p", "q": "q"}],
    ["~x", "~x", {"x": "x"}],
    ["p", "p1", {"p": "p1"}],
    ["(p->q)", "(p1->q)", {"p": "p1", "q": "q"}],
    ["~p1", "~p1", {"p1": "p1"}],
    ["(p&p)", "(p1&p1)", {"p": "p1"}],
    ["(p->p1)", "(p1->p1)", {"p": "p1", "p1": "p1"}],
    ["p", "(x|y)", {"p": "(x|y)"}],
    ["(p->q)", "((x|y)->q)", {"p": "(x|y)", "q": "q"}],
    ["~p", "~(x|y)", {"p": "(x|y)"}],
    ["(T&~p)", "(T&~(x|y))", {"p": "(x|y)"}],
    ["(p&p)", "((x|y)&(x|y))", {"p": "(x|y)"}],
    ["(p->q)", "((x|y)->~w)", {"p": "(x|y)", "q": "~w"}],
    [
        "((p->q)->(~q->~p))",
        "(((x|y)->~w)->(~~w->~(x|y)))",
        {"p": "(x|y)", "q": "~w"},
    ],
    ["((x|x)&x)", "((F|F)&F)", {"x": "F"}],
    ["x", "T", {"x": "T"}],
    ["y", "(x&~(y->z))", {"y": "(x&~(y->z))"}],
    ["T", "T", {}],
    ["(F&T)", "(F&T)", {}],
    ["F", "x", None],
    ["~F", "x", None],
    ["~F", "~x", None],
    ["~F", "~T", None],
    ["F", "(x|y)", None],
    ["(x&y)", "F", None],
    ["(x&y)", "(F&F)", {"x": "F", "y": "F"}],
    ["(x&y)", "(F&~T)", {"x": "F", "y": "~T"}],
    ["(x&x)", "(F&T)", None],
    ["(F&F)", "(x&y)", None],
    ["(F&T)", "(F|T)", None],
    ["~F", "(F|T)", None],
    ["((x&y)->x)", "((F&F)->T)", None],
    ["((x&y)->x)", "((F&F)|F)", None],
    [
        "(~p->~(q|T))",
        "(~(x|y)->~((z&(w->~z))|T))",
        {"p": "(x|y)", "q": "(z&(w->~z))"},
    ],
    ["(~p->~(q|T))", "(~(x|y)->((z&(w->~z))|T))", None],
    ["(~p->~(q|T))", "(~(x|y)->~((z&(w->~z))|F))", None],
]


def test_formula_specialization_map(debug=False):
    for t in specializations:
        g = Formula.parse(t[0])
        s = Formula.parse(t[1])
        d = None if t[2] == None else {k: Formula.parse(t[2][k]) for k in t[2]}
        if debug:
            print(
                "Checking if and how formula ", s, " is a special acse of ", g
            )
        dd = InferenceRule._formula_specialization_map(g, s)
        if dd != None:
            for k in dd:
                assert is_variable(k)
                assert type(dd[k]) is Formula
        assert dd == d, "expected " + str(d) + " got " + str(dd)


rules = [
    [
        "(~p->~(q|T))",
        "(~(x|y)->~((z&(w->~z))|T))",
        [],
        [],
        {"p": "(x|y)", "q": "(z&(w->~z))"},
    ],
    ["(~p->~(q|T))", "(~(x|y)->((z&(w->~z))|T))", [], [], None],
    [
        "T",
        "T",
        ["(~p->~(q|T))"],
        ["(~(x|y)->~((z&(w->~z))|T))"],
        {"p": "(x|y)", "q": "(z&(w->~z))"},
    ],
    ["T", "T", ["(~p->~(q|T))"], [], None],
    ["T", "T", [], ["(~(x|y)->~((z&(w->~z))|T))"], None],
    ["F", "F", ["(~p->~(q|T))"], ["(~(x|y)->((z&(w->~z))|T))"], None],
    ["p", "p", ["(p->q)"], ["(p->q)"], {"p": "p", "q": "q"}],
    ["p", "p", ["(p->q)"], ["(p->q)", "(p->q)"], None],
    ["p", "p", ["(p->q)", "(p->q)"], ["(p->q)"], None],
    [
        "p",
        "p",
        ["(p->q)", "(p->q)"],
        ["(p->q)", "(p->q)"],
        {"p": "p", "q": "q"},
    ],
    ["p", "r", ["(p->q)"], ["(r->q)"], {"p": "r", "q": "q"}],
    ["p", "r", ["(p->q)"], ["(z->q)"], None],
    [
        "p",
        "p1",
        ["(p->q)", "(p&p)"],
        ["(p1->r)", "(p1&p1)"],
        {"p": "p1", "q": "r"},
    ],
    [
        "p",
        "p1",
        ["(p->q)", "(p&p)"],
        ["(p1->(r&~z))", "(p1&p1)"],
        {"p": "p1", "q": "(r&~z)"},
    ],
    [
        "p",
        "~T",
        ["(p->q)", "(p&p)"],
        ["(~T->(r&~z))", "(~T&~T)"],
        {"p": "~T", "q": "(r&~z)"},
    ],
    ["p", "T", ["(p->q)", "(p&p)"], ["(~T->(r&~z))", "(~T&~T)"], None],
    ["p", "~T", ["(p->q)", "(p&p)"], ["(~T->(r&~z))", "(~F&~F)"], None],
]


def test_specialization_map(debug=False):
    for t in rules:
        g = InferenceRule([Formula.parse(f) for f in t[2]], Formula.parse(t[0]))
        s = InferenceRule([Formula.parse(f) for f in t[3]], Formula.parse(t[1]))
        d = None if t[4] is None else {v: Formula.parse(t[4][v]) for v in t[4]}
        if debug:
            print("Testing if and how rule ", s, "is a special case of ", g)
        dd = g.specialization_map(s)
        assert d == dd, "expected " + str(d) + " got " + str(dd)
