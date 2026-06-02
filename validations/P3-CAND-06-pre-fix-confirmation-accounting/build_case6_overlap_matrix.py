#!/usr/bin/env python3
"""Build overlap matrix for P3-CAND-06."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


CASE_DIR = Path(__file__).resolve().parent
P3_CAND_04_KNOWN_ADDRESS = "gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09"


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


def overlap_status(row: dict[str, str]) -> tuple[str, str, str]:
    epoch = int(row["epoch"])
    if epoch == 276 and row["participant"] == P3_CAND_04_KNOWN_ADDRESS:
        return (
            "known_p3_cand_04_same_address",
            "blocked",
            "Known same-address overlap with local P3-CAND-04 evidence.",
        )
    if epoch == 276:
        return (
            "p3_cand_04_epoch_overlap_unresolved",
            "blocked",
            "Epoch 276 overlaps P3-CAND-04; full payout276 address list is not normalized in this repo.",
        )
    if 265 <= epoch <= 276:
        return (
            "p4_cand_01_epoch_range_overlap",
            "review",
            "Epoch is inside P4-CAND-01 Kimi restitution window; same-address duplicate check needs normalized P4 table.",
        )
    return ("no_known_overlap_in_local_repo", "clear", "No local P3/P4 overlap signal found.")


def build_rows() -> list[dict[str, Any]]:
    out = []
    for row in read_csv(CASE_DIR / "case6_row_formula_replay.csv"):
        status, action, reason = overlap_status(row)
        out.append(
            {
                "epoch": row["epoch"],
                "participant": row["participant"],
                "event_trigger_height": row["event_trigger_height"],
                "pass_models": row["pass_models"],
                "loss_gonka": row["loss_gonka"],
                "overlap_status": status,
                "recommended_action": action,
                "reason": reason,
            }
        )
    return out


def write_markdown(rows: list[dict[str, Any]]) -> None:
    by_status: dict[str, int] = {}
    for row in rows:
        by_status[row["overlap_status"]] = by_status.get(row["overlap_status"], 0) + 1
    lines = [
        "# P3-CAND-06 Overlap Matrix",
        "",
        "This matrix classifies duplicate-payment risk using only evidence",
        "available in this repository.",
        "",
        "## Summary",
        "",
        "| Overlap status | Rows |",
        "|---|---:|",
    ]
    for status, count in sorted(by_status.items()):
        lines.append(f"| `{status}` | `{count}` |")
    lines.extend(
        [
            "",
            "## Rows",
            "",
            "| Epoch | Participant | Pass model(s) | Loss, GONKA | Status | Action |",
            "|---:|---|---|---:|---|---|",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row['epoch']} | `{row['participant']}` | {row['pass_models']} | {row['loss_gonka']} | "
            f"`{row['overlap_status']}` | `{row['recommended_action']}` |"
        )
    lines.extend(
        [
            "",
            "## Rule",
            "",
            "- `blocked` rows must not be paid from P3-CAND-06 until duplicate risk is",
            "  resolved.",
            "- `review` rows need same-address comparison against a normalized external",
            "  table before payout.",
            "- `clear` rows have no local overlap signal, but still need eligibility",
            "  decision.",
            "",
            "Machine-readable versions are in `case6_overlap_matrix.csv` and",
            "`case6_overlap_matrix.json`.",
            "",
        ]
    )
    (CASE_DIR / "case6_overlap_matrix.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = build_rows()
    fieldnames = [
        "epoch",
        "participant",
        "event_trigger_height",
        "pass_models",
        "loss_gonka",
        "overlap_status",
        "recommended_action",
        "reason",
    ]
    write_csv(CASE_DIR / "case6_overlap_matrix.csv", rows, fieldnames)
    write_json(CASE_DIR / "case6_overlap_matrix.json", {"rows": rows})
    write_markdown(rows)
    print(json.dumps({"rows": len(rows), "blocked": sum(r["recommended_action"] == "blocked" for r in rows)}, sort_keys=True))


if __name__ == "__main__":
    main()
