#!/usr/bin/env python3
"""Build gross compensation tables for P3-CAND-06 before overlap review."""

from __future__ import annotations

import json
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
from typing import Any

from build_case6_evidence_ledger import amount, build_rows, write_csv, write_json


CASE_DIR = Path(__file__).resolve().parent


def decimal_sum(rows: list[dict[str, Any]], field: str = "gross_compensation_gonka") -> Decimal:
    return sum(Decimal(str(row[field])) for row in rows)


def sorted_join(values: set[str]) -> str:
    return ", ".join(sorted(values, key=lambda item: (int(item) if item.isdigit() else item)))


def build_calculation_rows() -> list[dict[str, Any]]:
    rows = []
    for row in build_rows():
        rows.append(
            {
                "epoch": row["epoch"],
                "participant": row["participant"],
                "event_trigger_height": row["event_trigger_height"],
                "exclusion_height": row["exclusion_height"],
                "pass_models": row["pass_models"],
                "qwen_pass_weight": row["qwen_pass_weight"],
                "kimi_pass_weight": row["kimi_pass_weight"],
                "stored_ratio_percent": row["stored_ratio_percent"],
                "old_formula_matches_stored": row["old_formula_matches_stored"],
                "bounded_new_algorithm_would_pass_alpha": row["new_algorithm_would_pass_alpha"],
                "technical_status": row["technical_status"],
                "overlap_status_reference_only": row["overlap_status"],
                "gross_compensation_gonka": row["loss_gonka"],
                "calculation_scope": "included_before_overlap_review",
                "note": "Gross candidate amount; do not treat as approved payout until policy and overlap review are complete.",
            }
        )
    return rows


def aggregate_by_epoch(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["epoch"]].append(row)
    return [
        {
            "epoch": epoch,
            "rows": len(epoch_rows),
            "unique_participants": len({row["participant"] for row in epoch_rows}),
            "gross_compensation_gonka": str(decimal_sum(epoch_rows)),
        }
        for epoch, epoch_rows in sorted(grouped.items(), key=lambda item: int(item[0]))
    ]


def aggregate_by_participant(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["participant"]].append(row)
    return [
        {
            "participant": participant,
            "rows": len(participant_rows),
            "epochs": sorted_join({row["epoch"] for row in participant_rows}),
            "pass_models": sorted_join({row["pass_models"] for row in participant_rows}),
            "gross_compensation_gonka": str(decimal_sum(participant_rows)),
            "overlap_statuses_reference_only": sorted_join(
                {row["overlap_status_reference_only"] for row in participant_rows}
            ),
        }
        for participant, participant_rows in sorted(
            grouped.items(), key=lambda item: (-decimal_sum(item[1]), item[0])
        )
    ]


def aggregate_by_pass_models(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["pass_models"]].append(row)
    return [
        {
            "pass_models": pass_models,
            "rows": len(model_rows),
            "unique_participants": len({row["participant"] for row in model_rows}),
            "gross_compensation_gonka": str(decimal_sum(model_rows)),
        }
        for pass_models, model_rows in sorted(grouped.items(), key=lambda item: item[0])
    ]


def aggregate_by_overlap_reference(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["overlap_status_reference_only"]].append(row)
    return [
        {
            "overlap_status_reference_only": status,
            "rows": len(status_rows),
            "gross_compensation_gonka": str(decimal_sum(status_rows)),
        }
        for status, status_rows in sorted(grouped.items(), key=lambda item: item[0])
    ]


