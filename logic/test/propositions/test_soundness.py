"""Tests for the propositions.soundness module."""

from logic.utils.logic_utils import frozendict
from logic.propositions.soundness import *
from logic.propositions.semantics import evaluate_inference


def test_rule_nonsoundness_from_specialization_nonsoundness(debug=False):
    # Test rule with a small number of variables
    general = InferenceRule(
        [Formula.parse("p"), Formula.parse("q")], Formula.parse("(p&r)")
    )
    specialization = InferenceRule(
        [Formula.parse("(x&~y)"), Formula.parse("~w")],
        Formula.parse("((x&~y)&~(p->z))"),
    )
    model = frozendict(
        {"x": True, "y": False, "w": False, "p": False, "z": True}
    )

    if debug:
        print(
            "Testing rule_nonsoundness_from_specialization_nonsoundness given"
            " the specialization ",
            specialization,
            " of the rule ",
            general,
            "and the model",
            model,
            "for the specialization",
        )
    assert not evaluate_inference(
        general,
        rule_nonsoundness_from_specialization_nonsoundness(
            general, specialization, model
        ),
    )

    # Test assumptionless rule with a large number of variables
    general = InferenceRule(
        [],
        Formula.parse(
            "(((((((((((((((((((((((((((((((p1|~p2)|p3)|p4)|~p5)|p6)|"
            "~p7)|~p8)|p9)|p10)|p11)|~p12)|p13)|p14)|~p15)|p16)|"
            "~p17)|~p18)|p19)|p20)|p21)|~p22)|p23)|p24)|~p25)|p26)|"
            "~p27)|~p28)|p29)|p30)|p31)|~p32)"
        ),
    )
    specialization = InferenceRule(
        [],
        Formula.parse(
            "(((((((((((((((((((((((((((((((p1|~p2)|p3)|p4)|~p5)|p6)|"
            "~p7)|~(z1&~z2))|p9)|p10)|p11)|~p12)|p13)|p14)|~p15)|"
            "p16)|~p17)|~p18)|p19)|p20)|p21)|~p22)|p23)|p24)|~p25)|"
            "p26)|~p27)|~p28)|p29)|p30)|p31)|~p32)"
        ),
    )
    model = frozendict(
        {
            "p1": False,
            "p2": True,
            "p3": False,
            "p4": False,
            "p5": True,
            "p6": False,
            "p7": True,
            "z1": True,
            "z2": False,
            "p9": False,
            "p10": False,
            "p11": False,
            "p12": True,
            "p13": False,
            "p14": False,
            "p15": True,
            "p16": False,
            "p17": True,
            "p18": True,
            "p19": False,
            "p20": False,
            "p21": False,
            "p22": True,
            "p23": False,
            "p24": False,
            "p25": True,
            "p26": False,
            "p27": True,
            "p28": True,
            "p29": False,
            "p30": False,
            "p31": False,
            "p32": True,
        }
    )

    if debug:
        print(
            "Testing rule_nonsoundness_from_specialization_nonsoundness given"
            " the specialization ",
            specialization,
            " of the rule ",
            general,
            "and the model",
            model,
            "for the specialization",
        )
    assert not evaluate_inference(
        general,
        rule_nonsoundness_from_specialization_nonsoundness(
            general, specialization, model
        ),
    )
