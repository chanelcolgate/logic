"""Some proofs in Propositional Logic."""

from logic.propositions.syntax import *
from logic.propositions.proofs import *

from logic.propositions.axiomatic_systems import *

# from logic.propositions.deduction import *

# Some inference rules that only use conjunction.

#: Conjunction introduction inference rule
A_RULE = InferenceRule(
    [Formula.parse("x"), Formula.parse("y")], Formula.parse("(x&y)")
)
#: Conjunction elimination (right) inference rule
AE1_RULE = InferenceRule([Formula.parse("(x&y)")], Formula.parse("y"))
#: Conjunction elimination (left) inference rule
AE2_RULE = InferenceRule([Formula.parse("(x&y)")], Formula.parse("x"))


def prove_and_commutativity() -> Proof:
    """Proves '(q&p)' from '(p&q)' via `A_RULE`, `AE1_RULE`, and `AE2_RULE`.

    Returns:
        A valid proof of '(q&p)' from the single assumption '(p&q)' via the
        inference rules `A_RULE`, `AE1_RULE`, and `AE2_RULE`.
    """
    # TODO: Task 4.7
    return Proof(
        InferenceRule([Formula.parse("(p&q)")], Formula.parse("(q&p)")),
        {A_RULE, AE1_RULE, AE2_RULE},
        [
            Proof.Line(Formula.parse("(p&q)")),
            Proof.Line(Formula("q"), AE1_RULE, [0]),
            Proof.Line(Formula("p"), AE2_RULE, [0]),
            Proof.Line(Formula.parse("(q&p)"), A_RULE, [1, 2]),
        ],
    )


def prove_I0() -> Proof:
    """Proves `~propositions.axiomatic_systems.IO` via
    `~propositions.axiomatic_systems.MP`, `~propositions.axiomatic_systems.I1`,
    and `~propositions.axiomatic_systems.D`.

    Returns:
        A valid proof of `~propositions.axiomatic_systems.I0` via the inference
        rules `~propositions.axiomatic_systems.MP`,
        `~propositions.axiomatic_systems.I1`, and
        `~propositions.axiomatic_systems.D`.
    """
    # TODO: Task 4.8
