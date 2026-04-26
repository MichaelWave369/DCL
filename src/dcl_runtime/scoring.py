"""Scoring functions for DCL Runtime."""

import math
from dataclasses import asdict

from .constants import DEFAULT_SIGMOID_K, EPSILON, PHI369_COHERENCE_THRESHOLD
from .models import ComputedScores, FieldScores

CONSTRAINT_FIELDS = ("B", "R", "I_g", "S", "E_x", "D_c")
COHERENCE_FIELDS = ("C_o", "K", "A", "M", "L_v", "R_s")



def constraint_score(scores: FieldScores) -> float:
    d = asdict(scores)
    return sum(d[k] for k in CONSTRAINT_FIELDS) / 6



def coherence_score(scores: FieldScores) -> float:
    d = asdict(scores)
    return sum(d[k] for k in COHERENCE_FIELDS) / 6



def demiurgic_constraint_ratio(d_score: float, phi_score: float) -> float:
    return d_score / (phi_score + EPSILON)



def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))



def cosmic_matrix_index(d_score: float, phi_score: float, k: float = DEFAULT_SIGMOID_K) -> float:
    return sigmoid(k * (d_score - phi_score))



def dominant_constraint(scores: FieldScores) -> str:
    data = asdict(scores)
    return sorted(CONSTRAINT_FIELDS, key=lambda f: (-data[f], f))[0]



def dominant_coherence(scores: FieldScores) -> str:
    data = asdict(scores)
    return sorted(COHERENCE_FIELDS, key=lambda f: (-data[f], f))[0]



def compute_scores(scores: FieldScores, classification: str) -> ComputedScores:
    d_score = constraint_score(scores)
    phi_score = coherence_score(scores)
    dcr = demiurgic_constraint_ratio(d_score, phi_score)
    cmi = cosmic_matrix_index(d_score, phi_score)
    return ComputedScores(
        D_score=d_score,
        Phi_score=phi_score,
        DCR=dcr,
        CMI=cmi,
        classification=classification,
        phi369_threshold_met=(phi_score >= PHI369_COHERENCE_THRESHOLD and dcr < 1.0),
        dominant_constraint=dominant_constraint(scores),
        dominant_coherence=dominant_coherence(scores),
    )
