# DCL Runtime v0.1 · Open Source

DCL — Demiurgic Cosmology Lattice Runtime is a local-first Python runtime for validating, verifying, snapshotting, comparing, and analyzing observation receipts from the DCL Observatory frontend.

**The Observatory may create the receipt, but the Runtime proves the receipt.**

**Do not prove the myth first. Prove the structure first.**

**The runtime does not prove metaphysical claims. It verifies whether an observation receipt is internally consistent under the DCL constraint-coherence model.**

## What this runtime does

- Validates required receipt structure and score bounds.
- Recomputes and verifies receipt computed fields and canonical `receipt_id`.
- Builds deterministic snapshots from verified receipts.
- Compares snapshots over time for signal changes.
- Computes Recapture Tax from receipt/snapshot transitions.
- Ranks intervention candidates with deterministic sorting.

## What this runtime does not claim

This runtime does **not** claim to prove any literal demiurge, literal prison universe, literal simulation, or literal 12-dimensional physics model.

## Core formulas

- `D_score = (B + R + I_g + S + E_x + D_c) / 6`
- `Phi_score = (C_o + K + A + M + L_v + R_s) / 6`
- `DCR = D_score / (Phi_score + epsilon)` where `epsilon = 0.000001`
- `CMI = sigmoid(k * (D_score - Phi_score))` where `k = 5.0`
- `sigmoid(x) = 1 / (1 + exp(-x))`
- `PHI = 1.618033988749895`
- `C_STAR = PHI / 2`
- `phi369_threshold_met = (Phi_score >= C_STAR and DCR < 1.0)`

## CLI examples

```bash
dcl constants --json

dcl score --B 0.70 --R 0.85 --Ig 0.55 --S 0.65 --Ex 0.75 --Dc 0.45 --Co 0.50 --K 0.60 --A 0.48 --M 0.55 --Lv 0.40 --Rs 0.52

dcl validate --receipt examples/receipt_example.json
dcl verify --receipt examples/receipt_example.json

dcl snapshot --receipts examples/*.json --out out/snapshot.json --timestamp 2026-01-01T00:00:00+00:00
dcl compare --before out/snapshot_a.json --after out/snapshot_b.json

dcl recapture --before before.json --after after.json

dcl recommend --receipt examples/receipt_example.json --json
```

## Receipt verification workflow

1. Load receipt JSON.
2. Validate required fields.
3. Recompute scores/classification and dominant variables.
4. Recompute canonical hash-based `receipt_id`.
5. Compare recomputed values to receipt values with tolerance `1e-6`.

## Snapshot workflow

1. Validate and verify each input receipt.
2. Sort by `receipt_id`.
3. Compute average `D_score` and `Phi_score`.
4. Compute derived `DCR` and `CMI` from averages.
5. Write deterministic `snapshot_id` with canonical hash payload.

## Recapture Tax

`R_T = delta_D / (delta_Phi + epsilon)`

If `delta_Phi <= 0 and delta_D > 0`, `recapture_tax` is `null` and `tax_infinite = true`.

## Intervention recommendations

Recommendations are ranked by:
1. Allowed interventions first (`expected_delta_phi - expected_delta_D > cost + risk`)
2. Highest LES next (`LES = (expected_delta_phi - expected_delta_D) / (cost + epsilon)`)

## Local-first privacy

- File-based workflows only
- No network calls
- No telemetry
- No hidden background services

## License

MIT License, copyright (c) 2026 PHI369 Labs / Parallax. See [LICENSE](LICENSE). Third-party material remains under its respective rights and attribution requirements.

## DCL Observatory (React)

An interactive static website lives in [`site/`](site/README.md). It runs the documented scoring equations against a local, illustrative scenario and shows the repository's sample observation receipt. **It is not the Python receipt verifier**, and its downloads are not canonical verified receipts.

**Website after enabling GitHub Actions Pages:** https://michaelwave369.github.io/DCL/
