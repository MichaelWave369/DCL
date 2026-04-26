"""Command line interface for dcl runtime."""

import argparse
import glob
import json
from dataclasses import asdict

from .classification import classify_cmi
from .constants import (
    ARCHETYPES,
    DIMENSION_BANDS,
    FIELD_VARIABLES,
    FRAMEWORK_NAME,
    SCALE_LAYERS,
    SCHEMA_VERSION,
)
from .interventions import rank_interventions
from .models import FieldScores
from .recapture import recapture_tax
from .receipts import validate_receipt, verify_receipt
from .scoring import compute_scores
from .snapshots import compare_snapshots, create_snapshot
from .storage import read_json



def _print(data, as_json: bool = True) -> None:
    if as_json:
        print(json.dumps(data, indent=2))
    else:
        print(data)



def cmd_constants(args):
    out = {
        "schema_version": SCHEMA_VERSION,
        "framework": FRAMEWORK_NAME,
        "dimensions": DIMENSION_BANDS,
        "fields": FIELD_VARIABLES,
        "scales": SCALE_LAYERS,
        "archetypes": ARCHETYPES,
    }
    _print(out, True)



def cmd_score(args):
    scores = FieldScores(
        B=args.B,
        R=args.R,
        I_g=args.Ig,
        S=args.S,
        E_x=args.Ex,
        D_c=args.Dc,
        C_o=args.Co,
        K=args.K,
        A=args.A,
        M=args.M,
        L_v=args.Lv,
        R_s=args.Rs,
    )
    temp = compute_scores(scores, classification="")
    computed = compute_scores(scores, classification=classify_cmi(temp.CMI))
    _print(asdict(computed), True)



def cmd_validate(args):
    report = validate_receipt(args.receipt)
    _print(report, True)



def cmd_verify(args):
    report = verify_receipt(args.receipt)
    _print(report, True)



def cmd_snapshot(args):
    paths = []
    for pattern in args.receipts:
        paths.extend(glob.glob(pattern))
    snapshot = create_snapshot(paths, args.out, timestamp=args.timestamp)
    _print(snapshot, True)



def cmd_compare(args):
    before = read_json(args.before)
    after = read_json(args.after)
    _print(compare_snapshots(before, after), True)



def cmd_recapture(args):
    before = read_json(args.before)
    after = read_json(args.after)
    _print(recapture_tax(before, after), True)



def cmd_recommend(args):
    report = verify_receipt(args.receipt)
    if not report["verified"]:
        raise SystemExit("receipt must validate and verify before recommendations")
    rec = read_json(args.receipt)
    ranked = rank_interventions(
        rec["computed"]["dominant_constraint"], rec["computed"]["dominant_coherence"]
    )
    if args.json:
        _print({"recommendations": ranked}, True)
    else:
        for idx, item in enumerate(ranked, start=1):
            print(f"{idx}. {item['title']} ({item['key']}) allowed={item['allowed']} LES={item['LES']:.4f}")



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dcl")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("constants")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_constants)

    p = sub.add_parser("score")
    for flag in ["B", "R", "Ig", "S", "Ex", "Dc", "Co", "K", "A", "M", "Lv", "Rs"]:
        p.add_argument(f"--{flag}", type=float, required=True)
    p.set_defaults(func=cmd_score)

    p = sub.add_parser("validate")
    p.add_argument("--receipt", required=True)
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("verify")
    p.add_argument("--receipt", required=True)
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("snapshot")
    p.add_argument("--receipts", nargs="+", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--timestamp")
    p.set_defaults(func=cmd_snapshot)

    p = sub.add_parser("compare")
    p.add_argument("--before", required=True)
    p.add_argument("--after", required=True)
    p.set_defaults(func=cmd_compare)

    p = sub.add_parser("recapture")
    p.add_argument("--before", required=True)
    p.add_argument("--after", required=True)
    p.set_defaults(func=cmd_recapture)

    p = sub.add_parser("recommend")
    p.add_argument("--receipt", required=True)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_recommend)
    return parser



def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
