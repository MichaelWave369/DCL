"""Intervention recommendation engine."""

from dataclasses import dataclass

from .constants import EPSILON


@dataclass(frozen=True)
class Intervention:
    key: str
    title: str
    description: str
    target_variables: tuple[str, ...]
    expected_delta_phi: float
    expected_delta_D: float
    cost: float
    risk: float


DEFAULT_INTERVENTIONS = [
    Intervention("clarity_journal_10m", "10-Minute Clarity Journal", "Write the loop, the burden, the false choice, and one next action.", ("K", "A", "C_o"), 0.15, 0.02, 0.03, 0.01),
    Intervention("one_boundary_action", "One Boundary Action", "Take one small action that reduces extraction or protects attention.", ("A", "R_s", "E_x"), 0.18, 0.04, 0.06, 0.03),
    Intervention("community_signal", "Community Signal", "Ask one trusted person for clarity, reflection, or support.", ("L_v", "K", "C_o"), 0.20, 0.03, 0.05, 0.03),
    Intervention("coherence_breath_3m", "3-Minute Coherence Breath", "Sit with breath for 3 minutes and feel the signal beneath the noise.", ("C_o",), 0.10, 0.00, 0.01, 0.00),
    Intervention("sovereignty_audit", "Sovereignty Audit", "Identify one narrative absorbed that does not feel self-authored.", ("R_s", "A"), 0.12, 0.01, 0.02, 0.02),
    Intervention("aliveness_move", "Aliveness Movement", "Move the body in a non-performative way.", ("L_v", "C_o"), 0.12, 0.01, 0.02, 0.00),
    Intervention("meaning_reconnect", "Meaning Reconnection", "Spend 15 minutes doing something that makes time disappear.", ("M", "L_v"), 0.14, 0.01, 0.04, 0.01),
    Intervention("knowledge_primary", "Primary Source Dive", "Read one primary source instead of someone else's summary.", ("K", "A"), 0.13, 0.02, 0.05, 0.01),
]



def is_allowed(intervention: Intervention) -> bool:
    return (intervention.expected_delta_phi - intervention.expected_delta_D) > (intervention.cost + intervention.risk)



def liberation_efficiency_score(intervention: Intervention) -> float:
    return (intervention.expected_delta_phi - intervention.expected_delta_D) / (intervention.cost + EPSILON)



def rank_interventions(dominant_constraint: str, dominant_coherence: str) -> list[dict]:
    ranked = []
    for iv in DEFAULT_INTERVENTIONS:
        ranked.append(
            {
                "key": iv.key,
                "title": iv.title,
                "description": iv.description,
                "target_variables": list(iv.target_variables),
                "expected_delta_phi": iv.expected_delta_phi,
                "expected_delta_D": iv.expected_delta_D,
                "cost": iv.cost,
                "risk": iv.risk,
                "allowed": is_allowed(iv),
                "LES": liberation_efficiency_score(iv),
                "context": {
                    "dominant_constraint": dominant_constraint,
                    "dominant_coherence": dominant_coherence,
                },
            }
        )
    return sorted(ranked, key=lambda x: (not x["allowed"], -x["LES"], x["key"]))
