"""Recapture tax calculations."""

from typing import Any

from .constants import EPSILON



def _extract_scores(data: dict[str, Any]) -> tuple[float, float]:
    if "computed" in data:
        return data["computed"]["D_score"], data["computed"]["Phi_score"]
    if "averages" in data:
        return data["averages"]["D_score"], data["averages"]["Phi_score"]
    raise ValueError("input must be receipt or snapshot")



def recapture_tax(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    before_d, before_phi = _extract_scores(before)
    after_d, after_phi = _extract_scores(after)
    delta_d = after_d - before_d
    delta_phi = after_phi - before_phi

    if delta_phi > 0 and delta_d <= 0:
        status = "no_recapture"
        tax = delta_d / (delta_phi + EPSILON)
        tax_infinite = False
    elif delta_phi > 0:
        tax = delta_d / (delta_phi + EPSILON)
        tax_infinite = False
        if 0 < tax < 1:
            status = "partial_recapture"
        else:
            status = "high_recapture"
    elif delta_phi <= 0 and delta_d > 0:
        status = "constraint_gain_without_coherence"
        tax = None
        tax_infinite = True
    else:
        status = "stable_or_unclear"
        tax = delta_d / (delta_phi + EPSILON)
        tax_infinite = False

    return {
        "delta_D": delta_d,
        "delta_Phi": delta_phi,
        "recapture_tax": tax,
        "tax_infinite": tax_infinite,
        "status": status,
    }
