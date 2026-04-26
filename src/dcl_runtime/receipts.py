"""Receipt validation and verification."""

from dataclasses import asdict
from typing import Any

from .classification import classify_cmi
from .constants import EPSILON, FRAMEWORK_NAME, SCHEMA_VERSION
from .models import (
    ComputedScores,
    Evidence,
    FieldScores,
    LatticeCoordinate,
    ObservationReceipt,
    ObserverAnchor,
)
from .scoring import compute_scores
from .storage import read_json, stable_sha256

SCORE_FIELDS = ["B", "R", "I_g", "S", "E_x", "D_c", "C_o", "K", "A", "M", "L_v", "R_s"]



def build_coordinate(data: dict[str, Any]) -> LatticeCoordinate:
    return LatticeCoordinate(
        dimension_id=data["dimension_id"],
        field_variable_id=data["field_variable_id"],
        scale_id=data["scale_id"],
        archetype_id=data["archetype_id"],
    )



def build_scores(data: dict[str, Any]) -> FieldScores:
    return FieldScores(**{k: data[k] for k in SCORE_FIELDS})



def compute_receipt_id(payload: dict[str, Any]) -> str:
    return "dcl_obs_" + stable_sha256(payload)[:16]



def receipt_id_payload(receipt: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": receipt["schema_version"],
        "timestamp": receipt["timestamp"],
        "coordinate": build_coordinate(receipt["coordinate"]).key(),
        "scores": {k: receipt["scores"][k] for k in SCORE_FIELDS},
        "claim": receipt["claim"],
        "evidence_grade": receipt["evidence"]["grade"],
        "counter_evidence": receipt["evidence"]["counter_evidence"],
        "omega_id": receipt["observer_anchor"]["omega_id"],
    }



def validate_receipt_data(receipt: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    try:
        if not receipt.get("schema_version"):
            errors.append("schema_version missing")
        if not receipt.get("framework"):
            errors.append("framework missing")
        build_coordinate(receipt.get("coordinate", {}))
        ObserverAnchor(**receipt.get("observer_anchor", {}))
        if not receipt.get("claim"):
            errors.append("claim missing")
        Evidence(**receipt.get("evidence", {}))
        scores = receipt.get("scores", {})
        for f in SCORE_FIELDS:
            if f not in scores:
                errors.append(f"scores.{f} missing")
        if not errors:
            build_scores(scores)
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return (len(errors) == 0, errors)



def validate_receipt(path: str) -> dict[str, Any]:
    receipt = read_json(path)
    valid, errors = validate_receipt_data(receipt)
    return {"valid": valid, "errors": errors}



def _float_close(a: float, b: float) -> bool:
    return abs(a - b) <= EPSILON



def recompute(receipt: dict[str, Any]) -> tuple[ComputedScores, str]:
    scores = build_scores(receipt["scores"])
    dummy = compute_scores(scores, classification="")
    classification = classify_cmi(dummy.CMI)
    computed = compute_scores(scores, classification)
    rid = compute_receipt_id(receipt_id_payload(receipt))
    return computed, rid



def verify_receipt_data(receipt: dict[str, Any]) -> dict[str, Any]:
    valid, errors = validate_receipt_data(receipt)
    if not valid:
        return {
            "valid": False,
            "verified": False,
            "receipt_id_match": False,
            "mismatches": errors,
            "recomputed": {},
            "receipt_values": receipt.get("computed", {}),
        }

    recomputed, expected_id = recompute(receipt)
    mismatches: list[str] = []
    receipt_computed = receipt.get("computed", {})

    for key, val in asdict(recomputed).items():
        actual = receipt_computed.get(key)
        if isinstance(val, float):
            if actual is None or not _float_close(val, actual):
                mismatches.append(f"computed.{key}")
        elif actual != val:
            mismatches.append(f"computed.{key}")

    id_match = receipt.get("receipt_id") == expected_id
    if not id_match:
        mismatches.append("receipt_id")

    return {
        "valid": True,
        "verified": len(mismatches) == 0,
        "receipt_id_match": id_match,
        "mismatches": mismatches,
        "recomputed": asdict(recomputed),
        "receipt_values": receipt_computed,
        "expected_receipt_id": expected_id,
    }



def verify_receipt(path: str) -> dict[str, Any]:
    return verify_receipt_data(read_json(path))



def materialize_receipt(data: dict[str, Any]) -> ObservationReceipt:
    computed = ComputedScores(**data["computed"])
    return ObservationReceipt(
        receipt_id=data["receipt_id"],
        schema_version=data.get("schema_version", SCHEMA_VERSION),
        timestamp=data["timestamp"],
        framework=data.get("framework", FRAMEWORK_NAME),
        coordinate=build_coordinate(data["coordinate"]),
        observer_anchor=ObserverAnchor(**data["observer_anchor"]),
        claim=data["claim"],
        evidence=Evidence(**data["evidence"]),
        scores=build_scores(data["scores"]),
        computed=computed,
    )
