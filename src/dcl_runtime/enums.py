"""Enumerations for DCL Runtime."""

from enum import Enum


class Classification(str, Enum):
    LIBERATION_FIELD = "liberation_field"
    GARDEN_GROWTH_FIELD = "garden_growth_field"
    CONTESTED_FIELD = "contested_field"
    PRISON_EXTRACTION_FIELD = "prison_extraction_field"
    HIGH_MATRIX_CAPTURE = "high_matrix_capture"
