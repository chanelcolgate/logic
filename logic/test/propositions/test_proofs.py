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
