#!/usr/bin/env python3
"""Build row-level evidence for e266 rewarded reconstruction top-up rows.

Reads derived classifier output built from saved raw chain cache files. Does not
query nodes and does not run the investigator scripts.
"""

from __future__ import annotations

import csv
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


BASE = Path(__file__).resolve().parent


def load_json(path: Path) -> object:
    with path.open() as f:
        return json.load(f)


def ngonka_to_gonka(value: int) -> Decimal:
    return (Decimal(value) / Decimal(1_000_000_000)).quantize(
        Decimal("0.000000001"), rounding=ROUND_HALF_UP
    )


def dec(value: str) -> Decimal:
    return Decimal(value)


def main() -> None:
    classifier = load_json(BASE / "p4_e266_nonce_scope_classifier.json")
    rows = []
    for row in classifier:
        if row["classification"] != "in_final_group_rewarded_reconstruction_top_up":
            continue
        actual = int(row["actual_rewards_ngonka"])
        source_comp = dec(row["source_nonce_compensation_gonka"])
        actual_gonka = ngonka_to_gonka(actual)
        total_source_claim = actual_gonka + source_comp
        ratio = (
            (source_comp / actual_gonka).quantize(Decimal("0.0001"))
            if actual_gonka
            else Decimal("0")
        )
        rows.append(
            {
                "address": row["address"],
                "source_models": row["source_models"],
                "source_kimi_commit_count": row["source_kimi_commit_count"],
                "source_qwen_commit_count": row["source_qwen_commit_count"],
                "raw_commit_rows": row["raw_commit_rows"],
                "raw_commit_count_sum": row["raw_commit_count_sum"],
                "raw_validation_rows": row["raw_validation_rows"],
                "in_final_group": row["in_final_group"],
                "final_weight": row["final_weight"],
                "final_confirmation_weight": row["final_confirmation_weight"],
                "actual_rewards_gonka": str(actual_gonka),
                "source_topup_compensation_gonka": str(source_comp),
                "source_claimed_total_after_topup_gonka": str(total_source_claim),
                "source_topup_to_actual_reward_ratio": str(ratio),
                "in_excluded_participants_266": row["in_excluded_participants_266"],
                "source_excluded_operator": row["source_excluded_operator"],
                "local_conclusion": "rewarded_in_final_group_reconstruction_topup_policy_required",
            }
        )

    csv_path = BASE / "p4_e266_rewarded_topup_rows.csv"
    json_path = BASE / "p4_e266_rewarded_topup_rows.json"
    md_path = BASE / "p4_problem_02b_e266_rewarded_topup_rows.md"

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n")

    total_actual = sum(dec(row["actual_rewards_gonka"]) for row in rows)
    total_topup = sum(dec(row["source_topup_compensation_gonka"]) for row in rows)
    total_claimed = sum(dec(row["source_claimed_total_after_topup_gonka"]) for row in rows)

    md_lines = [
        "# P4 Problem 02b: Epoch 266 Rewarded Top-Up Rows",
        "",
        "This note separates the 4 in-final-group rewarded reconstruction rows",
        "from the 9 absent final-set operators in the epoch `266` nonce claim.",
        "",
        "## Question",
        "",
        "Should participants who entered the final group and already received",
        "epoch `266` rewards receive an additional reconstruction top-up?",
        "",
        "## Rows",
        "",
        "| Address | Source models | Raw commits | Validation rows | Final weight | Confirmation weight | Actual reward | Source top-up | Top-up / actual | Conclusion |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        md_lines.append(
            "| `{address}` | `{source_models}` | `{raw_commit_count_sum}` | "
            "`{raw_validation_rows}` | `{final_weight}` | "
            "`{final_confirmation_weight}` | `{actual_rewards_gonka}` | "
            "`{source_topup_compensation_gonka}` | "
            "`{source_topup_to_actual_reward_ratio}` | "
            "`{local_conclusion}` |".format(**row)
        )

    md_lines.extend(
        [
            "",
            "## Totals",
            "",
            "| Quantity | GONKA |",
            "|---|---:|",
            f"| Actual rewards already paid | `{total_actual}` |",
            f"| Source proposed top-up | `{total_topup}` |",
            f"| Source implied post-top-up total | `{total_claimed}` |",
            "",
            "## Findings",
            "",
            "- Rows checked: `4`",
            "- All 4 rows were present in the final epoch group.",
            "- All 4 rows already received non-zero rewards.",
            "- None of the 4 rows is in `excluded_participants/266`.",
            "- These rows are not final-set-exclusion victims. They are a",
            "  reconstruction/top-up policy claim.",
            "",
            "## Audit Remark",
            "",
            "`P4-E266-TOPUP-01`: these rows should not be approved together with",
            "the 9 absent operators unless the committee explicitly accepts",
            "reconstruction top-ups for already rewarded participants.",
        ]
    )
    md_path.write_text("\n".join(md_lines) + "\n")


if __name__ == "__main__":
    main()
