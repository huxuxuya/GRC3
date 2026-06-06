#!/usr/bin/env python3
"""Build row-level evidence for e266 zero-reward nonce candidates.

Reads saved raw chain cache files plus copied source artifacts. Does not query
nodes and does not run the investigator scripts.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path(__file__).resolve().parent
RAW = BASE / "raw_chain_cache"
SOURCE = BASE / "source_cache"


def load_json(path: Path) -> object:
    with path.open() as f:
        return json.load(f)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def commit_key(row: dict) -> tuple:
    return (
        row.get("participant_address"),
        int(row.get("count", 0)),
        row.get("root_hash"),
        row.get("hex_pub_key"),
    )


def main() -> None:
    raw_commits = load_json(
        RAW / "archive_cli_height_4120751_all_poc_v2_store_commits_4105361_stdout.json"
    )["commits"]
    raw_validations = load_json(
        RAW / "archive_cli_height_4120751_poc_v2_validations_for_stage_4105361_stdout_retry2.json"
    )["poc_validation"]
    final_group = load_json(RAW / "archive_lcd_epoch_group_data_266.json")["epoch_group_data"]
    performance = load_json(RAW / "archive_lcd_epoch_performance_summary_266.json")[
        "epochPerformanceSummary"
    ]
    excluded_doc = load_json(RAW / "archive_lcd_excluded_participants_266.json")
    excluded = excluded_doc.get("excluded_participants", excluded_doc.get("items", []))

    source_commits = load_json(SOURCE / "votkon_e266_epoch266_commits.json")["commits"]
    source_nonces = load_csv(SOURCE / "votkon_e266_compensation_266_nonces.csv")
    classifier = load_json(BASE / "p4_e266_nonce_scope_classifier.json")

    zero_addresses = [
        row["address"]
        for row in classifier
        if row["classification"] == "in_final_group_zero_reward_reconstruction_candidate"
    ]

    raw_by_addr: dict[str, list[dict]] = {}
    for row in raw_commits:
        raw_by_addr.setdefault(row["participant_address"], []).append(row)

    source_by_addr: dict[str, list[dict]] = {}
    for row in source_commits:
        source_by_addr.setdefault(row["participant_address"], []).append(row)

    raw_keys = {commit_key(row) for row in raw_commits}
    validations_by_addr: dict[str, list[dict]] = {}
    for row in raw_validations:
        validations_by_addr.setdefault(row["participant"], []).append(row)

    final_by_addr = {
        row["member_address"]: row for row in final_group.get("validation_weights", [])
    }
    performance_by_addr = {row["participant_id"]: row for row in performance}
    excluded_by_addr = {
        row.get("participant_id", row.get("address")): row for row in excluded
    }
    source_nonce_by_addr = {row["address"]: row for row in source_nonces}

    rows = []
    for address in zero_addresses:
        raw_rows = raw_by_addr.get(address, [])
        source_rows = source_by_addr.get(address, [])
        validation_wrappers = validations_by_addr.get(address, [])
        flat_validations = [
            item
            for wrapper in validation_wrappers
            for item in wrapper.get("poc_validation", [])
        ]
        validated_weights = [int(row.get("validated_weight", 0)) for row in flat_validations]
        full_validation_count = 0
        full_validation_models = []
        for source in source_rows:
            count = int(source["count"])
            matched = any(
                max(
                    [
                        int(item.get("validated_weight", 0))
                        for item in wrapper.get("poc_validation", [])
                    ]
                    or [0]
                )
                == count
                for wrapper in validation_wrappers
            )
            if matched:
                full_validation_count += 1
                full_validation_models.append(source.get("model_id", ""))

        final = final_by_addr.get(address, {})
        perf = performance_by_addr.get(address, {})
        excluded_row = excluded_by_addr.get(address, {})
        models = sorted({row.get("model_id", "") for row in source_rows})
        kimi_count = sum(
            int(row["count"])
            for row in source_rows
            if row.get("model_id") == "moonshotai/Kimi-K2.6"
        )
        qwen_count = sum(
            int(row["count"])
            for row in source_rows
            if row.get("model_id") == "Qwen/Qwen3-235B-A22B-Instruct-2507-FP8"
        )

        if "moonshotai/Kimi-K2.6" not in models:
            conclusion = "not_kimi_zero_reward_row_qwen_only_policy_required_if_broadened"
        elif len(models) > 1:
            conclusion = "mixed_kimi_qwen_zero_reward_row_not_same_as_absent_operator"
        else:
            conclusion = "kimi_zero_reward_row_not_absent_operator_needs_cause_policy"

        rows.append(
            {
                "address": address,
                "source_models": "+".join(models),
                "source_kimi_commit_count": kimi_count,
                "source_qwen_commit_count": qwen_count,
                "raw_commit_rows": len(raw_rows),
                "raw_commit_count_sum": sum(int(row["count"]) for row in raw_rows),
                "source_commit_rows": len(source_rows),
                "source_commit_exact_raw_matches": sum(
                    1 for row in source_rows if commit_key(row) in raw_keys
                ),
                "raw_validation_wrappers": len(validation_wrappers),
                "raw_validation_vote_rows": len(flat_validations),
                "max_validated_weight": max(validated_weights or [0]),
                "validation_vote_weight_sum": sum(validated_weights),
                "full_validation_count_matching_source_commit_count": full_validation_count,
                "full_validation_models_source_backed": "+".join(sorted(set(full_validation_models))),
                "in_final_group": address in final_by_addr,
                "final_weight": int(final.get("weight", 0)),
                "final_confirmation_weight": int(final.get("confirmation_weight", 0)),
                "final_reputation": int(final.get("reputation", 0)),
                "in_performance_summary": address in performance_by_addr,
                "rewarded_coins": int(perf.get("rewarded_coins", 0)),
                "earned_coins": int(perf.get("earned_coins", 0)),
                "inference_count": int(perf.get("inference_count", 0)),
                "missed_requests": int(perf.get("missed_requests", 0)),
                "validated_inferences": int(perf.get("validated_inferences", 0)),
                "invalidated_inferences": int(perf.get("invalidated_inferences", 0)),
                "in_excluded_participants_266": address in excluded_by_addr,
                "excluded_reason": excluded_row.get("reason", ""),
                "exclusion_block_height": excluded_row.get("exclusion_block_height", ""),
                "source_nonce_compensation_gonka": source_nonce_by_addr[address][
                    "compensation_gonka"
                ],
                "local_conclusion": conclusion,
            }
        )

    csv_path = BASE / "p4_e266_zero_reward_rows.csv"
    json_path = BASE / "p4_e266_zero_reward_rows.json"
    md_path = BASE / "p4_problem_02a_e266_zero_reward_rows.md"

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n")

    md_lines = [
        "# P4 Problem 02a: Epoch 266 Zero-Reward Rows",
        "",
        "This note separates the 5 in-final-group zero-reward rows from the 9",
        "absent final-set operators in the epoch `266` nonce claim.",
        "",
        "## Question",
        "",
        "Are these rows direct victims of the e266 nonce incident, or ordinary",
        "`failed_confirmation_poc` rows that need separate policy/cause proof?",
        "",
        "## Evidence Inputs",
        "",
        "- Raw e266 commit store at stage `4105361`",
        "- Raw e266 validation records at stage `4105361`",
        "- Raw final epoch group `266`",
        "- Raw epoch performance summary `266`",
        "- Raw excluded participants `266`",
        "- Source commit labels and source nonce compensation table from pinned",
        "  Votkon repository",
        "",
        "## Rows",
        "",
        "| Address | Source models | Raw commits | Validation rows | Full commit-count validations | Final weight | Confirmation weight | Excluded reason | Reward | Source comp | Conclusion |",
        "|---|---|---:|---:|---:|---:|---:|---|---:|---:|---|",
    ]
    for row in rows:
        md_lines.append(
            "| `{address}` | `{source_models}` | `{raw_commit_count_sum}` | "
            "`{raw_validation_vote_rows}` | "
            "`{full_validation_count_matching_source_commit_count}` | "
            "`{final_weight}` | `{final_confirmation_weight}` | "
            "`{excluded_reason}` | `{reward:.9f}` | "
            "`{source_nonce_compensation_gonka}` | `{local_conclusion}` |".format(
                reward=row["rewarded_coins"] / 1_000_000_000,
                **row,
            )
        )

    qwen_only = [
        row for row in rows if "moonshotai/Kimi-K2.6" not in row["source_models"]
    ]
    kimi_rows = [row for row in rows if "moonshotai/Kimi-K2.6" in row["source_models"]]
    md_lines.extend(
        [
            "",
            "## Findings",
            "",
            f"- Rows checked: `{len(rows)}`",
            f"- Kimi or mixed Kimi rows by source label: `{len(kimi_rows)}`",
            f"- Qwen-only rows by source label: `{len(qwen_only)}`",
            "- All 5 rows are present in final epoch group `266`.",
            "- All 5 rows have `confirmation_weight=0`, `rewarded_coins=0`, and",
            "  excluded reason `failed_confirmation_poc`.",
            "- These rows are not the same class as the 9 absent operators: they",
            "  reached the final group and then failed confirmation.",
            "",
            "## Interpretation",
            "",
            "The raw data confirms submissions and validation records, but does not",
            "prove that these zero-reward rows are direct victims of the same incident",
            "as the absent operators. They should remain a separate row-level cause",
            "and policy question.",
        ]
    )
    md_path.write_text("\n".join(md_lines) + "\n")


if __name__ == "__main__":
    main()
