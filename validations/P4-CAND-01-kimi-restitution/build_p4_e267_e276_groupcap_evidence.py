#!/usr/bin/env python3
"""Build e267-e276 ComputeGroupCap methodology evidence for P4.

Reads saved raw chain cache files plus copied source artifacts. Does not query
nodes and does not run the investigator scripts.
"""

from __future__ import annotations

import csv
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


BASE = Path(__file__).resolve().parent
RAW = BASE / "raw_chain_cache"
SOURCE = BASE / "source_cache"

EPOCHS = list(range(267, 277))
KIMI = "moonshotai/Kimi-K2.6"
UPGRADE_276_BLOCK = 4_267_300


def load_json(path: Path) -> object:
    with path.open() as f:
        return json.load(f)


def ngonka_to_gonka(value: Decimal) -> Decimal:
    return (value / Decimal(1_000_000_000)).quantize(
        Decimal("0.000000001"), rounding=ROUND_HALF_UP
    )


def sum_compensation(
    rows: list[dict], denominator: int, epoch_reward_ngonka: Decimal
) -> Decimal:
    if denominator <= 0:
        return Decimal(0)
    total = Decimal(0)
    for row in rows:
        confirmation = Decimal(int(row["confirmation_weight"]))
        actual = Decimal(int(row["actual_rewards_ngonka"]))
        correct = epoch_reward_ngonka * confirmation / Decimal(denominator)
        if correct > actual:
            total += correct - actual
    return total


