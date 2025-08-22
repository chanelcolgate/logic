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


def test_is_specialization_map(debug=False):
    # Test 1
    rule = InferenceRule([], Formula.parse("(~p|p)"))
    for conclusion, instantiation_map_infix in [
        ["(~q|q)", {"p": "q"}],
        ["(~p|p)", {"p": "p"}],
        ["(~p4|p4)", {"p": "p4"}],
        ["(~r7|r7)", {"p": "r7"}],
        ["(~~(p|q)|~(p|q))", {"p": "~(p|q)"}],
        ["(~p|q)", None],
        ["(~p1|p2)", None],
        ["(~~(p|p)|~(p|q))", None],
    ]:
        candidate = InferenceRule([], Formula.parse(conclusion))
        if debug:
            print("Testing whether ", candidate, " is a special case of ", rule)
        assert candidate.is_specialization_of(rule) == (
            instantiation_map_infix is not None
        )


# Tests for Proof


def test_rule_for_line(debug=False):
    x1 = Formula.parse("(x&y)")
    x2 = Formula.parse("(p12->p13)")
    x3 = Formula.parse("~~~~x")
    xyxy = Formula.parse("((x|y)->(x|y))")
    r1 = Formula.parse("r")
    lemma = InferenceRule([x1, x3], r1)
    p1 = Formula.parse("p")
    p2 = Formula.parse("~~p")
    p3 = Formula.parse("~~~~p")
    pp = Formula.parse("(p->p)")
    rule0 = InferenceRule([p2], p1)
    rule1 = InferenceRule([p1, p2], p3)
    rule2 = InferenceRule([], pp)
    z = [None] * 6
    z[0] = (Proof.Line(x1), None)
    z[1] = (Proof.Line(x1, rule0, [0]), InferenceRule([x1], x1))
    z[2] = (Proof.Line(x2, rule0, [0]), InferenceRule([x1], x2))
    z[3] = (Proof.Line(x3, rule1, [2, 1]), InferenceRule([x2, x1], x3))
    z[4] = (Proof.Line(p3, rule1, [2, 1]), InferenceRule([x2, x1], p3))
    z[5] = (Proof.Line(xyxy, rule2, []), InferenceRule([], xyxy))
    proof = Proof(lemma, {rule0, rule1, rule2}, [r for (r, a) in z])
    if debug:
        print("\nChecking rule_for_line...")
    for i in range(len(z)):
        if debug:
            print("Checking rule of line ", str(i) + ":", proof.lines[i])
        assert proof.rule_for_line(i) == z[i][1]


def test_is_line_valid(debug=True):
    x1 = Formula.parse("x")
    x2 = Formula.parse("~~x")
    x3 = Formula.parse("~~~~x")
    ff = Formula.parse("(F->F)")
    r1 = Formula.parse("r")
    lemma = InferenceRule([x1, x3], r1)
    p1 = Formula.parse("p")
    p2 = Formula.parse("~~p")
    p3 = Formula.parse("~~~~p")
    pp = Formula.parse("(p->p)")
    rule0 = InferenceRule([p2], p1)
    rule1 = InferenceRule([p1, p2], p3)
    rule2 = InferenceRule([], pp)
    rule3 = InferenceRule([p1], p1)
    rule4 = InferenceRule([p1], p2)
    z = [None] * 18
    z[0] = (Proof.Line(x1), True)
    z[1] = (Proof.Line(p1), False)
    z[2] = (Proof.Line(x2), False)
    z[3] = (Proof.Line(x1, rule0, [2]), True)
    z[4] = (Proof.Line(p1, rule0, [2]), False)
    z[5] = (Proof.Line(x3, rule1, [2]), False)
    z[6] = (Proof.Line(x2, InferenceRule([p2], Formula.parse("p")), [5]), True)
    z[7] = (Proof.Line(x2, rule0, [8]), False)
    z[8] = (Proof.Line(x3, rule1, [0, 6]), True)
    z[9] = (Proof.Line(x3, rule1, [4, 6]), False)
    z[10] = (Proof.Line(x3, InferenceRule([], x3), []), False)
    z[11] = (Proof.Line(ff, rule2, []), True)
    z[12] = (Proof.Line(ff, rule0, []), False)
    z[13] = (Proof.Line(p3, rule2, []), False)
    z[14] = (Proof.Line(ff, rule2, [12]), False)
    z[15] = (Proof.Line(x1, rule3, [0]), True)
    z[16] = (Proof.Line(x1, rule3, [16]), False)
    z[17] = (Proof.Line(x2, rule4, [15]), True)
    proof = Proof(
        lemma, {rule0, rule1, rule2, rule3, rule4}, [r for (r, _) in z]
    )
    if debug:
        print(
            "\nChecking proof line validity in proof of ",
            lemma,
            " using rules ",
            {rule0, rule1},
        )
    for i in range(len(z)):
        if debug:
            print("Checking line ", str(i) + ":", proof.lines[i])
        assert proof.is_line_valid(i) == z[i][1]


# Two proofs for use in various tests below

