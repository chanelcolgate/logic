"""Programmatic proof of the soundness of Propositional Logic."""

from typing import Tuple

from logic.propositions.syntax import *
from logic.propositions.semantics import *
from logic.propositions.proofs import *


def rule_nonsoundness_from_specialization_nonsoundness(
    general: InferenceRule, specialization: InferenceRule, model: Model
) -> Model:
    """Demonstrates the non-soundness of the given general inference rule given
    an example of the non-soundness of the given specialization of this rule.

    Parameters:
        general: inference rule to the soundness of which to find a
            counterexample.
        specialization: non-sound specialization of `general`.
        model: model in which `specialization` does not hold.

    Returns:
        A model in which `general` does not hold.
    """
    assert specialization.is_specialization_of(general)
    assert not evaluate_inference(specialization, model)
    # TODO: Task 4.9
    map1 = general.specialization_map(specialization)
    g_model = dict()
    for key in map1.keys():
        g_model[key] = evaluate(map1[key], model)
    return g_model


def nonsound_rule_of_nonsound_proof(
    proof: Proof, model: Model
) -> Tuple[InferenceRule, Model]:
    """Finds a non-sound inference rule used by the given valid proof of a
    non-sound inference rule, and demonstrates the non-soundness of the former
    rule.

    Parameters:
        proof: valid proof of a non-sound inference rule.
        model: model in which the inference rule proved by the given proof does
            not build.

    Returns:
        A pair of a non-sound inference rule used in the given proof and a model
        in which this rule does not hold.
    """
    assert proof.is_valid()
    assert not evaluate_inference(proof.statement, model)
    # TODO: Task 4.10
