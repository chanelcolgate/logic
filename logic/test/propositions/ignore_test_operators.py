from logic.propositions.syntax import *
from logic.propositions.semantics import *
from logic.propositions.operators import *

many_fs = [
    "F",
    "T",
    "r",
    "~x",
    "(x+y)",
    "(x<->y)",
    "(x-&y)",
    "(x-|y)",
    "(x|y)",
    "(x->y)",
    "(x&y)",
    "(x&x)",
    "(p&q)",
    "(x|(y&z))",
    "~(~x|~(y|z))",
    "((p1|~p2)|~(p3|~~p4))",
    "((x+y)<->(~x+~y))",
    "((x-|~y)&(~F->(z<->T)))",
    "~~~~F",
]


def test_operators_defined(debug=False):
    if debug:
        print("Veryfying that all operators are recognized.")
    for s in {"&", "|", "->", "+", "<->", "-&", "-|"}:
        assert is_binary(s)


def test_to_not_and_or(debug=False):
    if debug:
        print()
    for f in many_fs:
        if debug:
            print(
                "Testing conversion of ",
                f,
                " to a formula using only '&', '|' and '~'.",
            )
        f = Formula.parse(f)
        ff = to_not_and_or(f)
        assert ff.operators().issubset({"&", "|", "~"}), (
            str(ff) + " contains wrong operators"
        )
        assert is_tautology(Formula("<->", f, ff))


def test_to_not_and(debug=False):
    if debug:
        print()
    for f in many_fs:
        if debug:
            print(
                "Testing conversion of ",
                f,
                " to a formula using only '~' and '&'.",
            )
        f = Formula.parse(f)
        ff = to_not_and(f)
        assert ff.operators().issubset({"~", "&"}), (
            str(ff) + " contains wrong operators"
        )
        assert is_tautology(Formula("<->", f, ff))


def test_to_nand(debug=False):
    if debug:
        print()
    for f in many_fs:
        if debug:
            print(
                "Testing conversion of ",
                f,
                " to a formula using only '-&'",
            )
        f = Formula.parse(f)
        ff = to_nand(f)
        assert ff.operators().issubset({"-&"}), (
            str(ff) + " contains wrong operators"
        )
        assert is_tautology(Formula("<->", f, ff))


def test_to_implies_not(debug=False):
    if debug:
        print()
    for f in many_fs:
        if debug:
            print(
                "Testing conversion of ",
                f,
                " to a formula using only '->' and '~'.",
            )
        f = Formula.parse(f)
        ff = to_implies_not(f)
        assert ff.operators().issubset({"->", "~"}), (
            str(ff) + " contains wrong operators"
        )
        assert is_tautology(Formula("<->", f, ff))


def test_to_implies_false(debug=False):
    if debug:
        print()
    for f in many_fs:
        if debug:
            print(
                "Testing conversion of ",
                f,
                " to a formula using only '->' and 'F'.",
            )
        f = Formula.parse(f)
        ff = to_implies_false(f)
        assert ff.operators().issubset({"->", "F"}), (
            str(ff) + " contains wrong operators"
        )
        assert is_tautology(Formula("<->", f, ff))


def test_to_not_or(debug=False):
    if debug:
        print()
    for f in many_fs:
        if debug:
            print(
                "Testing conversion of ",
                f,
                " to a formula using only '~' and '|'",
            )
        f = Formula.parse(f)
        ff = to_not_or(f)
        assert ff.operators().issubset({"~", "|"}), (
            str(ff) + " contains wrong operators"
        )
        assert is_tautology(Formula("<->", f, ff))


def test_to_nor(debug=False):
    if debug:
        print()
    for f in many_fs:
        if debug:
            print("Testing conversion of ", f, " to a formula using only '-|'")
        f = Formula.parse(f)
        ff = to_nor(f)
        assert ff.operators().issubset({"-|"}), (
            str(ff) + " contains wrong operators"
        )
        assert is_tautology(Formula("<->", f, ff))
