import pytest

from dcl_runtime.models import Evidence, FieldScores, LatticeCoordinate, LatticeObservation, ObserverAnchor


def test_valid_coordinate_passes():
    c = LatticeCoordinate(1, 1, 1, 1)
    assert c.key() == "d01_f01_s01_a01"


def test_invalid_coordinate_fails():
    with pytest.raises(ValueError):
        LatticeCoordinate(13, 1, 1, 1)


def test_score_below_zero_fails():
    with pytest.raises(ValueError):
        FieldScores(-0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)


def test_score_above_one_fails():
    with pytest.raises(ValueError):
        FieldScores(1.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)


def test_missing_claim_fails():
    with pytest.raises(ValueError):
        LatticeObservation(
            coordinate=LatticeCoordinate(1, 1, 1, 1),
            scores=FieldScores(0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1),
            evidence=Evidence(1, "x", "s", "c"),
            observer_anchor=ObserverAnchor("o"),
            claim="",
        )


def test_missing_evidence_summary_fails():
    with pytest.raises(ValueError):
        Evidence(1, "x", "", "counter")


def test_missing_counter_evidence_fails():
    with pytest.raises(ValueError):
        Evidence(1, "x", "summary", "")


def test_confidence_outside_bounds_fails():
    with pytest.raises(ValueError):
        ObserverAnchor("omega", confidence=1.5)
