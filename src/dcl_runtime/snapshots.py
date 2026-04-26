"""Snapshot creation and comparison."""

from datetime import datetime, timezone
from statistics import mean
from typing import Any

from .classification import classify_cmi
from .constants import DEFAULT_SIGMOID_K, EPSILON
from .receipts import verify_receipt_data
from .scoring import cosmic_matrix_index
from .storage import read_json, stable_sha256, write_json



def _now_iso() -> str:
    return datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat()



def _snapshot_id_payload(omega_id: str, timestamp: str, receipt_ids: list[str]) -> dict[str, Any]:
    return {"omega_id": omega_id, "timestamp": timestamp, "receipt_ids": sorted(receipt_ids)}



def compute_snapshot_id(omega_id: str, timestamp: str, receipt_ids: list[str]) -> str:
    return "dcl_snap_" + stable_sha256(_snapshot_id_payload(omega_id, timestamp, receipt_ids))[:16]



def create_snapshot(receipt_paths: list[str], out_path: str, timestamp: str | None = None) -> dict[str, Any]:
    receipts: list[dict[str, Any]] = []
    for path in receipt_paths:
        receipt = read_json(path)
        if not isinstance(receipt, dict) or "receipt_id" not in receipt:
            continue
        report = verify_receipt_data(receipt)
        if not (report["valid"] and report["verified"]):
            raise ValueError(f"receipt failed verification: {path}")
        receipts.append(receipt)

    if not receipts:
        raise ValueError("no valid receipts found")

    receipts = sorted(receipts, key=lambda r: r["receipt_id"])
    omega_ids = {r["observer_anchor"]["omega_id"] for r in receipts}
    if len(omega_ids) != 1:
        raise ValueError("all receipts must share the same omega_id")
    omega_id = next(iter(omega_ids))

    d_avg = mean(r["computed"]["D_score"] for r in receipts)
    p_avg = mean(r["computed"]["Phi_score"] for r in receipts)
    dcr_avg = d_avg / (p_avg + EPSILON)
    cmi_avg = cosmic_matrix_index(d_avg, p_avg, k=DEFAULT_SIGMOID_K)

    ts = timestamp or _now_iso()
    receipt_ids = [r["receipt_id"] for r in receipts]
    snap_id = compute_snapshot_id(omega_id, ts, receipt_ids)
    snapshot = {
        "snapshot_id": snap_id,
        "timestamp": ts,
        "omega_id": omega_id,
        "observation_count": len(receipts),
        "receipt_ids": receipt_ids,
        "averages": {
            "D_score": d_avg,
            "Phi_score": p_avg,
            "DCR": dcr_avg,
            "CMI": cmi_avg,
            "classification": classify_cmi(cmi_avg),
        },
        "receipts": receipts,
    }
    write_json(out_path, snapshot)
    return snapshot



def compare_snapshots(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    delta_d = after["averages"]["D_score"] - before["averages"]["D_score"]
    delta_phi = after["averages"]["Phi_score"] - before["averages"]["Phi_score"]
    delta_dcr = after["averages"]["DCR"] - before["averages"]["DCR"]
    delta_cmi = after["averages"]["CMI"] - before["averages"]["CMI"]

    if delta_phi > 0 and delta_d <= 0:
        interpretation = "coherence_gain_without_recapture"
    elif delta_phi > 0 and delta_d > 0:
        interpretation = "coherence_gain_with_possible_recapture"
    elif delta_phi <= 0 and delta_d > 0:
        interpretation = "constraint_increase"
    else:
        interpretation = "mixed_or_stable"

    return {
        "delta_D": delta_d,
        "delta_Phi": delta_phi,
        "delta_DCR": delta_dcr,
        "delta_CMI": delta_cmi,
        "interpretation": interpretation,
    }
