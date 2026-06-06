#!/usr/bin/env python3
"""Build row-level cPoC evidence for disputed P4 epoch 265 rows.

This parser uses raw chain cache files only. It does not query nodes and does
not execute the investigator repository.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path(__file__).resolve().parent
RAW = BASE / "raw_chain_cache"

STAGE = "4102890"
SNAPSHOT_HEIGHT = "4103171"

ADDRESSES = [
    "gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6",
    "gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu",
    "gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y",
]

MODELS = [
    "Qwen/Qwen3-235B-A22B-Instruct-2507-FP8",
    "moonshotai/Kimi-K2.6",
]

FILES = {
    "commits": RAW / "case6_raw_stage_4102890_all_poc_v2_store_commits.json",
    "validations": RAW / "case6_raw_stage_4102890_poc_v2_validations_for_stage.json",
    "snapshot": RAW / "case6_raw_height_4103171_stage_4102890_poc_validation_snapshot.json",
    "root_group_healthy": RAW / "archive_cli_height_4103170_epoch_group_data_265_stdout.json",
    "root_group_end": RAW / "archive_cli_height_4105360_epoch_group_data_265_stdout.json",
    "kimi_group": RAW / "archive_cli_height_4103170_epoch_group_data_265_model_kimi_stdout.json",
    "qwen_group": RAW / "case6_raw_epoch265_model_qwen_epoch_group_data.json",
}


def load_json(path: Path) -> object:
    with path.open() as f:
        return json.load(f)


def group_weight(data: dict, address: str) -> dict | None:
    rows = data.get("epoch_group_data", {}).get("validation_weights", [])
    for row in rows:
        if row.get("member_address") == address:
            return row
    return None


def weight_value(row: dict | None, key: str) -> int | None:
    if not row or key not in row:
        return None
    return int(row[key])


def main() -> None:
    commits = load_json(FILES["commits"])["commits"]
    validations = load_json(FILES["validations"])["poc_validation"]
    snapshot = load_json(FILES["snapshot"])["snapshot"]
    root_group_healthy = load_json(FILES["root_group_healthy"])
    root_group_end = load_json(FILES["root_group_end"])
    kimi_group = load_json(FILES["kimi_group"])
    qwen_group = load_json(FILES["qwen_group"])

    model_total_vp = {}
    model_vp_by_address = {}
    for model_row in snapshot.get("model_voting_powers", []):
        model_id = model_row["model_id"]
        powers = {
            item["address"]: int(item["voting_power"])
            for item in model_row.get("voting_powers", [])
        }
        model_vp_by_address[model_id] = powers
        model_total_vp[model_id] = sum(powers.values())

    validation_by_participant_model = {
        (row.get("participant"), row.get("model_id")): row.get("poc_validation", [])
        for row in validations
    }

    rows = []
    for address in ADDRESSES:
        root_healthy = group_weight(root_group_healthy, address)
        root_end = group_weight(root_group_end, address)
        kimi_weight = group_weight(kimi_group, address)
        qwen_weight = group_weight(qwen_group, address)

        for model_id in MODELS:
            commit_rows = [
                row
                for row in commits
                if row.get("participant_address") == address
                and row.get("model_id") == model_id
            ]
            validation_rows = validation_by_participant_model.get((address, model_id), [])
            positive_validated_weight = sum(
                int(row["validated_weight"])
                for row in validation_rows
                if int(row["validated_weight"]) > 0
            )
            valid_validator_voting_power = sum(
                model_vp_by_address.get(model_id, {}).get(
                    row["validator_participant_address"], 0
                )
                for row in validation_rows
                if int(row["validated_weight"]) > 0
            )
            invalid_validator_voting_power = sum(
                model_vp_by_address.get(model_id, {}).get(
                    row["validator_participant_address"], 0
                )
                for row in validation_rows
                if int(row["validated_weight"]) < 0
            )
            invalid_votes = sum(
                1
                for row in validation_rows
                if int(row["validated_weight"]) < 0
            )
            commit_count = sum(int(row["count"]) for row in commit_rows)
            model_vp = model_vp_by_address.get(model_id, {}).get(address)
            total_vp = model_total_vp.get(model_id)
            threshold = None if total_vp is None else (total_vp * 2) / 3

            if not commit_rows and not validation_rows:
                classification = "no_submission_or_validation_record_at_stage"
            elif commit_rows and threshold is not None and valid_validator_voting_power <= threshold:
                classification = "submitted_but_below_two_thirds_validation_power"
            elif commit_rows:
                classification = "submitted_with_validation_record"
            else:
                classification = "validation_record_without_commit_row"

            rows.append(
                {
                    "address": address,
                    "stage_start_height": STAGE,
                    "snapshot_height": SNAPSHOT_HEIGHT,
                    "model_id": model_id,
                    "root_weight_healthy": weight_value(root_healthy, "weight"),
                    "root_confirmation_weight_healthy": weight_value(root_healthy, "confirmation_weight"),
                    "root_weight_end": weight_value(root_end, "weight"),
                    "root_confirmation_weight_end": weight_value(root_end, "confirmation_weight"),
                    "model_group_weight": weight_value(
                        kimi_weight if model_id == "moonshotai/Kimi-K2.6" else qwen_weight,
                        "weight",
                    ),
                    "model_group_confirmation_weight": weight_value(
                        kimi_weight if model_id == "moonshotai/Kimi-K2.6" else qwen_weight,
                        "confirmation_weight",
                    ),
                    "model_voting_power_at_snapshot": model_vp,
                    "model_total_voting_power_at_snapshot": total_vp,
                    "two_thirds_model_voting_power": threshold,
                    "commit_rows": len(commit_rows),
                    "commit_count_sum": commit_count,
                    "validation_rows": len(validation_rows),
                    "positive_validated_weight_sum": positive_validated_weight,
                    "valid_validator_voting_power_sum": valid_validator_voting_power,
                    "invalid_vote_rows": invalid_votes,
                    "invalid_validator_voting_power_sum": invalid_validator_voting_power,
                    "classification": classification,
                }
            )

    csv_path = BASE / "p4_e265_gonka1830_cpoc_evidence.csv"
    json_path = BASE / "p4_e265_gonka1830_cpoc_evidence.json"
    md_path = BASE / "p4_audit_pass_03_e265_gonka1830.md"

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n")

    md_lines = [
        "# P4 Conceptual Audit Pass 03: Epoch 265 `gonka1830...` cPoC Evidence",
        "",
        "This pass checks whether the disputed epoch `265` row",
        "`gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` has the same direct",
        "Kimi cPoC shortfall signature as the confirmed Case 3 overlap row.",
        "",
        "The parser reads only saved raw chain cache files and does not query a node.",
        "",
        "Raw inputs copied into `raw_chain_cache/`:",
        "",
        "- `case6_raw_stage_4102890_all_poc_v2_store_commits.json`",
        "- `case6_raw_stage_4102890_poc_v2_validations_for_stage.json`",
        "- `case6_raw_height_4103171_stage_4102890_poc_validation_snapshot.json`",
        "- `case6_raw_epoch265_model_qwen_epoch_group_data.json`",
        "",
        "Derived outputs:",
        "",
        "- `p4_e265_gonka1830_cpoc_evidence.csv`",
        "- `p4_e265_gonka1830_cpoc_evidence.json`",
        "",
        "## Key Rows",
        "",
        "| Address | Model | Model VP | Commit count | Validation rows | Valid validator VP | Classification |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        if row["address"] in {
            "gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6",
            "gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y",
        }:
            md_lines.append(
                "| `{address}` | `{model_id}` | `{model_voting_power_at_snapshot}` | "
                "`{commit_count_sum}` | `{validation_rows}` | "
                "`{valid_validator_voting_power_sum}` | `{classification}` |".format(**row)
            )

    md_lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The confirmed Case 3 overlap address `gonka1j7...` has raw cPoC",
            "  commit rows on the same stage for both Qwen and Kimi. Its Kimi commit",
            "  count is `52028`, and its valid Kimi validator voting power is `256727`,",
            "  below the `>2/3` model-voting-power rule.",
            "- The disputed `gonka1830...` row has Kimi model voting power `13490`",
            "  in the snapshot and appears in the Kimi model group, but it has zero",
            "  commit rows and zero validation records on stage `4102890` for both",
            "  Kimi and Qwen.",
            "- Therefore this row is not proven to be the same direct Kimi cPoC",
            "  shortfall class as the Case 3 overlap. The chain evidence supports a",
            "  different classification: zero-reward `failed_confirmation_poc` with",
            "  no cPoC submission/validation record at the final checked stage.",
        ]
    )
    md_path.write_text("\n".join(md_lines) + "\n")


if __name__ == "__main__":
    main()
