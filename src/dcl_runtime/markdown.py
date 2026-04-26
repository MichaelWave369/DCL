"""Markdown export helpers."""

from .constants import PHI, PHI369_COHERENCE_THRESHOLD



def receipt_to_markdown(receipt: dict) -> str:
    c = receipt["coordinate"]
    oa = receipt["observer_anchor"]
    ev = receipt["evidence"]
    lines = [
        f"# Observation Receipt {receipt['receipt_id']}",
        "",
        f"- Timestamp: {receipt['timestamp']}",
        "",
        "## Coordinate",
        "",
        "| axis | value |",
        "|---|---|",
        f"| dimension_id | {c['dimension_id']} |",
        f"| field_variable_id | {c['field_variable_id']} |",
        f"| scale_id | {c['scale_id']} |",
        f"| archetype_id | {c['archetype_id']} |",
        "",
        "## Observer Anchor",
        f"- omega_id: {oa['omega_id']}",
        f"- observer_role: {oa.get('observer_role', '')}",
        f"- epistemic_stance: {oa.get('epistemic_stance', '')}",
        f"- confidence: {oa.get('confidence', '')}",
        f"- bias_notes: {oa.get('bias_notes', '')}",
        "",
        "## Claim",
        receipt["claim"],
        "",
        "## Evidence",
        f"- grade: {ev['grade']}",
        f"- summary: {ev['summary']}",
        f"- counter_evidence: {ev['counter_evidence']}",
        "",
        "## Scores",
    ]
    for k, v in receipt["scores"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Computed")
    for k, v in receipt["computed"].items():
        lines.append(f"- {k}: {v}")
    lines.extend(
        [
            "",
            "## PHI369 Constants",
            f"- PHI: {PHI}",
            f"- C_STAR: {PHI369_COHERENCE_THRESHOLD}",
        ]
    )
    return "\n".join(lines) + "\n"
