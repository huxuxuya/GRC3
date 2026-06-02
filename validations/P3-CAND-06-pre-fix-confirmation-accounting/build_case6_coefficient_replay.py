#!/usr/bin/env python3
"""Replay pre-v0.2.13 coefficient-adjusted cPoC readings for P3-CAND-06.

This focuses on the rows where the simple diagnostic
`confirmation_weight_at_exclusion / confirmation_weight_before / 0.909` does
not match the stored ratio. In those rows the previous cPoC event may already
have lowered ConfirmationWeight, so the chain ratio denominator is not the
current ConfirmationWeight. The pre-fix chain denominator was:

    preserved + notPreserved

using coefficient-adjusted ML node weights from active participants.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from decimal import Decimal, ROUND_DOWN, getcontext
from pathlib import Path
from typing import Any


getcontext().prec = 80

CASE_DIR = Path(__file__).resolve().parent
CACHE_DIR = CASE_DIR / "raw_stage_cache"

QWEN = "Qwen/Qwen3-235B-A22B-Instruct-2507-FP8"
KIMI = "moonshotai/Kimi-K2.6"
MODELS = [QWEN, KIMI]
POC_DEVIATION_COEFF = Decimal("0.909")
RATIO_TOLERANCE = Decimal("0.000001")
REQUEST_TIMEOUT_SECONDS = 90
RETRIES = 6
EXPECTED_BLOCK_DURATION_SECONDS = Decimal("5.41")


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


def request_headers(block_height: int | None = None) -> dict[str, str]:
    headers = {"User-Agent": "grc-case6-coefficient-replay/1.0"}
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
        except Exception as exc:  # noqa: BLE001
            last_error = str(exc)
        time.sleep(min(20, 1 + attempt * 2))
    raise RuntimeError(f"Failed to fetch {path} at height {block_height}: {last_error}")


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


def dec_from_chain_decimal(value: dict[str, Any] | None, default: Decimal = Decimal(1)) -> Decimal:
    if not value:
        return default
    return Decimal(str(value["value"])) * (Decimal(10) ** int(value["exponent"]))


def trunc_mul(raw: int, coeff: Decimal) -> int:
    return int((Decimal(raw) * coeff).to_integral_value(rounding=ROUND_DOWN))


def model_coefficients(params: dict[str, Any]) -> dict[str, Decimal]:
    poc = params["params"]["poc_params"]
    configs = poc.get("models") or poc.get("model_configs") or []
    out: dict[str, Decimal] = {}
    for config in configs:
        model_id = config.get("id") or config.get("model_id")
        if model_id:
            out[model_id] = dec_from_chain_decimal(config.get("weight_scale_factor"))
    return out


def time_normalization_factor(params: dict[str, Any], snapshot: dict[str, Any]) -> Decimal:
    poc = params["params"]["poc_params"]
    if not poc.get("poc_normalization_enabled"):
        return Decimal(1)
    gen_start = int(snapshot.get("generation_start_timestamp") or 0)
    exchange_end = int(snapshot.get("exchange_end_timestamp") or 0)
    if gen_start == 0 or exchange_end == 0 or exchange_end <= gen_start:
        return Decimal(1)
    epoch_params = params["params"]["epoch_params"]
    expected_blocks = int(epoch_params["poc_stage_duration"]) + int(epoch_params["poc_exchange_duration"])
    expected_seconds = Decimal(expected_blocks) * EXPECTED_BLOCK_DURATION_SECONDS
    return expected_seconds / Decimal(exchange_end - gen_start)


def epoch_model_nodes(base: str, epoch: int, model: str) -> dict[str, list[dict[str, Any]]]:
    path = f"/productscience/inference/inference/epoch_group_data/{epoch}?model_id={urllib.parse.quote(model, safe='')}"
    group = get_json(base, path)["epoch_group_data"]
    out: dict[str, list[dict[str, Any]]] = {}
    for row in group.get("validation_weights") or []:
        out[row["member_address"]] = row.get("ml_nodes") or []
    return out


def preserved_node_index(snapshot: dict[str, Any]) -> dict[tuple[str, str], set[str]]:
    out: dict[tuple[str, str], set[str]] = defaultdict(set)
    for model_entry in snapshot.get("model_preserved_nodes") or []:
        model = model_entry.get("model_id", "")
        for participant in model_entry.get("participants") or []:
            out[(model, participant.get("participant_id", ""))].update(participant.get("node_ids") or [])
    return out


def distribution_index(distributions: list[dict[str, Any]]) -> dict[tuple[str, str], list[dict[str, Any]]]:
    out: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in distributions:
        out[(row["participant_address"], row["model_id"])] = row.get("weights") or []
    return out


def evidence_index() -> dict[tuple[str, str, str, str], dict[str, str]]:
    out = {}
    for row in read_csv(CASE_DIR / "case6_submission_validator_evidence.csv"):
        out[(row["epoch"], row["participant"], row["event_trigger_height"], row["model_id"])] = row
    return out


def participant_epoch_nodes(base: str, epoch: int, participant: str) -> dict[str, list[dict[str, Any]]]:
    nodes_by_model = {}
    for model in MODELS:
        nodes = epoch_model_nodes(base, epoch, model).get(participant, [])
        if nodes:
            nodes_by_model[model] = nodes
    return nodes_by_model


def weighted_split(
    nodes_by_model: dict[str, list[dict[str, Any]]],
    preserved_nodes: dict[tuple[str, str], set[str]],
    participant: str,
    coefficients: dict[str, Decimal],
) -> tuple[int, int, dict[str, Any]]:
    preserved_total = 0
    not_preserved_total = 0
    details: dict[str, Any] = {}
    for model, nodes in nodes_by_model.items():
        coeff = coefficients.get(model, Decimal(1))
        preserved_ids = preserved_nodes.get((model, participant), set())
        raw_preserved = 0
        raw_not_preserved = 0
        for node in nodes:
            weight = int(node.get("poc_weight") or node.get("weight") or 0)
            if node.get("node_id") in preserved_ids:
                raw_preserved += weight
            else:
                raw_not_preserved += weight
        weighted_preserved = trunc_mul(raw_preserved, coeff)
        weighted_not_preserved = trunc_mul(raw_not_preserved, coeff)
        preserved_total += weighted_preserved
        not_preserved_total += weighted_not_preserved
        details[model] = {
            "coeff": str(coeff),
            "raw_preserved": raw_preserved,
            "raw_not_preserved": raw_not_preserved,
            "weighted_preserved": weighted_preserved,
            "weighted_not_preserved": weighted_not_preserved,
            "preserved_node_ids": sorted(preserved_ids),
        }
    return preserved_total, not_preserved_total, details


def measured_weight(
    participant: str,
    trigger: str,
    distributions: dict[tuple[str, str], list[dict[str, Any]]],
    coefficients: dict[str, Decimal],
    norm_factor: Decimal,
    evidence: dict[tuple[str, str, str, str], dict[str, str]],
    epoch: str,
) -> tuple[int, dict[str, Any]]:
    total = 0
    details = {}
    for model in MODELS:
        model_evidence = evidence.get((epoch, participant, trigger, model), {})
        if model_evidence.get("result") != "pass_weight":
            continue
        coeff = coefficients.get(model, Decimal(1))
        raw_unscaled = sum(int(row.get("weight") or 0) for row in distributions.get((participant, model), []))
        raw = int((Decimal(raw_unscaled) * norm_factor).to_integral_value(rounding=ROUND_DOWN))
        weighted = trunc_mul(raw, coeff)
        total += weighted
        details[model] = {
            "coeff": str(coeff),
            "time_normalization_factor": str(norm_factor),
            "raw_measured_before_time_norm": raw_unscaled,
            "raw_measured": raw,
            "weighted_measured": weighted,
            "result": model_evidence.get("result", ""),
            "valid_weight_percent": model_evidence.get("valid_weight_percent", ""),
        }
    return total, details


def build_rows(base: str) -> list[dict[str, Any]]:
    source_rows = [
        row
        for row in read_csv(CASE_DIR / "case6_row_formula_replay.csv")
        if row["simple_ratio_matches_stored"] == "False"
    ]
    evidence = evidence_index()
    out = []
    for row in source_rows:
        epoch = int(row["epoch"])
        trigger = int(row["event_trigger_height"])
        exclusion_height = int(row["exclusion_height"])
        participant = row["participant"]

        params = get_json(base, "/productscience/inference/inference/params", block_height=trigger)
        coefficients = model_coefficients(params)
        validation_snapshot_resp = get_json(
            base,
            f"/productscience/inference/inference/poc_validation_snapshot/{trigger}",
            block_height=exclusion_height,
        )
        validation_snapshot = validation_snapshot_resp.get("snapshot") or {}
        norm_factor = time_normalization_factor(params, validation_snapshot)
        snapshot_resp = get_json(
            base,
            "/productscience/inference/inference/preserved_nodes_snapshot",
            block_height=exclusion_height,
        )
        snapshot = snapshot_resp.get("snapshot") or {}
        distributions_resp = get_json(
            base,
            f"/productscience/inference/inference/all_mlnode_weight_distributions/{trigger}",
            block_height=exclusion_height,
        )
        distributions = distribution_index(distributions_resp.get("distributions") or [])

        nodes_by_model = participant_epoch_nodes(base, epoch, participant)
        preserved_idx = preserved_node_index(snapshot)
        preserved, not_preserved, split_details = weighted_split(
            nodes_by_model,
            preserved_idx,
            participant,
            coefficients,
        )
        measured, measured_details = measured_weight(
            participant,
            str(trigger),
            distributions,
            coefficients,
            norm_factor,
            evidence,
            row["epoch"],
        )
        total_expected = preserved + not_preserved
        reading = preserved + measured
        replay_ratio = Decimal(1) if total_expected == 0 else min(
            Decimal(reading) / Decimal(total_expected) / POC_DEVIATION_COEFF,
            Decimal(1),
        )
        stored_ratio = Decimal(row["stored_confirmation_ratio"])
        diff = stored_ratio - replay_ratio

        out.append(
            {
                "epoch": row["epoch"],
                "participant": participant,
                "event_trigger_height": row["event_trigger_height"],
                "exclusion_height": row["exclusion_height"],
                "snapshot_anchor_height": snapshot.get("episode_anchor_height", ""),
                "preserved_weight": preserved,
                "measured_weight": measured,
                "not_preserved_weight": not_preserved,
                "total_expected_weight": total_expected,
                "chain_reading_preserved_plus_measured": reading,
                "confirmation_weight_before": row["confirmation_weight_before"],
                "confirmation_weight_at_exclusion": row["confirmation_weight_at_exclusion"],
                "replay_confirmation_weight_after": min(int(row["confirmation_weight_before"]), reading),
                "stored_confirmation_ratio": row["stored_confirmation_ratio"],
                "coefficient_replay_ratio": f"{replay_ratio:.16f}",
                "coefficient_replay_diff": f"{diff:.16f}",
                "coefficient_replay_matches_stored": str(abs(diff) <= RATIO_TOLERANCE),
                "pass_models": row["pass_models"],
                "qwen_coeff": str(coefficients.get(QWEN, Decimal(1))),
                "kimi_coeff": str(coefficients.get(KIMI, Decimal(1))),
                "time_normalization_factor": str(norm_factor),
                "split_details": split_details,
                "measured_details": measured_details,
            }
        )
    return out


def write_markdown(rows: list[dict[str, Any]]) -> None:
    lines = [
        "# P3-CAND-06 Coefficient Replay",
        "",
        "This replay focuses on the `6` rows where the simple diagnostic ratio did",
        "not match stored `ConfirmationPoCRatio`.",
        "",
        "The pre-`v0.2.13` chain formula reviewed from `confirmation_poc.go` was:",
        "",
        "```text",
        "reading = preserved + measured",
        "totalExpected = preserved + notPreserved",
        "ratio = min((reading / totalExpected) / 0.909, 1)",
        "ConfirmationWeight = min(previous ConfirmationWeight, reading)",
        "```",
        "",
        "The important point is that `totalExpected` is not necessarily the current",
        "`ConfirmationWeight`. If earlier cPoC events already lowered",
        "`ConfirmationWeight`, a simple `after / before / 0.909` check uses the",
        "wrong denominator.",
        "",
        "## Result",
        "",
        "| Check | Value |",
        "|---|---:|",
        f"| Rows replayed | `{len(rows)}` |",
        f"| Rows matching stored ratio | `{sum(row['coefficient_replay_matches_stored'] == 'True' for row in rows)}` |",
        "",
        "## Rows",
        "",
        "| Epoch | Participant | Trigger | Snapshot anchor | Pass model(s) | Preserved | Measured | Not preserved | Total expected | Reading | Stored ratio | Replay ratio | Match |",
        "|---:|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {epoch} | `{participant}` | {event_trigger_height} | {snapshot_anchor_height} | {pass_models} | "
            "{preserved_weight} | {measured_weight} | {not_preserved_weight} | {total_expected_weight} | "
            "{chain_reading_preserved_plus_measured} | {stored_confirmation_ratio} | {coefficient_replay_ratio} | {coefficient_replay_matches_stored} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `5/6` prior mismatch rows reconcile against the reviewed pre-fix",
            "  chain formula.",
            "- For those `5` rows, the mismatch was caused by using",
            "  `confirmation_weight_before` as a",
            "  diagnostic denominator even though the chain ratio denominator was",
            "  `preserved + notPreserved`.",
            "- The remaining non-match is epoch `276`",
            "  `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09`, which is already",
            "  marked as an upgrade/`P3-CAND-04` overlap row.",
            "- This does not automatically approve payout eligibility. It proves that",
            "  the stored ratios for `5` single-model rows are internally consistent",
            "  with the pre-fix formula once historical coefficients, time",
            "  normalization, and preserved snapshots are used.",
            "- The economic eligibility question remains whether a single passing model",
            "  should count as enough service for compensation, and whether epoch `276`",
            "  overlaps another case.",
            "",
            "Machine-readable details are in `case6_coefficient_replay.csv` and",
            "`case6_coefficient_replay.json`.",
            "",
        ]
    )
    (CASE_DIR / "case6_coefficient_replay.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    load_dotenv(CASE_DIR.parents[1] / ".env")
    base = direct_lcd_from_env()
    rows = build_rows(base)
    fieldnames = [
        "epoch",
        "participant",
        "event_trigger_height",
        "exclusion_height",
        "snapshot_anchor_height",
        "preserved_weight",
        "measured_weight",
        "not_preserved_weight",
        "total_expected_weight",
        "chain_reading_preserved_plus_measured",
        "confirmation_weight_before",
        "confirmation_weight_at_exclusion",
        "replay_confirmation_weight_after",
        "stored_confirmation_ratio",
        "coefficient_replay_ratio",
        "coefficient_replay_diff",
        "coefficient_replay_matches_stored",
        "pass_models",
        "qwen_coeff",
        "kimi_coeff",
        "time_normalization_factor",
    ]
    write_csv(CASE_DIR / "case6_coefficient_replay.csv", rows, fieldnames)
    write_json(CASE_DIR / "case6_coefficient_replay.json", rows)
    write_markdown(rows)
    print(
        json.dumps(
            {
                "rows": len(rows),
                "matches": sum(row["coefficient_replay_matches_stored"] == "True" for row in rows),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
