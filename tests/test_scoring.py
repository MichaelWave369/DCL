import pytest

from dcl_runtime.classification import classify_cmi
from dcl_runtime.models import FieldScores
from dcl_runtime.scoring import compute_scores


def test_scoring_values():
    s = FieldScores(
        B=0.70, R=0.85, I_g=0.55, S=0.65, E_x=0.75, D_c=0.45,
        C_o=0.50, K=0.60, A=0.48, M=0.55, L_v=0.40, R_s=0.52,
    )
    temp = compute_scores(s, "")
    computed = compute_scores(s, classify_cmi(temp.CMI))
    assert computed.D_score == pytest.approx(0.658333, abs=1e-6)
    assert computed.Phi_score == pytest.approx(0.508333, abs=1e-6)
    assert computed.DCR == pytest.approx(1.295079, abs=1e-6)
    assert computed.CMI == pytest.approx(0.679179, abs=1e-6)
    assert computed.classification == "prison_extraction_field"
    assert computed.dominant_constraint == "R"
    assert computed.dominant_coherence == "K"
