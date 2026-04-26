import copy

from dcl_runtime.markdown import receipt_to_markdown
from dcl_runtime.receipts import compute_receipt_id, receipt_id_payload, verify_receipt_data
from dcl_runtime.storage import read_json


def test_receipt_id_deterministic():
    receipt = read_json("examples/receipt_example.json")
    rid1 = compute_receipt_id(receipt_id_payload(receipt))
    rid2 = compute_receipt_id(receipt_id_payload(receipt))
    assert rid1 == rid2


def test_receipt_id_recomputation_matches():
    receipt = read_json("examples/receipt_example.json")
    assert receipt["receipt_id"] == compute_receipt_id(receipt_id_payload(receipt))


def test_verification_passes_for_valid_receipt():
    receipt = read_json("examples/receipt_example.json")
    report = verify_receipt_data(receipt)
    assert report["valid"] is True
    assert report["verified"] is True


def test_verification_fails_if_computed_altered():
    receipt = read_json("examples/receipt_example.json")
    tampered = copy.deepcopy(receipt)
    tampered["computed"]["CMI"] = 0.0
    report = verify_receipt_data(tampered)
    assert report["verified"] is False


def test_verification_fails_if_receipt_id_altered():
    receipt = read_json("examples/receipt_example.json")
    tampered = copy.deepcopy(receipt)
    tampered["receipt_id"] = "dcl_obs_badbadbadbadbad"
    report = verify_receipt_data(tampered)
    assert report["verified"] is False


def test_json_and_markdown_export_work():
    receipt = read_json("examples/receipt_example.json")
    md = receipt_to_markdown(receipt)
    assert receipt["receipt_id"] in md
    assert "PHI369 Constants" in md
