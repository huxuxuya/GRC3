#!/usr/bin/env python3
"""Build row-by-row evidence and decision summaries for P3-CAND-06."""

from __future__ import annotations

import csv
import json
from collections import Counter
from decimal import Decimal
from pathlib import Path
from typing import Any


CASE_DIR = Path(__file__).resolve().parent


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


def key(row: dict[str, str]) -> tuple[str, str, str]:
    trigger = row.get("event_trigger_height") or row.get("cpoc_trigger_height")
    if trigger is None:
        raise KeyError(f"missing trigger height in row keys: {sorted(row)}")
    return row["epoch"], row["participant"], trigger


def model_key(row: dict[str, str]) -> tuple[str, str, str, str]:
    return row["epoch"], row["participant"], row["event_trigger_height"], row["model_label"]


def bool_text(value: str) -> str:
    return "yes" if value == "True" else "no"


def percent_from_ratio(value: str) -> str:
    return f"{(Decimal(value) * Decimal(100)).quantize(Decimal('0.0001'))}%"


def pct(value: str) -> str:
    return f"{Decimal(value).quantize(Decimal('0.0001'))}%"


def amount(value: Decimal | str) -> str:
    return f"{Decimal(value):,.9f}"


def compact_model(row: dict[str, str] | None) -> str:
    if not row:
        return "missing evidence row"
    result = row["result"]
    submitted = "commit" if row["commit_present"] == "True" else "no commit"
    valid = f"{row['valid_weight']}/{row['strict_two_thirds_min']} ({pct(row['valid_weight_percent'])})"
    commits = row["commit_count"]
    validators = f"{row['valid_validator_count']}/{row['validator_count']}"
    return f"{result}; {submitted}; commits {commits}; valid {valid}; validators {validators}"


def action_label(eligibility: dict[str, str], overlap: dict[str, str]) -> str:
    if overlap["recommended_action"] == "blocked":
        return "blocked: resolve P3-CAND-04 duplicate risk"
    if overlap["recommended_action"] == "review":
        return "review: compare against P4-CAND-01 before payout"
    if eligibility["eligibility_decision"] == "committee_policy_required":
        return "policy: decide whether single-model pass is compensable"
    return eligibility["eligibility_decision"]


def build_rows() -> list[dict[str, Any]]:
    candidates = read_csv(CASE_DIR / "candidate_rows.csv")
    timeline = {key(row): row for row in read_csv(CASE_DIR / "participant_epoch_timeline.csv")}
    old_replay = {key(row): row for row in read_csv(CASE_DIR / "case6_full_old_formula_replay.csv")}
    new_replay = {key(row): row for row in read_csv(CASE_DIR / "case6_new_algorithm_replay.csv")}
    eligibility = {key(row): row for row in read_csv(CASE_DIR / "case6_eligibility_matrix.csv")}
    overlap = {key(row): row for row in read_csv(CASE_DIR / "case6_overlap_matrix.csv")}
    submissions = {
        model_key(row): row for row in read_csv(CASE_DIR / "case6_submission_validator_evidence.csv")
    }

    rows: list[dict[str, Any]] = []
    for candidate in sorted(candidates, key=lambda r: (int(r["epoch"]), r["participant"], int(r["event_trigger_height"]))):
        row_key = key(candidate)
        old = old_replay[row_key]
        new = new_replay[row_key]
        elig = eligibility[row_key]
        ov = overlap[row_key]
        tl = timeline[row_key]
        qwen = submissions.get((*row_key, "qwen"))
        kimi = submissions.get((*row_key, "kimi"))
        pass_models = old["pass_models"]
        qwen_pass = qwen is not None and qwen["result"] == "pass_weight"
        kimi_pass = kimi is not None and kimi["result"] == "pass_weight"
        row = {
            "epoch": candidate["epoch"],
            "participant": candidate["participant"],
            "poc_start_height": tl["poc_start_height"],
            "cpoc_sequence": tl["cpoc_sequence"],
            "event_trigger_height": candidate["event_trigger_height"],
            "exclusion_height": candidate["exclusion_height"],
            "pass_models": pass_models,
            "qwen_evidence": compact_model(qwen),
            "kimi_evidence": compact_model(kimi),
            "qwen_pass_weight": qwen_pass,
            "kimi_pass_weight": kimi_pass,
            "stored_ratio_percent": percent_from_ratio(old["stored_confirmation_ratio"]),
            "old_formula_ratio_percent": percent_from_ratio(old["old_formula_ratio"]),
            "old_formula_diff": old["old_formula_diff"],
            "old_formula_matches_stored": old["old_formula_matches_stored"],
            "new_algorithm_ratio_percent": percent_from_ratio(new["new_algorithm_ratio"]),
            "new_algorithm_would_pass_alpha": new["new_algorithm_would_pass_alpha"],
            "loss_gonka": candidate["loss_gonka"],
            "loss_gonka_display": amount(candidate["loss_gonka"]),
            "technical_status": elig["technical_status"],
            "overlap_status": ov["overlap_status"],
            "recommended_action": ov["recommended_action"],
            "decision_boundary": action_label(elig, ov),
            "evidence_summary": (
                f"{pass_models} reached strict >2/3 cPoC validation; "
                f"stored ratio {percent_from_ratio(old['stored_confirmation_ratio'])}; "
                f"old replay match {bool_text(old['old_formula_matches_stored'])}; "
                f"bounded v0.2.13-style pass {bool_text(new['new_algorithm_would_pass_alpha'])}."
            ),
        }
        rows.append(row)
    return rows


