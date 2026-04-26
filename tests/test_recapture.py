from dcl_runtime.recapture import recapture_tax


def test_no_recapture():
    r = recapture_tax({"computed": {"D_score": 0.5, "Phi_score": 0.4}}, {"computed": {"D_score": 0.4, "Phi_score": 0.5}})
    assert r["status"] == "no_recapture"


def test_partial_recapture():
    r = recapture_tax({"computed": {"D_score": 0.5, "Phi_score": 0.4}}, {"computed": {"D_score": 0.55, "Phi_score": 0.6}})
    assert r["status"] == "partial_recapture"


def test_high_recapture():
    r = recapture_tax({"computed": {"D_score": 0.5, "Phi_score": 0.4}}, {"computed": {"D_score": 0.8, "Phi_score": 0.6}})
    assert r["status"] == "high_recapture"


def test_constraint_gain_without_coherence():
    r = recapture_tax({"computed": {"D_score": 0.5, "Phi_score": 0.4}}, {"computed": {"D_score": 0.7, "Phi_score": 0.3}})
    assert r["status"] == "constraint_gain_without_coherence"
    assert r["recapture_tax"] is None
    assert r["tax_infinite"] is True
