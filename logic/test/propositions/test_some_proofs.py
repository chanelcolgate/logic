"""Tests for the propositional.some_proofs module."""

from logic.propositions.syntax import *
from logic.propositions.proofs import *
from logic.propositions.axiomatic_systems import *
from logic.propositions.some_proofs import *


def offending_line(proof):
    """Finds the first invalid line in the given proof.

    Parameters:
        proof: proof to search.

    Returns:
        An error message containing the line number and string representation of
        the first invalid line in the given proof, or `None` if all the lines
        of the given proof are valid.
    """
    for i in range(len(proof.lines)):
        if not proof.is_line_valid(i):
            return "Invalid line " + str(i) + ": " + str(proof.lines[i])
    return None


def __test_prove_inference(prover, rule, rules, debug):
    if debug:
        print("Testing ", prover.__qualname__)
    proof = prover()
    assert proof.statement == rule
    assert proof.rules.issubset(rules), (
        " got " + str(proof.rules) + ", expected " + str(rules)
    )
    assert proof.is_valid(), offending_line(proof)


def test_prove_and_commutativity(debug=True):
    __test_prove_inference(
        prove_and_commutativity,
        InferenceRule([Formula.parse("(p&q)")], Formula.parse("(q&p)")),
        {A_RULE, AE1_RULE, AE2_RULE},
        debug,
    )

def test_prove_IO(debug=False):
    __test_prove_inference(prove_I0, I0, {MP, I1, D}, debug)
