import pytest

from dcl_runtime.interventions import (
    Intervention,
    is_allowed,
    liberation_efficiency_score,
    rank_interventions,
)


def test_allowed_intervention_when_net_gain_exceeds_cost_risk():
    iv = Intervention("x", "t", "d", ("K",), 0.2, 0.05, 0.03, 0.01)
    assert is_allowed(iv) is True


def test_rejected_intervention_otherwise():
    iv = Intervention("x", "t", "d", ("K",), 0.1, 0.05, 0.03, 0.03)
    assert is_allowed(iv) is False


def test_les_computed_correctly():
    iv = Intervention("x", "t", "d", ("K",), 0.2, 0.05, 0.03, 0.01)
    assert liberation_efficiency_score(iv) == pytest.approx((0.15 / 0.030001), abs=1e-6)


def test_recommendations_sorted_correctly():
    ranked = rank_interventions("R", "K")
    allowed_prefix_done = False
    for item in ranked:
        if not item["allowed"]:
            allowed_prefix_done = True
        if allowed_prefix_done:
            assert item["allowed"] is False
    les_values = [x["LES"] for x in ranked if x["allowed"]]
    assert les_values == sorted(les_values, reverse=True)