def write_md(path: Path, rows: list[dict[str, Any]]) -> None:
    total_loss = sum(Decimal(row["loss_gonka"]) for row in rows)
    technical_counts = Counter(row["technical_status"] for row in rows)
    overlap_counts = Counter(row["overlap_status"] for row in rows)
    action_counts = Counter(row["recommended_action"] for row in rows)
    old_matches = sum(1 for row in rows if row["old_formula_matches_stored"] == "True")
    new_passes = sum(1 for row in rows if row["new_algorithm_would_pass_alpha"] == "True")

    lines = [
        "# P3-CAND-06 Evidence Ledger",
        "",
        "This ledger is the row-by-row audit surface for P3-CAND-06. It combines",
        "`candidate_rows.csv`, raw cPoC submission/validator evidence, old-formula",
        "replay, bounded v0.2.13-style replay, eligibility status, and overlap",
        "status. It does not approve payouts.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Candidate rows | `{len(rows)}` |",
        f"| Estimated zero-reward loss | `{amount(total_loss)} GONKA` |",
        f"| Old-formula replay matches stored ratio | `{old_matches}` |",
        f"| Bounded v0.2.13-style rows passing alpha | `{new_passes}` |",
        "",
        "## Technical Status",
        "",
        "| Status | Rows |",
        "|---|---:|",
    ]
    for status, count in sorted(technical_counts.items()):
        lines.append(f"| `{status}` | `{count}` |")

    lines.extend(["", "## Overlap Status", "", "| Status | Rows |", "|---|---:|"])
    for status, count in sorted(overlap_counts.items()):
        lines.append(f"| `{status}` | `{count}` |")

    lines.extend(["", "## Recommended Action", "", "| Action | Rows |", "|---|---:|"])
    for action, count in sorted(action_counts.items()):
        lines.append(f"| `{action}` | `{count}` |")

    lines.extend(
        [
            "",
            "## Row Ledger",
            "",
            "| Epoch | Participant | Trigger -> Exclusion | Pass model(s) | Qwen evidence | Kimi evidence | Stored ratio | Old replay | New-style pass | Loss, GNK | Decision boundary |",
            "|---:|---|---|---|---|---|---:|---|---|---:|---|",
        ]
    )
    for row in rows:
        lines.append(
            "| {epoch} | `{participant}` | `{event_trigger_height}` -> `{exclusion_height}` | "
            "{pass_models} | {qwen_evidence} | {kimi_evidence} | {stored_ratio_percent} | "
            "{old_formula_ratio_percent}; match `{old_formula_matches_stored}` | "
            "`{new_algorithm_would_pass_alpha}` | {loss_gonka_display} | `{decision_boundary}` |".format(**row)
        )

    lines.extend(
        [
            "",
            "## How To Read This",
            "",
            "- `pass_weight` means the model had strict validator weight above",
            "  `TotalNetworkWeight * 2 / 3` for the cPoC stage.",
            "- `old replay match True` means the pre-fix chain accounting formula",
            "  reproduces the stored confirmation ratio for that row.",
            "- `New-style pass False` means the bounded replay using the available",
            "  Qwen/Kimi evidence does not by itself make the row pass alpha.",
            "- `blocked` rows must be resolved against P3-CAND-04 before payout.",
            "- `review` rows need duplicate-payment comparison against P4-CAND-01.",
            "- `policy` rows are technically reproducible, but payout depends on",
            "  whether single-model pass rows are compensable.",
            "",
            "Machine-readable versions are in `case6_evidence_ledger.csv` and",
            "`case6_evidence_ledger.json`.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_decision_summary(path: Path, rows: list[dict[str, Any]]) -> None:
    total_loss = sum(Decimal(row["loss_gonka"]) for row in rows)
    technical_counts = Counter(row["technical_status"] for row in rows)
    action_counts = Counter(row["recommended_action"] for row in rows)
    overlap_counts = Counter(row["overlap_status"] for row in rows)
    old_matches = sum(1 for row in rows if row["old_formula_matches_stored"] == "True")
    new_passes = sum(1 for row in rows if row["new_algorithm_would_pass_alpha"] == "True")
    clear_loss = sum(Decimal(row["loss_gonka"]) for row in rows if row["recommended_action"] == "clear")
    review_loss = sum(Decimal(row["loss_gonka"]) for row in rows if row["recommended_action"] == "review")
    blocked_loss = sum(Decimal(row["loss_gonka"]) for row in rows if row["recommended_action"] == "blocked")

    lines = [
        "# P3-CAND-06 Decision Summary",
        "",
        "P3-CAND-06 is a candidate set for pre-fix confirmation-accounting losses.",
        "The rows were found independently from archive-chain data. The common",
        "shape is: the participant received zero reward after",
        "`failed_confirmation_poc`, while at least one submitted Qwen/Kimi model",
        "had strict cPoC validator weight above the chain's `2/3` threshold.",
        "",
        "## Current Conclusion",
        "",
        "The technical evidence supports a pre-`v0.2.13` confirmation-accounting",
        "mismatch as the root-cause family. It does not prove that all rows should",
        "be paid automatically.",
        "",
        "| Check | Result |",
        "|---|---:|",
        f"| Candidate rows | `{len(rows)}` |",
        f"| Unique participants | `{len({row['participant'] for row in rows})}` |",
        f"| Estimated zero-reward loss | `{amount(total_loss)} GONKA` |",
        f"| Old-formula replay matches stored ratio | `{old_matches}` |",
        f"| Bounded v0.2.13-style rows passing alpha | `{new_passes}` |",
        f"| Formula-reconciled rows needing policy decision | `{technical_counts['formula_reconciled_policy_required']}` |",
        f"| Epoch-276 rows blocked by overlap | `{technical_counts['blocked_epoch276_overlap']}` |",
        "",
        "## What Is Proven",
        "",
        "- For every row, at least one Qwen/Kimi model had cPoC evidence that reached",
        "  strict `pass_weight`.",
        "- The evidence includes chain cPoC store commits/root hashes, validation",
        "  rows, validator counts, and valid validator voting weight.",
        "- The full pre-fix formula replay matches stored confirmation ratios for",
        f"  `{old_matches}` of `{len(rows)}` rows.",
        "- The two old-formula non-matches are both in epoch `276`, which is already",
        "  blocked for overlap review.",
        "- The fix family is `v0.2.13` / PR `#1143`, where the chain added a stable",
        "  confirmation-weight snapshot and reused it across confirmation and reward",
        "  calculations.",
        "",
        "## What Is Not Proven",
        "",
        "- The available raw endpoints do not expose every off-chain nonce/payload",
        "  body; the proof is at chain commit and validator-row level.",
        "- The bounded v0.2.13-style replay does not make any of these rows pass",
        "  alpha automatically, so single-model compensation remains a committee",
        "  policy decision.",
        "- Epoch `276` rows cannot be paid from this case until P3-CAND-04 duplicate",
        "  risk is resolved.",
        "",
        "## Action Split",
        "",
        "| Action | Rows | Loss, GNK | Meaning |",
        "|---|---:|---:|---|",
        f"| `clear` | `{action_counts['clear']}` | `{amount(clear_loss)}` | No local overlap signal; still needs single-model policy decision. |",
        f"| `review` | `{action_counts['review']}` | `{amount(review_loss)}` | Compare against P4-CAND-01 before payout. |",
        f"| `blocked` | `{action_counts['blocked']}` | `{amount(blocked_loss)}` | Resolve P3-CAND-04 duplicate risk first. |",
        "",
        "For a full calculation that includes all rows before overlap filtering, see",
        "`case6_gross_compensation_calculation.md`.",
        "",
        "## Overlap Split",
        "",
        "| Overlap status | Rows |",
        "|---|---:|",
    ]
    for status, count in sorted(overlap_counts.items()):
        lines.append(f"| `{status}` | `{count}` |")

    lines.extend(
        [
            "",
            "## Recommended Reading Order",
            "",
            "1. `case6_decision_summary.md` for the one-page conclusion.",
            "2. `case6_evidence_ledger.md` for row-by-row evidence.",
            "3. `case6_gross_compensation_calculation.md` for the all-row gross table.",
            "4. `case6_full_old_formula_replay.md` for formula reconciliation.",
            "5. `case6_new_algorithm_replay.md` for the bounded post-fix counterfactual.",
            "6. `case6_overlap_matrix.md` before any payout decision.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = build_rows()
    fieldnames = [
        "epoch",
        "participant",
        "poc_start_height",
        "cpoc_sequence",
        "event_trigger_height",
        "exclusion_height",
        "pass_models",
        "qwen_evidence",
        "kimi_evidence",
        "qwen_pass_weight",
        "kimi_pass_weight",
        "stored_ratio_percent",
        "old_formula_ratio_percent",
        "old_formula_diff",
        "old_formula_matches_stored",
        "new_algorithm_ratio_percent",
        "new_algorithm_would_pass_alpha",
        "loss_gonka",
        "technical_status",
        "overlap_status",
        "recommended_action",
        "decision_boundary",
        "evidence_summary",
    ]
    write_csv(CASE_DIR / "case6_evidence_ledger.csv", rows, fieldnames)
    write_json(CASE_DIR / "case6_evidence_ledger.json", {"rows": rows})
    write_md(CASE_DIR / "case6_evidence_ledger.md", rows)
    write_decision_summary(CASE_DIR / "case6_decision_summary.md", rows)
    print(
        json.dumps(
            {
                "rows": len(rows),
                "old_formula_matches": sum(1 for row in rows if row["old_formula_matches_stored"] == "True"),
                "new_algorithm_passes": sum(
                    1 for row in rows if row["new_algorithm_would_pass_alpha"] == "True"
                ),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
