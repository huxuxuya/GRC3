#!/usr/bin/env python3
"""Build P4 e265/e266 attack-track summary.

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


def load_json(path: Path) -> object:
    with path.open() as f:
        return json.load(f)


def gonka(ngonka: int | Decimal) -> Decimal:
    return (Decimal(ngonka) / Decimal(1_000_000_000)).quantize(
        Decimal("0.000000001"), rounding=ROUND_HALF_UP
    )


def gonka_str(ngonka: int | Decimal) -> str:
    return f"{gonka(ngonka):.9f}"


def epoch_raw(epoch: int) -> tuple[list[dict], list[dict], list[dict]]:
    if epoch == 265:
        performance = load_json(RAW / "node1_epoch_performance_summary_265.json")[
            "epochPerformanceSummary"
        ]
        group = load_json(RAW / "node1_epoch_group_data_265.json")["epoch_group_data"][
            "validation_weights"
        ]
        excluded = load_json(RAW / "node1_excluded_participants_265.json").get(
            "items", []
        )
    elif epoch == 266:
        performance = load_json(RAW / "archive_lcd_epoch_performance_summary_266.json")[
            "epochPerformanceSummary"
        ]
        group = load_json(RAW / "archive_lcd_epoch_group_data_266.json")[
            "epoch_group_data"
        ]["validation_weights"]
        excluded = load_json(RAW / "archive_lcd_excluded_participants_266.json").get(
            "items", []
        )
    else:
        raise ValueError(epoch)
    return performance, group, excluded


def source_affected(epoch: int) -> tuple[int, int, set[str], Decimal]:
    source = load_json(SOURCE / f"votkon_e{epoch}_compensation_{epoch}.json")
    if epoch == 265:
        rows = source["compensation"]
        addresses = {row["address"] for row in rows}
        return len(rows), len(addresses), addresses, Decimal(
            str(source["total_compensation_gonka"])
        )

    nonce = source["nonce_compensation"]["entries"]
    delegation = source["delegation_compensation"]["entries"]
    addresses = {row["address"] for row in nonce} | {row["address"] for row in delegation}
    total = Decimal(str(source["grand_total_gonka"]))
    return len(nonce) + len(delegation), len(addresses), addresses, total


def e266_subtrack_counts() -> dict[str, int]:
    classifier = load_json(BASE / "p4_e266_nonce_scope_classifier.json")
    delegation = load_json(BASE / "p4_e266_delegation_evidence.json")
    return {
        "excluded_operator_rows": sum(
            1
            for row in classifier
            if row["classification"]
            == "source_excluded_operator_confirmed_absent_from_final_group"
        ),
        "zero_reward_rows": sum(
            1
            for row in classifier
            if row["classification"]
            == "in_final_group_zero_reward_reconstruction_candidate"
        ),
        "rewarded_topup_rows": sum(
            1
            for row in classifier
            if row["classification"] == "in_final_group_rewarded_reconstruction_top_up"
        ),
        "delegation_rows": len(delegation),
    }


def main() -> None:
    rows = []
    for epoch in (265, 266):
        performance, group, excluded = epoch_raw(epoch)
        source = load_json(SOURCE / f"votkon_e{epoch}_compensation_{epoch}.json")
        reward_pool = int(source["epoch_theoretical_reward_ngonka"])
        rewarded = sum(int(row.get("rewarded_coins", 0)) for row in performance)
        burned = sum(int(row.get("burned_coins", 0)) for row in performance)
        gov_remainder = reward_pool - rewarded - burned

        perf_addrs = {row["participant_id"] for row in performance}
        group_addrs = {row["member_address"] for row in group}
        excluded_addrs = {row.get("address", row.get("participant_id")) for row in excluded}
        union_addrs = perf_addrs | group_addrs | excluded_addrs
        zero_reward_perf = sum(
            1 for row in performance if int(row.get("rewarded_coins", 0)) == 0
        )
        affected_rows, affected_unique, _affected_addresses, source_total = source_affected(
            epoch
        )

        rows.append(
            {
                "epoch": epoch,
                "final_group_participants": len(group_addrs),
                "performance_rows": len(perf_addrs),
                "excluded_rows": len(excluded_addrs),
                "participant_union_count": len(union_addrs),
                "zero_reward_performance_rows": zero_reward_perf,
                "source_affected_rows": affected_rows,
                "source_affected_unique_addresses": affected_unique,
                "source_compensation_gonka": str(source_total),
                "theoretical_reward_pool_gonka": gonka_str(reward_pool),
                "reward_pool_input": "source_compensation_json",
                "actual_rewarded_gonka": gonka_str(rewarded),
                "burned_gonka": gonka_str(burned),
                "gov_remainder_gonka": gonka_str(gov_remainder),
                "source_comp_minus_gov_remainder_gonka": str(
                    (source_total - gonka(gov_remainder)).quantize(
                        Decimal("0.000000001"), rounding=ROUND_HALF_UP
                    )
                ),
            }
        )

    csv_path = BASE / "p4_attack_epoch_summary.csv"
    json_path = BASE / "p4_attack_epoch_summary.json"
    md_path = BASE / "p4_attack_summary.md"

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=list(rows[0].keys()), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)

    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n")

    e266_counts = e266_subtrack_counts()
    total_source = sum(Decimal(row["source_compensation_gonka"]) for row in rows)
    total_gov = sum(Decimal(row["gov_remainder_gonka"]) for row in rows)

    md_lines = [
        "# P4 Attack Summary: Epochs 265-266",
        "",
        "This note summarizes the P4 attack-attributed part only: epochs `265`",
        "and `266`. It uses saved raw chain cache files and copied source",
        "artifacts; it does not query nodes and does not run source scripts.",
        "",
        "Important data-source split: participant counts, final rewarded coins,",
        "burned coins, final group rows, and exclusion rows come from saved raw",
        "chain responses. The theoretical fixed epoch reward pool is taken from",
        "the saved source compensation JSON, because the raw performance summary",
        "endpoint does not expose that pool directly.",
        "",
        "## Epoch Summary",
        "",
        "| Epoch | Participants union | Final group | Excluded | Zero-reward perf rows | Source affected rows | Source affected unique | Source comp | Gov remainder |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        md_lines.append(
            "| `{epoch}` | `{participant_union_count}` | `{final_group_participants}` | "
            "`{excluded_rows}` | `{zero_reward_performance_rows}` | "
            "`{source_affected_rows}` | `{source_affected_unique_addresses}` | "
            "`{source_compensation_gonka}` | `{gov_remainder_gonka}` |".format(
                **row
            )
        )

    md_lines.extend(
        [
            "",
            "## E266 Source Split",
            "",
            "| Sub-track | Rows |",
            "|---|---:|",
            f"| Absent final-set operators | `{e266_counts['excluded_operator_rows']}` |",
            f"| In-final-group zero-reward rows | `{e266_counts['zero_reward_rows']}` |",
            f"| In-final-group rewarded top-up rows | `{e266_counts['rewarded_topup_rows']}` |",
            f"| Delegation rows | `{e266_counts['delegation_rows']}` |",
            "",
            "## Gov Remainder Interpretation",
            "",
            f"- Source e265+e266 compensation total: `{total_source}` GONKA.",
            f"- Raw-settlement gov remainder for e265+e266: `{total_gov}` GONKA.",
            "- These numbers are not expected to match. Source compensation is a",
            "  counterfactual reconstruction; gov remainder is the epoch reward pool",
            "  left undistributed after actual rewarded/burned coins.",
            "- Treat the gov remainder as an epoch-level undistributed settlement",
            "  remainder, not as a direct proof of a wallet balance delta.",
            "- For e266 especially, source compensation is much larger than the gov",
            "  remainder, so the source claim cannot be described as simply",
            "  'all lost rewards went to the gov wallet'.",
            "",
            "## Main Takeaway",
            "",
            "The attack-attributed source package covers a small subset of participant",
            "rows, but its proposed compensation is not equal to the amount that can",
            "be directly identified as epoch-level governance remainder.",
        ]
    )
    md_path.write_text("\n".join(md_lines) + "\n")


if __name__ == "__main__":
    main()
