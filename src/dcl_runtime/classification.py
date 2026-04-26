"""Classification mapping for CMI bands."""

from .enums import Classification



def classify_cmi(cmi: float) -> str:
    if cmi <= 0.20:
        return Classification.LIBERATION_FIELD.value
    if cmi <= 0.40:
        return Classification.GARDEN_GROWTH_FIELD.value
    if cmi <= 0.60:
        return Classification.CONTESTED_FIELD.value
    if cmi <= 0.80:
        return Classification.PRISON_EXTRACTION_FIELD.value
    return Classification.HIGH_MATRIX_CAPTURE.value
