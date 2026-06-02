#!/usr/bin/env python3
"""Build a participant-grouped cPoC timeline for P3-CAND-06.

The source candidate set is intentionally narrow: the 24 rows already selected
in candidate_rows.csv. For each row this script expands the epoch from PoC
start, through every cPoC before the next epoch boundary, and then adds the
next epoch PoC baseline so weight restoration is visible.
"""

from __future__ import annotations

import csv
import datetime as dt
import importlib.util
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
CASE_DIR = Path(__file__).resolve().parent
CASE3_DIR = REPO_ROOT / "validations" / "P3-CAND-03-failed-cpoc-epoch-267"
SCAN_SCRIPT = CASE3_DIR / "scan_neighbor_epochs.py"
CACHE_DIR = Path("/tmp/grc3-case3-neighbor-scan")


def load_scan_module() -> Any:
    spec = importlib.util.spec_from_file_location("case3_scan", SCAN_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {SCAN_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scan = load_scan_module()
QWEN = scan.QWEN
KIMI = scan.KIMI
MODELS = [QWEN, KIMI]
MODEL_LABEL = {QWEN: "Qwen", KIMI: "Kimi"}


def fmt_int(value: Any) -> str:
    if value in ("", None):
        return ""
    return f"{int(value):,}"


def fmt_height(value: Any) -> str:
    if value in ("", None):
        return ""
    return f"`{fmt_int(value)}`"


def fmt_weight(value: Any) -> str:
    if value in ("", None):
        return ""
    return f"`{fmt_int(value)}`"


def fmt_delta(value: Any) -> str:
    if value in ("", None):
        return ""
    value = int(value)
    if value > 0:
        return f"`+{fmt_int(value)}`"
    return f"`{fmt_int(value)}`"


def fmt_percent_from_ratio(value: str | int | float) -> str:
    try:
        return f"{float(value):.4f}%"
    except (TypeError, ValueError):
        return ""


def model_cell(row: dict[str, Any], prefix: str) -> str:
    if row.get("row_type") in {"poc_baseline", "next_epoch_poc"}:
        result = row.get(f"{prefix}_poc_result")
        if result == "not_in_epoch_group":
            return "not in epoch group"
        if result != "in_epoch_group":
            return ""
        parts = [
            f"PoC weight {fmt_int(row.get(f'{prefix}_poc_weight'))}",
            f"voting {fmt_int(row.get(f'{prefix}_poc_voting_power'))}",
            f"CW {fmt_int(row.get(f'{prefix}_poc_confirmation_weight'))}",
        ]
        nodes = row.get(f"{prefix}_poc_nodes")
        if nodes:
            parts.append(f"nodes {nodes}")
        return "; ".join(parts)
    if not row.get(f"{prefix}_result"):
        return ""
    submitted = int(row[f"{prefix}_submitted_count"])
    valid = int(row[f"{prefix}_valid_weight"])
    percent = row[f"{prefix}_valid_weight_percent"]
    result = row[f"{prefix}_result"]
    return f"{result}; sub {fmt_int(submitted)}; valid {fmt_int(valid)} ({percent}%)"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def block_time(base: str, height: int) -> tuple[str, str]:
    payload = scan.get_json(
        base,
        f"/cosmos/base/tendermint/v1beta1/blocks/{height}",
        CACHE_DIR,
        refresh=False,
    )
    raw = payload["block"]["header"]["time"]
    utc = dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
    msk = utc.astimezone(dt.timezone(dt.timedelta(hours=3)))
    return (
        utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
        msk.strftime("%Y-%m-%d %H:%M:%S MSK"),
    )


def row_key(row: dict[str, str]) -> tuple[int, str, int]:
    return (int(row["epoch"]), row["participant"], int(row["event_trigger_height"]))


def build_rows() -> list[dict[str, Any]]:
    scan.load_dotenv(REPO_ROOT / ".env")
    base = scan.direct_lcd_from_env()

    candidate_keys = {
        (int(row["epoch"]), row["participant"], int(row["event_trigger_height"]))
        for row in read_csv(CASE_DIR / "candidate_rows.csv")
    }
    failed_rows = [
        row
        for row in read_csv(CASE3_DIR / "case3_neighbor_failed_cpoc_rows.csv")
        if row_key(row) in candidate_keys
    ]
    failed_by_key = {row_key(row): row for row in failed_rows}

    rows: list[dict[str, Any]] = []
    epoch_cache: dict[int, dict[str, Any]] = {}
    stage_cache: dict[int, Any] = {}
    group_cache: dict[tuple[int, int], dict[str, Any]] = {}

    def epoch_data(epoch: int) -> dict[str, Any]:
        if epoch in epoch_cache:
            return epoch_cache[epoch]
        root_group = scan.get_epoch_group(base, CACHE_DIR, epoch, None, False)
        model_groups = {model: scan.get_epoch_group(base, CACHE_DIR, epoch, model, False) for model in MODELS}
        events = scan.get_json(
            base,
            f"/productscience/inference/inference/confirmation_poc_events/{epoch}",
            CACHE_DIR,
            refresh=False,
        )["events"]
        events = sorted(events, key=lambda item: int(item["event_sequence"]))
        model_votes = {model: scan.model_voting_power(group) for model, group in model_groups.items()}
        next_epoch_group = scan.get_epoch_group(base, CACHE_DIR, epoch + 1, None, False)
        next_epoch_model_groups = {
            model: scan.get_epoch_group(base, CACHE_DIR, epoch + 1, model, False) for model in MODELS
        }
        epoch_cache[epoch] = {
            "root_group": root_group,
            "root_weights": scan.root_weight_map(root_group),
            "total_network_weight": int(root_group["total_weight"]),
            "events": events,
            "model_groups": model_groups,
            "model_votes": model_votes,
            "poc_start": int(root_group["poc_start_block_height"]),
            "effective_start": int(root_group["effective_block_height"]),
            "next_epoch_height": int(next_epoch_group["poc_start_block_height"]),
            "next_epoch_root_weights": scan.root_weight_map(next_epoch_group),
            "next_epoch_total_network_weight": int(next_epoch_group["total_weight"]),
            "next_epoch_model_groups": next_epoch_model_groups,
        }
        return epoch_cache[epoch]

    def model_poc_fields(data: dict[str, Any], participant: str, prefix: str, model: str, *, next_epoch: bool = False) -> dict[str, Any]:
        groups_key = "next_epoch_model_groups" if next_epoch else "model_groups"
        group = data[groups_key][model]
        for item in group.get("validation_weights") or []:
            if item.get("member_address") != participant:
                continue
            nodes = item.get("ml_nodes") or []
            return {
                f"{prefix}_poc_result": "in_epoch_group",
                f"{prefix}_poc_weight": item.get("weight", ""),
                f"{prefix}_poc_voting_power": item.get("voting_power", ""),
                f"{prefix}_poc_confirmation_weight": item.get("confirmation_weight", ""),
                f"{prefix}_poc_nodes": ";".join(
                    f"{node.get('node_id')}:{node.get('poc_weight') or node.get('weight') or ''}" for node in nodes
                ),
            }
        return {
            f"{prefix}_poc_result": "not_in_epoch_group",
            f"{prefix}_poc_weight": "",
            f"{prefix}_poc_voting_power": "",
            f"{prefix}_poc_confirmation_weight": "",
            f"{prefix}_poc_nodes": "",
        }

    def group_at(epoch: int, height: int) -> dict[str, Any]:
        key = (epoch, height)
        if key not in group_cache:
            group_cache[key] = scan.get_epoch_group(base, CACHE_DIR, epoch, None, False, height=height)
        return group_cache[key]

    def stage(trigger_height: int) -> Any:
        if trigger_height not in stage_cache:
            stage_cache[trigger_height] = scan.load_stage(base, CACHE_DIR, trigger_height, False)
        return stage_cache[trigger_height]

    for key in sorted(failed_by_key):
        epoch, participant, failed_trigger = key
        failed = failed_by_key[key]
        data = epoch_data(epoch)
        root_weight = int(failed["root_weight"])
        failed_sequence = int(failed["event_sequence"])
        exclusion_height = int(failed["exclusion_height"])
        poc_utc, poc_msk = block_time(base, data["poc_start"])

        poc_row = {
                "participant": participant,
                "epoch": epoch,
                "event_epoch": epoch,
                "row_order": 0,
                "row_type": "poc_baseline",
                "event_label": "PoC",
                "poc_start_height": data["poc_start"],
                "poc_start_utc": poc_utc,
                "poc_start_msk": poc_msk,
                "effective_start_height": data["effective_start"],
                "next_epoch_height": data["next_epoch_height"],
                "total_network_weight": data["total_network_weight"],
                "two_thirds_min_weight": data["total_network_weight"] * 2 // 3 + 1,
                "root_weight_at_poc": root_weight,
                "cpoc_sequence": "",
                "cpoc_trigger_height": "",
                "cpoc_trigger_utc": "",
                "cpoc_trigger_msk": "",
                "snapshot_height": data["poc_start"],
                "snapshot_utc": poc_utc,
                "snapshot_msk": poc_msk,
                "confirmation_weight_before": "",
                "confirmation_weight_after": "",
                "confirmation_weight_delta": "",
                "confirmation_weight_after_pct_of_root": "",
                "qwen_submitted_count": "",
                "qwen_valid_weight": "",
                "qwen_valid_weight_percent": "",
                "qwen_result": "",
                "kimi_submitted_count": "",
                "kimi_valid_weight": "",
                "kimi_valid_weight_percent": "",
                "kimi_result": "",
                "event_status": "poc_baseline",
                "exclusion_height": "",
                "blocks_to_next_epoch_from_snapshot": data["next_epoch_height"] - data["poc_start"],
                "loss_gonka": "",
                "note": "epoch PoC baseline before any confirmation PoC event",
            }
        poc_row.update(model_poc_fields(data, participant, "qwen", QWEN))
        poc_row.update(model_poc_fields(data, participant, "kimi", KIMI))
        rows.append(poc_row)

        events = data["events"]
        for index, event in enumerate(events):
            sequence = int(event["event_sequence"])
            trigger_height = int(event["trigger_height"])
            is_failure = trigger_height == failed_trigger
            is_after_failure = sequence > failed_sequence
            if is_failure:
                before_height = exclusion_height - 1
                after_height = exclusion_height
            else:
                next_trigger_height = (
                    int(events[index + 1]["trigger_height"]) if index + 1 < len(events) else data["next_epoch_height"]
                )
                before_height = max(data["poc_start"], trigger_height - 1)
                after_height = next_trigger_height - 1

            before_group = group_at(epoch, before_height)
            after_group = group_at(epoch, after_height)
            before_weight = scan.confirmation_weight_for(before_group, participant)
            after_weight = scan.confirmation_weight_for(after_group, participant)
            delta = after_weight - before_weight
            trigger_utc, trigger_msk = block_time(base, trigger_height)
            after_utc, after_msk = block_time(base, after_height)
            commits_by_key, validations_by_key = stage(trigger_height)
            model_results = {
                model: scan.classify_model(
                    participant,
                    model,
                    data["total_network_weight"],
                    data["model_votes"][model],
                    commits_by_key,
                    validations_by_key,
                )
                for model in MODELS
            }
            ratio_vs_root = "" if root_weight == 0 else f"{after_weight * 100 / root_weight:.4f}"
            if is_failure:
                status = "lost_at_failed_confirmation_poc"
                note = "confirmation weight drops below alpha and participant is excluded"
            elif is_after_failure:
                status = "after_loss_until_next_epoch"
                note = "participant already lost in this epoch; row kept to show no same-epoch restoration"
            elif delta < 0:
                status = "reduced_before_failure"
                note = "confirmation weight already reduced before the later exclusion"
            else:
                status = "kept_before_next_cpoc"
                note = "participant remains active before the next cPoC"

            rows.append(
                {
                    "participant": participant,
                    "epoch": epoch,
                    "event_epoch": epoch,
                    "row_order": sequence + 1,
                    "row_type": "cpoc",
                    "event_label": f"cPoC #{sequence}",
                    "poc_start_height": data["poc_start"],
                    "poc_start_utc": poc_utc,
                    "poc_start_msk": poc_msk,
                    "effective_start_height": data["effective_start"],
                    "next_epoch_height": data["next_epoch_height"],
                    "total_network_weight": data["total_network_weight"],
                    "two_thirds_min_weight": data["total_network_weight"] * 2 // 3 + 1,
                    "root_weight_at_poc": root_weight,
                    "cpoc_sequence": sequence,
                    "cpoc_trigger_height": trigger_height,
                    "cpoc_trigger_utc": trigger_utc,
                    "cpoc_trigger_msk": trigger_msk,
                    "snapshot_height": after_height,
                    "snapshot_utc": after_utc,
                    "snapshot_msk": after_msk,
                    "confirmation_weight_before": before_weight,
                    "confirmation_weight_after": after_weight,
                    "confirmation_weight_delta": delta,
                    "confirmation_weight_after_pct_of_root": ratio_vs_root,
                    "qwen_submitted_count": model_results[QWEN]["submitted_count"],
                    "qwen_valid_weight": model_results[QWEN]["valid_weight"],
                    "qwen_valid_weight_percent": model_results[QWEN]["valid_weight_percent"],
                    "qwen_result": model_results[QWEN]["result"],
                    "kimi_submitted_count": model_results[KIMI]["submitted_count"],
                    "kimi_valid_weight": model_results[KIMI]["valid_weight"],
                    "kimi_valid_weight_percent": model_results[KIMI]["valid_weight_percent"],
                    "kimi_result": model_results[KIMI]["result"],
                    "event_status": status,
                    "exclusion_height": exclusion_height if is_failure else "",
                    "blocks_to_next_epoch_from_snapshot": data["next_epoch_height"] - after_height,
                    "loss_gonka": failed["loss_gonka"] if is_failure else "",
                    "note": note,
                }
            )
        next_poc_utc, next_poc_msk = block_time(base, data["next_epoch_height"])
        next_root_weights = data["next_epoch_root_weights"]
        next_root_weight = next_root_weights.get(participant, 0)
        next_network_weight = data["next_epoch_total_network_weight"]
        next_poc_row = {
                "participant": participant,
                "epoch": epoch,
                "event_epoch": epoch + 1,
                "row_order": len(events) + 1,
                "row_type": "next_epoch_poc",
                "event_label": f"PoC epoch {epoch + 1}",
                "poc_start_height": data["poc_start"],
                "poc_start_utc": poc_utc,
                "poc_start_msk": poc_msk,
                "effective_start_height": data["effective_start"],
                "next_epoch_height": data["next_epoch_height"],
                "total_network_weight": next_network_weight,
                "two_thirds_min_weight": next_network_weight * 2 // 3 + 1,
                "root_weight_at_poc": next_root_weight,
                "cpoc_sequence": "",
                "cpoc_trigger_height": "",
                "cpoc_trigger_utc": "",
                "cpoc_trigger_msk": "",
                "snapshot_height": data["next_epoch_height"],
                "snapshot_utc": next_poc_utc,
                "snapshot_msk": next_poc_msk,
                "confirmation_weight_before": "",
                "confirmation_weight_after": "",
                "confirmation_weight_delta": "",
                "confirmation_weight_after_pct_of_root": "",
                "qwen_submitted_count": "",
                "qwen_valid_weight": "",
                "qwen_valid_weight_percent": "",
                "qwen_result": "",
                "kimi_submitted_count": "",
                "kimi_valid_weight": "",
                "kimi_valid_weight_percent": "",
                "kimi_result": "",
                "event_status": "next_epoch_poc",
                "exclusion_height": "",
                "blocks_to_next_epoch_from_snapshot": 0,
                "loss_gonka": "",
                "note": "next epoch PoC baseline; use this to see whether participant weight restored",
            }
        next_poc_row.update(model_poc_fields(data, participant, "qwen", QWEN, next_epoch=True))
        next_poc_row.update(model_poc_fields(data, participant, "kimi", KIMI, next_epoch=True))
        rows.append(next_poc_row)
    return rows


def write_markdown(path: Path, rows: list[dict[str, Any]]) -> None:
    participants: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        participants.setdefault(row["participant"], []).append(row)

    lines = [
        "# P3-CAND-06 Grouped cPoC Timeline",
        "",
        "This view groups the candidate timeline by participant, then by epoch, then by cPoC event.",
        "It is meant to show where confirmation weight was still preserved and where it was lost.",
        "",
        "Time columns are derived from Tendermint block header time. MSK is UTC+03:00.",
        "",
        "Column notes:",
        "",
        "- Each participant/epoch section starts with the epoch PoC baseline and ends with the next epoch PoC baseline.",
        "- `PoC weight` is the participant root weight for that row's event epoch.",
        "- For PoC baseline rows, `Qwen` and `Kimi` show model-level PoC weight, voting power, confirmation weight, and node ids.",
        "- For cPoC rows, `Qwen` and `Kimi` show submitted nonce count, validating weight, and validation result.",
        "- `CW before -> after` is root confirmation weight before the cPoC effect and at the post-cPoC snapshot.",
        "- `CW before -> after` is intentionally blank for PoC baseline rows; those rows show PoC model membership instead.",
        "- For non-failing cPoC rows, the post-cPoC snapshot is the block before the next cPoC trigger.",
        "- For the failing cPoC row, the post-cPoC snapshot is the exclusion block.",
        "- For cPoC rows after `LOST`, the post-cPoC snapshot continues to the next cPoC or the next epoch PoC.",
        "- `2/3 min` is computed from the root/network total weight for that epoch, matching the chain validation threshold convention.",
        "",
        "## Participants",
        "",
    ]

    for participant in sorted(participants):
        participant_rows = sorted(participants[participant], key=lambda row: (int(row["epoch"]), int(row["row_order"])))
        total_loss = sum(float(row["loss_gonka"] or 0) for row in participant_rows)
        epochs = sorted({int(row["epoch"]) for row in participant_rows})
        lines.extend(
            [
                f"### `{participant}`",
                "",
                f"Candidate epochs: `{', '.join(str(epoch) for epoch in epochs)}`. Candidate loss sum: `{total_loss:.9f}` GONKA.",
                "",
            ]
        )
        for epoch in epochs:
            epoch_rows = [row for row in participant_rows if int(row["epoch"]) == epoch]
            first = epoch_rows[0]
            failing = [row for row in epoch_rows if row["event_status"] == "lost_at_failed_confirmation_poc"][0]
            lines.extend(
                [
                    f"#### Epoch `{epoch}`",
                    "",
                    "| Metric | Value |",
                    "|---|---:|",
                    f"| PoC start | {fmt_height(first['poc_start_height'])} / `{first['poc_start_msk']}` |",
                    f"| Epoch effective start | {fmt_height(first['effective_start_height'])} |",
                    f"| Next epoch PoC start | {fmt_height(first['next_epoch_height'])} |",
                    f"| Total network weight | {fmt_weight(first['total_network_weight'])} |",
                    f"| `>2/3` minimum validating weight | {fmt_weight(first['two_thirds_min_weight'])} |",
                    f"| Participant PoC weight | {fmt_weight(first['root_weight_at_poc'])} |",
                    f"| Exclusion | cPoC `#{failing['cpoc_sequence']}` at {fmt_height(failing['exclusion_height'])} / `{failing['snapshot_msk']}` |",
                    f"| Blocks left to next epoch after loss | `{fmt_int(failing['blocks_to_next_epoch_from_snapshot'])}` |",
                    f"| Candidate loss | `{failing['loss_gonka']}` GONKA |",
                    "",
                    "| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |",
                    "|---:|---|---|---:|---|---|---:|---:|---:|---|",
                ]
            )
            for row in epoch_rows:
                status_by_event = {
                    "poc_baseline": "PoC",
                    "kept_before_next_cpoc": "kept",
                    "reduced_before_failure": "reduced",
                    "lost_at_failed_confirmation_poc": "LOST",
                    "after_loss_until_next_epoch": "after loss",
                    "next_epoch_poc": "next PoC",
                }
                status = status_by_event.get(row["event_status"], row["event_status"])
                trigger_display = (
                    f"{fmt_height(row['cpoc_trigger_height'])} / `{row['cpoc_trigger_msk']}`"
                    if row["cpoc_trigger_height"] not in ("", None)
                    else ""
                )
                after_pct = fmt_percent_from_ratio(row["confirmation_weight_after_pct_of_root"])
                after_pct_display = f"`{after_pct}`" if after_pct else ""
                lines.append(
                    "| `{event_label}` | {trigger} | {snapshot} / `{snapshot_msk}` | {poc_weight} | {qwen} | {kimi} | {before_after} | {delta} | {after_pct} | {status} |".format(
                        event_label=row["event_label"],
                        trigger=trigger_display,
                        snapshot=fmt_height(row["snapshot_height"]),
                        snapshot_msk=row["snapshot_msk"],
                        poc_weight=fmt_weight(row["root_weight_at_poc"]),
                        qwen=model_cell(row, "qwen"),
                        kimi=model_cell(row, "kimi"),
                        before_after=(
                            f"{fmt_weight(row['confirmation_weight_before'])} -> {fmt_weight(row['confirmation_weight_after'])}"
                            if row["confirmation_weight_before"] not in ("", None)
                            else fmt_weight(row["confirmation_weight_after"])
                        ),
                        delta=fmt_delta(row["confirmation_weight_delta"]),
                        after_pct=after_pct_display,
                        status=status,
                    )
                )
            lines.extend(
                [
                    "",
                    f"Loss point: at cPoC `#{failing['cpoc_sequence']}` confirmation weight moves from "
                    f"{fmt_weight(failing['confirmation_weight_before'])} to {fmt_weight(failing['confirmation_weight_after'])}; "
                    f"this is the row where the participant becomes a candidate for lost reward accounting.",
                    "",
                ]
            )

    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    rows = build_rows()
    fieldnames = [
        "participant",
        "epoch",
        "event_epoch",
        "row_order",
        "row_type",
        "event_label",
        "poc_start_height",
        "poc_start_utc",
        "poc_start_msk",
        "effective_start_height",
        "next_epoch_height",
        "total_network_weight",
        "two_thirds_min_weight",
        "root_weight_at_poc",
        "cpoc_sequence",
        "cpoc_trigger_height",
        "cpoc_trigger_utc",
        "cpoc_trigger_msk",
        "snapshot_height",
        "snapshot_utc",
        "snapshot_msk",
        "confirmation_weight_before",
        "confirmation_weight_after",
        "confirmation_weight_delta",
        "confirmation_weight_after_pct_of_root",
        "qwen_submitted_count",
        "qwen_valid_weight",
        "qwen_valid_weight_percent",
        "qwen_result",
        "qwen_poc_result",
        "qwen_poc_weight",
        "qwen_poc_voting_power",
        "qwen_poc_confirmation_weight",
        "qwen_poc_nodes",
        "kimi_submitted_count",
        "kimi_valid_weight",
        "kimi_valid_weight_percent",
        "kimi_result",
        "kimi_poc_result",
        "kimi_poc_weight",
        "kimi_poc_voting_power",
        "kimi_poc_confirmation_weight",
        "kimi_poc_nodes",
        "event_status",
        "exclusion_height",
        "blocks_to_next_epoch_from_snapshot",
        "loss_gonka",
        "note",
    ]
    write_csv(CASE_DIR / "participant_grouped_cpoc_timeline.csv", rows, fieldnames)
    write_markdown(CASE_DIR / "participant_grouped_cpoc_timeline.md", rows)
    print(json.dumps({"rows": len(rows), "participants": len({row["participant"] for row in rows})}, sort_keys=True))


if __name__ == "__main__":
    main()
