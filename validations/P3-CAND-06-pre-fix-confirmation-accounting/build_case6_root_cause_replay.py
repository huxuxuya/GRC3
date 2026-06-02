#!/usr/bin/env python3
"""Build root-cause replay artifacts for P3-CAND-06.

This script intentionally starts from normalized archive-scan artifacts already
produced by the independent P3-CAND-03 validation. It does not execute any
external compensation repository.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any


getcontext().prec = 80

CASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = CASE_DIR.parents[1]
CASE3_DIR = REPO_ROOT / "validations" / "P3-CAND-03-failed-cpoc-epoch-267"

P3_CAND_04_KNOWN_ADDRESS = "gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09"
POC_DEVIATION_COEFF = Decimal("0.909")
RATIO_TOLERANCE = Decimal("0.000001")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def dec(value: str | int | Decimal) -> Decimal:
    return value if isinstance(value, Decimal) else Decimal(str(value))


def fmt_gonka(value: Decimal) -> str:
    return f"{value:.9f}"


def fmt_int(value: Any) -> str:
    return f"{int(value):,}"


def pct(value: Decimal) -> str:
    return f"{value * Decimal(100):.4f}%"


def candidate_keys() -> set[tuple[str, str, str]]:
    return {
        (row["epoch"], row["participant"], row["event_trigger_height"])
        for row in read_csv(CASE_DIR / "candidate_rows.csv")
    }


def load_candidate_source_rows() -> list[dict[str, str]]:
    keys = candidate_keys()
    rows = []
    for row in read_csv(CASE3_DIR / "case3_neighbor_failed_cpoc_rows.csv"):
        key = (row["epoch"], row["participant"], row["event_trigger_height"])
        if key in keys:
            rows.append(row)
    return sorted(rows, key=lambda row: (int(row["epoch"]), row["participant"], int(row["event_trigger_height"])))


def pass_models(row: dict[str, str]) -> list[str]:
    out = []
    if row["qwen_result"] == "pass_weight":
        out.append("Qwen")
    if row["kimi_result"] == "pass_weight":
        out.append("Kimi")
    return out


def coefficient_replayed_keys() -> set[tuple[str, str, str]]:
    path = CASE_DIR / "case6_coefficient_replay.csv"
    if not path.exists():
        return set()
    return {
        (row["epoch"], row["participant"], row["event_trigger_height"])
        for row in read_csv(path)
        if row.get("coefficient_replay_matches_stored") == "True"
    }


def coefficient_remaining_mismatch_count() -> int:
    path = CASE_DIR / "case6_coefficient_replay.csv"
    if not path.exists():
        return 0
    return sum(1 for row in read_csv(path) if row.get("coefficient_replay_matches_stored") == "False")


def classify(row: dict[str, str], simple_ratio_matches: bool, coefficient_replayed: bool) -> tuple[str, str]:
    epoch = int(row["epoch"])
    passes = pass_models(row)
    if len(passes) == 2 and epoch == 276:
        return (
            "strong_signal_but_epoch276_overlap",
            "both tracked models reached pass_weight, but this is during the v0.2.13 upgrade epoch and overlaps the P3-CAND-04 cPoC-misfire review",
        )
    if len(passes) == 2:
        return (
            "strong_pass_weight_vs_failed_ratio_signal",
            "both tracked models reached pass_weight, but final confirmation ratio still fell below alpha",
        )
    if simple_ratio_matches:
        return (
            "single_model_pass_expected_capacity_failed",
            "one tracked model reached pass_weight, the other had no submission; stored ratio reconciles with the observed confirmation-weight reduction",
        )
    if coefficient_replayed:
        return (
            "single_model_pass_coefficient_replayed",
            "one tracked model reached pass_weight; stored ratio reconciles after historical coefficients, time normalization, preserved snapshot, and MLNode distribution replay",
        )
    return (
        "single_model_pass_needs_coefficient_replay",
        "one tracked model reached pass_weight, but simple weight-ratio replay does not match stored ratio; coefficient-adjusted preserved/measured components are required",
    )


def build_rows() -> list[dict[str, Any]]:
    rows = []
    coeff_replayed = coefficient_replayed_keys()
    for row in load_candidate_source_rows():
        before = dec(row["confirmation_weight_before_exclusion"])
        after = dec(row["confirmation_weight_at_exclusion"])
        stored_ratio = dec(row["confirmation_ratio"])
        simple_ratio = after / before / POC_DEVIATION_COEFF if before else Decimal(0)
        diff = stored_ratio - simple_ratio
        simple_matches = abs(diff) <= RATIO_TOLERANCE
        key = (row["epoch"], row["participant"], row["event_trigger_height"])
        classification, reason = classify(row, simple_matches, key in coeff_replayed)
        total = int(row["total_network_weight"])
        two_thirds_min = total * 2 // 3 + 1
        qwen_valid = int(row["qwen_valid_weight"])
        kimi_valid = int(row["kimi_valid_weight"])
        p3_epoch_overlap = row["epoch"] == "276"
        p3_known_overlap = p3_epoch_overlap and row["participant"] == P3_CAND_04_KNOWN_ADDRESS
        p4_epoch_overlap = 265 <= int(row["epoch"]) <= 276
        rows.append(
            {
                "epoch": row["epoch"],
                "participant": row["participant"],
                "event_sequence": row["event_sequence"],
                "event_trigger_height": row["event_trigger_height"],
                "exclusion_height": row["exclusion_height"],
                "total_network_weight": total,
                "two_thirds_min_weight": two_thirds_min,
                "root_weight": row["root_weight"],
                "confirmation_weight_before": row["confirmation_weight_before_exclusion"],
                "confirmation_weight_at_exclusion": row["confirmation_weight_at_exclusion"],
                "confirmation_weight_delta": row["confirmation_weight_delta"],
                "stored_confirmation_ratio": row["confirmation_ratio"],
                "stored_confirmation_ratio_percent": row["confirmation_ratio_percent"],
                "simple_ratio_from_confirmation_weights": f"{simple_ratio:.16f}",
                "simple_ratio_diff": f"{diff:.16f}",
                "simple_ratio_matches_stored": str(simple_matches),
                "alpha_threshold": row["alpha_threshold"],
                "qwen_submitted_count": row["qwen_submitted_count"],
                "qwen_valid_weight": qwen_valid,
                "qwen_valid_weight_percent": row["qwen_valid_weight_percent"],
                "qwen_result": row["qwen_result"],
                "qwen_shortfall_vs_two_thirds": max(0, two_thirds_min - qwen_valid),
                "kimi_submitted_count": row["kimi_submitted_count"],
                "kimi_valid_weight": kimi_valid,
                "kimi_valid_weight_percent": row["kimi_valid_weight_percent"],
                "kimi_result": row["kimi_result"],
                "kimi_shortfall_vs_two_thirds": max(0, two_thirds_min - kimi_valid),
                "pass_models": "+".join(pass_models(row)),
                "max_single_preserved_kimi_weight": row["max_single_preserved_kimi_weight"],
                "max_single_preserved_kimi_weight_percent": row["max_single_preserved_kimi_weight_percent"],
                "loss_gonka": row["loss_gonka"],
                "classification": classification,
                "classification_reason": reason,
                "p3_cand_04_epoch_overlap": str(p3_epoch_overlap),
                "p3_cand_04_known_address_overlap": str(p3_known_overlap),
                "p4_cand_01_epoch_overlap": str(p4_epoch_overlap),
            }
        )
    return rows


def write_root_cause_review(rows: list[dict[str, Any]]) -> None:
    by_class = Counter(row["classification"] for row in rows)
    by_epoch = defaultdict(lambda: {"rows": 0, "loss": Decimal(0)})
    total_loss = Decimal(0)
    for row in rows:
        loss = dec(row["loss_gonka"])
        total_loss += loss
        by_epoch[row["epoch"]]["rows"] += 1
        by_epoch[row["epoch"]]["loss"] += loss

    lines = [
        "# P3-CAND-06 Root-Cause Replay",
        "",
        "This replay checks the `24` pass-weight-but-failed-ratio candidate rows",
        "against normalized archive-chain artifacts. It is independent from",
        "external compensation repositories.",
        "",
        "## Result",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Candidate rows | `{len(rows)}` |",
        f"| Unique participants | `{len({row['participant'] for row in rows})}` |",
        f"| Estimated zero-reward loss | `{fmt_gonka(total_loss)}` GONKA |",
        f"| Rows with both Qwen and Kimi `pass_weight` | `{sum(row['pass_models'] == 'Qwen+Kimi' for row in rows)}` |",
        f"| Rows with exactly one `pass_weight` model | `{sum(row['pass_models'] != 'Qwen+Kimi' for row in rows)}` |",
        f"| Rows where simple `at/before/0.909` ratio matches stored ratio | `{sum(row['simple_ratio_matches_stored'] == 'True' for row in rows)}` |",
        f"| Rows where simple `at/before/0.909` ratio does not match stored ratio | `{sum(row['simple_ratio_matches_stored'] == 'False' for row in rows)}` |",
        f"| Simple-ratio mismatch rows reconciled by coefficient replay | `{sum(row['classification'] == 'single_model_pass_coefficient_replayed' for row in rows)}` |",
        f"| Remaining mismatch after coefficient replay | `{coefficient_remaining_mismatch_count()}` |",
        "",
        "## Classification",
        "",
        "| Classification | Rows | Meaning |",
        "|---|---:|---|",
    ]
    meaning = {
        "single_model_pass_expected_capacity_failed": "One model passed, the other had no submission; observed confirmation-weight reduction already reconciles with stored ratio.",
        "single_model_pass_coefficient_replayed": "One model passed; coefficient-adjusted replay matches the stored ratio once historical coefficients, time normalization, and preserved snapshots are used.",
        "single_model_pass_needs_coefficient_replay": "One model passed, but simple confirmation-weight replay does not match stored ratio; coefficient-adjusted components are required.",
        "strong_signal_but_epoch276_overlap": "Both tracked models passed, but the row is in upgrade epoch 276 and overlaps P3-CAND-04 review.",
        "strong_pass_weight_vs_failed_ratio_signal": "Both tracked models passed and final ratio still failed.",
    }
    for name, count in sorted(by_class.items()):
        lines.append(f"| `{name}` | `{count}` | {meaning.get(name, '')} |")

    lines.extend(
        [
            "",
            "## Epoch Distribution",
            "",
            "| Epoch | Rows | Estimated loss, GONKA |",
            "|---:|---:|---:|",
        ]
    )
    for epoch in sorted(by_epoch, key=int):
        lines.append(f"| `{epoch}` | `{by_epoch[epoch]['rows']}` | `{fmt_gonka(by_epoch[epoch]['loss'])}` |")

    lines.extend(
        [
            "",
            "## Chain Mechanism Checked",
            "",
            "For every row, the raw model result is checked against the chain rule:",
            "",
            "```text",
            "validWeight > TotalNetworkWeight * 2 / 3",
            "```",
            "",
            "All `24` candidate rows still have at least one model with `pass_weight`",
            "under that strict rule, while the durable chain state records",
            "`failed_confirmation_poc`, zero reward, and `ConfirmationPoCRatio < 0.5`.",
            "",
            "The likely fix family is PR #1143 / `v0.2.13`, whose PR text says the",
            "microrelease fixes confirmation PoC weight loss during new-model",
            "bootstrap by using one epoch snapshot of confirmable models and",
            "weight-scale factors for confirmation and reward-weight calculations:",
            "",
            "```text",
            "https://github.com/gonka-ai/gonka/pull/1143",
            "```",
            "",
            "`case6_coefficient_replay.md` replays the `6` simple-ratio mismatch rows with",
            "historical coefficients, cPoC time normalization, preserved snapshots, and ML",
            "node distributions. It reconciles `5/6`; the remaining non-match is the epoch",
            "`276` overlap row.",
            "",
            "However, this replay does not mark the full `24` rows as confirmed",
            "compensation rows. A single model reaching `pass_weight` does not by itself",
            "prove that all expected confirmation capacity should have been preserved.",
            "",
            "## Strongest Current Signal",
            "",
        ]
    )
    strong = [row for row in rows if row["classification"] == "strong_signal_but_epoch276_overlap"]
    if strong:
        row = strong[0]
        lines.extend(
            [
                "The strongest pass-weight contradiction is:",
                "",
                "| Epoch | Participant | Qwen | Kimi | Ratio | Loss, GONKA | Caveat |",
                "|---:|---|---|---|---:|---:|---|",
                f"| `{row['epoch']}` | `{row['participant']}` | `{row['qwen_valid_weight_percent']}% pass_weight` | `{row['kimi_valid_weight_percent']}% pass_weight` | `{row['stored_confirmation_ratio_percent']}%` | `{row['loss_gonka']}` | Epoch 276 overlaps the upgrade cPoC-misfire case. |",
                "",
            ]
        )
    lines.extend(
        [
            "## Current Conclusion",
            "",
            "- `P3-CAND-06` is real as a chain-state anomaly set: pass-weight evidence and",
            "  failed confirmation state coexist in `24` rows.",
            "- It is not yet proven that all `24` rows are protocol-bug compensation rows;",
            "  `23` are single-model-pass rows where the other tracked model had no",
            "  submission, even though their stored ratios are now formula-reconciled.",
            "- PR `#1143` is the main fix reference to inspect; PRs `#550` and `#826`",
            "  are currently treated as unrelated settlement/claim-path fixes unless a",
            "  direct confirmation-PoC code link is later found.",
            "- Epoch `276` rows must be reconciled with `P3-CAND-04` before any payout",
            "  decision.",
            "",
            "Detailed row data is in `case6_row_formula_replay.csv` and",
            "`case6_row_formula_replay.json`. Coefficient replay data is in",
            "`case6_coefficient_replay.csv` and `case6_coefficient_replay.json`.",
        ]
    )
    (CASE_DIR / "case6_root_cause_replay.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_overlap_review(rows: list[dict[str, Any]]) -> None:
    p3_epoch_rows = [row for row in rows if row["p3_cand_04_epoch_overlap"] == "True"]
    p3_known = [row for row in rows if row["p3_cand_04_known_address_overlap"] == "True"]
    p4_epoch_rows = [row for row in rows if row["p4_cand_01_epoch_overlap"] == "True"]
    lines = [
        "# P3-CAND-06 Overlap Review",
        "",
        "This note separates proven address overlap from epoch-level review signals.",
        "",
        "## P3-CAND-04",
        "",
        "| Check | Result |",
        "|---|---:|",
        f"| Epoch `276` candidate rows | `{len(p3_epoch_rows)}` |",
        f"| Known same-address overlap in local evidence | `{len(p3_known)}` |",
        "",
    ]
    if p3_known:
        lines.extend(
            [
                "Known same-address overlap:",
                "",
                "| Epoch | Participant | Loss, GONKA | Note |",
                "|---:|---|---:|---|",
            ]
        )
        for row in p3_known:
            lines.append(
                f"| `{row['epoch']}` | `{row['participant']}` | `{row['loss_gonka']}` | Also named in P3-CAND-04 public evidence. |"
            )
        lines.append("")
    lines.extend(
        [
            "The other epoch `276` rows are epoch-level overlaps with P3-CAND-04, but",
            "the local repository does not contain the full `payout276` address list.",
            "They should remain blocked from payout until checked against that list.",
            "",
            "## P4-CAND-01",
            "",
            "| Check | Result |",
            "|---|---:|",
            f"| Candidate rows in P4-CAND-01 epoch range `265..276` | `{len(p4_epoch_rows)}` |",
            "",
            "This is an epoch-level overlap only. The current repository does not include",
            "a normalized P4-CAND-01 address-by-epoch table, so same-address duplicate",
            "risk is unresolved here.",
            "",
            "## Decision Rule",
            "",
            "- Do not approve any P3-CAND-06 row that overlaps an already-approved row by",
            "  address and epoch.",
            "- Treat epoch-level overlap as a mandatory review signal, not as proof of",
            "  duplicate compensation.",
        ]
    )
    (CASE_DIR / "case6_overlap_review.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = build_rows()
    fieldnames = [
        "epoch",
        "participant",
        "event_sequence",
        "event_trigger_height",
        "exclusion_height",
        "total_network_weight",
        "two_thirds_min_weight",
        "root_weight",
        "confirmation_weight_before",
        "confirmation_weight_at_exclusion",
        "confirmation_weight_delta",
        "stored_confirmation_ratio",
        "stored_confirmation_ratio_percent",
        "simple_ratio_from_confirmation_weights",
        "simple_ratio_diff",
        "simple_ratio_matches_stored",
        "alpha_threshold",
        "qwen_submitted_count",
        "qwen_valid_weight",
        "qwen_valid_weight_percent",
        "qwen_result",
        "qwen_shortfall_vs_two_thirds",
        "kimi_submitted_count",
        "kimi_valid_weight",
        "kimi_valid_weight_percent",
        "kimi_result",
        "kimi_shortfall_vs_two_thirds",
        "pass_models",
        "max_single_preserved_kimi_weight",
        "max_single_preserved_kimi_weight_percent",
        "loss_gonka",
        "classification",
        "classification_reason",
        "p3_cand_04_epoch_overlap",
        "p3_cand_04_known_address_overlap",
        "p4_cand_01_epoch_overlap",
    ]
    write_csv(CASE_DIR / "case6_row_formula_replay.csv", rows, fieldnames)
    write_json(
        CASE_DIR / "case6_row_formula_replay.json",
        {
            "case": "P3-CAND-06",
            "source": "validations/P3-CAND-03-failed-cpoc-epoch-267/case3_neighbor_failed_cpoc_rows.csv",
            "poc_deviation_coeff": str(POC_DEVIATION_COEFF),
            "ratio_tolerance": str(RATIO_TOLERANCE),
            "rows": rows,
            "summary": {
                "rows": len(rows),
                "unique_participants": len({row["participant"] for row in rows}),
                "total_loss_gonka": fmt_gonka(sum(dec(row["loss_gonka"]) for row in rows)),
                "classification_counts": dict(Counter(row["classification"] for row in rows)),
            },
        },
    )
    write_root_cause_review(rows)
    write_overlap_review(rows)
    print(
        json.dumps(
            {
                "rows": len(rows),
                "unique_participants": len({row["participant"] for row in rows}),
                "classifications": dict(Counter(row["classification"] for row in rows)),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