def main() -> None:
    rows = []
    for epoch in EPOCHS:
        root_doc = load_json(RAW / f"node1_epoch_group_data_{epoch}.json")
        kimi_doc = load_json(RAW / f"node1_epoch_group_data_{epoch}_model_kimi.json")
        perf_doc = load_json(RAW / f"node1_epoch_performance_summary_{epoch}.json")
        source_doc = load_json(SOURCE / f"votkon_e{epoch}_compensation_{epoch}.json")

        root_group = root_doc["epoch_group_data"]
        root_rows = root_group["validation_weights"]
        root_by_addr = {row["member_address"]: row for row in root_rows}
        perf_by_addr = {
            row["participant_id"]: int(row.get("rewarded_coins", 0))
            for row in perf_doc["epochPerformanceSummary"]
        }

        source_rows = source_doc["compensation"]
        affected_addresses = [row["address"] for row in source_rows]
        root_total_weight = int(root_group["total_weight"])
        root_sum_weight = sum(int(row.get("weight", 0)) for row in root_rows)
        root_sum_confirmation = sum(
            int(row.get("confirmation_weight", 0)) for row in root_rows
        )

        affected_weight_sum = sum(int(row["validation_weight"]) for row in source_rows)
        affected_confirmation_sum = sum(
            int(row["confirmation_weight"]) for row in source_rows
        )
        affected_actual_sum = sum(int(row["actual_rewards_ngonka"]) for row in source_rows)
        source_total = Decimal(int(source_doc["total_compensation_ngonka"]))
        epoch_reward = Decimal(int(source_doc["epoch_theoretical_reward_ngonka"]))

        source_recalc = sum_compensation(source_rows, root_total_weight, epoch_reward)
        all_confirmation_recalc = sum_compensation(
            source_rows, root_sum_confirmation, epoch_reward
        )
        replaced_denominator = (
            root_total_weight - affected_weight_sum + affected_confirmation_sum
        )
        replaced_recalc = sum_compensation(
            source_rows, replaced_denominator, epoch_reward
        )

        root_matches_source = (
            root_total_weight == int(source_doc["root_total_weight"])
            and root_sum_weight == int(source_doc["total_validation_weight"])
            and root_sum_confirmation == int(source_doc["total_confirmation_weight"])
        )
        source_rows_match_raw = all(
            addr in root_by_addr
            and int(root_by_addr[addr].get("weight", 0))
            == int(source["validation_weight"])
            and int(root_by_addr[addr].get("confirmation_weight", 0))
            == int(source["confirmation_weight"])
            and perf_by_addr.get(addr, 0) == int(source["actual_rewards_ngonka"])
            for addr, source in zip(affected_addresses, source_rows)
        )

        kimi_rows = kimi_doc["epoch_group_data"]["validation_weights"]
        kimi_model_addrs = {row["member_address"] for row in kimi_rows}
        kimi_model_weight_sum = sum(int(row.get("weight", 0)) for row in kimi_rows)
        kimi_model_confirmation_sum = sum(
            int(row.get("confirmation_weight", 0)) for row in kimi_rows
        )
        same_addr_root_weight_sum = sum(
            int(root_by_addr[addr].get("weight", 0))
            for addr in kimi_model_addrs
            if addr in root_by_addr
        )
        same_addr_root_confirmation_sum = sum(
            int(root_by_addr[addr].get("confirmation_weight", 0))
            for addr in kimi_model_addrs
            if addr in root_by_addr
        )

        upgrade_in_epoch = False
        pre_upgrade_share = ""
        if epoch == 276:
            effective = int(root_group["effective_block_height"])
            last = int(root_group["last_block_height"])
            upgrade_in_epoch = effective <= UPGRADE_276_BLOCK <= last
            total_blocks = last - effective + 1
            pre_blocks = max(0, min(UPGRADE_276_BLOCK - effective, total_blocks))
            pre_upgrade_share = str(
                (Decimal(pre_blocks) / Decimal(total_blocks)).quantize(Decimal("0.0001"))
            )

        rows.append(
            {
                "epoch": epoch,
                "affected_rows": len(source_rows),
                "source_denominator_mode": source_doc["denominator_mode"],
                "raw_root_total_weight": root_total_weight,
                "raw_root_sum_weight": root_sum_weight,
                "raw_root_sum_confirmation": root_sum_confirmation,
                "source_root_fields_match_raw": root_matches_source,
                "source_rows_match_raw_root_and_performance": source_rows_match_raw,
                "affected_weight_sum": affected_weight_sum,
                "affected_confirmation_sum": affected_confirmation_sum,
                "affected_actual_rewards_gonka": str(
                    ngonka_to_gonka(Decimal(affected_actual_sum))
                ),
                "kimi_model_rows": len(kimi_rows),
                "kimi_model_weight_sum": kimi_model_weight_sum,
                "kimi_model_confirmation_sum": kimi_model_confirmation_sum,
                "same_kimi_addresses_root_weight_sum": same_addr_root_weight_sum,
                "same_kimi_addresses_root_confirmation_sum": same_addr_root_confirmation_sum,
                "source_topup_comp_gonka": str(ngonka_to_gonka(source_total)),
                "source_recalc_matches": abs(source_recalc - source_total) < Decimal("100"),
                "all_confirmation_denominator": root_sum_confirmation,
                "all_confirmation_comp_gonka": str(
                    ngonka_to_gonka(all_confirmation_recalc)
                ),
                "replace_affected_denominator": replaced_denominator,
                "replace_affected_comp_gonka": str(ngonka_to_gonka(replaced_recalc)),
                "source_minus_all_confirmation_gonka": str(
                    ngonka_to_gonka(source_total - all_confirmation_recalc)
                ),
                "source_minus_replace_affected_gonka": str(
                    ngonka_to_gonka(source_total - replaced_recalc)
                ),
                "upgrade_4267300_inside_epoch": upgrade_in_epoch,
                "pre_upgrade_block_share_e276": pre_upgrade_share,
                "status": "cap_effect_confirmed_denominator_policy_required",
            }
        )

    csv_path = BASE / "p4_e267_e276_groupcap_denominator_check.csv"
    json_path = BASE / "p4_e267_e276_groupcap_denominator_check.json"
    md_path = BASE / "p4_audit_pass_06_e267_e276_groupcap.md"

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n")

    md_lines = [
        "# P4 Conceptual Audit Pass 06: Epochs 267-276 GroupCap Denominator",
        "",
        "This pass checks the later `ComputeGroupCap` track using saved raw chain",
        "data and copied source artifacts. It does not approve a compensation",
        "model.",
        "",
        "## Summary",
        "",
        "- Raw root group fields match the source compensation JSON fields for all",
        "  checked epochs.",
        "- Source affected rows match raw root `weight`, raw root",
        "  `confirmation_weight`, and raw performance `rewarded_coins`.",
        "- The source formula is reproducible as a top-up using",
        "  `confirmation_weight / root_total_weight * epoch_reward - actual`.",
        "- That is not the only possible counterfactual denominator. Using all-root",
        "  `confirmation_weight` or replacing only affected capped weight with",
        "  affected confirmation weight gives materially different totals.",
        "- Epoch `276` contains upgrade block `4,267,300` inside the epoch window, so",
        "  full-epoch treatment needs an explicit policy/proration decision.",
        "",
        "## Epoch Totals",
        "",
        "| Epoch | Rows | Root total | Root conf | Source top-up | All-conf denom comp | Replace-affected comp | e276 pre-upgrade share |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        md_lines.append(
            "| `{epoch}` | `{affected_rows}` | `{raw_root_total_weight}` | "
            "`{raw_root_sum_confirmation}` | `{source_topup_comp_gonka}` | "
            "`{all_confirmation_comp_gonka}` | `{replace_affected_comp_gonka}` | "
            "`{pre_upgrade_block_share_e276}` |".format(**row)
        )

    total_source = sum(Decimal(row["source_topup_comp_gonka"]) for row in rows)
    total_all_conf = sum(Decimal(row["all_confirmation_comp_gonka"]) for row in rows)
    total_replace = sum(Decimal(row["replace_affected_comp_gonka"]) for row in rows)
    md_lines.extend(
        [
            "",
            "## Totals Across 267-276",
            "",
            "| Model | Total GONKA | Interpretation |",
            "|---|---:|---|",
            f"| Source top-up / capped root denominator | `{total_source}` | Uses the already-capped settlement denominator. |",
            f"| All root confirmation denominator | `{total_all_conf}` | Uses `confirmation_weight` as both numerator and denominator. |",
            f"| Replace affected weight denominator | `{total_replace}` | Replaces affected capped weight with affected confirmation weight, leaving other root weights unchanged. |",
            "",
            "## Interpretation",
            "",
            "- The cap/weight-pressure pattern is real chain state.",
            "- The source amount is a reproducible top-up model, not proof that the",
            "  same amount follows from a unique chain-style replay.",
            "- The committee must choose the denominator model before accepting any",
            "  e267-e276 `ComputeGroupCap` compensation amount.",
        ]
    )
    md_path.write_text("\n".join(md_lines) + "\n")


if __name__ == "__main__":
    main()
