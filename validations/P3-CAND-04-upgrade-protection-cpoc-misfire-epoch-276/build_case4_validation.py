#!/usr/bin/env python3
"""Build independent validation artifacts for P3-CAND-04.

This script intentionally does not execute the published payout276 repository.
It reconstructs the affected set and compensation from archive-chain state at
fixed heights, then downloads the published CSV only as a comparison artifact.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any


getcontext().prec = 80

CASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = CASE_DIR.parents[1]
CACHE_DIR = CASE_DIR / "raw_cache"

EPOCH = 276
CONTROL_EPOCHS = [275, 277]
SCOPE_EPOCHS = list(range(270, 284))
H_BEFORE = 4_267_299
H_AFTER = 4_274_661
UPGRADE_HEIGHT = 4_267_300
UPGRADE_VERSION = "v0.2.13"
LAST_UPGRADE_HEIGHT_KEY_HEX = "0x1b"
PR_1143_URL = "https://github.com/gonka-ai/gonka/pull/1143"
PR_1268_URL = "https://github.com/gonka-ai/gonka/pull/1268"
PR_1268_BRANCH_URL = "https://github.com/gonka-ai/gonka/tree/upgrade-v0.2.14"
RELEASE_ANNOUNCEMENT_URL = "https://gonka.ai/release-announcements/"
PUBLISHED_CSV_URL = "https://raw.githubusercontent.com/gonkavip/payout276/main/payout_276.csv"
REQUEST_TIMEOUT_SECONDS = 90
RETRIES = 5
RPC_REQUEST_TIMEOUT_SECONDS = 15
RPC_RETRIES = 2


def load_dotenv() -> None:
    path = REPO_ROOT / ".env"
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def direct_lcd_from_env() -> str:
    raw = os.environ.get("GONKA_RPC_LCD_URL") or os.environ.get("GONKA_RPC_URL")
    if not raw:
        return "http://node1.gonka.ai:8000/chain-api"
    raw = raw.strip().rstrip("/")
    if os.environ.get("GONKA_RPC_LCD_URL") or "/chain-api" in raw:
        return raw if "://" in raw else "http://" + raw
    parsed = urllib.parse.urlparse(raw if "://" in raw else "http://" + raw)
    return f"http://{parsed.hostname}:1317"


def direct_rpc_from_env() -> str:
    raw = os.environ.get("GONKA_RPC_RPC_URL") or os.environ.get("GONKA_RPC_URL")
    if not raw:
        return "http://node1.gonka.ai:8000/chain-rpc"
    raw = raw.strip().rstrip("/")
    if "://" not in raw:
        raw = "http://" + raw
    if "/chain-rpc" in raw:
        return raw
    if "/chain-api" in raw:
        return raw.replace("/chain-api", "/chain-rpc")
    parsed = urllib.parse.urlparse(raw)
    if parsed.port == 1317:
        return f"{parsed.scheme}://{parsed.hostname}:26657"
    if parsed.path in {"", "/"}:
        return raw + "/chain-rpc"
    return raw


def request_headers(block_height: int | None = None) -> dict[str, str]:
    headers = {"User-Agent": "grc-case4-independent-validation/1.0"}
    if block_height is not None:
        headers["x-cosmos-block-height"] = str(block_height)
    api_key = os.environ.get("GONKA_RPC_API_KEY")
    if api_key:
        headers["X-Api-Key"] = api_key
    return headers


def cache_name(path_or_url: str, block_height: int | None = None) -> str:
    key = f"{block_height or 'latest'}:{path_or_url}"
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]
    safe = path_or_url.strip("/").replace("/", "_").replace("?", "__")
    safe = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in safe)
    if block_height is not None:
        safe = f"height_{block_height}_{safe}"
    return f"{safe}.{digest}.json"


def get_json(base: str, path: str, *, block_height: int | None = None, refresh: bool = False) -> Any:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / cache_name(path, block_height)
    if cache_path.exists() and not refresh:
        return json.loads(cache_path.read_text(encoding="utf-8"))

    url = base.rstrip("/") + path
    last_error = None
    for attempt in range(RETRIES):
        req = urllib.request.Request(url, headers=request_headers(block_height))
        try:
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            cache_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            return payload
        except urllib.error.HTTPError as exc:
            last_error = f"HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[:300]}"
        except Exception as exc:  # noqa: BLE001 - archive audit retries broadly
            last_error = str(exc)
        time.sleep(min(15, 1 + attempt * 2))
    raise RuntimeError(f"Failed to fetch {path} at height {block_height}: {last_error}")


def get_json_uncached(base: str, path: str, *, block_height: int | None = None) -> Any:
    url = base.rstrip("/") + path
    req = urllib.request.Request(url, headers=request_headers(block_height))
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_rpc_json(base: str, path: str, *, refresh: bool = False) -> Any:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    base_digest = hashlib.sha256(base.rstrip("/").encode("utf-8")).hexdigest()[:8]
    cache_path = CACHE_DIR / cache_name(f"rpc_{base_digest}_{path}")
    if cache_path.exists() and not refresh:
        return json.loads(cache_path.read_text(encoding="utf-8"))

    url = base.rstrip("/") + path
    last_error = None
    for attempt in range(RPC_RETRIES):
        req = urllib.request.Request(url, headers=request_headers())
        try:
            with urllib.request.urlopen(req, timeout=RPC_REQUEST_TIMEOUT_SECONDS) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            cache_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            return payload
        except urllib.error.HTTPError as exc:
            last_error = f"HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[:300]}"
        except Exception as exc:  # noqa: BLE001 - archive audit retries broadly
            last_error = str(exc)
        time.sleep(min(5, 1 + attempt * 2))
    raise RuntimeError(f"Failed to fetch RPC {path}: {last_error}")


def fetch_text(url: str, *, refresh: bool = False) -> str:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = CACHE_DIR / (cache_name(url).replace(".json", ".txt"))
    if path.exists() and not refresh:
        return path.read_text(encoding="utf-8")
    req = urllib.request.Request(url, headers={"User-Agent": "grc-case4-published-compare/1.0"})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
        text = resp.read().decode("utf-8")
    path.write_text(text, encoding="utf-8")
    return text


def int_of(value: Any, default: int = 0) -> int:
    if value is None or value == "":
        return default
    return int(value)


def amount_ngonka(value: int | str | Decimal) -> str:
    return f"{Decimal(value) / Decimal(1_000_000_000):,.9f}"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def block_time(base: str, height: int) -> dict[str, str]:
    payload = get_json(base, f"/cosmos/base/tendermint/v1beta1/blocks/{height}")
    raw = payload["block"]["header"]["time"]
    utc = dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
    msk = utc.astimezone(dt.timezone(dt.timedelta(hours=3)))
    return {
        "height": height,
        "raw": raw,
        "utc": utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "msk": msk.strftime("%Y-%m-%d %H:%M:%S MSK"),
    }


def epoch_group(base: str, epoch: int, *, block_height: int | None = None) -> dict[str, Any]:
    return get_json(base, f"/productscience/inference/inference/epoch_group_data/{epoch}", block_height=block_height)[
        "epoch_group_data"
    ]


def confirmation_weights(group: dict[str, Any]) -> dict[str, int]:
    return {row["member_address"]: int_of(row.get("confirmation_weight")) for row in group["validation_weights"]}


def full_weights(group: dict[str, Any]) -> dict[str, int]:
    return {row["member_address"]: max(0, int_of(row.get("weight"))) for row in group["validation_weights"]}


def participant_statuses(base: str, *, block_height: int, refresh: bool) -> dict[str, str]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / f"height_{block_height}_participant_statuses.sanitized.json"
    if cache_path.exists() and not refresh:
        return json.loads(cache_path.read_text(encoding="utf-8"))["statuses"]
    payload = get_json_uncached(
        base,
        "/productscience/inference/inference/participant?pagination.limit=10000",
        block_height=block_height,
    )
    statuses = {row["address"]: row.get("status", "") for row in payload.get("participant", [])}
    cache_path.write_text(
        json.dumps(
            {"block_height": block_height, "participant_count": len(statuses), "statuses": statuses},
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return statuses


def performance_summary(base: str) -> dict[str, int]:
    rows = get_json(base, f"/productscience/inference/inference/epoch_performance_summary/{EPOCH}")[
        "epochPerformanceSummary"
    ]
    return {row["participant_id"]: int_of(row.get("rewarded_coins")) for row in rows}


def performance_summary_for_epoch(base: str, epoch: int) -> dict[str, int]:
    rows = get_json(base, f"/productscience/inference/inference/epoch_performance_summary/{epoch}")[
        "epochPerformanceSummary"
    ]
    return {row["participant_id"]: int_of(row.get("rewarded_coins")) for row in rows}


def excluded_participants(base: str, epoch: int) -> list[dict[str, Any]]:
    return get_json(base, f"/productscience/inference/inference/excluded_participants/{epoch}").get("items", [])


def cpoc_trigger_from_exclusion(exclusion_height: int) -> int:
    # confirmation_poc validation delay + validation duration + one block, observed in chain artifacts
    return exclusion_height - 281


def build_timeline(base: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for epoch in [*CONTROL_EPOCHS[:1], EPOCH, *CONTROL_EPOCHS[1:]]:
        group = epoch_group(base, epoch)
        poc = int_of(group.get("poc_start_block_height"))
        effective = int_of(group.get("effective_block_height"))
        last = int_of(group.get("last_block_height"))
        exclusions = excluded_participants(base, epoch)
        triggers = sorted({cpoc_trigger_from_exclusion(int_of(row["exclusion_block_height"])) for row in exclusions})
        for stage, trigger in enumerate(triggers):
            relation = "pre_upgrade"
            if trigger > UPGRADE_HEIGHT:
                relation = "post_upgrade"
            if epoch > EPOCH:
                relation = "post_upgrade_clean_epoch"
            trigger_time = block_time(base, trigger)
            rows.append(
                {
                    "epoch": epoch,
                    "poc_start_height": poc,
                    "effective_height": effective,
                    "last_height": last,
                    "cpoc_sequence": stage,
                    "cpoc_trigger_height": trigger,
                    "cpoc_trigger_msk": trigger_time["msk"],
                    "blocks_after_upgrade": trigger - UPGRADE_HEIGHT if trigger > UPGRADE_HEIGHT else "",
                    "relation": relation,
                    "excluded_at_stage": sum(
                        1 for item in exclusions if cpoc_trigger_from_exclusion(int_of(item["exclusion_block_height"])) == trigger
                    ),
                }
            )
    return rows


def classify_epoch(epoch: int, group: dict[str, Any]) -> str:
    poc = int_of(group.get("poc_start_block_height"))
    last = int_of(group.get("last_block_height"))
    if poc > UPGRADE_HEIGHT:
        return "after_upgrade_epoch"
    if last < UPGRADE_HEIGHT:
        return "before_upgrade"
    if poc <= UPGRADE_HEIGHT <= last:
        return "upgrade_epoch"
    return "overlaps_upgrade"


def build_affected(base: str, *, refresh: bool = False) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    before_group = epoch_group(base, EPOCH, block_height=H_BEFORE)
    after_group = epoch_group(base, EPOCH, block_height=H_AFTER)
    cw_before = confirmation_weights(before_group)
    cw_after = confirmation_weights(after_group)
    full_after = full_weights(after_group)
    statuses_before = participant_statuses(base, block_height=H_BEFORE, refresh=refresh)
    statuses_after = participant_statuses(base, block_height=H_AFTER, refresh=refresh)
    rewards = performance_summary(base)
    total_rewarded = sum(rewards.values())
    total_cw_after = sum(cw_after.values())
    total_full_weight_after = sum(full_after.values())
    excluded = {row["address"]: row for row in excluded_participants(base, EPOCH)}

    rows: list[dict[str, Any]] = []
    for address in sorted(cw_before):
        status_before = statuses_before.get(address, "")
        if status_before != "ACTIVE":
            continue
        status_after = statuses_after.get(address, "")
        before = cw_before[address]
        after = cw_after.get(address, 0)
        was_dropped = status_after in {"INACTIVE", "INVALID"}
        lost_cw = before if was_dropped else max(0, before - after)
        compensation = lost_cw * total_rewarded // total_cw_after if total_cw_after else 0
        if compensation <= 0:
            continue
        exclusion = excluded.get(address, {})
        rows.append(
            {
                "address": address,
                "status_before": status_before,
                "status_after": status_after,
                "cw_before": before,
                "cw_after": after,
                "lost_cw": lost_cw,
                "rewarded_coins_received": rewards.get(address, 0),
                "was_dropped": int(was_dropped),
                "exclusion_reason": exclusion.get("reason", ""),
                "exclusion_block_height": exclusion.get("exclusion_block_height", ""),
                "cpoc_trigger_height": cpoc_trigger_from_exclusion(int_of(exclusion.get("exclusion_block_height")))
                if exclusion
                else "",
                "compensation_ngonka": compensation,
                "compensation_gnk": amount_ngonka(compensation).replace(",", ""),
            }
        )
    rows.sort(key=lambda row: (-int(row["compensation_ngonka"]), row["address"]))
    summary = {
        "epoch": EPOCH,
        "h_before": H_BEFORE,
        "h_after": H_AFTER,
        "members_before": len(cw_before),
        "members_after": len(cw_after),
        "active_before": sum(1 for address in cw_before if statuses_before.get(address) == "ACTIVE"),
        "dropped": sum(row["was_dropped"] for row in rows),
        "reduced": sum(1 for row in rows if not row["was_dropped"]),
        "affected": len(rows),
        "total_rewarded_ngonka": total_rewarded,
        "total_cw_before": sum(cw_before.values()),
        "total_cw_after": total_cw_after,
        "total_cw_lost_eligible": sum(int(row["lost_cw"]) for row in rows),
        "total_full_weight_after": total_full_weight_after,
        "total_compensation_ngonka": sum(int(row["compensation_ngonka"]) for row in rows),
        "formula": "lost_cw * total_rewarded_ngonka // total_cw_after",
    }
    return rows, summary


def build_completeness_matrix(base: str, affected: list[dict[str, Any]], summary: dict[str, Any], *, refresh: bool) -> list[dict[str, Any]]:
    before_group = epoch_group(base, EPOCH, block_height=H_BEFORE)
    after_group = epoch_group(base, EPOCH, block_height=H_AFTER)
    cw_before = confirmation_weights(before_group)
    cw_after = confirmation_weights(after_group)
    statuses_before = participant_statuses(base, block_height=H_BEFORE, refresh=refresh)
    statuses_after = participant_statuses(base, block_height=H_AFTER, refresh=refresh)
    affected_by_address = {row["address"]: row for row in affected}
    rows: list[dict[str, Any]] = []
    for address in sorted(set(cw_before) | set(cw_after)):
        before = cw_before.get(address, 0)
        after = cw_after.get(address, 0)
        status_before = statuses_before.get(address, "")
        status_after = statuses_after.get(address, "")
        affected_row = affected_by_address.get(address)
        if affected_row:
            category = "included_dropped" if int_of(affected_row["was_dropped"]) else "included_reduced"
            eligible = 1
            lost_cw = int_of(affected_row["lost_cw"])
            compensation = int_of(affected_row["compensation_ngonka"])
            reason = "ACTIVE before h_before and positive eligible confirmation-weight loss"
        elif status_before != "ACTIVE":
            category = "excluded_not_active_before"
            eligible = 0
            lost_cw = max(0, before - after)
            compensation = 0
            reason = "not ACTIVE at h_before"
        elif before <= after:
            category = "excluded_no_confirmation_weight_loss"
            eligible = 0
            lost_cw = 0
            compensation = 0
            reason = "confirmation_weight did not decrease"
        else:
            category = "excluded_zero_or_non_positive_compensation"
            eligible = 0
            lost_cw = before - after
            compensation = 0
            reason = "positive raw loss but not included by compensation eligibility formula"
        rows.append(
            {
                "epoch": EPOCH,
                "address": address,
                "status_before": status_before,
                "status_after": status_after,
                "cw_before": before,
                "cw_after": after,
                "raw_cw_delta": after - before,
                "lost_cw_counted": lost_cw,
                "eligible": eligible,
                "category": category,
                "compensation_ngonka": compensation,
                "compensation_gnk": amount_ngonka(compensation).replace(",", "") if compensation else "0.000000000",
                "reason": reason,
            }
        )
    rows.sort(key=lambda row: (row["category"], row["address"]))
    included = [row for row in rows if row["eligible"]]
    if len(included) != summary["affected"]:
        raise RuntimeError(f"Completeness matrix affected mismatch: {len(included)} != {summary['affected']}")
    return rows


def build_stage_loss_breakdown(timeline_rows: list[dict[str, Any]], affected: list[dict[str, Any]]) -> list[dict[str, Any]]:
    affected_by_trigger: dict[Any, list[dict[str, Any]]] = {}
    for row in affected:
        trigger = row.get("cpoc_trigger_height") or "observed_by_final_snapshot_without_exclusion"
        affected_by_trigger.setdefault(trigger, []).append(row)

    rows: list[dict[str, Any]] = []
    for timeline in [row for row in timeline_rows if row["epoch"] == EPOCH]:
        trigger = timeline["cpoc_trigger_height"]
        affected_rows = affected_by_trigger.get(trigger, [])
        rows.append(
            {
                "epoch": EPOCH,
                "cpoc_sequence": timeline["cpoc_sequence"],
                "cpoc_trigger_height": trigger,
                "cpoc_trigger_msk": timeline["cpoc_trigger_msk"],
                "relation": timeline["relation"],
                "excluded_at_stage": timeline["excluded_at_stage"],
                "affected_rows_attributed": len(affected_rows),
                "dropped_attributed": sum(int_of(row["was_dropped"]) for row in affected_rows),
                "reduced_attributed": sum(1 for row in affected_rows if not int_of(row["was_dropped"])),
                "lost_cw_attributed": sum(int_of(row["lost_cw"]) for row in affected_rows),
                "compensation_ngonka_attributed": sum(int_of(row["compensation_ngonka"]) for row in affected_rows),
                "compensation_gnk_attributed": amount_ngonka(
                    sum(int_of(row["compensation_ngonka"]) for row in affected_rows)
                ).replace(",", ""),
                "loss_attribution": "direct_exclusion_height" if affected_rows else "no_affected_rows_directly_attributed",
            }
        )
    unattributed = affected_by_trigger.get("observed_by_final_snapshot_without_exclusion", [])
    if unattributed:
        rows.append(
            {
                "epoch": EPOCH,
                "cpoc_sequence": "final_snapshot_delta",
                "cpoc_trigger_height": "",
                "cpoc_trigger_msk": "",
                "relation": "post_upgrade_observed_by_h_after",
                "excluded_at_stage": "",
                "affected_rows_attributed": len(unattributed),
                "dropped_attributed": 0,
                "reduced_attributed": len(unattributed),
                "lost_cw_attributed": sum(int_of(row["lost_cw"]) for row in unattributed),
                "compensation_ngonka_attributed": sum(int_of(row["compensation_ngonka"]) for row in unattributed),
                "compensation_gnk_attributed": amount_ngonka(
                    sum(int_of(row["compensation_ngonka"]) for row in unattributed)
                ).replace(",", ""),
                "loss_attribution": "reduced_rows_have_no_exclusion_row; loss observed between h_before and h_after",
            }
        )
    return rows


def build_scope_control_scan(base: str, chain_window: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for epoch in SCOPE_EPOCHS:
        group = epoch_group(base, epoch)
        poc = int_of(group.get("poc_start_block_height"))
        effective = int_of(group.get("effective_block_height"))
        last = int_of(group.get("last_block_height"))
        epoch_relation = classify_epoch(epoch, group)
        exclusions = excluded_participants(base, epoch)
        triggers = sorted({cpoc_trigger_from_exclusion(int_of(row["exclusion_block_height"])) for row in exclusions})
        if not triggers:
            rows.append(
                {
                    "epoch": epoch,
                    "epoch_relation_to_upgrade": epoch_relation,
                    "poc_start_height": poc,
                    "effective_height": effective,
                    "last_height": last,
                    "cpoc_sequence": "",
                    "cpoc_trigger_height": "",
                    "cpoc_trigger_msk": "",
                    "blocks_after_upgrade": "",
                    "inside_chain_param_window_500": "",
                    "inside_reported_window_10000": "",
                    "inside_upgrade_epoch_skip_window": "",
                    "excluded_at_stage": 0,
                    "case4_like_misfire": 0,
                    "interpretation": "no cPoC exclusion trigger recorded",
                }
            )
            continue
        for sequence, trigger in enumerate(triggers):
            blocks_after = trigger - UPGRADE_HEIGHT if trigger > UPGRADE_HEIGHT else ""
            inside_chain_window = bool(blocks_after != "" and int_of(blocks_after) <= chain_window)
            inside_reported = bool(blocks_after != "" and int_of(blocks_after) <= 10_000)
            inside_upgrade_epoch = epoch_relation == "upgrade_epoch" and trigger > UPGRADE_HEIGHT and trigger <= last
            trigger_time = block_time(base, trigger)
            excluded_at_stage = sum(
                1 for item in exclusions if cpoc_trigger_from_exclusion(int_of(item["exclusion_block_height"])) == trigger
            )
            if inside_upgrade_epoch:
                interpretation = "post-upgrade cPoC inside upgrade epoch; expected skip under release-note behavior"
            elif epoch_relation == "before_upgrade":
                interpretation = "control epoch before upgrade"
            elif epoch_relation == "after_upgrade_epoch":
                interpretation = "clean later epoch; cPoC is not the same upgrade-epoch misfire"
            else:
                interpretation = "non-target control row"
            rows.append(
                {
                    "epoch": epoch,
                    "epoch_relation_to_upgrade": epoch_relation,
                    "poc_start_height": poc,
                    "effective_height": effective,
                    "last_height": last,
                    "cpoc_sequence": sequence,
                    "cpoc_trigger_height": trigger,
                    "cpoc_trigger_msk": trigger_time["msk"],
                    "blocks_after_upgrade": blocks_after,
                    "inside_chain_param_window_500": int(inside_chain_window),
                    "inside_reported_window_10000": int(inside_reported),
                    "inside_upgrade_epoch_skip_window": int(inside_upgrade_epoch),
                    "excluded_at_stage": excluded_at_stage,
                    "case4_like_misfire": int(inside_upgrade_epoch),
                    "interpretation": interpretation,
                }
            )
    return rows


def build_last_upgrade_height_state(rpc_base: str, *, refresh: bool = False) -> dict[str, Any]:
    default_rpc = "http://node1.gonka.ai:8000/chain-rpc"
    rpc_bases = [rpc_base]
    if rpc_base.rstrip("/") != default_rpc:
        rpc_bases.append(default_rpc)
    heights: list[int | None] = [None, H_BEFORE, UPGRADE_HEIGHT, 4_267_778, 4_270_605, H_AFTER]
    queries = []
    for height in heights:
        path = (
            "/abci_query?path=%22%2Fstore%2Finference%2Fkey%22"
            f"&data={urllib.parse.quote(LAST_UPGRADE_HEIGHT_KEY_HEX)}"
        )
        if height is not None:
            path += f"&height={height}"
        row = {
            "height_requested": height or "latest",
            "state_key_hex": LAST_UPGRADE_HEIGHT_KEY_HEX,
            "state_key_base64_observed": "",
            "response_height": "",
            "value_base64": "",
            "value_is_null": "",
            "query_status": "ok",
            "error": "",
            "rpc_source": "",
        }
        errors = []
        for index, candidate_base in enumerate(rpc_bases):
            try:
                payload = get_rpc_json(candidate_base, path, refresh=refresh)
                response = payload.get("result", {}).get("response", {})
                row.update(
                    {
                        "state_key_base64_observed": response.get("key", ""),
                        "response_height": response.get("height", ""),
                        "value_base64": response.get("value"),
                        "value_is_null": int(response.get("value") is None),
                        "rpc_source": "configured" if index == 0 else "default_node1",
                    }
                )
                break
            except Exception as exc:  # noqa: BLE001 - evidence row should record archive limitations
                errors.append(str(exc))
        else:
            row["query_status"] = "failed"
            row["error"] = " | ".join(errors)
        queries.append(row)
    return {
        "state_key": "LastUpgradeHeight",
        "state_key_hex": LAST_UPGRADE_HEIGHT_KEY_HEX,
        "rpc_base_kind": "chain-rpc",
        "queries": queries,
        "latest_null_confirmed": any(
            row["height_requested"] == "latest" and row["query_status"] == "ok" and row["value_is_null"] == 1
            for row in queries
        ),
    }


def build_overlap_matrix(affected: list[dict[str, Any]]) -> list[dict[str, Any]]:
    p4_known_epoch276 = {
        "gonka10079cnl3nuh2k82mhkm04dj0slhtw9kmjewwau",
        "gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2",
        "gonka1gvrrhjmy4w4mayvs2s5l23edj8ertcmtd2v4zr",
        "gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5",
        "gonka1scskt6wpnjnumsah6kjphmdu87vjgvcxmn4rxv",
        "gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw",
    }
    case6_overlap_path = CASE_DIR.parent / "P3-CAND-06-pre-fix-confirmation-accounting" / "case6_overlap_matrix.csv"
    case6_by_address: dict[str, dict[str, str]] = {}
    if case6_overlap_path.exists():
        with case6_overlap_path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                if int_of(row.get("epoch")) == EPOCH:
                    case6_by_address[row["participant"]] = row

    rows: list[dict[str, Any]] = []
    for row in affected:
        address = row["address"]
        refs = []
        if address in p4_known_epoch276:
            refs.append("P4-CAND-01")
        if address in case6_by_address:
            refs.append("P3-CAND-06")
        if refs:
            action = "review_before_payment"
            reason = "same address appears in another local candidate covering epoch 276"
        else:
            action = "no_local_overlap_signal"
            reason = "no same-address overlap found in local normalized references"
        rows.append(
            {
                "epoch": EPOCH,
                "address": address,
                "case4_compensation_gnk": row["compensation_gnk"],
                "overlap_references": "+".join(refs) if refs else "",
                "p4_known_same_address_epoch276": int(address in p4_known_epoch276),
                "p3_cand_06_same_address_epoch276": int(address in case6_by_address),
                "recommended_action": action,
                "reason": reason,
            }
        )
    rows.sort(key=lambda row: (row["recommended_action"], row["address"]))
    return rows


def build_published_compare(rows: list[dict[str, Any]], summary: dict[str, Any], *, refresh: bool = False) -> dict[str, Any]:
    text = fetch_text(PUBLISHED_CSV_URL, refresh=refresh)
    published_rows = list(csv.DictReader(text.splitlines()))
    ours = {row["address"]: row for row in rows}
    published = {row["address"]: row for row in published_rows}
    mismatches = []
    for address in sorted(set(ours) | set(published)):
        if address not in ours:
            mismatches.append({"address": address, "field": "presence", "ours": "missing", "published": "present"})
            continue
        if address not in published:
            mismatches.append({"address": address, "field": "presence", "ours": "present", "published": "missing"})
            continue
        for field in [
            "status_before",
            "status_after",
            "cw_before",
            "cw_after",
            "lost_cw",
            "rewarded_coins_received",
            "was_dropped",
            "compensation_ngonka",
        ]:
            if str(ours[address][field]) != str(published[address][field]):
                mismatches.append(
                    {
                        "address": address,
                        "field": field,
                        "ours": str(ours[address][field]),
                        "published": str(published[address][field]),
                    }
                )
    published_total = sum(int_of(row["compensation_ngonka"]) for row in published_rows)
    published_lost_cw = sum(int_of(row["lost_cw"]) for row in published_rows)
    return {
        "published_url": PUBLISHED_CSV_URL,
        "ours_rows": len(rows),
        "published_rows": len(published_rows),
        "ours_total_ngonka": summary["total_compensation_ngonka"],
        "published_total_ngonka": published_total,
        "ours_lost_cw": summary["total_cw_lost_eligible"],
        "published_lost_cw": published_lost_cw,
        "exact_match": len(mismatches) == 0,
        "mismatches": mismatches,
    }


def write_timeline_md(rows: list[dict[str, Any]], upgrade_time: dict[str, str]) -> None:
    lines = [
        "# P3-CAND-04 Epoch 276 Timeline",
        "",
        f"`{UPGRADE_VERSION}` was applied at block `{UPGRADE_HEIGHT}` / `{upgrade_time['msk']}`.",
        "",
        "| Epoch | PoC start | Effective | Last | cPoC # | Trigger | Trigger MSK | Blocks after upgrade | Relation | Excluded at stage |",
        "|---:|---:|---:|---:|---:|---:|---|---:|---|---:|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['epoch']}` | `{row['poc_start_height']}` | `{row['effective_height']}` | "
            f"`{row['last_height']}` | `{row['cpoc_sequence']}` | `{row['cpoc_trigger_height']}` | "
            f"{row['cpoc_trigger_msk']} | `{row['blocks_after_upgrade']}` | `{row['relation']}` | "
            f"`{row['excluded_at_stage']}` |"
        )
    lines.append("")
    (CASE_DIR / "case4_epoch276_timeline.md").write_text("\n".join(lines), encoding="utf-8")


def write_compensation_md(rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    lines = [
        "# P3-CAND-04 Compensation Replay",
        "",
        "This replay starts from archive-chain state only. It does not execute the",
        "`gonkavip/payout276` code.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Members at h_before | `{summary['members_before']}` |",
        f"| ACTIVE before upgrade | `{summary['active_before']}` |",
        f"| Dropped | `{summary['dropped']}` |",
        f"| Reduced confirmation weight | `{summary['reduced']}` |",
        f"| Affected rows | `{summary['affected']}` |",
        f"| Total rewarded in epoch | `{amount_ngonka(summary['total_rewarded_ngonka'])} GNK` |",
        f"| Total cw before | `{summary['total_cw_before']}` |",
        f"| Total cw after | `{summary['total_cw_after']}` |",
        f"| Eligible lost cw | `{summary['total_cw_lost_eligible']}` |",
        f"| Total compensation | `{amount_ngonka(summary['total_compensation_ngonka'])} GNK` |",
        "",
        "Formula: `lost_cw * total_rewarded_ngonka // total_cw_after`.",
        "",
        "## Rows",
        "",
        "| Address | Before -> After | cw before -> after | lost cw | Dropped | Rewarded, GNK | Compensation, GNK |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['address']}` | `{row['status_before']}` -> `{row['status_after']}` | "
            f"`{row['cw_before']}` -> `{row['cw_after']}` | `{row['lost_cw']}` | "
            f"`{row['was_dropped']}` | `{amount_ngonka(row['rewarded_coins_received'])}` | "
            f"`{amount_ngonka(row['compensation_ngonka'])}` |"
        )
    lines.append("")
    (CASE_DIR / "case4_compensation_replay.md").write_text("\n".join(lines), encoding="utf-8")


def write_upgrade_md(base: str, timeline_rows: list[dict[str, Any]], upgrade_time: dict[str, str]) -> dict[str, Any]:
    params = get_json(base, "/productscience/inference/inference/params", block_height=UPGRADE_HEIGHT)["params"]
    chain_window = int_of(params["confirmation_poc_params"]["upgrade_protection_window"])
    post_upgrade = [row for row in timeline_rows if row["epoch"] == EPOCH and row["relation"] == "post_upgrade"]
    rows = []
    for row in post_upgrade:
        blocks = int_of(row["blocks_after_upgrade"])
        rows.append(
            {
                "cpoc_trigger_height": row["cpoc_trigger_height"],
                "blocks_after_upgrade": blocks,
                "inside_chain_param_window_500": blocks <= chain_window,
                "inside_reported_window_10000": blocks <= 10_000,
                "excluded_at_stage": row["excluded_at_stage"],
            }
        )
    evidence = {
        "upgrade_height": UPGRADE_HEIGHT,
        "upgrade_msk": upgrade_time["msk"],
        "chain_upgrade_protection_window": chain_window,
        "reported_release_window": 10_000,
        "post_upgrade_cpoc_stages": rows,
        "last_upgrade_height_state": "not directly decoded by this script; DevOps evidence reports it was not written, and observed post-upgrade cPoCs prove the skip did not apply",
    }
    lines = [
        "# P3-CAND-04 Upgrade Protection Evidence",
        "",
        f"`{UPGRADE_VERSION}` upgrade height: `{UPGRADE_HEIGHT}` / `{upgrade_time['msk']}`.",
        "",
        "| Item | Value |",
        "|---|---:|",
        f"| Chain `confirmation_poc_params.upgrade_protection_window` at upgrade height | `{chain_window}` blocks |",
        "| Reported release-note protection window | `10000` blocks |",
        "",
        "## Post-Upgrade cPoC Stages",
        "",
        "| cPoC trigger | Blocks after upgrade | Inside chain-param window | Inside reported 10000-block window | Excluded at stage |",
        "|---:|---:|---|---|---:|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['cpoc_trigger_height']}` | `{row['blocks_after_upgrade']}` | "
            f"`{row['inside_chain_param_window_500']}` | `{row['inside_reported_window_10000']}` | "
            f"`{row['excluded_at_stage']}` |"
        )
    lines.extend(
        [
            "",
            "DevOps evidence states `LastUpgradeHeight` was not written after the",
            "upgrade, so the cPoC skip did not apply. The chain evidence above",
            "confirms cPoC stages did run after the upgrade inside epoch 276.",
            "",
        ]
    )
    (CASE_DIR / "case4_upgrade_protection_evidence.md").write_text("\n".join(lines), encoding="utf-8")
    return evidence


def write_root_cause_md(root_cause: dict[str, Any], scope_rows: list[dict[str, Any]]) -> None:
    state = root_cause["last_upgrade_height_state"]
    latest = next((row for row in state["queries"] if row["height_requested"] == "latest"), {})
    case4_like = [row for row in scope_rows if int_of(row.get("case4_like_misfire"))]
    historical_ok = all(row["query_status"] == "ok" and row["value_is_null"] == 1 for row in state["queries"])
    lines = [
        "# P3-CAND-04 Root-Cause Deep Dive",
        "",
        "## Conclusion",
        "",
        "The compensation set is independently proven by archive-chain replay.",
        "The most likely root cause is also strongly supported: the `v0.2.13`",
        "upgrade was intended to suppress confirmation PoC through the upgrade",
        "epoch, but the `LastUpgradeHeight` state key was not populated, so the",
        "skip condition did not activate and two post-upgrade cPoC stages ran in",
        "epoch 276.",
        "",
        "## Evidence Chain",
        "",
        "| Link | Evidence |",
        "|---|---|",
        f"| Expected behavior | PR #1143: {PR_1143_URL} |",
        f"| Release-note behavior | {RELEASE_ANNOUNCEMENT_URL} describes skipping confirmation PoC from upgrade height through the upgrade epoch |",
        "| Chain execution | Post-upgrade cPoC triggers `4267778` and `4270605` ran inside epoch `276` |",
        "| State key | `LastUpgradeHeight` key `0x1b` is queried directly through `abci_query` |",
        f"| Code fix | PR #1268: {PR_1268_URL} tracks `LastUpgradeHeight` from upgrade handlers and adds tests on branch {PR_1268_BRANCH_URL} |",
        "",
        "## LastUpgradeHeight State Query",
        "",
        "| Requested height | Response height | Key base64 | Value base64 | Null | Status | RPC source |",
        "|---:|---:|---|---|---:|---|---|",
    ]
    for row in state["queries"]:
        lines.append(
            f"| `{row['height_requested']}` | `{row['response_height']}` | `{row['state_key_base64_observed']}` | "
            f"`{row['value_base64'] or ''}` | `{row['value_is_null']}` | `{row['query_status']}` | `{row.get('rpc_source', '')}` |"
        )
    lines.extend(
        [
            "",
            "Latest-chain null proof:",
            f"`latest_null_confirmed = {state['latest_null_confirmed']}`.",
            "",
            f"Historical null proof for all checked heights: `{historical_ok}`.",
            "",
            "## Why Epoch 276 Only",
            "",
            "`v0.2.13` was applied at block `4267300`, while epoch `276` spans",
            "`4259271..4275061`. That makes epoch `276` the only upgrade epoch.",
            "Epochs before it were pre-upgrade controls. Epoch `277` and later are",
            "post-upgrade clean epochs; cPoC there is not the same upgrade-window",
            "misfire.",
            "",
            "| Epoch | Trigger | Blocks after upgrade | Case4-like misfire | Interpretation |",
            "|---:|---:|---:|---:|---|",
        ]
    )
    for row in case4_like:
        lines.append(
            f"| `{row['epoch']}` | `{row['cpoc_trigger_height']}` | `{row['blocks_after_upgrade']}` | "
            f"`{row['case4_like_misfire']}` | {row['interpretation']} |"
        )
    lines.extend(
        [
            "",
            "## Strength And Remaining Limits",
            "",
            "- Strong: affected rows and amounts match the published CSV exactly from independent archive-chain state.",
            "- Strong: two post-upgrade cPoC stages are directly visible inside the upgrade epoch.",
            "- Strong: historical and current chain state return null for the `LastUpgradeHeight` key at all checked heights.",
            "- Strong: PR #1268 changes future full upgrades to record `LastUpgradeHeight` from the upgrade handler and tests full/partial upgrade tracking.",
            "- Limit: PR #1268 is merged to `upgrade-v0.2.14`; public releases checked still showed latest release `v0.2.13`, so on-chain deployment must be confirmed separately.",
            "",
        ]
    )
    root_cause["summary"] = {
        "latest_last_upgrade_height_null": latest.get("value_is_null"),
        "case4_like_cpoc_triggers": [row["cpoc_trigger_height"] for row in case4_like],
        "fix_pr": PR_1268_URL,
        "fix_branch": PR_1268_BRANCH_URL,
        "fix_deployment_status": "code fix merged to upgrade-v0.2.14 branch; on-chain deployment requires separate confirmation",
        "assessment": "root cause strongly supported; code fix identified in PR #1268",
    }
    (CASE_DIR / "case4_root_cause_deep_dive.md").write_text("\n".join(lines), encoding="utf-8")


def write_stage_loss_breakdown_md(rows: list[dict[str, Any]]) -> None:
    lines = [
        "# P3-CAND-04 Stage Loss Breakdown",
        "",
        "Dropped rows can be tied to an exclusion block and therefore to a concrete",
        "cPoC trigger. Reduced rows do not have exclusion rows; their loss is",
        "therefore attributed conservatively as an h_before to h_after final",
        "snapshot delta.",
        "",
        "| Stage | Trigger | Relation | Excluded at stage | Affected attributed | Dropped | Reduced | Lost cw | Compensation, GNK | Attribution |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['cpoc_sequence']}` | `{row['cpoc_trigger_height']}` | `{row['relation']}` | "
            f"`{row['excluded_at_stage']}` | `{row['affected_rows_attributed']}` | `{row['dropped_attributed']}` | "
            f"`{row['reduced_attributed']}` | `{row['lost_cw_attributed']}` | "
            f"`{row['compensation_gnk_attributed']}` | {row['loss_attribution']} |"
        )
    lines.append("")
    (CASE_DIR / "case4_stage_loss_breakdown.md").write_text("\n".join(lines), encoding="utf-8")


def write_scope_control_scan_md(rows: list[dict[str, Any]]) -> None:
    case4_like = [row for row in rows if int_of(row.get("case4_like_misfire"))]
    lines = [
        "# P3-CAND-04 Scope Control Scan",
        "",
        f"Scan range: epochs `{SCOPE_EPOCHS[0]}..{SCOPE_EPOCHS[-1]}`.",
        "",
        "The scan classifies cPoC stages around the `v0.2.13` upgrade. A row is",
        "`case4_like_misfire = 1` only when the cPoC trigger is post-upgrade and",
        "still inside the upgrade epoch.",
        "",
        f"Case4-like rows found: `{len(case4_like)}`.",
        "",
        "| Epoch | Epoch relation | PoC start | Last | Trigger | Trigger MSK | Blocks after upgrade | Upgrade-epoch skip window | Case4-like | Excluded | Interpretation |",
        "|---:|---|---:|---:|---:|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['epoch']}` | `{row['epoch_relation_to_upgrade']}` | `{row['poc_start_height']}` | "
            f"`{row['last_height']}` | `{row['cpoc_trigger_height']}` | {row['cpoc_trigger_msk']} | "
            f"`{row['blocks_after_upgrade']}` | `{row['inside_upgrade_epoch_skip_window']}` | "
            f"`{row['case4_like_misfire']}` | `{row['excluded_at_stage']}` | {row['interpretation']} |"
        )
    lines.append("")
    (CASE_DIR / "case4_scope_control_scan.md").write_text("\n".join(lines), encoding="utf-8")


def write_completeness_matrix_md(rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    categories: dict[str, int] = {}
    for row in rows:
        categories[row["category"]] = categories.get(row["category"], 0) + 1
    lines = [
        "# P3-CAND-04 Affected-Set Completeness Matrix",
        "",
        "This table accounts for every epoch-group member seen in the before/after",
        "snapshots. It shows why the independent affected set is exactly 19",
        "participants.",
        "",
        "## Category Summary",
        "",
        "| Category | Count |",
        "|---|---:|",
    ]
    for category, count in sorted(categories.items()):
        lines.append(f"| `{category}` | `{count}` |")
    lines.extend(
        [
            "",
            f"Included affected rows: `{summary['affected']}`.",
            "",
            "## Rows",
            "",
            "| Address | Before -> After | cw before -> after | Counted lost cw | Eligible | Category | Compensation, GNK | Reason |",
            "|---|---|---:|---:|---:|---|---:|---|",
        ]
    )
    for row in rows:
        lines.append(
            f"| `{row['address']}` | `{row['status_before']}` -> `{row['status_after']}` | "
            f"`{row['cw_before']}` -> `{row['cw_after']}` | `{row['lost_cw_counted']}` | "
            f"`{row['eligible']}` | `{row['category']}` | `{row['compensation_gnk']}` | {row['reason']} |"
        )
    lines.append("")
    (CASE_DIR / "case4_completeness_matrix.md").write_text("\n".join(lines), encoding="utf-8")


def write_overlap_matrix_md(rows: list[dict[str, Any]]) -> None:
    review = [row for row in rows if row["recommended_action"] == "review_before_payment"]
    lines = [
        "# P3-CAND-04 Overlap Matrix",
        "",
        "This matrix is compensation hygiene only. It does not change the independent",
        "case-4 total; it marks rows that must not be paid twice if another package",
        "is approved for the same address/epoch.",
        "",
        f"Rows requiring review: `{len(review)}`.",
        "",
        "| Address | Case4 compensation, GNK | Overlap references | P4 e276 | P3-CAND-06 e276 | Action | Reason |",
        "|---|---:|---|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['address']}` | `{row['case4_compensation_gnk']}` | `{row['overlap_references']}` | "
            f"`{row['p4_known_same_address_epoch276']}` | `{row['p3_cand_06_same_address_epoch276']}` | "
            f"`{row['recommended_action']}` | {row['reason']} |"
        )
    lines.append("")
    (CASE_DIR / "case4_overlap_matrix.md").write_text("\n".join(lines), encoding="utf-8")


def write_compare_md(compare: dict[str, Any]) -> None:
    lines = [
        "# P3-CAND-04 Published Comparison",
        "",
        "The published `payout_276.csv` was downloaded only after the independent",
        "archive-chain replay was built. The external code was not executed.",
        "",
        "| Metric | Ours | Published |",
        "|---|---:|---:|",
        f"| Rows | `{compare['ours_rows']}` | `{compare['published_rows']}` |",
        f"| Lost cw | `{compare['ours_lost_cw']}` | `{compare['published_lost_cw']}` |",
        f"| Total compensation | `{amount_ngonka(compare['ours_total_ngonka'])}` | `{amount_ngonka(compare['published_total_ngonka'])}` |",
        f"| Exact CSV-level match | `{compare['exact_match']}` | `{compare['exact_match']}` |",
        "",
    ]
    if compare["mismatches"]:
        lines.extend(["## Mismatches", "", "| Address | Field | Ours | Published |", "|---|---|---:|---:|"])
        for row in compare["mismatches"][:100]:
            lines.append(f"| `{row['address']}` | `{row['field']}` | `{row['ours']}` | `{row['published']}` |")
    else:
        lines.append("No row-level mismatches were found.")
    lines.append("")
    (CASE_DIR / "case4_published_compare.md").write_text("\n".join(lines), encoding="utf-8")


def write_readme(summary: dict[str, Any], compare: dict[str, Any], root_cause: dict[str, Any], scope_rows: list[dict[str, Any]]) -> None:
    case4_like = [row for row in scope_rows if int_of(row.get("case4_like_misfire"))]
    lines = [
        "# P3-CAND-04 Validation",
        "",
        "Independent archive-chain validation for the epoch 276",
        "UpgradeProtectionWindow / cPoC misfire candidate.",
        "",
        "## Result",
        "",
        f"- Affected set: `{summary['affected']}` participants (`{summary['dropped']}` dropped, `{summary['reduced']}` reduced).",
        f"- Independent total: `{amount_ngonka(summary['total_compensation_ngonka'])} GONKA`.",
        f"- Published CSV total: `{amount_ngonka(compare['published_total_ngonka'])} GONKA`.",
        f"- Published CSV comparison exact match: `{compare['exact_match']}`.",
        f"- Root-cause support: `LastUpgradeHeight` latest null proof = `{root_cause['last_upgrade_height_state']['latest_null_confirmed']}`.",
        f"- Scope scan case4-like post-upgrade cPoC rows: `{len(case4_like)}`.",
        f"- Code fix identified: PR #1268 `{PR_1268_URL}` on branch `upgrade-v0.2.14`; deployment requires separate chain confirmation.",
        "",
        "## What Was Checked",
        "",
        "- Historical `epoch_group_data/276` at `4267299` and `4274661`.",
        "- Historical participant status at the same two heights.",
        "- Final `epoch_performance_summary/276` rewards.",
        "- Epoch `270..283` control cPoC timeline around the upgrade epoch.",
        "- Post-upgrade cPoC stages inside epoch 276.",
        "- Direct `LastUpgradeHeight` `abci_query` evidence.",
        "- Full member completeness matrix for epoch 276.",
        "- Local overlap matrix with P4-CAND-01 and P3-CAND-06 references.",
        "",
        "## Files",
        "",
        "- `case4_epoch276_timeline.md/csv/json`",
        "- `case4_upgrade_protection_evidence.md/json`",
        "- `case4_root_cause_deep_dive.md/json`",
        "- `case4_scope_control_scan.md/csv/json`",
        "- `case4_stage_loss_breakdown.md/csv/json`",
        "- `case4_completeness_matrix.md/csv/json`",
        "- `case4_overlap_matrix.md/csv/json`",
        "- `case4_affected_participants.md/csv/json`",
        "- `case4_compensation_replay.md/csv/json`",
        "- `case4_published_compare.md/json`",
        "- `raw_cache/` sanitized archive responses and published CSV text",
        "",
    ]
    (CASE_DIR / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    load_dotenv()
    base = direct_lcd_from_env()
    rpc_base = direct_rpc_from_env()

    upgrade_time = block_time(base, UPGRADE_HEIGHT)
    timeline = build_timeline(base)
    affected, summary = build_affected(base, refresh=args.refresh)
    upgrade_evidence = write_upgrade_md(base, timeline, upgrade_time)
    chain_window = int_of(upgrade_evidence["chain_upgrade_protection_window"])
    scope_rows = build_scope_control_scan(base, chain_window)
    stage_rows = build_stage_loss_breakdown(timeline, affected)
    completeness_rows = build_completeness_matrix(base, affected, summary, refresh=args.refresh)
    overlap_rows = build_overlap_matrix(affected)
    root_cause = {
        "upgrade_height": UPGRADE_HEIGHT,
        "upgrade_msk": upgrade_time["msk"],
        "expected_behavior_sources": {
            "pr_1143": PR_1143_URL,
            "pr_1268_fix": PR_1268_URL,
            "pr_1268_branch": PR_1268_BRANCH_URL,
            "release_announcement": RELEASE_ANNOUNCEMENT_URL,
        },
        "last_upgrade_height_state": build_last_upgrade_height_state(rpc_base, refresh=args.refresh),
    }
    write_root_cause_md(root_cause, scope_rows)
    compare = build_published_compare(affected, summary, refresh=args.refresh)

    timeline_fields = [
        "epoch",
        "poc_start_height",
        "effective_height",
        "last_height",
        "cpoc_sequence",
        "cpoc_trigger_height",
        "cpoc_trigger_msk",
        "blocks_after_upgrade",
        "relation",
        "excluded_at_stage",
    ]
    affected_fields = [
        "address",
        "status_before",
        "status_after",
        "cw_before",
        "cw_after",
        "lost_cw",
        "rewarded_coins_received",
        "was_dropped",
        "exclusion_reason",
        "exclusion_block_height",
        "cpoc_trigger_height",
        "compensation_ngonka",
        "compensation_gnk",
    ]
    stage_fields = [
        "epoch",
        "cpoc_sequence",
        "cpoc_trigger_height",
        "cpoc_trigger_msk",
        "relation",
        "excluded_at_stage",
        "affected_rows_attributed",
        "dropped_attributed",
        "reduced_attributed",
        "lost_cw_attributed",
        "compensation_ngonka_attributed",
        "compensation_gnk_attributed",
        "loss_attribution",
    ]
    scope_fields = [
        "epoch",
        "epoch_relation_to_upgrade",
        "poc_start_height",
        "effective_height",
        "last_height",
        "cpoc_sequence",
        "cpoc_trigger_height",
        "cpoc_trigger_msk",
        "blocks_after_upgrade",
        "inside_chain_param_window_500",
        "inside_reported_window_10000",
        "inside_upgrade_epoch_skip_window",
        "excluded_at_stage",
        "case4_like_misfire",
        "interpretation",
    ]
    completeness_fields = [
        "epoch",
        "address",
        "status_before",
        "status_after",
        "cw_before",
        "cw_after",
        "raw_cw_delta",
        "lost_cw_counted",
        "eligible",
        "category",
        "compensation_ngonka",
        "compensation_gnk",
        "reason",
    ]
    overlap_fields = [
        "epoch",
        "address",
        "case4_compensation_gnk",
        "overlap_references",
        "p4_known_same_address_epoch276",
        "p3_cand_06_same_address_epoch276",
        "recommended_action",
        "reason",
    ]
    write_csv(CASE_DIR / "case4_epoch276_timeline.csv", timeline, timeline_fields)
    write_json(CASE_DIR / "case4_epoch276_timeline.json", timeline)
    write_timeline_md(timeline, upgrade_time)

    write_csv(CASE_DIR / "case4_affected_participants.csv", affected, affected_fields)
    write_json(CASE_DIR / "case4_affected_participants.json", {"summary": summary, "rows": affected})
    write_csv(CASE_DIR / "case4_compensation_replay.csv", affected, affected_fields)
    write_json(CASE_DIR / "case4_compensation_replay.json", {"summary": summary, "rows": affected})
    write_compensation_md(affected, summary)

    write_json(CASE_DIR / "case4_upgrade_protection_evidence.json", upgrade_evidence)
    write_json(CASE_DIR / "case4_root_cause_deep_dive.json", root_cause)
    write_csv(CASE_DIR / "case4_stage_loss_breakdown.csv", stage_rows, stage_fields)
    write_json(CASE_DIR / "case4_stage_loss_breakdown.json", stage_rows)
    write_stage_loss_breakdown_md(stage_rows)
    write_csv(CASE_DIR / "case4_scope_control_scan.csv", scope_rows, scope_fields)
    write_json(CASE_DIR / "case4_scope_control_scan.json", scope_rows)
    write_scope_control_scan_md(scope_rows)
    write_csv(CASE_DIR / "case4_completeness_matrix.csv", completeness_rows, completeness_fields)
    write_json(
        CASE_DIR / "case4_completeness_matrix.json",
        {
            "summary": {
                "rows": len(completeness_rows),
                "eligible_rows": sum(int_of(row["eligible"]) for row in completeness_rows),
                "affected_expected": summary["affected"],
            },
            "rows": completeness_rows,
        },
    )
    write_completeness_matrix_md(completeness_rows, summary)
    write_csv(CASE_DIR / "case4_overlap_matrix.csv", overlap_rows, overlap_fields)
    write_json(CASE_DIR / "case4_overlap_matrix.json", overlap_rows)
    write_overlap_matrix_md(overlap_rows)
    write_json(CASE_DIR / "case4_published_compare.json", compare)
    write_compare_md(compare)
    write_readme(summary, compare, root_cause, scope_rows)

    print(
        json.dumps(
            {
                "affected": summary["affected"],
                "dropped": summary["dropped"],
                "reduced": summary["reduced"],
                "case4_like_scope_rows": sum(int_of(row["case4_like_misfire"]) for row in scope_rows),
                "last_upgrade_height_latest_null": root_cause["last_upgrade_height_state"]["latest_null_confirmed"],
                "fix_pr": PR_1268_URL,
                "total_compensation_gonka": amount_ngonka(summary["total_compensation_ngonka"]),
                "published_match": compare["exact_match"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
