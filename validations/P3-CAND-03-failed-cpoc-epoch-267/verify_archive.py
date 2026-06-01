#!/usr/bin/env python3
"""Independently validate P3-CAND-03 against an archive LCD.

This audit intentionally does not execute or import the published Case 3
repository. The published numbers are used only as a final comparison target.
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
from dataclasses import dataclass
from decimal import Decimal, ROUND_DOWN, getcontext
from pathlib import Path
from typing import Any


CASE_ID = "P3-CAND-03"
EPOCH = 267
CLAIMANT = "gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6"
HIGH_POWER_KIMI_NON_VOTER = "gonka17gpuntq09zsaqtmpe544gc32tk4424dwv5t34f"
KIMI = "moonshotai/Kimi-K2.6"
QWEN = "Qwen/Qwen3-235B-A22B-Instruct-2507-FP8"
MODELS = [QWEN, KIMI]
EXPECTED_TRIGGER_HEIGHTS = [4122271, 4130085, 4133665, 4134529]
EXPECTED_PUBLISHED_AMOUNT_NGONKA = 10_262_057_515_369
DEFAULT_WORKDIR = Path("/tmp/grc3-case3-audit")
DEFAULT_ARTIFACT_DIR = Path("validations/P3-CAND-03-failed-cpoc-epoch-267")
REQUEST_TIMEOUT_SECONDS = 60
RETRIES = 6
BECH32_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


@dataclass(frozen=True)
class EventData:
    sequence: int
    trigger_height: int
    generation_start_height: int
    phase: str


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
    headers = {"User-Agent": "grc-case3-independent-audit/1.0"}
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


def bech32_polymod(values: list[int]) -> int:
    generators = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    chk = 1
    for value in values:
        top = chk >> 25
        chk = (chk & 0x1FFFFFF) << 5 ^ value
        for i in range(5):
            if (top >> i) & 1:
                chk ^= generators[i]
    return chk


def bech32_hrp_expand(hrp: str) -> list[int]:
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def bech32_decode(addr: str) -> tuple[str, list[int]]:
    addr = addr.strip()
    if addr.lower() != addr and addr.upper() != addr:
        raise ValueError("mixed-case bech32")
    addr = addr.lower()
    pos = addr.rfind("1")
    if pos < 1 or pos + 7 > len(addr):
        raise ValueError("invalid bech32 separator")
    hrp = addr[:pos]
    data = [BECH32_CHARSET.find(ch) for ch in addr[pos + 1 :]]
    if any(value < 0 for value in data):
        raise ValueError("invalid bech32 character")
    if bech32_polymod(bech32_hrp_expand(hrp) + data) != 1:
        raise ValueError("invalid bech32 checksum")
    return hrp, data[:-6]


def bech32_encode(hrp: str, data: list[int]) -> str:
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
    checksum = [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]
    return hrp + "1" + "".join(BECH32_CHARSET[d] for d in data + checksum)


def operator_to_account(addr: str) -> str:
    _hrp, data = bech32_decode(addr)
    return bech32_encode("gonka", data)


def int_of(value: Any, default: int = 0) -> int:
    if value is None or value == "":
        return default
    return int(value)


def decimal_from_chain(value: dict[str, Any]) -> Decimal:
    return Decimal(str(value["value"])) * (Decimal(10) ** int(value["exponent"]))


def fixed_epoch_reward_ngonka(params: dict[str, Any], epoch: int) -> int:
    """Mirror the chain's fixed exponent path for the mainnet decay rate."""
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


def normalize_events(raw_events: list[dict[str, Any]]) -> list[EventData]:
    events = [
        EventData(
            sequence=int_of(row["event_sequence"]),
            trigger_height=int_of(row["trigger_height"]),
            generation_start_height=int_of(row["generation_start_height"]),
            phase=row.get("phase", ""),
        )
        for row in raw_events
    ]
    return sorted(events, key=lambda event: event.sequence)


