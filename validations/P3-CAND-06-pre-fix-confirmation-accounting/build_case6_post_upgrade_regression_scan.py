#!/usr/bin/env python3
"""Scan post-v0.2.13 epochs for P3-CAND-06 recurrence.

The scan starts from archive LCD chain state and does not execute any external
case repository. It looks for the P3-CAND-06 signature:

    failed_confirmation_poc + zero reward + ratio below alpha
    + at least one tracked model has strict pass_weight.
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


getcontext().prec = 100

CASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = CASE_DIR.parents[1]
CACHE_DIR = CASE_DIR / "raw_stage_cache" / "post_upgrade_scan"
REQUEST_TIMEOUT_SECONDS = 90
RETRIES = 6

START_EPOCH = 277
END_EPOCH = 287
UPGRADE_HEIGHT = 4_267_300
UPGRADE_VERSION = "v0.2.13"

QWEN = "Qwen/Qwen3-235B-A22B-Instruct-2507-FP8"
KIMI = "moonshotai/Kimi-K2.6"
MODELS = [QWEN, KIMI]


def load_dotenv() -> None:
    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def direct_lcd_from_env() -> str:
    raw = os.environ.get("GONKA_RPC_LCD_URL") or os.environ.get("GONKA_RPC_URL")
    if not raw:
        return "http://node1.gonka.ai:8000/chain-api"
    raw = raw.strip().rstrip("/")
    if os.environ.get("GONKA_RPC_LCD_URL"):
        return raw if raw.startswith(("http://", "https://")) else "http://" + raw
    parsed = urllib.parse.urlparse(raw if "://" in raw else "dummy://" + raw)
    if not parsed.hostname:
        raise SystemExit("Could not parse GONKA_RPC_URL host")
    if parsed.port == 8000 or parsed.path.rstrip("/").endswith("/chain-api"):
        return raw if raw.startswith(("http://", "https://")) else "http://" + raw
    return f"http://{parsed.hostname}:1317"


def request_headers(block_height: int | None = None) -> dict[str, str]:
    headers = {"User-Agent": "grc-case6-post-upgrade-regression-scan/1.0"}
    if block_height is not None:
        headers["x-cosmos-block-height"] = str(block_height)
    api_key = os.environ.get("GONKA_RPC_API_KEY")
    if api_key:
        headers["X-Api-Key"] = api_key
    return headers


def path_cache_name(path: str, block_height: int | None = None) -> str:
    cache_key = f"{block_height or 'latest'}:{path}"
    digest = hashlib.sha256(cache_key.encode("utf-8")).hexdigest()[:16]
    safe = path.strip("/").replace("/", "_").replace("?", "__")
    safe = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in safe)
    if block_height is not None:
        safe = f"height_{block_height}_{safe}"
    return f"{safe}.{digest}.json"


def get_json(base: str, path: str, *, block_height: int | None = None, refresh: bool = False) -> Any:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / path_cache_name(path, block_height)
    if cache_path.exists() and not refresh:
        return json.loads(cache_path.read_text(encoding="utf-8"))

    url = base.rstrip("/") + path
    last_error = None
    for attempt in range(RETRIES):
        req = urllib.request.Request(url, headers=request_headers(block_height))
        try:
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            cache_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            return payload
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")
            last_error = f"HTTP {exc.code}: {body[:300]}"
            if exc.code == 404:
                raise RuntimeError(f"Failed to fetch {path} at height {block_height}: {last_error}") from exc
        except Exception as exc:  # noqa: BLE001 - audit tool retries broadly
            last_error = str(exc)
        time.sleep(min(20, 1 + attempt * 2))
    raise RuntimeError(f"Failed to fetch {path} at height {block_height}: {last_error}")


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
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


def decimal_percent(value: dict[str, Any] | None) -> str:
    decimal_value = decimal_from_chain(value)
    if decimal_value is None:
        return ""
    return f"{decimal_value * Decimal(100):.4f}"


def percent(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return ""
    return f"{Decimal(numerator) * Decimal(100) / Decimal(denominator):.4f}"


def fixed_epoch_reward_ngonka(params: dict[str, Any], epoch: int) -> int:
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
        exponent = decay_rate.exp() if decay_rate is not None else Decimal("1")
    epochs_since_genesis = epoch - genesis_epoch
    if epochs_since_genesis <= 0:
        return int(initial)
    return int((initial * (exponent ** epochs_since_genesis)).to_integral_value(rounding=ROUND_DOWN))


def get_epoch_group(
    base: str,
    epoch: int,
    model_id: str | None,
    refresh: bool,
    *,
    block_height: int | None = None,
) -> dict[str, Any]:
    path = f"/productscience/inference/inference/epoch_group_data/{epoch}"
    if model_id:
        path += "?model_id=" + urllib.parse.quote(model_id, safe="")
    return get_json(base, path, block_height=block_height, refresh=refresh)["epoch_group_data"]


def root_weight_map(root_group: dict[str, Any]) -> dict[str, int]:
    return {
        row["member_address"]: int_of(row.get("weight"))
        for row in root_group.get("validation_weights") or []
    }


def confirmation_weight_for(group: dict[str, Any], participant: str) -> int:
    for row in group.get("validation_weights") or []:
        if row.get("member_address") == participant:
            return int_of(row.get("confirmation_weight"))
    return 0


def model_voting_power(group: dict[str, Any]) -> dict[str, int]:
    return {
        row["member_address"]: int_of(row.get("voting_power") or row.get("weight"))
        for row in group.get("validation_weights") or []
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
    strict_two_thirds_line = total_network_weight * 2 // 3
    if not commit:
        result = "no_submission"
    elif valid_weight > strict_two_thirds_line:
        result = "pass_weight"
    elif invalid_weight > strict_two_thirds_line:
        result = "fail_weight"
    else:
        result = "weight_shortfall"
    return {
        "submitted_count": int_of(commit.get("count")) if commit else 0,
        "validator_count": len(valid_validators | invalid_validators),
        "valid_weight": valid_weight,
        "valid_weight_percent": percent(valid_weight, total_network_weight),
        "invalid_weight": invalid_weight,
        "invalid_weight_percent": percent(invalid_weight, total_network_weight),
        "result": result,
        "validators": ";".join(sorted(valid_validators | invalid_validators)),
    }


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
    trigger_height: int,
    refresh: bool,
) -> tuple[dict[tuple[str, str], dict[str, Any]], dict[tuple[str, str], list[dict[str, Any]]]]:
    commits = get_json(
        base,
        f"/productscience/inference/inference/all_poc_v2_store_commits/{trigger_height}",
        refresh=refresh,
    )["commits"]
    validations = get_json(
        base,
        f"/productscience/inference/inference/poc_v2_validations_for_stage/{trigger_height}",
        refresh=refresh,
    )["poc_validation"]
    return commitment_index(commits), validation_index(validations)


def scan_epoch(base: str, epoch: int, params: dict[str, Any], refresh: bool) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    root_group = get_epoch_group(base, epoch, None, refresh)
    root_weights = root_weight_map(root_group)
    total_network_weight = int_of(root_group.get("total_weight"))
    model_groups = {model: get_epoch_group(base, epoch, model, refresh) for model in MODELS}
    model_votes = {model: model_voting_power(group) for model, group in model_groups.items()}
    performance_rows = get_json(
        base,
        f"/productscience/inference/inference/epoch_performance_summary/{epoch}",
        refresh=refresh,
    )["epochPerformanceSummary"]
    performance = {row["participant_id"]: row for row in performance_rows}
    excluded_rows = get_json(
        base,
        f"/productscience/inference/inference/excluded_participants/{epoch}",
        refresh=refresh,
    )["items"]
    events = get_json(
        base,
        f"/productscience/inference/inference/confirmation_poc_events/{epoch}",
        refresh=refresh,
    )["events"]
    failed_rows = [row for row in excluded_rows if row.get("reason") == "failed_confirmation_poc"]
    fixed_reward = fixed_epoch_reward_ngonka(params, epoch)
    two_thirds_min_weight = total_network_weight * 2 // 3 + 1

    stage_cache: dict[int, tuple[dict[tuple[str, str], dict[str, Any]], dict[tuple[str, str], list[dict[str, Any]]]]] = {}
    rows: list[dict[str, Any]] = []
    for exclusion in failed_rows:
        participant = exclusion.get("address", "")
        exclusion_height = int_of(exclusion.get("exclusion_block_height"))
        selected_event = event_for_exclusion(events, exclusion_height)
        event_sequence = "" if selected_event is None else int_of(selected_event.get("event_sequence"))
        trigger_height = 0 if selected_event is None else int_of(selected_event.get("trigger_height"))
        if trigger_height and trigger_height not in stage_cache:
            stage_cache[trigger_height] = load_stage(base, trigger_height, refresh)
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
        qwen = model_results[QWEN]
        kimi = model_results[KIMI]

        participant_at = get_json(
            base,
            f"/productscience/inference/inference/participant/{participant}",
            block_height=exclusion_height,
            refresh=refresh,
        )["participant"]
        params_at = get_json(
            base,
            "/productscience/inference/inference/params",
            block_height=exclusion_height,
            refresh=refresh,
        )["params"]
        before_group = get_epoch_group(base, epoch, None, refresh, block_height=max(1, exclusion_height - 1))
        at_group = get_epoch_group(base, epoch, None, refresh, block_height=exclusion_height)

        actual_reward = int_of(performance.get(participant, {}).get("rewarded_coins"))
        expected_reward = root_weights.get(participant, 0) * fixed_reward // total_network_weight if total_network_weight else 0
        ratio_raw = (participant_at.get("current_epoch_stats") or {}).get("confirmationPoCRatio")
        alpha_raw = (params_at.get("confirmation_poc_params") or {}).get("alpha_threshold")
        ratio = decimal_from_chain(ratio_raw)
        alpha = decimal_from_chain(alpha_raw)
        pass_models = [
            name
            for name, result in (("Qwen", qwen), ("Kimi", kimi))
            if result["result"] == "pass_weight"
        ]
        ratio_below_alpha = ratio < alpha if ratio is not None and alpha is not None else False
        case6_like = actual_reward == 0 and ratio_below_alpha and bool(pass_models)
        reason_parts = []
        if actual_reward == 0:
            reason_parts.append("zero_reward")
        if ratio_below_alpha:
            reason_parts.append("ratio_below_alpha")
        if pass_models:
            reason_parts.append("pass_weight_model:" + "+".join(pass_models))

        rows.append(
            {
                "epoch": epoch,
                "participant": participant,
                "root_weight": root_weights.get(participant, 0),
                "total_network_weight": total_network_weight,
                "two_thirds_min_weight": two_thirds_min_weight,
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
                "ratio_below_alpha": str(ratio_below_alpha),
                "confirmation_weight_before_exclusion": confirmation_weight_for(before_group, participant),
                "confirmation_weight_at_exclusion": confirmation_weight_for(at_group, participant),
                "confirmation_weight_delta": confirmation_weight_for(at_group, participant)
                - confirmation_weight_for(before_group, participant),
                "event_sequence": event_sequence,
                "event_trigger_height": trigger_height,
                "qwen_submitted_count": qwen["submitted_count"],
                "qwen_validator_count": qwen["validator_count"],
                "qwen_valid_weight": qwen["valid_weight"],
                "qwen_valid_weight_percent": qwen["valid_weight_percent"],
                "qwen_invalid_weight": qwen["invalid_weight"],
                "qwen_invalid_weight_percent": qwen["invalid_weight_percent"],
                "qwen_result": qwen["result"],
                "kimi_submitted_count": kimi["submitted_count"],
                "kimi_validator_count": kimi["validator_count"],
                "kimi_valid_weight": kimi["valid_weight"],
                "kimi_valid_weight_percent": kimi["valid_weight_percent"],
                "kimi_invalid_weight": kimi["invalid_weight"],
                "kimi_invalid_weight_percent": kimi["invalid_weight_percent"],
                "kimi_result": kimi["result"],
                "pass_models": "+".join(pass_models),
                "case6_like_signature": str(case6_like),
                "signature_reason": ",".join(reason_parts),
            }
        )

    summary = {
        "epoch": epoch,
        "root_participant_count": len(root_weights),
        "total_network_weight": total_network_weight,
        "two_thirds_min_weight": two_thirds_min_weight,
        "cpoc_event_count": len(events),
        "excluded_count": len(excluded_rows),
        "failed_confirmation_poc_count": len(failed_rows),
        "zero_reward_failed_confirmation_poc_count": sum(1 for row in rows if int_of(row["actual_reward_ngonka"]) == 0),
        "pass_weight_failed_confirmation_poc_count": sum(1 for row in rows if row["pass_models"]),
        "single_pass_model_failed_confirmation_poc_count": sum(
            1 for row in rows if row["pass_models"] and "+" not in row["pass_models"]
        ),
        "both_pass_models_failed_confirmation_poc_count": sum(1 for row in rows if row["pass_models"] == "Qwen+Kimi"),
        "case6_like_count": sum(1 for row in rows if row["case6_like_signature"] == "True"),
        "case6_like_participants": ";".join(row["participant"] for row in rows if row["case6_like_signature"] == "True"),
    }
    return summary, rows


def write_markdown(path: Path, summaries: list[dict[str, Any]], rows: list[dict[str, Any]], requested_end_epoch: int) -> None:
    case6_like = [row for row in rows if row["case6_like_signature"] == "True"]
    single_pass_case6_like = [row for row in case6_like if row["pass_models"] and "+" not in row["pass_models"]]
    both_pass_case6_like = [row for row in case6_like if row["pass_models"] == "Qwen+Kimi"]
    total_failed = sum(int(row["failed_confirmation_poc_count"]) for row in summaries)
    lines = [
        "# P3-CAND-06 Post-v0.2.13 Regression Scan",
        "",
        f"Range checked: epochs `{summaries[0]['epoch']}` through `{summaries[-1]['epoch']}`.",
        f"`{UPGRADE_VERSION}` was installed at block `{UPGRADE_HEIGHT}` during epoch `276`; epoch `277` is the first clean start after the upgrade.",
        "",
        "The scan looks for recurrence of the P3-CAND-06 signature:",
        "",
        "1. participant excluded with `failed_confirmation_poc`;",
        "2. actual epoch reward is zero;",
        "3. `ConfirmationPoCRatio` is below `AlphaThreshold`;",
        "4. at least one tracked model (`Qwen` or `Kimi`) has strict `pass_weight` using `validWeight > TotalNetworkWeight * 2 / 3`.",
        "",
    ]
    if requested_end_epoch > int(summaries[-1]["epoch"]):
        lines.extend(
            [
                f"The requested end epoch was `{requested_end_epoch}`, but epoch `{int(summaries[-1]['epoch']) + 1}`",
                "was not available from the archive LCD during this run, so the artifact records the complete available range.",
                "",
            ]
        )
    lines.extend(
        [
            "## Result",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Epochs checked | `{len(summaries)}` |",
            f"| failed_confirmation_poc rows | `{total_failed}` |",
            f"| Rows with pass-weight model and failed ratio | `{len(case6_like)}` |",
            f"| Case-6-like rows with exactly one passing tracked model | `{len(single_pass_case6_like)}` |",
            f"| Case-6-like rows with both tracked models passing | `{len(both_pass_case6_like)}` |",
            "",
            "Interpretation: this is a recurrence scan for the broad signal, not a",
            "standalone proof that the pre-`v0.2.13` root cause still exists. Rows",
            "where exactly one tracked model passes and the other has `no_submission`",
            "can be ordinary post-upgrade multi-model accounting unless formula replay",
            "proves otherwise.",
            "",
            "## Epoch Summary",
            "",
            "| Epoch | Participants | Total weight | >2/3 min | cPoC events | Excluded | failed_confirmation_poc | pass-weight failed rows | single pass | both pass | Case-6-like rows | Participants |",
            "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    for row in summaries:
        lines.append(
            "| {epoch} | {root_participant_count} | {total_network_weight} | {two_thirds_min_weight} | "
            "{cpoc_event_count} | {excluded_count} | {failed_confirmation_poc_count} | "
            "{pass_weight_failed_confirmation_poc_count} | {single_pass_model_failed_confirmation_poc_count} | "
            "{both_pass_models_failed_confirmation_poc_count} | {case6_like_count} | {case6_like_participants} |".format(**row)
        )

    lines.extend(["", "## Case-6-like Rows", ""])
    if not case6_like:
        lines.append("No post-upgrade epoch in this range produced the P3-CAND-06 recurrence signature.")
    else:
        lines.extend(
            [
                "| Epoch | Participant | Ratio | Alpha | Pass model(s) | Qwen valid | Kimi valid | Loss, GONKA |",
                "|---:|---|---:|---:|---|---:|---:|---:|",
            ]
        )
        for row in case6_like:
            lines.append(
                "| {epoch} | `{participant}` | {confirmation_ratio_percent}% | {alpha_threshold} | {pass_models} | "
                "{qwen_valid_weight} ({qwen_valid_weight_percent}%) | "
                "{kimi_valid_weight} ({kimi_valid_weight_percent}%) | {loss_gonka} |".format(**row)
            )

    lines.extend(["", "## All failed_confirmation_poc Rows", ""])
    if not rows:
        lines.append("No `failed_confirmation_poc` exclusions were found in the scanned range.")
    else:
        lines.extend(
            [
                "| Epoch | Participant | Reward | Ratio | Pass model(s) | Qwen result | Kimi result | Reason |",
                "|---:|---|---:|---:|---|---|---|---|",
            ]
        )
        for row in rows:
            lines.append(
                "| {epoch} | `{participant}` | {actual_reward_ngonka} | {confirmation_ratio_percent}% | {pass_models} | "
                "{qwen_result} | {kimi_result} | {signature_reason} |".format(**row)
            )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


SUMMARY_FIELDS = [
    "epoch",
    "root_participant_count",
    "total_network_weight",
    "two_thirds_min_weight",
    "cpoc_event_count",
    "excluded_count",
    "failed_confirmation_poc_count",
    "zero_reward_failed_confirmation_poc_count",
    "pass_weight_failed_confirmation_poc_count",
    "single_pass_model_failed_confirmation_poc_count",
    "both_pass_models_failed_confirmation_poc_count",
    "case6_like_count",
    "case6_like_participants",
]

ROW_FIELDS = [
    "epoch",
    "participant",
    "root_weight",
    "total_network_weight",
    "two_thirds_min_weight",
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
    "qwen_validator_count",
    "qwen_valid_weight",
    "qwen_valid_weight_percent",
    "qwen_invalid_weight",
    "qwen_invalid_weight_percent",
    "qwen_result",
    "kimi_submitted_count",
    "kimi_validator_count",
    "kimi_valid_weight",
    "kimi_valid_weight_percent",
    "kimi_invalid_weight",
    "kimi_invalid_weight_percent",
    "kimi_result",
    "pass_models",
    "case6_like_signature",
    "signature_reason",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-epoch", type=int, default=START_EPOCH)
    parser.add_argument("--end-epoch", type=int, default=END_EPOCH)
    parser.add_argument(
        "--stop-on-missing",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="stop and write artifacts when the first future epoch is not available",
    )
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()

    if args.end_epoch < args.start_epoch:
        raise SystemExit("--end-epoch must be >= --start-epoch")

    load_dotenv()
    base = direct_lcd_from_env()
    params = get_json(base, "/productscience/inference/inference/params", refresh=args.refresh)["params"]

    summaries: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    for epoch in range(args.start_epoch, args.end_epoch + 1):
        try:
            summary, epoch_rows = scan_epoch(base, epoch, params, args.refresh)
        except RuntimeError as exc:
            if args.stop_on_missing and "HTTP 404" in str(exc) and summaries:
                print(
                    json.dumps(
                        {
                            "missing_epoch": epoch,
                            "stopped_after_epoch": summaries[-1]["epoch"],
                            "reason": "epoch data not available from archive LCD",
                        },
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    file=sys.stderr,
                )
                break
            raise
        summaries.append(summary)
        rows.extend(epoch_rows)

    if not summaries:
        raise SystemExit("No epochs were scanned")

    write_csv(CASE_DIR / "case6_post_upgrade_epoch_summary.csv", summaries, SUMMARY_FIELDS)
    write_csv(CASE_DIR / "case6_post_upgrade_failed_cpoc_rows.csv", rows, ROW_FIELDS)
    write_json(
        CASE_DIR / "case6_post_upgrade_regression_scan.json",
        {
            "method": "archive LCD scan; external case repository code not executed or imported",
            "upgrade_version": UPGRADE_VERSION,
            "upgrade_height": UPGRADE_HEIGHT,
            "start_epoch": args.start_epoch,
            "requested_end_epoch": args.end_epoch,
            "end_epoch": summaries[-1]["epoch"],
            "signature": [
                "failed_confirmation_poc exclusion",
                "zero actual reward",
                "ConfirmationPoCRatio below AlphaThreshold",
                "at least one tracked model reaches strict pass_weight",
            ],
            "epoch_summary": summaries,
            "failed_confirmation_poc_rows": rows,
        },
    )
    write_markdown(CASE_DIR / "case6_post_upgrade_regression_scan.md", summaries, rows, args.end_epoch)

    print(
        json.dumps(
            {
                "epochs": [args.start_epoch, summaries[-1]["epoch"]],
                "requested_end_epoch": args.end_epoch,
                "failed_confirmation_poc_rows": len(rows),
                "case6_like_rows": sum(1 for row in rows if row["case6_like_signature"] == "True"),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
