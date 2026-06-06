#!/usr/bin/env python3
"""Classify epoch 266 nonce/delegation claims for P4.

This parser does not run the investigator scripts. It reads:
- raw chain cache files saved by this audit;
- copied source artifacts as claim labels only.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path(__file__).resolve().parent
RAW = BASE / "raw_chain_cache"
SOURCE = BASE / "source_cache"

KIMI = "moonshotai/Kimi-K2.6"
QWEN = "Qwen/Qwen3-235B-A22B-Instruct-2507-FP8"


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


def index_by_address(rows: list[dict], key: str) -> dict[str, dict]:
    return {row[key]: row for row in rows}


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
    source_delegation = load_csv(SOURCE / "votkon_e266_compensation_266_delegation.csv")
    source_comp = load_json(SOURCE / "votkon_e266_compensation_266.json")

    source_by_key = {commit_key(row): row for row in source_commits}
    raw_by_key = {commit_key(row): row for row in raw_commits}
    source_by_addr = {}
    for row in source_commits:
        source_by_addr.setdefault(row["participant_address"], []).append(row)

    raw_by_addr = {}
    for row in raw_commits:
        raw_by_addr.setdefault(row["participant_address"], []).append(row)

    validation_by_addr = {
        row["participant"]: row.get("poc_validation", []) for row in raw_validations
    }

    final_weights = {
        row["member_address"]: int(row.get("weight", 0))
        for row in final_group.get("validation_weights", [])
    }
    final_confirmation_weights = {
        row["member_address"]: int(row.get("confirmation_weight", 0))
        for row in final_group.get("validation_weights", [])
    }
    performance_by_addr = index_by_address(performance, "participant_id")
    excluded_by_addr = {
        row.get("participant_id", row.get("address")): row for row in excluded
    }
    source_nonce_by_addr = index_by_address(source_nonces, "address")

    source_excluded = set(source_comp["excluded_operators"])
    source_delegators = {row["address"] for row in source_delegation}

    nonce_addresses = [row["address"] for row in source_nonces]
    rows = []
    for address in nonce_addresses:
        raw_rows = raw_by_addr.get(address, [])
        source_rows = source_by_addr.get(address, [])
        exact_source_match_count = sum(
            1 for row in raw_rows if commit_key(row) in source_by_key
        )
        exact_raw_match_count = sum(
            1 for row in source_rows if commit_key(row) in raw_by_key
        )
        source_models = sorted({row.get("model_id", "") for row in source_rows})
        source_kimi_count = sum(
            int(row["count"]) for row in source_rows if row.get("model_id") == KIMI
        )
        source_qwen_count = sum(
            int(row["count"]) for row in source_rows if row.get("model_id") == QWEN
        )
        raw_commit_count = sum(int(row["count"]) for row in raw_rows)
        validation_rows = validation_by_addr.get(address, [])
        positive_validation_rows = [
            row for row in validation_rows if int(row.get("validated_weight", 0)) > 0
        ]
        negative_validation_rows = [
            row for row in validation_rows if int(row.get("validated_weight", 0)) < 0
        ]

        in_final = address in final_weights
        actual_rewards = int(performance_by_addr.get(address, {}).get("rewarded_coins", 0))
        source_nonce = source_nonce_by_addr[address]

        if address in source_excluded and not in_final:
            classification = "source_excluded_operator_confirmed_absent_from_final_group"
            status = "confirmed_for_submission_and_absence_policy_for_compensation"
        elif in_final and actual_rewards > 0:
            classification = "in_final_group_rewarded_reconstruction_top_up"
            status = "policy_required_not_exclusion_victim"
        elif in_final and actual_rewards == 0:
            classification = "in_final_group_zero_reward_reconstruction_candidate"
            status = "needs_cause_policy"
        else:
            classification = "not_in_final_group_non_source_excluded_nonce_candidate"
            status = "needs_cause_policy"

        rows.append(
            {
                "address": address,
                "source_models": "+".join(source_models),
                "source_kimi_commit_count": source_kimi_count,
                "source_qwen_commit_count": source_qwen_count,
                "raw_commit_rows": len(raw_rows),
                "raw_commit_count_sum": raw_commit_count,
                "raw_commit_has_model_id": any("model_id" in row for row in raw_rows),
                "source_commit_exact_match_rows": exact_source_match_count,
                "raw_commit_exact_match_rows": exact_raw_match_count,
                "raw_validation_rows": len(validation_rows),
                "raw_positive_validation_rows": len(positive_validation_rows),
                "raw_negative_validation_rows": len(negative_validation_rows),
                "in_final_group": in_final,
                "final_weight": final_weights.get(address),
                "final_confirmation_weight": final_confirmation_weights.get(address),
                "in_performance_summary": address in performance_by_addr,
                "actual_rewards_ngonka": actual_rewards,
                "in_excluded_participants_266": address in excluded_by_addr,
                "excluded_reason": excluded_by_addr.get(address, {}).get("reason", ""),
                "source_excluded_operator": address in source_excluded,
                "source_nonce_compensation_gonka": source_nonce["compensation_gonka"],
                "source_delegator": address in source_delegators,
                "classification": classification,
                "status": status,
            }
        )

    csv_path = BASE / "p4_e266_nonce_scope_classifier.csv"
    json_path = BASE / "p4_e266_nonce_scope_classifier.json"
    md_path = BASE / "p4_audit_pass_04_e266_nonce_scope.md"

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n")

    excluded_rows = [row for row in rows if row["source_excluded_operator"]]
    topup_rows = [row for row in rows if row["classification"] == "in_final_group_rewarded_reconstruction_top_up"]
    zero_rows = [row for row in rows if row["classification"] == "in_final_group_zero_reward_reconstruction_candidate"]

    source_commit_rows_matching_raw = sum(1 for row in source_commits if commit_key(row) in raw_by_key)
    raw_commit_rows_matching_source = sum(1 for row in raw_commits if commit_key(row) in source_by_key)

    md_lines = [
        "# P4 Conceptual Audit Pass 04: Epoch 266 Nonce Scope",
        "",
        "This pass checks the conceptual scope of the epoch `266` nonce claim.",
        "It does not reproduce the investigator arithmetic and does not approve",
        "the compensation amount.",
        "",
        "## Raw And Source Inputs",
        "",
        "- Raw chain commit store: `archive_cli_height_4120751_all_poc_v2_store_commits_4105361_stdout.json`",
        "- Raw chain validation records: `archive_cli_height_4120751_poc_v2_validations_for_stage_4105361_stdout_retry2.json`",
        "- Raw final epoch group/performance/exclusion files for epoch `266`",
        "- Source claim artifacts copied from the pinned Votkon repository under `source_cache/`",
        "",
        "Important limitation: the independent raw archive CLI commit output has",
        "`participant_address`, `count`, `root_hash`, and `hex_pub_key`, but no",
        "`model_id`. The source artifact has `model_id`; those labels are treated",
        "as source claims, not chain-only proof.",
        "",
        "## Commit Artifact Match",
        "",
        f"- Raw commit rows: `{len(raw_commits)}`",
        f"- Source commit rows: `{len(source_commits)}`",
        f"- Source rows with exact raw match by address/count/root/pubkey: `{source_commit_rows_matching_raw}`",
        f"- Raw rows with exact source match by address/count/root/pubkey: `{raw_commit_rows_matching_source}`",
        "",
        "## Source Nonce Compensation Rows",
        "",
        f"- Source nonce-compensation rows: `{len(rows)}`",
        f"- Rows also listed as excluded operators: `{len(excluded_rows)}`",
        f"- Rows that were in the final group and already rewarded: `{len(topup_rows)}`",
        f"- Rows that were in the final group but zero reward: `{len(zero_rows)}`",
        "",
        "## Excluded Operators",
        "",
        "| Address | Source Kimi commits | Raw commit count | Raw validation rows | Final group | Performance row | Source compensation |",
        "|---|---:|---:|---:|---|---|---:|",
    ]
    for row in excluded_rows:
        md_lines.append(
            "| `{address}` | `{source_kimi_commit_count}` | `{raw_commit_count_sum}` | "
            "`{raw_validation_rows}` | {final} | {perf} | `{source_nonce_compensation_gonka}` |".format(
                final="yes" if row["in_final_group"] else "no",
                perf="yes" if row["in_performance_summary"] else "no",
                **row,
            )
        )

    md_lines.extend(
        [
            "",
            "## Non-Excluded Top-Up Rows",
            "",
            "| Address | Source models | Final weight | Actual rewards (GONKA) | Source compensation | Classification |",
            "|---|---|---:|---:|---:|---|",
        ]
    )
    for row in topup_rows:
        md_lines.append(
            "| `{address}` | `{source_models}` | `{final_weight}` | `{actual:.9f}` | "
            "`{source_nonce_compensation_gonka}` | `{classification}` |".format(
                actual=row["actual_rewards_ngonka"] / 1_000_000_000,
                **row,
            )
        )

    if zero_rows:
        md_lines.extend(
            [
                "",
                "## In-Final-Group Zero-Reward Rows",
                "",
                "| Address | Source models | Final weight | Source compensation | Status |",
                "|---|---|---:|---:|---|",
            ]
        )
        for row in zero_rows:
            md_lines.append(
                "| `{address}` | `{source_models}` | `{final_weight}` | "
                "`{source_nonce_compensation_gonka}` | `{status}` |".format(**row)
            )

    md_lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The narrow e266 claim that nine listed addresses submitted PoC commits",
            "  and were absent from the final epoch group remains confirmed by raw",
            "  chain data.",
            "- The Kimi-specific label for those commits is not proven by the raw CLI",
            "  output alone. The Votkon source artifact labels the matching commit",
            "  rows as Kimi, and those rows match our raw commit rows exactly by",
            "  address/count/root/pubkey, but that is source-backed evidence rather",
            "  than a chain-only model-id proof.",
            "- The source nonce-compensation table contains more than the nine excluded",
            "  operators: it also compensates participants that were in the final group",
            "  and already received rewards. Those rows are reconstruction/top-up policy",
            "  rows, not final-set-exclusion victims.",
            "- Delegation compensation is a separate policy track. It depends on accepting",
            "  the excluded-operator event as compensable and on accepting indirect",
            "  delegator losses.",
        ]
    )
    md_path.write_text("\n".join(md_lines) + "\n")


if __name__ == "__main__":
    main()
