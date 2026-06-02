#!/usr/bin/env python3
"""Build technical eligibility matrix for P3-CAND-06 rows."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


CASE_DIR = Path(__file__).resolve().parent


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def index(rows: list[dict[str, str]]) -> dict[tuple[str, str, str], dict[str, str]]:
    return {(row["epoch"], row["participant"], row["event_trigger_height"]): row for row in rows}


def technical_status(row: dict[str, str], old_row: dict[str, str], new_row: dict[str, str]) -> tuple[str, str]:
    if row["epoch"] == "276":
        return (
            "blocked_epoch276_overlap",
            "Epoch 276 must be resolved against P3-CAND-04 before payout, regardless of formula replay status.",
        )
    if old_row.get("old_formula_matches_stored") == "True" and new_row.get("new_algorithm_would_pass_alpha") == "False":
        return (
            "formula_reconciled_policy_required",
            "The chain formula is reproducible and still below alpha in bounded v0.2.13-style replay; payout depends on single-model policy.",
        )
    if old_row.get("old_formula_matches_stored") != "True":
        return (
            "technical_replay_gap",
            "Stored ratio is not fully reproduced by the old formula replay; keep blocked until explained.",
        )
    return (
        "review_required",
        "Technical facts are available, but classification needs manual review.",
    )


def build_rows() -> list[dict[str, Any]]:
    root_rows = read_csv(CASE_DIR / "case6_row_formula_replay.csv")
    old_by_key = index(read_csv(CASE_DIR / "case6_full_old_formula_replay.csv"))
    new_by_key = index(read_csv(CASE_DIR / "case6_new_algorithm_replay.csv"))
    out = []
    for row in root_rows:
        key = (row["epoch"], row["participant"], row["event_trigger_height"])
        old_row = old_by_key.get(key, {})
        new_row = new_by_key.get(key, {})
        status, reason = technical_status(row, old_row, new_row)
        out.append(
            {
                "epoch": row["epoch"],
                "participant": row["participant"],
                "event_trigger_height": row["event_trigger_height"],
                "pass_models": row["pass_models"],
                "qwen_result": row["qwen_result"],
                "kimi_result": row["kimi_result"],
                "stored_confirmation_ratio": row["stored_confirmation_ratio"],
                "old_formula_matches_stored": old_row.get("old_formula_matches_stored", ""),
                "new_algorithm_would_pass_alpha": new_row.get("new_algorithm_would_pass_alpha", ""),
                "loss_gonka": row["loss_gonka"],
                "technical_status": status,
                "eligibility_decision": "committee_policy_required",
                "reason": reason,
            }
        )
    return out


def write_markdown(rows: list[dict[str, Any]]) -> None:
    by_status: dict[str, int] = {}
    for row in rows:
        by_status[row["technical_status"]] = by_status.get(row["technical_status"], 0) + 1
    lines = [
        "# P3-CAND-06 Eligibility Matrix",
        "",
        "This matrix separates technical replay status from compensation eligibility.",
        "It does not approve payouts.",
        "",
        "## Summary",
        "",
        "| Technical status | Rows |",
        "|---|---:|",
    ]
    for status, count in sorted(by_status.items()):
        lines.append(f"| `{status}` | `{count}` |")
    lines.extend(
        [
            "",
            "## Rows",
            "",
            "| Epoch | Participant | Pass model(s) | Old formula match | New replay pass alpha | Loss, GONKA | Technical status |",
            "|---:|---|---|---|---|---:|---|",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row['epoch']} | `{row['participant']}` | {row['pass_models']} | "
            f"{row['old_formula_matches_stored']} | {row['new_algorithm_would_pass_alpha']} | "
            f"{row['loss_gonka']} | `{row['technical_status']}` |"
        )
    lines.extend(
        [
            "",
            "## Decision Boundary",
            "",
            "- `formula_reconciled_policy_required` means the technical chain state is",
            "  reproducible, but payout still depends on whether the committee treats",
            "  single-model pass rows as compensable.",
            "- `blocked_epoch276_overlap` must be resolved against P3-CAND-04 before",
            "  any payout decision.",
            "- `technical_replay_gap` requires more technical work before policy review.",
            "",
            "Machine-readable versions are in `case6_eligibility_matrix.csv` and",
            "`case6_eligibility_matrix.json`.",
            "",
        ]
    )
    (CASE_DIR / "case6_eligibility_matrix.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = build_rows()
    fieldnames = [
        "epoch",
        "participant",
        "event_trigger_height",
        "pass_models",
        "qwen_result",
        "kimi_result",
        "stored_confirmation_ratio",
        "old_formula_matches_stored",
        "new_algorithm_would_pass_alpha",
        "loss_gonka",
        "technical_status",
        "eligibility_decision",
        "reason",
    ]
    write_csv(CASE_DIR / "case6_eligibility_matrix.csv", rows, fieldnames)
    write_json(CASE_DIR / "case6_eligibility_matrix.json", {"rows": rows})
    write_markdown(rows)
    print(json.dumps({"rows": len(rows), "statuses": {s: sum(r["technical_status"] == s for r in rows) for s in sorted({r["technical_status"] for r in rows})}}, sort_keys=True))


if __name__ == "__main__":
    main()
