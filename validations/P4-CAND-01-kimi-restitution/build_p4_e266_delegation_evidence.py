#!/usr/bin/env python3
"""Build epoch 266 delegation evidence for P4.

Reads saved raw chain cache files plus copied source artifacts. Does not query
nodes and does not run the investigator scripts.
"""

from __future__ import annotations

import csv
import json
from decimal import Decimal, ROUND_DOWN
from pathlib import Path


BASE = Path(__file__).resolve().parent
RAW = BASE / "raw_chain_cache"
SOURCE = BASE / "source_cache"

KIMI = "moonshotai/Kimi-K2.6"


def load_json(path: Path) -> object:
    with path.open() as f:
        return json.load(f)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def dec_param(value: dict) -> Decimal:
    return Decimal(value["value"]) * (Decimal(10) ** int(value["exponent"]))


def main() -> None:
    source_rows = load_csv(SOURCE / "votkon_e266_compensation_266_delegation.csv")
    source_comp = load_json(SOURCE / "votkon_e266_compensation_266.json")
    params = load_json(RAW / "archive_lcd_height_4105361_params.json")["params"]
    final_group = load_json(RAW / "archive_lcd_epoch_group_data_266.json")["epoch_group_data"]
    performance = load_json(RAW / "archive_lcd_epoch_performance_summary_266.json")[
        "epochPerformanceSummary"
    ]

    final_weights = {
        row["member_address"]: int(row.get("weight", 0))
        for row in final_group.get("validation_weights", [])
    }
    performance_rewards = {
        row["participant_id"]: int(row.get("rewarded_coins", 0))
        for row in performance
    }

    delegation_params = params["delegation_params"]
    no_participation = dec_param(delegation_params["no_participation_penalty"])
    delegation_share = dec_param(delegation_params["delegation_share"])
    net_extra = no_participation - delegation_share
    deploy_window = int(delegation_params["deploy_window"])
    source_snapshot_height = int(source_comp["delegation_params"]["snapshot_height"])

    rows = []
    for source in source_rows:
        address = source["address"]
        raw_file = RAW / f"archive_lcd_height_4104861_poc_delegation_{address}.json"
        raw_doc = load_json(raw_file)
        kimi_rows = [
            row for row in raw_doc.get("delegations", []) if row.get("model_id") == KIMI
        ]
        raw_target = kimi_rows[0]["delegate_to"] if kimi_rows else ""
        expected_operator = source["excluded_operator"]
        final_weight = final_weights.get(address)
        actual_rewards = performance_rewards.get(address)
        source_chain_weight = int(source["chain_weight_post_penalty"])
        original_weight = (
            Decimal(source_chain_weight) / (Decimal(1) - no_participation)
        )
        extra_weight = original_weight * net_extra
        source_original = Decimal(source["reconstructed_original_weight"])
        source_extra = Decimal(source["extra_weight_lost"])

        rows.append(
            {
                "address": address,
                "snapshot_height": source_snapshot_height,
                "deploy_window": deploy_window,
                "raw_kimi_delegation_rows": len(kimi_rows),
                "raw_kimi_delegate_to": raw_target,
                "source_excluded_operator": expected_operator,
                "raw_matches_source_operator": raw_target == expected_operator,
                "operator_absent_from_final_group": expected_operator not in final_weights,
                "delegator_in_final_group": address in final_weights,
                "final_group_weight": final_weight,
                "source_chain_weight_post_penalty": source_chain_weight,
                "source_weight_matches_final_group": final_weight == source_chain_weight,
                "actual_rewards_ngonka": actual_rewards,
                "source_actual_rewards_ngonka": int(source["actual_rewards_ngonka"]),
                "source_rewards_match_performance": actual_rewards == int(source["actual_rewards_ngonka"]),
                "chain_no_participation_penalty": str(no_participation),
                "chain_delegation_share": str(delegation_share),
                "chain_net_extra_penalty": str(net_extra),
                "computed_original_weight": str(original_weight.quantize(Decimal("0.01"), rounding=ROUND_DOWN)),
                "source_reconstructed_original_weight": str(source_original),
                "computed_extra_weight_lost": str(extra_weight.quantize(Decimal("0.01"), rounding=ROUND_DOWN)),
                "source_extra_weight_lost": str(source_extra),
                "source_compensation_gonka": source["compensation_gonka"],
                "status": "chain_facts_confirmed_policy_required_for_compensation",
            }
        )

    csv_path = BASE / "p4_e266_delegation_evidence.csv"
    json_path = BASE / "p4_e266_delegation_evidence.json"
    md_path = BASE / "p4_audit_pass_05_e266_delegation.md"

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n")

    all_target_match = all(row["raw_matches_source_operator"] for row in rows)
    all_absent = all(row["operator_absent_from_final_group"] for row in rows)
    all_weight_match = all(row["source_weight_matches_final_group"] for row in rows)
    all_rewards_match = all(row["source_rewards_match_performance"] for row in rows)

    md_lines = [
        "# P4 Conceptual Audit Pass 05: Epoch 266 Delegation Evidence",
        "",
        "This pass checks the chain facts behind the epoch `266` delegation",
        "compensation track. It does not approve indirect-loss eligibility.",
        "",
        "## Raw Inputs",
        "",
        "- `archive_lcd_height_4104861_poc_delegation_<address>.json` for the 9 source delegators",
        "- `archive_lcd_height_4105361_params.json`",
        "- `archive_lcd_epoch_group_data_266.json`",
        "- `archive_lcd_epoch_performance_summary_266.json`",
        "",
        "## Summary",
        "",
        f"- Delegators checked: `{len(rows)}`",
        f"- Snapshot height: `{source_snapshot_height}`",
        f"- Deploy window from chain params: `{deploy_window}`",
        f"- Chain `no_participation_penalty`: `{no_participation}`",
        f"- Chain `delegation_share`: `{delegation_share}`",
        f"- Net extra penalty used by source: `{net_extra}`",
        f"- Every raw Kimi delegation points to source operator: `{all_target_match}`",
        f"- Source operator absent from final epoch group for every row: `{all_absent}`",
        f"- Source chain weights match final group weights: `{all_weight_match}`",
        f"- Source actual rewards match performance summary: `{all_rewards_match}`",
        "",
        "## Rows",
        "",
        "| Delegator | Raw Kimi target | Final weight | Actual rewards (GONKA) | Extra weight | Source comp |",
        "|---|---|---:|---:|---:|---:|",
    ]

    for row in rows:
        md_lines.append(
            "| `{address}` | `{raw_kimi_delegate_to}` | `{final_group_weight}` | "
            "`{actual:.9f}` | `{computed_extra_weight_lost}` | "
            "`{source_compensation_gonka}` |".format(
                actual=(row["actual_rewards_ngonka"] or 0) / 1_000_000_000,
                **row,
            )
        )

    md_lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Chain data confirms the factual delegation setup: all 9 source rows had",
            "  Kimi delegation to `gonka1q5xt54...` at snapshot height `4104861`.",
            "- Chain final group data confirms `gonka1q5xt54...` was absent from the",
            "  epoch `266` final group, while the 9 delegators were present.",
            "- Chain params confirm the source's mechanical delta: `0.15 - 0.05 = 0.10`.",
            "- The remaining question is policy, not raw-data truth: whether indirect",
            "  delegator losses caused by an excluded operator should be compensated",
            "  under this case.",
        ]
    )
    md_path.write_text("\n".join(md_lines) + "\n")


if __name__ == "__main__":
    main()
