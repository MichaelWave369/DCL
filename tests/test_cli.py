import json
import os
import subprocess
import sys

from dcl_runtime.storage import read_json, write_json



def run_cli(args):
    env = dict(os.environ)
    env["PYTHONPATH"] = "src"
    return subprocess.run([sys.executable, "-m", "dcl_runtime.cli", *args], check=False, capture_output=True, text=True, env=env)


def test_dcl_score_returns_expected_json():
    p = run_cli([
        "score", "--B", "0.70", "--R", "0.85", "--Ig", "0.55", "--S", "0.65", "--Ex", "0.75", "--Dc", "0.45",
        "--Co", "0.50", "--K", "0.60", "--A", "0.48", "--M", "0.55", "--Lv", "0.40", "--Rs", "0.52"
    ])
    assert p.returncode == 0
    data = json.loads(p.stdout)
    assert data["classification"] == "prison_extraction_field"


def test_dcl_validate_passes_valid_receipt():
    p = run_cli(["validate", "--receipt", "examples/receipt_example.json"])
    assert json.loads(p.stdout)["valid"] is True


def test_dcl_validate_fails_missing_counter_evidence(tmp_path):
    receipt = read_json("examples/receipt_example.json")
    receipt["evidence"]["counter_evidence"] = ""
    pth = tmp_path / "bad.json"
    write_json(pth, receipt)
    p = run_cli(["validate", "--receipt", str(pth)])
    assert json.loads(p.stdout)["valid"] is False


def test_dcl_verify_detects_mismatch(tmp_path):
    receipt = read_json("examples/receipt_example.json")
    receipt["computed"]["D_score"] = 0.0
    pth = tmp_path / "bad2.json"
    write_json(pth, receipt)
    p = run_cli(["verify", "--receipt", str(pth)])
    assert json.loads(p.stdout)["verified"] is False


def test_dcl_constants_json_returns_tables():
    p = run_cli(["constants", "--json"])
    data = json.loads(p.stdout)
    assert "dimensions" in data and "fields" in data and "scales" in data and "archetypes" in data
