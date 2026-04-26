from dcl_runtime.classification import classify_cmi


def test_classification_bands():
    assert classify_cmi(0.10) == "liberation_field"
    assert classify_cmi(0.30) == "garden_growth_field"
    assert classify_cmi(0.50) == "contested_field"
    assert classify_cmi(0.70) == "prison_extraction_field"
    assert classify_cmi(0.90) == "high_matrix_capture"
