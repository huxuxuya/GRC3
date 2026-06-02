#!/usr/bin/env python3
"""Replay the pre-v0.2.13 cPoC formula for all P3-CAND-06 rows."""

from __future__ import annotations

import csv
import json
from decimal import Decimal
from pathlib import Path
from typing import Any

from build_case6_coefficient_replay import (
    CASE_DIR,
    POC_DEVIATION_COEFF,
    RATIO_TOLERANCE,
    direct_lcd_from_env,
    distribution_index,
    evidence_index,
    get_json,
    load_dotenv,
    measured_weight,
    model_coefficients,
    participant_epoch_nodes,
    preserved_node_index,
    read_csv,
    time_normalization_factor,
    weighted_split,
    write_csv,
    write_json,
)


def replay_row(base: str, row: dict[str, str], evidence: dict[tuple[str, str, str, str], dict[str, str]]) -> dict[str, Any]:
    epoch = int(row["epoch"])
    trigger = int(row["event_trigger_height"])
    exclusion_height = int(row["exclusion_height"])
    participant = row["participant"]

    params = get_json(base, "/productscience/inference/inference/params", block_height=trigger)
    coefficients = model_coefficients(params)
    validation_snapshot = get_json(
        base,
        f"/productscience/inference/inference/poc_validation_snapshot/{trigger}",
        block_height=exclusion_height,
    ).get("snapshot") or {}
    norm_factor = time_normalization_factor(params, validation_snapshot)
    preserved_snapshot = get_json(
        base,
        "/productscience/inference/inference/preserved_nodes_snapshot",
        block_height=exclusion_height,
    ).get("snapshot") or {}
    distributions = distribution_index(
        (
            get_json(
                base,
                f"/productscience/inference/inference/all_mlnode_weight_distributions/{trigger}",
                block_height=exclusion_height,
            ).get("distributions")
            or []
        )
    )

    nodes_by_model = participant_epoch_nodes(base, epoch, participant)
    preserved, not_preserved, _ = weighted_split(
        nodes_by_model,
        preserved_node_index(preserved_snapshot),
        participant,
        coefficients,
    )
    measured, _ = measured_weight(participant, str(trigger), distributions, coefficients, norm_factor, evidence, row["epoch"])
    total_expected = preserved + not_preserved
    reading = preserved + measured
    ratio = Decimal(1) if total_expected == 0 else min(
        Decimal(reading) / Decimal(total_expected) / POC_DEVIATION_COEFF,
        Decimal(1),
    )
    stored_ratio = Decimal(row["stored_confirmation_ratio"])
    diff = stored_ratio - ratio
    return {
        "epoch": row["epoch"],
        "participant": participant,
        "event_trigger_height": row["event_trigger_height"],
        "exclusion_height": row["exclusion_height"],
        "pass_models": row["pass_models"],
        "preserved_weight": preserved,
        "measured_weight": measured,
        "not_preserved_weight": not_preserved,
        "total_expected_weight": total_expected,
        "reading_weight": reading,
        "confirmation_weight_before": row["confirmation_weight_before"],
        "confirmation_weight_at_exclusion": row["confirmation_weight_at_exclusion"],
        "old_formula_confirmation_weight_after": min(int(row["confirmation_weight_before"]), reading),
        "stored_confirmation_ratio": row["stored_confirmation_ratio"],
        "old_formula_ratio": f"{ratio:.16f}",
        "old_formula_diff": f"{diff:.16f}",
        "old_formula_matches_stored": str(abs(diff) <= RATIO_TOLERANCE),
        "ratio_below_alpha": str(ratio < Decimal(row["alpha_threshold"])),
        "loss_gonka": row["loss_gonka"],
        "classification": row["classification"],
    }


def write_markdown(rows: list[dict[str, Any]]) -> None:
    lines = [
        "# P3-CAND-06 Full Old Formula Replay",
        "",
        "This artifact replays the reviewed pre-`v0.2.13` cPoC formula for all",
        "`24` candidate rows using historical params, cPoC time normalization,",
        "preserved snapshots, MLNode distributions, and raw submission evidence.",
        "",
        "## Result",
        "",
        "| Check | Value |",
        "|---|---:|",
        f"| Rows replayed | `{len(rows)}` |",
        f"| Rows matching stored ratio | `{sum(row['old_formula_matches_stored'] == 'True' for row in rows)}` |",
        f"| Rows below alpha in replay | `{sum(row['ratio_below_alpha'] == 'True' for row in rows)}` |",
        "",
        "## Rows",
        "",
        "| Epoch | Participant | Pass model(s) | Preserved | Measured | Not preserved | Total expected | Reading | Stored ratio | Replay ratio | Match |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['epoch']} | `{row['participant']}` | {row['pass_models']} | {row['preserved_weight']} | "
            f"{row['measured_weight']} | {row['not_preserved_weight']} | {row['total_expected_weight']} | "
            f"{row['reading_weight']} | {row['stored_confirmation_ratio']} | {row['old_formula_ratio']} | "
            f"{row['old_formula_matches_stored']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The replay proves that the durable failed ratios are internally",
            "  reproducible from chain data for the formula-reconciled rows.",
            "- Rows that remain non-matching are treated as overlap/upgrade review",
            "  candidates rather than forced into the generic pre-fix formula bucket.",
            "- Formula reconciliation is technical evidence, not automatic payout",
            "  eligibility for single-model service rows.",
            "",
            "Machine-readable versions are in `case6_full_old_formula_replay.csv` and",
            "`case6_full_old_formula_replay.json`.",
            "",
        ]
    )
    (CASE_DIR / "case6_full_old_formula_replay.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    load_dotenv(CASE_DIR.parents[1] / ".env")
    base = direct_lcd_from_env()
    evidence = evidence_index()
    rows = [replay_row(base, row, evidence) for row in read_csv(CASE_DIR / "case6_row_formula_replay.csv")]
    fieldnames = [
        "epoch",
        "participant",
        "event_trigger_height",
        "exclusion_height",
        "pass_models",
        "preserved_weight",
        "measured_weight",
        "not_preserved_weight",
        "total_expected_weight",
        "reading_weight",
        "confirmation_weight_before",
        "confirmation_weight_at_exclusion",
        "old_formula_confirmation_weight_after",
        "stored_confirmation_ratio",
        "old_formula_ratio",
        "old_formula_diff",
        "old_formula_matches_stored",
        "ratio_below_alpha",
        "loss_gonka",
        "classification",
    ]
    write_csv(CASE_DIR / "case6_full_old_formula_replay.csv", rows, fieldnames)
    write_json(CASE_DIR / "case6_full_old_formula_replay.json", {"rows": rows})
    write_markdown(rows)
    print(
        json.dumps(
            {
                "rows": len(rows),
                "matches": sum(row["old_formula_matches_stored"] == "True" for row in rows),
                "below_alpha": sum(row["ratio_below_alpha"] == "True" for row in rows),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