def get_epoch_group(
    base: str,
    workdir: Path,
    model_id: str | None,
    refresh: bool,
    *,
    height: int | None = None,
) -> dict[str, Any]:
    path = f"/productscience/inference/inference/epoch_group_data/{EPOCH}"
    if model_id:
        path += "?model_id=" + urllib.parse.quote(model_id, safe="")
    return get_json(base, path, workdir, refresh=refresh, height=height)["epoch_group_data"]


def model_voting_maps(model_groups: dict[str, dict[str, Any]]) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for model, group in model_groups.items():
        out[model] = {
            row["member_address"]: int_of(row.get("voting_power") or row.get("weight"))
            for row in group.get("validation_weights", [])
        }
    return out


def root_weight_map(root_group: dict[str, Any]) -> dict[str, int]:
    return {
        row["member_address"]: int_of(row.get("weight"))
        for row in root_group.get("validation_weights", [])
    }


def validation_weight_for(group: dict[str, Any], participant: str) -> dict[str, Any]:
    for row in group.get("validation_weights", []):
        if row.get("member_address") == participant:
            return row
    return {}


def decimal_to_string(value: dict[str, Any] | None) -> str:
    if not value:
        return ""
    return format(decimal_from_chain(value), "f")


def preserved_rows(snapshot: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not snapshot:
        return []
    rows: list[dict[str, Any]] = []
    for model in snapshot.get("model_preserved_nodes") or []:
        for participant in model.get("participants") or []:
            rows.append(
                {
                    "episode_anchor_height": snapshot.get("episode_anchor_height", ""),
                    "model_id": model.get("model_id", ""),
                    "participant": participant.get("participant_id", ""),
                    "node_ids": ";".join(participant.get("node_ids") or []),
                    "node_count": len(participant.get("node_ids") or []),
                }
            )
    return rows


def voting_power_from_snapshot(snapshot: dict[str, Any], model: str, participant: str) -> int:
    for model_row in snapshot.get("model_voting_powers") or []:
        if model_row.get("model_id") != model:
            continue
        for row in model_row.get("voting_powers") or []:
            if row.get("address") == participant:
                return int_of(row.get("voting_power"))
    return 0


def commitment_index(commits: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    return {
        (row["participant_address"], row["model_id"]): row
        for row in commits
    }


def validation_index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], list[dict[str, Any]]]:
    out: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for outer in rows:
        for inner in outer.get("poc_validation") or []:
            key = (inner["participant_address"], inner["model_id"])
            out.setdefault(key, []).append(inner)
    return out


def classify(
    *,
    participant: str,
    model: str,
    total_network_weight: int,
    model_voting_power: dict[str, int],
    guardians: set[str],
    commit: dict[str, Any] | None,
    validations: list[dict[str, Any]],
) -> dict[str, Any]:
    submitted_count = int_of(commit.get("count")) if commit else 0
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
    valid_weight = sum(model_voting_power.get(addr, 0) for addr in valid_validators)
    invalid_weight = sum(model_voting_power.get(addr, 0) for addr in invalid_validators)
    guardian_valid = len(valid_validators & guardians)
    guardian_invalid = len(invalid_validators & guardians)
    guardian_no_vote = max(0, len(guardians) - guardian_valid - guardian_invalid)
    two_thirds = total_network_weight * 2 // 3
    pass_by_weight = valid_weight > two_thirds
    fail_by_weight = invalid_weight > two_thirds
    pass_by_guardian = (not pass_by_weight and not fail_by_weight and guardian_valid > 0 and guardian_invalid == 0)
    fail_by_guardian = (not pass_by_weight and not fail_by_weight and guardian_invalid > 0 and guardian_valid == 0)
    if not commit:
        result = "no_submission"
    elif pass_by_weight:
        result = "pass_weight"
    elif fail_by_weight:
        result = "fail_weight"
    elif pass_by_guardian:
        result = "pass_guardian"
    elif fail_by_guardian:
        result = "fail_guardian"
    else:
        result = "weight_and_guardian_shortfall"
    return {
        "participant": participant,
        "model_id": model,
        "submitted_count": submitted_count,
        "validator_count": len(valid_validators | invalid_validators),
        "valid_weight": valid_weight,
        "invalid_weight": invalid_weight,
        "total_network_weight": total_network_weight,
        "valid_weight_ratio": f"{(Decimal(valid_weight) / Decimal(total_network_weight)):.6f}",
        "guardian_valid": guardian_valid,
        "guardian_invalid": guardian_invalid,
        "guardian_no_vote": guardian_no_vote,
        "pass_by_weight": pass_by_weight,
        "pass_by_guardian": pass_by_guardian,
        "result": result,
        "validators": ";".join(sorted(valid_validators | invalid_validators)),
    }


