#!/usr/bin/env python3
"""Scan epochs around Case 3 for the same failed-cPoC signature.

The scan is intentionally independent from the published Case 3 repository.
It uses archive LCD state directly and writes only normalized artifacts.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from decimal import Decimal, ROUND_DOWN, getcontext
from pathlib import Path
from typing import Any


CASE_EPOCH = 267
DEFAULT_EPOCHS_BEFORE = 5
DEFAULT_EPOCHS_AFTER = 5
DEFAULT_WORKDIR = Path("/tmp/grc3-case3-neighbor-scan")
DEFAULT_ARTIFACT_DIR = Path("validations/P3-CAND-03-failed-cpoc-epoch-267")
REQUEST_TIMEOUT_SECONDS = 60
RETRIES = 6

KIMI = "moonshotai/Kimi-K2.6"
QWEN = "Qwen/Qwen3-235B-A22B-Instruct-2507-FP8"
MODELS = [QWEN, KIMI]


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def direct_lcd_from_env() -> str:
    raw = os.environ.get("GONKA_RPC_LCD_URL") or os.environ.get("GONKA_RPC_URL")
    if not raw:
        raise SystemExit("Set GONKA_RPC_URL or GONKA_RPC_LCD_URL in .env")
    raw = raw.strip().rstrip("/")
    parsed = urllib.parse.urlparse(raw if "://" in raw else "dummy://" + raw)
    if not parsed.hostname:
        raise SystemExit("Could not parse GONKA_RPC_URL host")
    if os.environ.get("GONKA_RPC_LCD_URL"):
        return raw if "://" in raw else "http://" + raw
    return f"http://{parsed.hostname}:1317"


def request_headers() -> dict[str, str]:
    headers = {"User-Agent": "grc-case3-neighbor-scan/1.0"}
    api_key = os.environ.get("GONKA_RPC_API_KEY")
    if api_key:
        headers["X-Api-Key"] = api_key
    return headers


def path_cache_name(path: str) -> str:
    digest = hashlib.sha256(path.encode("utf-8")).hexdigest()[:16]
    safe = path.strip("/").replace("/", "_").replace("?", "__")
    safe = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in safe)
    return f"{safe}.{digest}.json"


def get_json(base: str, path: str, workdir: Path, *, refresh: bool = False, height: int | None = None) -> Any:
    workdir.mkdir(parents=True, exist_ok=True)
    cache_key = path if height is None else f"{path}@height={height}"
    cache_path = workdir / path_cache_name(cache_key)
    if cache_path.exists() and not refresh:
        return json.loads(cache_path.read_text(encoding="utf-8"))

    url = base.rstrip("/") + path
    last_error = None
    for attempt in range(RETRIES):
        headers = request_headers()
        if height is not None:
            headers["x-cosmos-block-height"] = str(height)
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            cache_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
                encoding="utf-8",
            )
            return payload
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")
            last_error = f"HTTP {exc.code}: {body[:300]}"
        except Exception as exc:  # noqa: BLE001 - audit tool should retry broadly
            last_error = str(exc)
        time.sleep(min(20, 1 + attempt * 2))
    raise RuntimeError(f"Failed to fetch {path}: {last_error}")


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def int_of(value: Any, default: int = 0) -> int:
    if value is None or value == "":
        return default
    return int(value)


def decimal_from_chain(value: dict[str, Any] | None) -> Decimal | None:
    if not value:
        return None
    return Decimal(str(value["value"])) * (Decimal(10) ** int(value["exponent"]))


def decimal_to_string(value: dict[str, Any] | None) -> str:
    decimal_value = decimal_from_chain(value)
    return "" if decimal_value is None else format(decimal_value, "f")


def percent(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return ""
    return f"{(Decimal(numerator) * Decimal(100) / Decimal(denominator)):.4f}"


def decimal_percent(value: dict[str, Any] | None) -> str:
    decimal_value = decimal_from_chain(value)
    if decimal_value is None:
        return ""
    return f"{(decimal_value * Decimal(100)):.4f}"


def fixed_epoch_reward_ngonka(params: dict[str, Any], epoch: int) -> int:
    getcontext().prec = 100
    bitcoin = params["bitcoin_reward_params"]
    initial = Decimal(int(bitcoin["initial_epoch_reward"]))
    genesis_epoch = int(bitcoin["genesis_epoch"])
    decay_rate = decimal_from_chain(bitcoin["decay_rate"])
    if decay_rate == Decimal("-0.000475"):
        exponent = Decimal("0.9995251127946402")
    elif decay_rate == Decimal("-0.000001"):
        exponent = Decimal("0.9999990000005")
    elif decay_rate == Decimal("0.0001"):
        exponent = Decimal("1.0001000050001667")
    elif decay_rate == Decimal("0"):
        exponent = Decimal("1")
    else:
        exponent = decay_rate.exp()
    epochs_since_genesis = epoch - genesis_epoch
    if epochs_since_genesis <= 0:
        return int(initial)
    return int((initial * (exponent ** epochs_since_genesis)).to_integral_value(rounding=ROUND_DOWN))


def get_epoch_group(
    base: str,
    workdir: Path,
    epoch: int,
    model_id: str | None,
    refresh: bool,
    *,
    height: int | None = None,
) -> dict[str, Any]:
    path = f"/productscience/inference/inference/epoch_group_data/{epoch}"
    if model_id:
        path += "?model_id=" + urllib.parse.quote(model_id, safe="")
    return get_json(base, path, workdir, refresh=refresh, height=height)["epoch_group_data"]


def root_weight_map(root_group: dict[str, Any]) -> dict[str, int]:
    return {
        row["member_address"]: int_of(row.get("weight"))
        for row in root_group.get("validation_weights", [])
    }


def confirmation_weight_for(group: dict[str, Any], participant: str) -> int:
    for row in group.get("validation_weights", []):
        if row.get("member_address") == participant:
            return int_of(row.get("confirmation_weight"))
    return 0


def model_voting_power(group: dict[str, Any]) -> dict[str, int]:
    return {
        row["member_address"]: int_of(row.get("voting_power") or row.get("weight"))
        for row in group.get("validation_weights", [])
    }


def commitment_index(commits: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    return {(row["participant_address"], row["model_id"]): row for row in commits}


def validation_index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], list[dict[str, Any]]]:
    out: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for outer in rows:
        for inner in outer.get("poc_validation") or []:
            key = (inner["participant_address"], inner["model_id"])
            out.setdefault(key, []).append(inner)
    return out


def classify_model(
    participant: str,
    model: str,
    total_network_weight: int,
    model_votes: dict[str, int],
    commits_by_key: dict[tuple[str, str], dict[str, Any]],
    validations_by_key: dict[tuple[str, str], list[dict[str, Any]]],
) -> dict[str, Any]:
    commit = commits_by_key.get((participant, model))
    validations = validations_by_key.get((participant, model), [])
    valid_validators = {
        row["validator_participant_address"]
        for row in validations
        if int_of(row.get("validated_weight")) > 0
    }
    invalid_validators = {
        row["validator_participant_address"]
        for row in validations
        if int_of(row.get("validated_weight")) <= 0
    }
    valid_weight = sum(model_votes.get(addr, 0) for addr in valid_validators)
    invalid_weight = sum(model_votes.get(addr, 0) for addr in invalid_validators)
    two_thirds = total_network_weight * 2 // 3
    if not commit:
        result = "no_submission"
    elif valid_weight > two_thirds:
        result = "pass_weight"
    elif invalid_weight > two_thirds:
        result = "fail_weight"
    else:
        result = "weight_shortfall"
    return {
        "submitted_count": int_of(commit.get("count")) if commit else 0,
        "validator_count": len(valid_validators | invalid_validators),
        "valid_weight": valid_weight,
        "valid_weight_percent": percent(valid_weight, total_network_weight),
        "invalid_weight": invalid_weight,
        "result": result,
        "validators": ";".join(sorted(valid_validators | invalid_validators)),
    }


def preserved_model_rows(snapshot: dict[str, Any], model_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model in snapshot.get("model_preserved_nodes") or []:
        if model.get("model_id") != model_id:
            continue
        for participant in model.get("participants") or []:
            rows.append(
                {
                    "participant": participant.get("participant_id", ""),
                    "node_ids": ";".join(participant.get("node_ids") or []),
                    "node_count": len(participant.get("node_ids") or []),
                }
            )
    return rows


def event_for_exclusion(events: list[dict[str, Any]], exclusion_height: int) -> dict[str, Any] | None:
    ordered = sorted(events, key=lambda row: int_of(row.get("event_sequence")))
    for index, event in enumerate(ordered):
        start = int_of(event.get("trigger_height"))
        end = int_of(ordered[index + 1].get("trigger_height")) if index + 1 < len(ordered) else 10**18
        if start <= exclusion_height < end:
            return event
    return None


def load_stage(
    base: str,
    workdir: Path,
    trigger_height: int,
    refresh: bool,
) -> tuple[dict[tuple[str, str], dict[str, Any]], dict[tuple[str, str], list[dict[str, Any]]]]:
    commits = get_json(
        base,
        f"/productscience/inference/inference/all_poc_v2_store_commits/{trigger_height}",
        workdir,
        refresh=refresh,
    )["commits"]
    validations = get_json(
        base,
        f"/productscience/inference/inference/poc_v2_validations_for_stage/{trigger_height}",
        workdir,
        refresh=refresh,
    )["poc_validation"]
    return commitment_index(commits), validation_index(validations)


def scan_epoch(base: str, workdir: Path, epoch: int, params: dict[str, Any], refresh: bool) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    root_group = get_epoch_group(base, workdir, epoch, None, refresh)
    root_weights = root_weight_map(root_group)
    total_network_weight = int_of(root_group.get("total_weight"))
    model_groups = {model: get_epoch_group(base, workdir, epoch, model, refresh) for model in MODELS}
    model_votes = {model: model_voting_power(group) for model, group in model_groups.items()}
    performance_rows = get_json(
        base,
        f"/productscience/inference/inference/epoch_performance_summary/{epoch}",
        workdir,
        refresh=refresh,
    )["epochPerformanceSummary"]
    performance = {row["participant_id"]: row for row in performance_rows}
    excluded_rows = get_json(
        base,
        f"/productscience/inference/inference/excluded_participants/{epoch}",
        workdir,
        refresh=refresh,
    )["items"]
    events = get_json(
        base,
        f"/productscience/inference/inference/confirmation_poc_events/{epoch}",
        workdir,
        refresh=refresh,
    )["events"]
    failed_rows = [row for row in excluded_rows if row.get("reason") == "failed_confirmation_poc"]
    fixed_reward = fixed_epoch_reward_ngonka(params, epoch)

    stage_cache: dict[int, tuple[dict[tuple[str, str], dict[str, Any]], dict[tuple[str, str], list[dict[str, Any]]]]] = {}
    candidate_rows: list[dict[str, Any]] = []
    for exclusion in failed_rows:
        participant = exclusion.get("address", "")
        exclusion_height = int_of(exclusion.get("exclusion_block_height"))
        selected_event = event_for_exclusion(events, exclusion_height)
        event_sequence = "" if selected_event is None else int_of(selected_event.get("event_sequence"))
        trigger_height = 0 if selected_event is None else int_of(selected_event.get("trigger_height"))
        if trigger_height and trigger_height not in stage_cache:
            stage_cache[trigger_height] = load_stage(base, workdir, trigger_height, refresh)
        commits_by_key, validations_by_key = stage_cache.get(trigger_height, ({}, {}))

        model_results = {
            model: classify_model(
                participant,
                model,
                total_network_weight,
                model_votes[model],
                commits_by_key,
                validations_by_key,
            )
            for model in MODELS
        }

        participant_at = get_json(
            base,
            f"/productscience/inference/inference/participant/{participant}",
            workdir,
            refresh=refresh,
            height=exclusion_height,
        )["participant"]
        params_at = get_json(
            base,
            "/productscience/inference/inference/params",
            workdir,
            refresh=refresh,
            height=exclusion_height,
        )["params"]
        before_group = get_epoch_group(base, workdir, epoch, None, refresh, height=max(1, exclusion_height - 1))
        at_group = get_epoch_group(base, workdir, epoch, None, refresh, height=exclusion_height)
        preserved_payload = get_json(
            base,
            "/productscience/inference/inference/preserved_nodes_snapshot",
            workdir,
            refresh=refresh,
            height=exclusion_height,
        )
        preserved_snapshot = preserved_payload.get("snapshot") or {}
        kimi_preserved = preserved_model_rows(preserved_snapshot, KIMI)
        kimi_preserved_rows = [
            {
                **row,
                "voting_power": model_votes[KIMI].get(row["participant"], 0),
            }
            for row in kimi_preserved
        ]
        high_preserved_kimi = max((row["voting_power"] for row in kimi_preserved_rows), default=0)
        actual_reward = int_of(performance.get(participant, {}).get("rewarded_coins"))
        expected_reward = root_weights.get(participant, 0) * fixed_reward // total_network_weight
        ratio_raw = (participant_at.get("current_epoch_stats") or {}).get("confirmationPoCRatio")
        alpha_raw = (params_at.get("confirmation_poc_params") or {}).get("alpha_threshold")
        ratio = decimal_from_chain(ratio_raw)
        alpha = decimal_from_chain(alpha_raw)
        kimi_result = model_results[KIMI]
        qwen_result = model_results[QWEN]
        case3_like = (
            actual_reward == 0
            and ratio is not None
            and alpha is not None
            and ratio < alpha
            and int_of(kimi_result["submitted_count"]) > 0
            and int_of(kimi_result["valid_weight"]) <= total_network_weight * 2 // 3
            and high_preserved_kimi > 0
        )
        reason_parts = []
        if actual_reward == 0:
            reason_parts.append("zero_reward")
        if ratio is not None and alpha is not None and ratio < alpha:
            reason_parts.append("ratio_below_alpha")
        if int_of(kimi_result["submitted_count"]) > 0:
            reason_parts.append("kimi_submitted")
        if int_of(kimi_result["valid_weight"]) <= total_network_weight * 2 // 3:
            reason_parts.append("kimi_below_2_3")
        if high_preserved_kimi > 0:
            reason_parts.append("kimi_preserved_power_present")

        candidate_rows.append(
            {
                "epoch": epoch,
                "participant": participant,
                "root_weight": root_weights.get(participant, 0),
                "total_network_weight": total_network_weight,
                "actual_reward_ngonka": actual_reward,
                "expected_reward_ngonka": expected_reward,
                "loss_ngonka": expected_reward - actual_reward,
                "loss_gonka": f"{Decimal(expected_reward - actual_reward) / Decimal(1_000_000_000):.9f}",
                "claimed": performance.get(participant, {}).get("claimed", ""),
                "exclusion_height": exclusion_height,
                "exclusion_reason": exclusion.get("reason", ""),
                "participant_status_at_exclusion": participant_at.get("status", ""),
                "confirmation_ratio": decimal_to_string(ratio_raw),
                "confirmation_ratio_percent": decimal_percent(ratio_raw),
                "alpha_threshold": decimal_to_string(alpha_raw),
                "ratio_below_alpha": ratio < alpha if ratio is not None and alpha is not None else "",
                "confirmation_weight_before_exclusion": confirmation_weight_for(before_group, participant),
                "confirmation_weight_at_exclusion": confirmation_weight_for(at_group, participant),
                "confirmation_weight_delta": confirmation_weight_for(at_group, participant)
                - confirmation_weight_for(before_group, participant),
                "event_sequence": event_sequence,
                "event_trigger_height": trigger_height,
                "qwen_submitted_count": qwen_result["submitted_count"],
                "qwen_valid_weight": qwen_result["valid_weight"],
                "qwen_valid_weight_percent": qwen_result["valid_weight_percent"],
                "qwen_result": qwen_result["result"],
                "kimi_submitted_count": kimi_result["submitted_count"],
                "kimi_valid_weight": kimi_result["valid_weight"],
                "kimi_valid_weight_percent": kimi_result["valid_weight_percent"],
                "kimi_result": kimi_result["result"],
                "kimi_preserved_participants": ";".join(
                    f"{row['participant']}:{row['voting_power']}:{row['node_ids']}" for row in kimi_preserved_rows
                ),
                "max_single_preserved_kimi_weight": high_preserved_kimi,
                "max_single_preserved_kimi_weight_percent": percent(high_preserved_kimi, total_network_weight),
                "case3_like_signature": case3_like,
                "signature_reason": ",".join(reason_parts),
            }
        )

    summary = {
        "epoch": epoch,
        "root_participant_count": len(root_weights),
        "total_network_weight": total_network_weight,
        "cpoc_event_count": len(events),
        "excluded_count": len(excluded_rows),
        "failed_confirmation_poc_count": len(failed_rows),
        "zero_reward_failed_confirmation_poc_count": sum(1 for row in candidate_rows if int_of(row["actual_reward_ngonka"]) == 0),
        "case3_like_count": sum(1 for row in candidate_rows if row["case3_like_signature"] is True),
        "case3_like_participants": ";".join(
            row["participant"] for row in candidate_rows if row["case3_like_signature"] is True
        ),
    }
    return summary, candidate_rows


def write_markdown(path: Path, summaries: list[dict[str, Any]], candidate_rows: list[dict[str, Any]]) -> None:
    case3_like = [row for row in candidate_rows if row["case3_like_signature"] is True]
    failed = candidate_rows
    lines = [
        "# Case 3 Neighbor Epoch Scan",
        "",
        f"Range checked: epochs `{summaries[0]['epoch']}` through `{summaries[-1]['epoch']}`.",
        "",
        "The scan looks for the same durable chain signature as Case 3:",
        "",
        "1. participant excluded with `failed_confirmation_poc`;",
        "2. `ConfirmationPoCRatio` below `AlphaThreshold`;",
        "3. zero actual epoch reward;",
        "4. Kimi submission exists but Kimi validation weight does not exceed the two-thirds weight line;",
        "5. Kimi preserved-node voting power is present at the exclusion height.",
        "",
        "## Epoch Summary",
        "",
        "| Epoch | Participants | Excluded | failed_confirmation_poc | Case-3-like | Participants |",
        "|---:|---:|---:|---:|---:|---|",
    ]
    for row in summaries:
        lines.append(
            "| {epoch} | {root_participant_count} | {excluded_count} | "
            "{failed_confirmation_poc_count} | {case3_like_count} | {case3_like_participants} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Case-3-like Rows",
            "",
        ]
    )
    if not case3_like:
        lines.append("No neighboring epoch produced the full Case-3-like signature.")
    else:
        lines.extend(
            [
                "| Epoch | Participant | Ratio | Alpha | Kimi submitted | Kimi valid weight | Preserved Kimi weight | Loss, GONKA |",
                "|---:|---|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for row in case3_like:
            lines.append(
                "| {epoch} | `{participant}` | {confirmation_ratio_percent}% | {alpha_threshold} | "
                "{kimi_submitted_count} | {kimi_valid_weight} ({kimi_valid_weight_percent}%) | "
                "{max_single_preserved_kimi_weight} ({max_single_preserved_kimi_weight_percent}%) | {loss_gonka} |".format(**row)
            )
    lines.extend(
        [
            "",
            "## All failed_confirmation_poc Rows",
            "",
        ]
    )
    if not failed:
        lines.append("No `failed_confirmation_poc` exclusions were found in the scanned range.")
    else:
        lines.extend(
            [
                "| Epoch | Participant | Reward | Ratio | Kimi result | Reason |",
                "|---:|---|---:|---:|---|---|",
            ]
        )
        for row in failed:
            lines.append(
                "| {epoch} | `{participant}` | {actual_reward_ngonka} | {confirmation_ratio_percent}% | "
                "{kimi_result} | {signature_reason} |".format(**row)
            )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--center-epoch", type=int, default=CASE_EPOCH)
    parser.add_argument("--epochs-before", type=int, default=DEFAULT_EPOCHS_BEFORE)
    parser.add_argument("--epochs-after", type=int, default=DEFAULT_EPOCHS_AFTER)
    parser.add_argument("--workdir", type=Path, default=DEFAULT_WORKDIR)
    parser.add_argument("--artifact-dir", type=Path, default=DEFAULT_ARTIFACT_DIR)
    parser.add_argument("--refresh", action="store_true", help="refresh the /tmp raw cache")
    args = parser.parse_args()

    load_dotenv(Path(".env"))
    base = direct_lcd_from_env()
    args.artifact_dir.mkdir(parents=True, exist_ok=True)
    params = get_json(base, "/productscience/inference/inference/params", args.workdir, refresh=args.refresh)["params"]

    start_epoch = args.center_epoch - args.epochs_before
    end_epoch = args.center_epoch + args.epochs_after
    summaries: list[dict[str, Any]] = []
    candidate_rows: list[dict[str, Any]] = []
    for epoch in range(start_epoch, end_epoch + 1):
        summary, rows = scan_epoch(base, args.workdir, epoch, params, args.refresh)
        summaries.append(summary)
        candidate_rows.extend(rows)

    write_csv(
        args.artifact_dir / "case3_neighbor_epoch_summary.csv",
        summaries,
        [
            "epoch",
            "root_participant_count",
            "total_network_weight",
            "cpoc_event_count",
            "excluded_count",
            "failed_confirmation_poc_count",
            "zero_reward_failed_confirmation_poc_count",
            "case3_like_count",
            "case3_like_participants",
        ],
    )
    write_csv(
        args.artifact_dir / "case3_neighbor_failed_cpoc_rows.csv",
        candidate_rows,
        [
            "epoch",
            "participant",
            "root_weight",
            "total_network_weight",
            "actual_reward_ngonka",
            "expected_reward_ngonka",
            "loss_ngonka",
            "loss_gonka",
            "claimed",
            "exclusion_height",
            "exclusion_reason",
            "participant_status_at_exclusion",
            "confirmation_ratio",
            "confirmation_ratio_percent",
            "alpha_threshold",
            "ratio_below_alpha",
            "confirmation_weight_before_exclusion",
            "confirmation_weight_at_exclusion",
            "confirmation_weight_delta",
            "event_sequence",
            "event_trigger_height",
            "qwen_submitted_count",
            "qwen_valid_weight",
            "qwen_valid_weight_percent",
            "qwen_result",
            "kimi_submitted_count",
            "kimi_valid_weight",
            "kimi_valid_weight_percent",
            "kimi_result",
            "kimi_preserved_participants",
            "max_single_preserved_kimi_weight",
            "max_single_preserved_kimi_weight_percent",
            "case3_like_signature",
            "signature_reason",
        ],
    )
    write_json(
        args.artifact_dir / "case3_neighbor_epoch_scan.json",
        {
            "method": "archive LCD scan; published Case 3 code not executed or imported",
            "center_epoch": args.center_epoch,
            "start_epoch": start_epoch,
            "end_epoch": end_epoch,
            "signature": [
                "failed_confirmation_poc exclusion",
                "ConfirmationPoCRatio below AlphaThreshold",
                "zero actual reward",
                "Kimi submitted but Kimi validation weight did not exceed two thirds",
                "Kimi preserved-node voting power present at exclusion height",
            ],
            "epoch_summary": summaries,
            "failed_confirmation_poc_rows": candidate_rows,
        },
    )
    write_markdown(args.artifact_dir / "case3_neighbor_epoch_scan.md", summaries, candidate_rows)

    print(
        json.dumps(
            {
                "artifact_dir": str(args.artifact_dir),
                "epochs": [start_epoch, end_epoch],
                "failed_confirmation_poc_rows": len(candidate_rows),
                "case3_like_rows": sum(1 for row in candidate_rows if row["case3_like_signature"] is True),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