R1 = InferenceRule(
    [Formula.parse("(p|q)"), Formula.parse("(~p|r)")], Formula.parse("(q|r)")
)
R2 = InferenceRule([], Formula.parse("(~p|p)"))
DISJUNCTION_COMMUTATIVITY_PROOF = Proof(
    InferenceRule([Formula.parse("(x|y)")], Formula.parse("(y|x)")),
    {R1, R2},
    [
        Proof.Line(Formula.parse("(x|y)")),
        Proof.Line(Formula.parse("(~x|x)"), R2, []),
        Proof.Line(Formula.parse("(y|x)"), R1, [0, 1]),
    ],
)
R3 = InferenceRule([Formula.parse("(x|y)")], Formula.parse("(y|x)"))
R4 = InferenceRule([Formula.parse("(x|(y|z))")], Formula.parse("((x|y)|z)"))
DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF = Proof(
    InferenceRule([Formula.parse("((x|y)|z)")], Formula.parse("(x|(y|z))")),
    {R3, R4},
    [
        Proof.Line(Formula.parse("((x|y)|z)")),
        Proof.Line(Formula.parse("(z|(x|y))"), R3, [0]),
        Proof.Line(Formula.parse("((z|x)|y)"), R4, [1]),
        Proof.Line(Formula.parse("(y|(z|x))"), R3, [2]),
        Proof.Line(Formula.parse("((y|z)|x)"), R4, [3]),
        Proof.Line(Formula.parse("(x|(y|z))"), R3, [4]),
    ],
)


def test_is_valid(debug=False):
    # Test variations on DISJUNCTION_COMMUTATIVITY_PROOF

    proof = DISJUNCTION_COMMUTATIVITY_PROOF
    if debug:
        print(
            "\nTesting validity of the following deductive proof:\n"
            + str(proof)
        )

    assert proof.is_valid()

    proof = Proof(
        InferenceRule(
            [Formula.parse("p"), Formula.parse("(x|y)")], Formula.parse("(y|x)")
        ),
        DISJUNCTION_COMMUTATIVITY_PROOF.rules,
        DISJUNCTION_COMMUTATIVITY_PROOF.lines,
    )

    if debug:
        print(
            "Testing validity of the following deductive proof:\n" + str(proof)
        )
    assert proof.is_valid()

    proof = Proof(
        DISJUNCTION_COMMUTATIVITY_PROOF.statement,
        DISJUNCTION_COMMUTATIVITY_PROOF.rules,
        [
            Proof.Line(Formula.parse("(~x|x)"), R2, []),
            Proof.Line(Formula.parse("(x|y)")),
            Proof.Line(Formula.parse("(y|x)"), R1, [1, 0]),
        ],
    )
    if debug:
        print(
            "Testing validity of the following deductive proof:\n" + str(proof)
        )
    assert proof.is_valid()

    proof = Proof(
        DISJUNCTION_COMMUTATIVITY_PROOF.statement,
        set(),
        DISJUNCTION_COMMUTATIVITY_PROOF.lines,
    )
    if debug:
        print(
            "Testing validity of the following deductive proof:\n" + str(proof)
        )
    assert not proof.is_valid()

    proof = Proof(
        DISJUNCTION_COMMUTATIVITY_PROOF.statement,
        DISJUNCTION_COMMUTATIVITY_PROOF.rules,
        [],
    )
    if debug:
        print(
            "Testing validity of the following deductive proof:\n" + str(proof)
        )
    assert not proof.is_valid()

    proof = Proof(
        InferenceRule([Formula.parse("(x|y)")], Formula.parse("(x|y)")),
        DISJUNCTION_COMMUTATIVITY_PROOF.rules,
        DISJUNCTION_COMMUTATIVITY_PROOF.lines,
    )
    if debug:
        print(
            "Testing validity of the following deductive proof:\n" + str(proof)
        )
    assert not proof.is_valid()

    proof = Proof(
        DISJUNCTION_COMMUTATIVITY_PROOF.statement,
        {R1, InferenceRule([], Formula.parse("(~x|~x)"))},
        DISJUNCTION_COMMUTATIVITY_PROOF.lines,
    )
    if debug:
        print(
            "Testing validity of the following deductive proof:\n" + str(proof)
        )
    assert not proof.is_valid()

    proof = Proof(
        DISJUNCTION_COMMUTATIVITY_PROOF.statement,
        DISJUNCTION_COMMUTATIVITY_PROOF.rules,
        [
            Proof.Line(Formula.parse("(x|y)")),
            Proof.Line(Formula.parse("(y|x)"), R1, [0, 0]),
        ],
    )
    if debug:
        print(
            "Testing validity of the following deductive proof:\n" + str(proof)
        )
    assert not proof.is_valid()

    # Test variations on DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF
    proof = DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF
    if debug:
        print(
            "Testing validity of the following deductive proof:\n" + str(proof)
        )
    assert proof.is_valid()

    proof = Proof(
        InferenceRule([Formula.parse("(x|y)")], Formula.parse("(y|x)")),
        DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF.rules,
        DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF.lines,
    )
    if debug:
        print(
            "Testing validity of the following deductive proof:\n" + str(proof)
        )
    assert not proof.is_valid()

    proof = Proof(
        DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF.statement,
        {R3, InferenceRule([], Formula("F"))},
        DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF.lines,
    )
    if debug:
        print(
            "Testing validity of the following deductive proof:\n" + str(proof)
        )
    assert not proof.is_valid()

    proof = Proof(
        DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF.statement,
        DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF.rules,
        [
            Proof.Line(Formula.parse("((x|y)|z)")),
            Proof.Line(Formula.parse("(x|(y|z))"), R3, [0]),
        ],
    )
    if debug:
        print(
            "Testing validity of the following deductive proof:\n" + str(proof)
        )
    assert not proof.is_valid()

    # Test circular proof
    R0 = InferenceRule([Formula.parse("(x|y)")], Formula.parse("(y|x)"))
    proof = Proof(
        InferenceRule([], Formula.parse("(x|y)")),
        {InferenceRule([Formula.parse("(x|y)")], Formula.parse("(y|x)"))},
        [
            Proof.Line(Formula.parse("(y|x)"), R0, [1]),
            Proof.Line(Formula.parse("(x|y)"), R0, [0]),
        ],
    )
    if debug:
        print(
            "Testing validity of the following deductive proof:\n" + str(proof)
        )
    assert not proof.is_valid()