def write_markdown(
    path: Path,
    rows: list[dict[str, Any]],
    by_epoch: list[dict[str, Any]],
    by_participant: list[dict[str, Any]],
    by_pass_models: list[dict[str, Any]],
    by_overlap: list[dict[str, Any]],
) -> None:
    total = decimal_sum(rows)
    lines = [
        "# P3-CAND-06 Gross Compensation Calculation",
        "",
        "This table calculates the gross candidate amount for every P3-CAND-06 row",
        "before overlap review. All `24` candidate rows are included in the gross",
        "sum. Overlap status is shown only as a reference column and is not used to",
        "filter this calculation.",
        "",
        "This is not an approved payout table. Final payout still requires:",
        "",
        "- committee policy decision for single-model `pass_weight` rows;",
        "- duplicate-payment review against P3-CAND-04 and P4-CAND-01;",
        "- final recipient/contact mapping if this candidate is promoted.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Candidate rows included | `{len(rows)}` |",
        f"| Unique participants | `{len({row['participant'] for row in rows})}` |",
        f"| Gross compensation before overlap review | `{amount(total)} GONKA` |",
        "",
        "## Totals By Epoch",
        "",
        "| Epoch | Rows | Unique participants | Gross compensation, GONKA |",
        "|---:|---:|---:|---:|",
    ]
    for row in by_epoch:
        lines.append(
            f"| `{row['epoch']}` | `{row['rows']}` | `{row['unique_participants']}` | "
            f"`{amount(row['gross_compensation_gonka'])}` |"
        )

    lines.extend(
        [
            "",
            "## Totals By Passing Model Set",
            "",
            "| Passing model(s) | Rows | Unique participants | Gross compensation, GONKA |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in by_pass_models:
        lines.append(
            f"| `{row['pass_models']}` | `{row['rows']}` | `{row['unique_participants']}` | "
            f"`{amount(row['gross_compensation_gonka'])}` |"
        )

    lines.extend(
        [
            "",
            "## Totals By Overlap Status",
            "",
            "These buckets are reference-only for this calculation; no rows are removed",
            "from the gross sum.",
            "",
            "| Overlap status | Rows | Gross compensation, GONKA |",
            "|---|---:|---:|",
        ]
    )
    for row in by_overlap:
        lines.append(
            f"| `{row['overlap_status_reference_only']}` | `{row['rows']}` | "
            f"`{amount(row['gross_compensation_gonka'])}` |"
        )

    lines.extend(
        [
            "",
            "## Totals By Participant",
            "",
            "| Participant | Rows | Epochs | Passing model(s) | Gross compensation, GONKA | Overlap reference |",
            "|---|---:|---|---|---:|---|",
        ]
    )
    for row in by_participant:
        lines.append(
            f"| `{row['participant']}` | `{row['rows']}` | `{row['epochs']}` | "
            f"`{row['pass_models']}` | `{amount(row['gross_compensation_gonka'])}` | "
            f"`{row['overlap_statuses_reference_only']}` |"
        )

    lines.extend(
        [
            "",
            "## Row-Level Gross Calculation",
            "",
            "| Epoch | Participant | Trigger -> Exclusion | Passing model(s) | Stored ratio | Old formula match | New-style pass alpha | Gross compensation, GONKA | Overlap reference |",
            "|---:|---|---|---|---:|---|---|---:|---|",
        ]
    )
    for row in rows:
        lines.append(
            f"| `{row['epoch']}` | `{row['participant']}` | "
            f"`{row['event_trigger_height']}` -> `{row['exclusion_height']}` | "
            f"`{row['pass_models']}` | `{row['stored_ratio_percent']}` | "
            f"`{row['old_formula_matches_stored']}` | "
            f"`{row['bounded_new_algorithm_would_pass_alpha']}` | "
            f"`{amount(row['gross_compensation_gonka'])}` | "
            f"`{row['overlap_status_reference_only']}` |"
        )

    lines.extend(
        [
            "",
            "Machine-readable versions:",
            "",
            "- `case6_gross_compensation_calculation.csv`",
            "- `case6_gross_compensation_calculation.json`",
            "- `case6_gross_compensation_by_epoch.csv`",
            "- `case6_gross_compensation_by_participant.csv`",
            "- `case6_gross_compensation_by_pass_models.csv`",
            "- `case6_gross_compensation_by_overlap_reference.csv`",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = build_calculation_rows()
    by_epoch = aggregate_by_epoch(rows)
    by_participant = aggregate_by_participant(rows)
    by_pass_models = aggregate_by_pass_models(rows)
    by_overlap = aggregate_by_overlap_reference(rows)

    row_fields = [
        "epoch",
        "participant",
        "event_trigger_height",
        "exclusion_height",
        "pass_models",
        "qwen_pass_weight",
        "kimi_pass_weight",
        "stored_ratio_percent",
        "old_formula_matches_stored",
        "bounded_new_algorithm_would_pass_alpha",
        "technical_status",
        "overlap_status_reference_only",
        "gross_compensation_gonka",
        "calculation_scope",
        "note",
    ]
    write_csv(CASE_DIR / "case6_gross_compensation_calculation.csv", rows, row_fields)
    write_csv(
        CASE_DIR / "case6_gross_compensation_by_epoch.csv",
        by_epoch,
        ["epoch", "rows", "unique_participants", "gross_compensation_gonka"],
    )
    write_csv(
        CASE_DIR / "case6_gross_compensation_by_participant.csv",
        by_participant,
        [
            "participant",
            "rows",
            "epochs",
            "pass_models",
            "gross_compensation_gonka",
            "overlap_statuses_reference_only",
        ],
    )
    write_csv(
        CASE_DIR / "case6_gross_compensation_by_pass_models.csv",
        by_pass_models,
        ["pass_models", "rows", "unique_participants", "gross_compensation_gonka"],
    )
    write_csv(
        CASE_DIR / "case6_gross_compensation_by_overlap_reference.csv",
        by_overlap,
        ["overlap_status_reference_only", "rows", "gross_compensation_gonka"],
    )
    write_json(
        CASE_DIR / "case6_gross_compensation_calculation.json",
        {
            "summary": {
                "rows": len(rows),
                "unique_participants": len({row["participant"] for row in rows}),
                "gross_compensation_gonka": str(decimal_sum(rows)),
                "scope": "before_overlap_review",
            },
            "rows": rows,
            "by_epoch": by_epoch,
            "by_participant": by_participant,
            "by_pass_models": by_pass_models,
            "by_overlap_reference": by_overlap,
        },
    )
    write_markdown(
        CASE_DIR / "case6_gross_compensation_calculation.md",
        rows,
        by_epoch,
        by_participant,
        by_pass_models,
        by_overlap,
    )
    print(
        json.dumps(
            {
                "rows": len(rows),
                "unique_participants": len({row["participant"] for row in rows}),
                "gross_compensation_gonka": str(decimal_sum(rows)),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
