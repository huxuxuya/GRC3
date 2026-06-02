#!/usr/bin/env python3
"""Counterfactual v0.2.13-style confirmation snapshot replay for P3-CAND-06."""

from __future__ import annotations

import json
from decimal import Decimal
from typing import Any

from build_case6_coefficient_replay import (
    CASE_DIR,
    KIMI,
    MODELS,
    POC_DEVIATION_COEFF,
    QWEN,
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


def snapshot_models(validation_snapshot: dict[str, Any]) -> list[str]:
    present = []
    for entry in validation_snapshot.get("model_voting_powers") or []:
        model = entry.get("model_id")
        if model in MODELS:
            present.append(model)
    return sorted(set(present))


def filter_nodes(nodes_by_model: dict[str, list[dict[str, Any]]], models: list[str]) -> dict[str, list[dict[str, Any]]]:
    allowed = set(models)
    return {model: nodes for model, nodes in nodes_by_model.items() if model in allowed}


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
    models = snapshot_models(validation_snapshot)
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

    nodes_by_model = filter_nodes(participant_epoch_nodes(base, epoch, participant), models)
    present_coefficients = {model: coefficients.get(model, Decimal(1)) for model in models}
    preserved, not_preserved, _ = weighted_split(
        nodes_by_model,
        preserved_node_index(preserved_snapshot),
        participant,
        present_coefficients,
    )
    measured, _ = measured_weight(participant, str(trigger), distributions, present_coefficients, norm_factor, evidence, row["epoch"])
    total_expected = preserved + not_preserved
    reading = preserved + measured
    ratio = Decimal(1) if total_expected == 0 else min(
        Decimal(reading) / Decimal(total_expected) / POC_DEVIATION_COEFF,
        Decimal(1),
    )
    alpha = Decimal(row["alpha_threshold"])
    return {
        "epoch": row["epoch"],
        "participant": participant,
        "event_trigger_height": row["event_trigger_height"],
        "pass_models": row["pass_models"],
        "snapshot_models": "+".join("Qwen" if model == QWEN else "Kimi" if model == KIMI else model for model in models),
        "preserved_weight": preserved,
        "measured_weight": measured,
        "not_preserved_weight": not_preserved,
        "total_expected_weight": total_expected,
        "reading_weight": reading,
        "stored_confirmation_ratio": row["stored_confirmation_ratio"],
        "new_algorithm_ratio": f"{ratio:.16f}",
        "stored_below_alpha": str(Decimal(row["stored_confirmation_ratio"]) < alpha),
        "new_algorithm_below_alpha": str(ratio < alpha),
        "new_algorithm_would_pass_alpha": str(ratio >= alpha),
        "qwen_coeff": str(present_coefficients.get(QWEN, "")),
        "kimi_coeff": str(present_coefficients.get(KIMI, "")),
        "loss_gonka": row["loss_gonka"],
        "classification": row["classification"],
    }


def write_markdown(rows: list[dict[str, Any]]) -> None:
    lines = [
        "# P3-CAND-06 v0.2.13-Style Counterfactual Replay",
        "",
        "This replay applies the v0.2.13-style idea of using one confirmation",
        "snapshot model set for measured, preserved, and total expected weight.",
        "It is limited to the Qwen/Kimi data available in this case folder.",
        "",
        "## Result",
        "",
        "| Check | Value |",
        "|---|---:|",
        f"| Rows replayed | `{len(rows)}` |",
        f"| Rows that would pass alpha in this counterfactual | `{sum(row['new_algorithm_would_pass_alpha'] == 'True' for row in rows)}` |",
        f"| Rows still below alpha in this counterfactual | `{sum(row['new_algorithm_below_alpha'] == 'True' for row in rows)}` |",
        "",
        "## Rows",
        "",
        "| Epoch | Participant | Pass model(s) | Snapshot models | Stored ratio | New ratio | Would pass alpha |",
        "|---:|---|---|---|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['epoch']} | `{row['participant']}` | {row['pass_models']} | {row['snapshot_models']} | "
            f"{row['stored_confirmation_ratio']} | {row['new_algorithm_ratio']} | {row['new_algorithm_would_pass_alpha']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This is a bounded counterfactual, not a claim that the exact production",
            "  upgrade state can be reconstructed without the final stored",
            "  `ConfirmationWeightScales` field.",
            "- If a single-model row remains below alpha here, it supports keeping",
            "  payout eligibility as a policy decision rather than automatically",
            "  treating every single-model pass as compensable.",
            "- Epoch `276` rows remain overlap-sensitive because the upgrade window",
            "  changed params and cPoC behavior.",
            "",
            "Machine-readable versions are in `case6_new_algorithm_replay.csv` and",
            "`case6_new_algorithm_replay.json`.",
            "",
        ]
    )
    (CASE_DIR / "case6_new_algorithm_replay.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    load_dotenv(CASE_DIR.parents[1] / ".env")
    base = direct_lcd_from_env()
    evidence = evidence_index()
    rows = [replay_row(base, row, evidence) for row in read_csv(CASE_DIR / "case6_row_formula_replay.csv")]
    fieldnames = [
        "epoch",
        "participant",
        "event_trigger_height",
        "pass_models",
        "snapshot_models",
        "preserved_weight",
        "measured_weight",
        "not_preserved_weight",
        "total_expected_weight",
        "reading_weight",
        "stored_confirmation_ratio",
        "new_algorithm_ratio",
        "stored_below_alpha",
        "new_algorithm_below_alpha",
        "new_algorithm_would_pass_alpha",
        "qwen_coeff",
        "kimi_coeff",
        "loss_gonka",
        "classification",
    ]
    write_csv(CASE_DIR / "case6_new_algorithm_replay.csv", rows, fieldnames)
    write_json(CASE_DIR / "case6_new_algorithm_replay.json", {"rows": rows})
    write_markdown(rows)
    print(
        json.dumps(
            {
                "rows": len(rows),
                "would_pass_alpha": sum(row["new_algorithm_would_pass_alpha"] == "True" for row in rows),
                "below_alpha": sum(row["new_algorithm_below_alpha"] == "True" for row in rows),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
