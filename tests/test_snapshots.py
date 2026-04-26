import pytest

from dcl_runtime.snapshots import compare_snapshots, create_snapshot
from dcl_runtime.storage import read_json, write_json


def test_snapshot_from_two_receipts(tmp_path):
    r = read_json("examples/receipt_example.json")
    p1 = tmp_path / "r1.json"
    p2 = tmp_path / "r2.json"
    write_json(p1, r)
    write_json(p2, r)

    out = tmp_path / "snapshot.json"
    snap = create_snapshot([str(p1), str(p2)], str(out), timestamp="2026-01-01T00:00:00+00:00")
    assert snap["observation_count"] == 2
    assert snap["averages"]["D_score"] == r["computed"]["D_score"]


def test_snapshot_id_deterministic(tmp_path):
    p = tmp_path / "snapshot.json"
    snap1 = create_snapshot(["examples/receipt_example.json"], str(p), timestamp="2026-01-01T00:00:00+00:00")
    snap2 = create_snapshot(["examples/receipt_example.json"], str(p), timestamp="2026-01-01T00:00:00+00:00")
    assert snap1["snapshot_id"] == snap2["snapshot_id"]


def test_compare_snapshots_reports_deltas():
    before = {"averages": {"D_score": 0.6, "Phi_score": 0.4, "DCR": 1.5, "CMI": 0.7}}
    after = {"averages": {"D_score": 0.5, "Phi_score": 0.5, "DCR": 1.0, "CMI": 0.5}}
    result = compare_snapshots(before, after)
    assert result["delta_D"] == pytest.approx(-0.1)
    assert result["delta_Phi"] == pytest.approx(0.1)
    assert result["interpretation"] == "coherence_gain_without_recapture"
