"""Data models for DCL Runtime."""

from dataclasses import asdict, dataclass

from .constants import MAX_SCORE, MIN_SCORE



def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required")



def _require_between(value: float, min_v: float, max_v: float, field_name: str) -> None:
    if not (min_v <= value <= max_v):
        raise ValueError(f"{field_name} must be between {min_v} and {max_v}")



def _require_int_range(value: int, min_v: int, max_v: int, field_name: str) -> None:
    if not isinstance(value, int) or not (min_v <= value <= max_v):
        raise ValueError(f"{field_name} must be between {min_v} and {max_v}")


@dataclass(frozen=True)
class LatticeCoordinate:
    dimension_id: int
    field_variable_id: int
    scale_id: int
    archetype_id: int

    def __post_init__(self) -> None:
        _require_int_range(self.dimension_id, 1, 12, "dimension_id")
        _require_int_range(self.field_variable_id, 1, 12, "field_variable_id")
        _require_int_range(self.scale_id, 1, 12, "scale_id")
        _require_int_range(self.archetype_id, 1, 12, "archetype_id")

    def key(self) -> str:
        return f"d{self.dimension_id:02d}_f{self.field_variable_id:02d}_s{self.scale_id:02d}_a{self.archetype_id:02d}"


@dataclass(frozen=True)
class FieldScores:
    B: float
    R: float
    I_g: float
    S: float
    E_x: float
    D_c: float
    C_o: float
    K: float
    A: float
    M: float
    L_v: float
    R_s: float

    def __post_init__(self) -> None:
        for field_name, value in asdict(self).items():
            _require_between(value, MIN_SCORE, MAX_SCORE, field_name)


@dataclass(frozen=True)
class Evidence:
    grade: int
    source_type: str
    summary: str
    counter_evidence: str

    def __post_init__(self) -> None:
        _require_int_range(self.grade, 0, 5, "grade")
        _require_non_empty(self.summary, "summary")
        _require_non_empty(self.counter_evidence, "counter_evidence")


@dataclass(frozen=True)
class ObserverAnchor:
    omega_id: str
    observer_role: str = ""
    epistemic_stance: str = ""
    confidence: float = 0.5
    bias_notes: str = ""

    def __post_init__(self) -> None:
        _require_non_empty(self.omega_id, "omega_id")
        _require_between(self.confidence, 0.0, 1.0, "confidence")


@dataclass(frozen=True)
class ComputedScores:
    D_score: float
    Phi_score: float
    DCR: float
    CMI: float
    classification: str
    phi369_threshold_met: bool
    dominant_constraint: str
    dominant_coherence: str


@dataclass(frozen=True)
class LatticeObservation:
    coordinate: LatticeCoordinate
    scores: FieldScores
    evidence: Evidence
    observer_anchor: ObserverAnchor
    claim: str
    notes: str = ""

    def __post_init__(self) -> None:
        _require_non_empty(self.claim, "claim")


@dataclass(frozen=True)
class ObservationReceipt:
    receipt_id: str
    schema_version: str
    timestamp: str
    framework: str
    coordinate: LatticeCoordinate
    observer_anchor: ObserverAnchor
    claim: str
    evidence: Evidence
    scores: FieldScores
    computed: ComputedScores


@dataclass(frozen=True)
class LatticeSnapshot:
    snapshot_id: str
    timestamp: str
    omega_id: str
    observation_count: int
    receipt_ids: list[str]
    averages: dict
    receipts: list[dict]