def summarize_distribution(matrix_rows: list[dict[str, Any]], event_sequence: int) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in matrix_rows:
        if row["event_sequence"] == event_sequence:
            key = f"{row['model_label']}:{row['result']}"
            counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def case_candidate_reason(
    participant: str,
    matrix: dict[tuple[str, int, str], dict[str, Any]],
    summary: dict[str, Any],
    exclusions: dict[str, dict[str, Any]],
    event_heights: list[int],
) -> tuple[bool, str]:
    actual_reward = int_of(summary.get(participant, {}).get("rewarded_coins"))
    exclusion = exclusions.get(participant, {})
    exclusion_reason = exclusion.get("reason", "")
    exclusion_height = int_of(exclusion.get("exclusion_block_height"))
    qwen_0 = matrix.get((participant, 0, QWEN), {})
    kimi_0 = matrix.get((participant, 0, KIMI), {})
    later_kimi = [matrix.get((participant, seq, KIMI), {}) for seq in (1, 2, 3)]
    if actual_reward != 0:
        return False, "non-zero actual reward"
    if exclusion_reason != "failed_confirmation_poc":
        return False, f"exclusion reason is {exclusion_reason or 'missing'}"
    if not (event_heights[0] <= exclusion_height < event_heights[1]):
        return False, f"failed_confirmation_poc exclusion happened at {exclusion_height}, not in cPoC #1 window"
    if not qwen_0 or not kimi_0:
        return False, "missing cPoC evidence"
    if int_of(qwen_0.get("submitted_count")) == 0:
        return False, "no cPoC #1 Qwen submission"
    if int_of(kimi_0.get("submitted_count")) == 0:
        return False, "no cPoC #1 Kimi submission"
    if int_of(kimi_0.get("valid_weight")) > int_of(kimi_0.get("total_network_weight")) * 2 // 3:
        return False, "cPoC #1 Kimi had >2/3 validation weight"
    if any(int_of(row.get("submitted_count")) == 0 for row in later_kimi):
        return False, "later Kimi cPoCs were not all submitted"
    return True, "zero reward, failed_confirmation_poc in cPoC #1 window, Qwen/Kimi submissions present, Kimi validation weight below 2/3, later Kimi submitted"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, default=DEFAULT_WORKDIR)
    parser.add_argument("--artifact-dir", type=Path, default=DEFAULT_ARTIFACT_DIR)
    parser.add_argument("--refresh", action="store_true", help="refresh the /tmp raw cache")
    args = parser.parse_args()

    load_dotenv(Path(".env"))
    base = direct_lcd_from_env()
    args.artifact_dir.mkdir(parents=True, exist_ok=True)

    params = get_json(base, "/productscience/inference/inference/params", args.workdir, refresh=args.refresh)["params"]
    root_group = get_epoch_group(base, args.workdir, None, args.refresh)
    model_groups = {model: get_epoch_group(base, args.workdir, model, args.refresh) for model in MODELS}
    performance_rows = get_json(
        base,
        f"/productscience/inference/inference/epoch_performance_summary/{EPOCH}",
        args.workdir,
        refresh=args.refresh,
    )["epochPerformanceSummary"]
    excluded_rows = get_json(
        base,
        f"/productscience/inference/inference/excluded_participants/{EPOCH}",
        args.workdir,
        refresh=args.refresh,
    )["items"]
    event_rows = get_json(
        base,
        f"/productscience/inference/inference/confirmation_poc_events/{EPOCH}",
        args.workdir,
        refresh=args.refresh,
    )["events"]
    events = normalize_events(event_rows)

    if [event.trigger_height for event in events] != EXPECTED_TRIGGER_HEIGHTS:
        raise SystemExit(f"Unexpected confirmation PoC heights: {[event.trigger_height for event in events]}")

    claimant_exclusion_height = int_of(
        next(
            (
                row.get("exclusion_block_height")
                for row in excluded_rows
                if row.get("address") == CLAIMANT
            ),
            0,
        )
    )
    root_group_before_exclusion = get_epoch_group(
        base,
        args.workdir,
        None,
        args.refresh,
        height=max(1, claimant_exclusion_height - 1),
    )
    root_group_at_exclusion = get_epoch_group(
        base,
        args.workdir,
        None,
        args.refresh,
        height=claimant_exclusion_height,
    )
    params_at_exclusion = get_json(
        base,
        "/productscience/inference/inference/params",
        args.workdir,
        refresh=args.refresh,
        height=claimant_exclusion_height,
    )["params"]
    participant_before_exclusion = get_json(
        base,
        f"/productscience/inference/inference/participant/{CLAIMANT}",
        args.workdir,
        refresh=args.refresh,
        height=max(1, claimant_exclusion_height - 1),
    )["participant"]
    participant_at_exclusion = get_json(
        base,
        f"/productscience/inference/inference/participant/{CLAIMANT}",
        args.workdir,
        refresh=args.refresh,
        height=claimant_exclusion_height,
    )["participant"]
    validation_snapshot_at_exclusion = get_json(
        base,
        f"/productscience/inference/inference/poc_validation_snapshot/{events[0].trigger_height}",
        args.workdir,
        refresh=args.refresh,
        height=claimant_exclusion_height,
    )
    preserved_snapshot_at_exclusion = get_json(
        base,
        "/productscience/inference/inference/preserved_nodes_snapshot",
        args.workdir,
        refresh=args.refresh,
        height=claimant_exclusion_height,
    )

    guardian_operator_addrs = params.get("genesis_guardian_params", {}).get("guardian_addresses") or []
    guardian_accounts: set[str] = set()
    guardian_conversion_errors: list[str] = []
    for addr in guardian_operator_addrs:
        try:
            guardian_accounts.add(operator_to_account(addr))
        except ValueError as exc:
            guardian_conversion_errors.append(f"{addr}: {exc}")

    root_weights = root_weight_map(root_group)
    model_votes = model_voting_maps(model_groups)
    total_network_weight = int_of(root_group["total_weight"])
    performance = {row["participant_id"]: row for row in performance_rows}
    exclusions = {row["address"]: row for row in excluded_rows}
    participants = sorted(root_weights)

    raw_stage_counts: list[dict[str, Any]] = []
    matrix_rows: list[dict[str, Any]] = []
    matrix_lookup: dict[tuple[str, int, str], dict[str, Any]] = {}
    source_hashes: dict[str, str] = {}

    for event in events:
        commits_path = f"/productscience/inference/inference/all_poc_v2_store_commits/{event.trigger_height}"
        validations_path = f"/productscience/inference/inference/poc_v2_validations_for_stage/{event.trigger_height}"
        commits_payload = get_json(base, commits_path, args.workdir, refresh=args.refresh)
        validations_payload = get_json(base, validations_path, args.workdir, refresh=args.refresh)
        commits = commits_payload["commits"]
        validations = validations_payload["poc_validation"]
        source_hashes[commits_path] = hashlib.sha256(
            json.dumps(commits_payload, sort_keys=True).encode("utf-8")
        ).hexdigest()
        source_hashes[validations_path] = hashlib.sha256(
            json.dumps(validations_payload, sort_keys=True).encode("utf-8")
        ).hexdigest()
        raw_stage_counts.append(
            {
                "event_sequence": event.sequence,
                "trigger_height": event.trigger_height,
                "generation_start_height": event.generation_start_height,
                "phase": event.phase,
                "commit_rows": len(commits),
                "validation_outer_rows": len(validations),
                "validation_inner_rows": sum(len(row.get("poc_validation") or []) for row in validations),
            }
        )
        commits_by_key = commitment_index(commits)
        validations_by_key = validation_index(validations)
        for participant in participants:
            for model in MODELS:
                classified = classify(
                    participant=participant,
                    model=model,
                    total_network_weight=total_network_weight,
                    model_voting_power=model_votes[model],
                    guardians=guardian_accounts,
                    commit=commits_by_key.get((participant, model)),
                    validations=validations_by_key.get((participant, model), []),
                )
                model_label = "Qwen" if model == QWEN else "Kimi"
                row = {
                    "event_sequence": event.sequence,
                    "trigger_height": event.trigger_height,
                    "participant": participant,
                    "model_label": model_label,
                    **classified,
                }
                matrix_rows.append(row)
                matrix_lookup[(participant, event.sequence, model)] = row

    zero_reward_rows: list[dict[str, Any]] = []
    candidates: list[str] = []
    for participant in participants:
        actual_reward = int_of(performance.get(participant, {}).get("rewarded_coins"))
        if actual_reward != 0:
            continue
        included, reason = case_candidate_reason(
            participant,
            matrix_lookup,
            performance,
            exclusions,
            [event.trigger_height for event in events],
        )
        if included:
            candidates.append(participant)
        zero_reward_rows.append(
            {
                "participant": participant,
                "root_weight": root_weights.get(participant, 0),
                "actual_reward_ngonka": actual_reward,
                "exclusion_reason": exclusions.get(participant, {}).get("reason", ""),
                "exclusion_block_height": exclusions.get(participant, {}).get("exclusion_block_height", ""),
                "case3_included": included,
                "reason": reason,
                "cpoc1_qwen_result": matrix_lookup[(participant, 0, QWEN)]["result"],
                "cpoc1_kimi_result": matrix_lookup[(participant, 0, KIMI)]["result"],
                "cpoc2_kimi_result": matrix_lookup[(participant, 1, KIMI)]["result"],
                "cpoc3_kimi_result": matrix_lookup[(participant, 2, KIMI)]["result"],
                "cpoc4_kimi_result": matrix_lookup[(participant, 3, KIMI)]["result"],
            }
        )

    claimant_weight = root_weights[CLAIMANT]
    fixed_reward = fixed_epoch_reward_ngonka(params, EPOCH)
    actual_reward = int_of(performance[CLAIMANT].get("rewarded_coins"))
    expected_reward = claimant_weight * fixed_reward // total_network_weight
    loss = expected_reward - actual_reward
    claimant_rows = [
        matrix_lookup[(CLAIMANT, seq, model)]
        for seq in range(len(events))
        for model in MODELS
    ]
    high_power_rows = [
        matrix_lookup[(HIGH_POWER_KIMI_NON_VOTER, seq, model)]
        for seq in range(len(events))
        for model in MODELS
    ]

    cohort_rows = [
        {
            "participant": participant,
            "root_weight": root_weights[participant],
            "confirmation_weight": next(
                (
                    int_of(row.get("confirmation_weight"))
                    for row in root_group.get("validation_weights", [])
                    if row["member_address"] == participant
                ),
                0,
            ),
            "qwen_voting_power": model_votes[QWEN].get(participant, 0),
            "kimi_voting_power": model_votes[KIMI].get(participant, 0),
            "rewarded_coins": int_of(performance.get(participant, {}).get("rewarded_coins")),
            "claimed": performance.get(participant, {}).get("claimed", ""),
            "exclusion_reason": exclusions.get(participant, {}).get("reason", ""),
            "exclusion_block_height": exclusions.get(participant, {}).get("exclusion_block_height", ""),
        }
        for participant in participants
    ]

    amount = {
        "case_id": CASE_ID,
        "epoch": EPOCH,
        "participant": CLAIMANT,
        "participant_root_weight": claimant_weight,
        "root_total_weight": total_network_weight,
        "fixed_epoch_reward_ngonka": fixed_reward,
        "actual_reward_ngonka": actual_reward,
        "expected_reward_ngonka": expected_reward,
        "loss_ngonka": loss,
        "loss_gonka": f"{Decimal(loss) / Decimal(1_000_000_000):.9f}",
        "formula": "participant_root_weight * fixed_epoch_reward_ngonka // root_total_weight - actual_reward_ngonka",
        "published_amount_ngonka": EXPECTED_PUBLISHED_AMOUNT_NGONKA,
        "matches_published_amount": loss == EXPECTED_PUBLISHED_AMOUNT_NGONKA,
    }

    claimant_vw_before = validation_weight_for(root_group_before_exclusion, CLAIMANT)
    claimant_vw_at = validation_weight_for(root_group_at_exclusion, CLAIMANT)
    high_power_vw_at = validation_weight_for(model_groups[KIMI], HIGH_POWER_KIMI_NON_VOTER)
    validation_snapshot = validation_snapshot_at_exclusion.get("snapshot") or {}
    preserved_snapshot = preserved_snapshot_at_exclusion.get("snapshot") or {}
    preserved_snapshot_rows = preserved_rows(preserved_snapshot)
    preserved_focus_rows = [
        row
        for row in preserved_snapshot_rows
        if row["participant"] in {CLAIMANT, HIGH_POWER_KIMI_NON_VOTER}
    ]
    confirmation_params = params_at_exclusion.get("confirmation_poc_params") or {}
    participant_stats_at = participant_at_exclusion.get("current_epoch_stats") or {}
    confirmation_ratio = participant_stats_at.get("confirmationPoCRatio")
    alpha_threshold = confirmation_params.get("alpha_threshold")
    root_cause_trace = {
        "case_id": CASE_ID,
        "epoch": EPOCH,
        "claimant": CLAIMANT,
        "exclusion_height": claimant_exclusion_height,
        "exclusion_reason": exclusions.get(CLAIMANT, {}).get("reason"),
        "status_before_exclusion": participant_before_exclusion.get("status"),
        "status_at_exclusion": participant_at_exclusion.get("status"),
        "epochs_completed_before_exclusion": participant_before_exclusion.get("epochs_completed"),
        "epochs_completed_at_exclusion": participant_at_exclusion.get("epochs_completed"),
        "confirmation_ratio_raw": confirmation_ratio,
        "confirmation_ratio_decimal": decimal_to_string(confirmation_ratio),
        "alpha_threshold_raw": alpha_threshold,
        "alpha_threshold_decimal": decimal_to_string(alpha_threshold),
        "ratio_below_alpha": (
            decimal_from_chain(confirmation_ratio) < decimal_from_chain(alpha_threshold)
            if confirmation_ratio and alpha_threshold
            else None
        ),
        "claimant_root_weight_before_exclusion": int_of(claimant_vw_before.get("weight")),
        "claimant_confirmation_weight_before_exclusion": int_of(claimant_vw_before.get("confirmation_weight")),
        "claimant_root_weight_at_exclusion": int_of(claimant_vw_at.get("weight")),
        "claimant_confirmation_weight_at_exclusion": int_of(claimant_vw_at.get("confirmation_weight")),
        "confirmation_weight_delta": int_of(claimant_vw_at.get("confirmation_weight"))
        - int_of(claimant_vw_before.get("confirmation_weight")),
        "first_cpoc_trigger_height": events[0].trigger_height,
        "validation_snapshot_found": bool(validation_snapshot_at_exclusion.get("found")),
        "validation_snapshot_height": validation_snapshot.get("snapshot_height"),
        "validation_snapshot_total_network_weight": validation_snapshot.get("total_network_weight"),
        "snapshot_claimant_qwen_voting_power": voting_power_from_snapshot(validation_snapshot, QWEN, CLAIMANT),
        "snapshot_claimant_kimi_voting_power": voting_power_from_snapshot(validation_snapshot, KIMI, CLAIMANT),
        "snapshot_high_power_kimi_voting_power": voting_power_from_snapshot(
            validation_snapshot,
            KIMI,
            HIGH_POWER_KIMI_NON_VOTER,
        ),
        "high_power_kimi_non_voter": HIGH_POWER_KIMI_NON_VOTER,
        "high_power_kimi_group_voting_power": int_of(high_power_vw_at.get("voting_power")),
        "preserved_snapshot_found": bool(preserved_snapshot_at_exclusion.get("found")),
        "preserved_snapshot_episode_anchor_height": preserved_snapshot.get("episode_anchor_height"),
        "preserved_focus_rows": preserved_focus_rows,
        "code_path": [
            "confirmation_poc.go:evaluateConfirmation sets participant.CurrentEpochStats.ConfirmationPoCRatio",
            "calculations/status.go:getConfirmationPoCStatus fails when ConfirmationPoCRatio < AlphaThreshold",
            "participant_status.go records failed_confirmation_poc exclusion when status changes to INACTIVE",
        ],
    }

    summary = {
        "case_id": CASE_ID,
        "method": "independent archive LCD reconstruction; published Case 3 code not executed or imported",
        "epoch": EPOCH,
        "claimant": CLAIMANT,
        "root_total_weight": total_network_weight,
        "root_participant_count": len(participants),
        "model_group_counts": {model: len(group.get("validation_weights", [])) for model, group in model_groups.items()},
        "guardian_count": len(guardian_accounts),
        "guardian_conversion_errors": guardian_conversion_errors,
        "confirmation_poc_events": [event.__dict__ for event in events],
        "stage_counts": raw_stage_counts,
        "zero_reward_count": len(zero_reward_rows),
        "excluded_participants": excluded_rows,
        "case3_candidate_count": len(candidates),
        "case3_candidates": candidates,
        "cpoc1_distribution": summarize_distribution(matrix_rows, 0),
        "amount": amount,
        "root_cause_trace": root_cause_trace,
        "hardware_vs_chain": {
            "claimant_cpoc1_qwen": matrix_lookup[(CLAIMANT, 0, QWEN)]["result"],
            "claimant_cpoc1_kimi": matrix_lookup[(CLAIMANT, 0, KIMI)]["result"],
            "claimant_later_kimi_results": [
                matrix_lookup[(CLAIMANT, seq, KIMI)]["result"] for seq in (1, 2, 3)
            ],
            "high_power_kimi_non_voter": HIGH_POWER_KIMI_NON_VOTER,
            "high_power_kimi_voting_power": model_votes[KIMI].get(HIGH_POWER_KIMI_NON_VOTER, 0),
            "high_power_cpoc1_kimi_result": matrix_lookup[(HIGH_POWER_KIMI_NON_VOTER, 0, KIMI)]["result"],
            "high_power_validated_claimant_kimi_cpoc1": HIGH_POWER_KIMI_NON_VOTER
            in set(matrix_lookup[(CLAIMANT, 0, KIMI)]["validators"].split(";")),
            "claimant_exclusion_reason": exclusions.get(CLAIMANT, {}).get("reason"),
            "claimant_exclusion_block_height": exclusions.get(CLAIMANT, {}).get("exclusion_block_height"),
        },
        "source_hashes": source_hashes,
    }

    write_csv(
        args.artifact_dir / "case3_epoch_cohort.csv",
        cohort_rows,
        [
            "participant",
            "root_weight",
            "confirmation_weight",
            "qwen_voting_power",
            "kimi_voting_power",
            "rewarded_coins",
            "claimed",
            "exclusion_reason",
            "exclusion_block_height",
        ],
    )
    write_csv(
        args.artifact_dir / "case3_cpoc_events.csv",
        raw_stage_counts,
        [
            "event_sequence",
            "trigger_height",
            "generation_start_height",
            "phase",
            "commit_rows",
            "validation_outer_rows",
            "validation_inner_rows",
        ],
    )
    write_csv(
        args.artifact_dir / "case3_cpoc_matrix.csv",
        matrix_rows,
        [
            "event_sequence",
            "trigger_height",
            "participant",
            "model_label",
            "model_id",
            "submitted_count",
            "validator_count",
            "valid_weight",
            "invalid_weight",
            "total_network_weight",
            "valid_weight_ratio",
            "guardian_valid",
            "guardian_invalid",
            "guardian_no_vote",
            "pass_by_weight",
            "pass_by_guardian",
            "result",
            "validators",
        ],
    )
    write_csv(
        args.artifact_dir / "case3_zero_reward_review.csv",
        zero_reward_rows,
        [
            "participant",
            "root_weight",
            "actual_reward_ngonka",
            "exclusion_reason",
            "exclusion_block_height",
            "case3_included",
            "reason",
            "cpoc1_qwen_result",
            "cpoc1_kimi_result",
            "cpoc2_kimi_result",
            "cpoc3_kimi_result",
            "cpoc4_kimi_result",
        ],
    )
    write_json(args.artifact_dir / "case3_amount_reconciliation.json", amount)
    write_json(args.artifact_dir / "case3_root_cause_trace.json", root_cause_trace)
    write_json(args.artifact_dir / "case3_inputs_manifest.json", summary)
    write_csv(
        args.artifact_dir / "case3_preserved_snapshot_focus.csv",
        preserved_focus_rows,
        ["episode_anchor_height", "model_id", "participant", "node_ids", "node_count"],
    )
    write_json(
        args.artifact_dir / "case3_published_compare.json",
        {
            "published_repo_used_as_algorithm": False,
            "published_case3_audit_executed": False,
            "published_amount_ngonka": EXPECTED_PUBLISHED_AMOUNT_NGONKA,
            "independent_loss_ngonka": loss,
            "matches_published_amount": loss == EXPECTED_PUBLISHED_AMOUNT_NGONKA,
            "published_claimant": CLAIMANT,
            "independent_candidates": candidates,
        },
    )
    write_csv(
        args.artifact_dir / "case3_claimant_trace.csv",
        claimant_rows,
        [
            "event_sequence",
            "trigger_height",
            "participant",
            "model_label",
            "submitted_count",
            "validator_count",
            "valid_weight",
            "total_network_weight",
            "valid_weight_ratio",
            "guardian_valid",
            "guardian_invalid",
            "guardian_no_vote",
            "result",
            "validators",
        ],
    )
    write_csv(
        args.artifact_dir / "case3_high_power_kimi_validator_trace.csv",
        high_power_rows,
        [
            "event_sequence",
            "trigger_height",
            "participant",
            "model_label",
            "submitted_count",
            "validator_count",
            "valid_weight",
            "total_network_weight",
            "valid_weight_ratio",
            "guardian_valid",
            "guardian_invalid",
            "guardian_no_vote",
            "result",
            "validators",
        ],
    )

    print(
        json.dumps(
            {
                "case": CASE_ID,
                "epoch": EPOCH,
                "candidates": candidates,
                "loss_ngonka": loss,
                "loss_gonka": amount["loss_gonka"],
                "matches_published_amount": loss == EXPECTED_PUBLISHED_AMOUNT_NGONKA,
                "artifact_dir": str(args.artifact_dir),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
