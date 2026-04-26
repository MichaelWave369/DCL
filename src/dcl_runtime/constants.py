"""Project constants for DCL Runtime."""

SCHEMA_VERSION = "0.1"
FRAMEWORK_NAME = "Demiurgic Cosmology Lattice Runtime"

DIMENSION_COUNT = 12
FIELD_VARIABLE_COUNT = 12
SCALE_COUNT = 12
ARCHETYPE_COUNT = 12
FULL_LATTICE_CELL_COUNT = 12 ** 4

EPSILON = 0.000001
DEFAULT_SIGMOID_K = 5.0

PHI = 1.618033988749895
PHI369_COHERENCE_THRESHOLD = PHI / 2

MIN_SCORE = 0.0
MAX_SCORE = 1.0

DIMENSION_BANDS = {
    1: "Point / Seed",
    2: "Plane / Surface",
    3: "Volume / Body",
    4: "Time / Sequence",
    5: "Probability / Choice",
    6: "Polarity / Relation",
    7: "Memory / Lineage",
    8: "Mind / Symbol",
    9: "Network / Society",
    10: "Planetary / Biospheric",
    11: "Cosmic / Law-Set",
    12: "Coherence / Integration",
}

FIELD_VARIABLES = {
    1: "B Boundary Pressure",
    2: "R Recurrence Pressure",
    3: "I_g Ignorance Gradient",
    4: "S Suffering Stabilization",
    5: "E_x Extraction Pressure",
    6: "D_c Decay / Entropy Constraint",
    7: "C_o Coherence",
    8: "K Knowledge / Clarity",
    9: "A Authentic Agency",
    10: "M Meaning",
    11: "L_v Life-Value / Aliveness",
    12: "R_s Sovereign Resistance",
}

SCALE_LAYERS = {
    1: "Subtle / Signal",
    2: "Physical",
    3: "Biological",
    4: "Emotional",
    5: "Cognitive",
    6: "Individual",
    7: "Relational",
    8: "Social",
    9: "Institutional",
    10: "Planetary",
    11: "Cosmic",
    12: "Meta-Cosmic",
}

ARCHETYPES = {
    1: "Void Field",
    2: "Boundary Field",
    3: "Recurrence Field",
    4: "Extraction Field",
    5: "Prison Field",
    6: "Simulation Field",
    7: "School Field",
    8: "Forge Field",
    9: "Garden Field",
    10: "Contested Field",
    11: "Liberation Field",
    12: "Sovereign Field",
}

EVIDENCE_GRADES = {
    0: "Symbolic Coherence",
    1: "Subjective Pattern",
    2: "Behavioral Evidence",
    3: "Social / Systemic Evidence",
    4: "Cross-Domain Evidence",
    5: "Predictive Evidence",
}
