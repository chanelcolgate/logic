"""Tests for the propositions.syntax module."""

from logic.utils.logic_utils import *
from logic.propositions.syntax import Formula


# Testing for Chapter 1
def test_variables(debug=True):
    for formula, expected_variables in [
        (Formula("T"), set()),
        (Formula("x1234"), {"x1234"}),
        (Formula("~", Formula("r")), {"r"}),
        (Formula("->", Formula("x"), Formula("y")), {"x", "y"}),
        (Formula("&", Formula("F"), Formula("~", Formula("T"))), set()),
        (
            Formula(
                "|",
                Formula("~", Formula("->", Formula("p1"), Formula("p2"))),
                Formula("F"),
            ),
            {"p1", "p2"},
        ),
        (
            Formula(
                "~",
                Formula(
                    "~", Formula("|", Formula("x"), Formula("~", Formula("x")))
                ),
            ),
            {"x"},
        ),
    ]:
        if debug:
            print("Testing variable of", formula)
        assert formula.variables() == expected_variables


def test_operators(debug=False):
    for f, ops in [
        (Formula("T"), {"T"}),
        (Formula("x1234"), set()),
        (Formula("~", Formula("r")), {"~"}),
        (Formula("->", Formula("x"), Formula("y")), {"->"}),
        (
            Formula("&", Formula("F"), Formula("~", Formula("T"))),
            {"F", "T", "&", "~"},
        ),
        (
            Formula(
                "|",
                Formula("~", Formula("->", Formula("p1"), Formula("p2"))),
                Formula("F"),
            ),
            {"|", "~", "->", "F"},
        ),
        (
            Formula(
                "~",
                Formula(
                    "~", Formula("|", Formula("x"), Formula("~", Formula("x")))
                ),
            ),
            {"|", "~"},
        ),
    ]:
        if debug:
            print("Testing operators of ", f)
        assert f.operators() == ops


parsing_tests = [
    ("", None, ""),
    ("x", "x", ""),
    ("T", "T", ""),
    ("a", None, ""),
    (")", None, ""),
    ("x&", "x", "&"),
    ("p3&y", "p3", "&y"),
    ("F)", "F", ")"),
    ("~x", "~x", ""),
    ("x2", "x2", ""),
    ("x|y", "x", "|y"),
    ("(p|x13)", "(p|x13)", ""),
    ("((p|x13))", None, ""),
    ("x13->x14", "x13", "->x14"),
    ("(x13->x14)", "(x13->x14)", ""),
    ("(x&y", None, ""),
    ("(T)", None, ""),
    ("(x&&y)", None, ""),
    ("-|x", None, ""),
    ("-->", None, ""),
    ("(q~p)", None, ""),
    ("(~F)", None, ""),
    ("(r&(y|(z->w)))", "(r&(y|(z->w)))", ""),
    ("~~~x~~", "~~~x", "~~"),
    ("(((~T->s45)&s45)|~y)", "(((~T->s45)&s45)|~y)", ""),
    ("((p->q)->(~q->~p))->T", "((p->q)->(~q->~p))", "->T"),
    ("((p->q)->(~q->~p)->T)", None, ""),
    ("(x|y|z)", None, ""),
    ("~((~x17->p)&~~(~F|~q))", "~((~x17->p)&~~(~F|~q))", ""),
]


def test_parse_prefix(debug=False):
    if debug:
        print()

    for s, f, r in parsing_tests:
        if debug:
            print("Testing parsing prefix of ", s)

        ff, rr = Formula._parse_prefix(s)
        if ff is None:
            assert f is None, "_parse_prefix returned error: " + rr
            if debug:
                print(
                    "... _parse_prefix correctly returned error message: ", rr
                )
            continue

        assert type(ff) is Formula
        assert type(rr) is str
        ff = str(ff)
        assert ff == f, "_parse_prefix parsed " + str(ff)
        assert rr == r, "_parse_prefix did not parse " + rr


def test_is_formula(debug=False):
    if debug:
        print()
    for s, f, r in parsing_tests:
        if debug:
            print("Testing is formula on ", s)
        if f != None and r == "":
            assert Formula.is_formula(s)
        else:
            assert not Formula.is_formula(s)


def test_parse(debug=False):
    if debug:
        print()
    for s, f, r in parsing_tests:
        if f is None or r != "":
            continue
        if debug:
            print("Testing parsing ", s)
        ff = Formula.parse(s)
        assert type(ff) is Formula
        assert str(ff) == f


def test_polish(debug=False):
    if debug:
        print("Testing polish of formula 'x12'")
    assert Formula("x12").polish() == "x12"
    if debug:
        print("Testing polish of formula '|pp' (in infix: 'p|p')")
    assert Formula("|", Formula("p"), Formula("p")).polish() == "|pp"
    if debug:
        print("Testing polish of formula '~&pq7' (in infix: '~(p&q7)')")
    assert (
        Formula("~", Formula("&", Formula("p"), Formula("q7"))).polish()
        == "~&pq7"
    )


def test_parse_polish(debug=False):
    for polish in ["p", "~x12", "&xy", "~~|x~T", "|&x1~x2F"]:
        if debug:
            print("Testsing polish parsing of formula ", polish)
        assert Formula.parse_polish(polish).polish() == polish
