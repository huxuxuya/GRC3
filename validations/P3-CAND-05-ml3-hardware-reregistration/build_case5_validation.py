#!/usr/bin/env python3
"""Independent archive reconstruction for P3-CAND-05.

This script intentionally does not import or execute any prior case solution.
It fetches chain LCD endpoints directly and emits normalized evidence tables.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "validations" / "P3-CAND-05-ml3-hardware-reregistration"
RAW = OUT / "raw_cache"

CLAIMANT = "gonka15munkmx6x7k6rqqeexjet4556p7at39ks9qgr5"
NODE_UNDER_CLAIM = "ml3"
EPOCHS = list(range(263, 284))
MODELS = {
    "Qwen": "Qwen/Qwen3-235B-A22B-Instruct-2507-FP8",
    "Kimi": "moonshotai/Kimi-K2.6",
}


def load_dotenv() -> None:
    env = ROOT / ".env"
    if not env.exists():
        return
    for line in env.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def normalize_base(raw: str) -> str:
    raw = raw.rstrip("/")
    if not raw.startswith(("http://", "https://")):
        raw = "http://" + raw
    if raw.endswith("/chain-api"):
        return raw + "/"
    return raw + "/chain-api/"


def add_default_port_if_missing(raw: str) -> str | None:
    parsed = urlparse(raw if raw.startswith(("http://", "https://")) else "http://" + raw)
    if parsed.port is not None or not parsed.hostname:
        return None
    return parsed._replace(netloc=f"{parsed.hostname}:8000").geturl()


def base_urls() -> list[str]:
    raw = (
        os.environ.get("GONKA_RPC_LCD_URL")
        or os.environ.get("GONKA_RPC_URL")
        or "http://node1.gonka.ai:8000"
    )
    candidates = [raw]
    raw_with_port = add_default_port_if_missing(raw)
    if raw_with_port:
        candidates.append(raw_with_port)
    candidates.append("http://node1.gonka.ai:8000")
    urls = [normalize_base(url) for url in candidates]
    out: list[str] = []
    for url in urls:
        if url not in out:
            out.append(url)
    return out


def safe_part(value: Any) -> str:
    return "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in str(value))


def cache_name(path: str, params: dict[str, str] | None = None) -> Path:
    safe = safe_part(path.strip("/").replace("/", "_"))
    if params:
        safe += "__" + "_".join(f"{safe_part(k)}_{safe_part(v)}" for k, v in sorted(params.items()))
    digest = hashlib.sha256((path + json.dumps(params or {}, sort_keys=True)).encode()).hexdigest()[:12]
    return RAW / f"{safe}.{digest}.json"


def get_json(path: str, params: dict[str, str] | None = None) -> Any:
    RAW.mkdir(parents=True, exist_ok=True)
    cpath = cache_name(path, params)
    if cpath.exists():
        return json.loads(cpath.read_text())

    errors = []
    headers = {"Accept": "application/json"}
    api_key = os.environ.get("GONKA_RPC_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
        headers["x-api-key"] = api_key
    for base in base_urls():
        url = urljoin(base, path.lstrip("/"))
        if params:
            url += "?" + urlencode(params)
        req = Request(url, headers=headers)
        try:
            with urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode())
            cpath.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
            return data
        except (HTTPError, URLError, TimeoutError) as exc:
            errors.append(f"{url}: {exc}")
            continue
    raise RuntimeError("Failed to fetch endpoint; tried " + " | ".join(errors))


def as_int(value: Any) -> int:
    if value in (None, ""):
        return 0
    return int(value)


def get_epoch_group(epoch: int, model_id: str) -> dict[str, Any]:
    data = get_json(
        f"/productscience/inference/inference/epoch_group_data/{epoch}",
        {"model_id": model_id},
    )
    group = data.get("epoch_group_data", data)
    if not isinstance(group, dict):
        raise RuntimeError(f"Unexpected epoch_group_data shape for epoch {epoch} {model_id}")
    return group


def find_member(group: dict[str, Any], address: str) -> dict[str, Any] | None:
    for row in group.get("validation_weights") or []:
        if row.get("member_address") == address:
            return row
    return None


def node_summary(nodes: list[dict[str, Any]]) -> str:
    parts = []
    for node in nodes:
        slots = node.get("timeslot_allocation")
        if isinstance(slots, list):
            slots_text = "".join("1" if bool(x) else "0" for x in slots)
        else:
            slots_text = ""
        parts.append(
            f"{node.get('node_id','')}:{node.get('poc_weight','')}:{node.get('throughput','')}:{slots_text}"
        )
    return ";".join(parts)


def slot_bits(node: dict[str, Any] | None) -> str:
    if not node:
        return ""
    slots = node.get("timeslot_allocation") or []
    return "".join("1" if bool(x) else "0" for x in slots)


def poc_slot(node: dict[str, Any] | None) -> bool:
    if not node:
        return False
    slots = node.get("timeslot_allocation") or []
    return len(slots) > 1 and bool(slots[1])


def pre_poc_slot(node: dict[str, Any] | None) -> bool:
    if not node:
        return False
    slots = node.get("timeslot_allocation") or []
    return len(slots) > 0 and bool(slots[0])


def performance_row(epoch: int) -> dict[str, Any]:
    data = get_json(f"/productscience/inference/inference/epoch_performance_summary/{epoch}")
    for row in data.get("epochPerformanceSummary") or []:
        if row.get("participant_id") == CLAIMANT:
            return row
    return {}


def excluded_row(epoch: int) -> dict[str, Any]:
    data = get_json(f"/productscience/inference/inference/excluded_participants/{epoch}")
    candidates = data.get("excluded_participants", data)
    if isinstance(candidates, dict):
        candidates = candidates.get("excluded_participants", [])
    for row in candidates or []:
        if not isinstance(row, dict):
            continue
        if row.get("address") == CLAIMANT or row.get("participant_id") == CLAIMANT:
            return row
    return {}


def main() -> int:
    load_dotenv()
    OUT.mkdir(parents=True, exist_ok=True)

    model_rows: list[dict[str, Any]] = []
    node_rows: list[dict[str, Any]] = []
    reward_rows: list[dict[str, Any]] = []
    by_epoch: dict[int, dict[str, Any]] = {}

    for epoch in EPOCHS:
        perf = performance_row(epoch)
        excl = excluded_row(epoch)
        reward_rows.append(
            {
                "epoch": epoch,
                "found_in_performance": bool(perf),
                "rewarded_coins": perf.get("rewarded_coins", ""),
                "earned_coins": perf.get("earned_coins", ""),
                "inference_count": perf.get("inference_count", ""),
                "missed_requests": perf.get("missed_requests", ""),
                "claimed": perf.get("claimed", ""),
                "excluded": bool(excl),
                "exclusion_reason": excl.get("reason", excl.get("failure_reason", "")),
                "exclusion_height": excl.get("block_height", excl.get("height", "")),
            }
        )

        by_epoch.setdefault(epoch, {"nodes": set(), "ml3_present": False, "ml3_pre_poc_slot": False, "ml3_poc_slot": False})
        for label, model_id in MODELS.items():
            group = get_epoch_group(epoch, model_id)
            member = find_member(group, CLAIMANT)
            nodes = member.get("ml_nodes", []) if member else []
            ml3 = next((n for n in nodes if n.get("node_id") == NODE_UNDER_CLAIM), None)
            poc_slot_nodes = [n for n in nodes if poc_slot(n)]
            node_ids = [n.get("node_id", "") for n in nodes]
            by_epoch[epoch]["nodes"].update(node_ids)
            by_epoch[epoch]["ml3_present"] = by_epoch[epoch]["ml3_present"] or bool(ml3)
            if ml3:
                by_epoch[epoch]["ml3_pre_poc_slot"] = by_epoch[epoch]["ml3_pre_poc_slot"] or pre_poc_slot(ml3)
                by_epoch[epoch]["ml3_poc_slot"] = by_epoch[epoch]["ml3_poc_slot"] or poc_slot(ml3)

            model_rows.append(
                {
                    "epoch": epoch,
                    "model": label,
                    "model_id": model_id,
                    "found": bool(member),
                    "total_weight": group.get("total_weight", ""),
                    "poc_start_block_height": group.get("poc_start_block_height", ""),
                    "weight": member.get("weight", "") if member else "",
                    "voting_power": member.get("voting_power", "") if member else "",
                    "confirmation_weight": member.get("confirmation_weight", "") if member else "",
                    "node_count": len(nodes),
                    "node_ids": ";".join(node_ids),
                    "nodes": node_summary(nodes),
                    "ml3_present": bool(ml3),
                    "ml3_poc_weight": ml3.get("poc_weight", "") if ml3 else "",
                    "ml3_throughput": ml3.get("throughput", "") if ml3 else "",
                    "ml3_timeslot_allocation": slot_bits(ml3),
                    "ml3_pre_poc_slot": pre_poc_slot(ml3),
                    "ml3_poc_slot": poc_slot(ml3),
                    "poc_slot_node_ids": ";".join(n.get("node_id", "") for n in poc_slot_nodes),
                }
            )
            for node in nodes:
                node_rows.append(
                    {
                        "epoch": epoch,
                        "model": label,
                        "node_id": node.get("node_id", ""),
                        "poc_weight": node.get("poc_weight", ""),
                        "throughput": node.get("throughput", ""),
                        "timeslot_allocation": "".join(
                            "1" if bool(x) else "0" for x in (node.get("timeslot_allocation") or [])
                        ),
                        "participant_weight": member.get("weight", "") if member else "",
                        "participant_voting_power": member.get("voting_power", "") if member else "",
                        "participant_confirmation_weight": member.get("confirmation_weight", "") if member else "",
                    }
                )

    write_csv(OUT / "case5_ml3_model_trace.csv", model_rows)
    write_csv(OUT / "case5_ml3_node_trace.csv", node_rows)
    write_csv(OUT / "case5_participant_reward_trace.csv", reward_rows)

    timeline_rows = []
    for epoch in EPOCHS:
        epoch_model_rows = [r for r in model_rows if r["epoch"] == epoch]
        timeline_rows.append(
            {
                "epoch": epoch,
                "models_found": sum(1 for r in epoch_model_rows if r["found"]),
                "node_ids": ";".join(sorted(by_epoch[epoch]["nodes"])),
                "ml3_present": by_epoch[epoch]["ml3_present"],
                "ml3_pre_poc_slot": by_epoch[epoch]["ml3_pre_poc_slot"],
                "ml3_poc_slot": by_epoch[epoch]["ml3_poc_slot"],
                "qwen_weight": next((r["weight"] for r in epoch_model_rows if r["model"] == "Qwen"), ""),
                "qwen_voting_power": next((r["voting_power"] for r in epoch_model_rows if r["model"] == "Qwen"), ""),
                "qwen_nodes": next((r["nodes"] for r in epoch_model_rows if r["model"] == "Qwen"), ""),
                "kimi_weight": next((r["weight"] for r in epoch_model_rows if r["model"] == "Kimi"), ""),
                "kimi_voting_power": next((r["voting_power"] for r in epoch_model_rows if r["model"] == "Kimi"), ""),
                "kimi_nodes": next((r["nodes"] for r in epoch_model_rows if r["model"] == "Kimi"), ""),
                "rewarded_gonka": atoms_to_gonka(next((r["rewarded_coins"] for r in reward_rows if r["epoch"] == epoch), "")),
                "excluded": next((r["excluded"] for r in reward_rows if r["epoch"] == epoch), ""),
                "exclusion_reason": next((r["exclusion_reason"] for r in reward_rows if r["epoch"] == epoch), ""),
            }
        )
    write_csv(OUT / "case5_timeline.csv", timeline_rows)
    write_markdown(timeline_rows, model_rows, reward_rows)
    return 0


def atoms_to_gonka(value: Any) -> str:
    if value in (None, ""):
        return ""
    return f"{as_int(value) / 1_000_000_000:.9f}"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(x) for x in row) + " |")
    return "\n".join(out)


def write_markdown(timeline_rows: list[dict[str, Any]], model_rows: list[dict[str, Any]], reward_rows: list[dict[str, Any]]) -> None:
    focus = [r for r in timeline_rows if 266 <= int(r["epoch"]) <= 273 or int(r["epoch"]) in (280, 283)]
    table = md_table(
        ["Epoch", "Nodes", "ml3 present", "ml3 PRE_POC_SLOT", "ml3 POC_SLOT", "Kimi weight", "Kimi voting power", "Qwen weight", "Reward, GONKA", "Excluded"],
        [
            [
                r["epoch"],
                r["node_ids"],
                r["ml3_present"],
                r["ml3_pre_poc_slot"],
                r["ml3_poc_slot"],
                r["kimi_weight"],
                r["kimi_voting_power"],
                r["qwen_weight"],
                r["rewarded_gonka"],
                r["excluded"],
            ]
            for r in focus
        ],
    )

    ml3_rows = [
        r for r in model_rows
        if r["ml3_present"] or (266 <= int(r["epoch"]) <= 273 and r["found"])
    ]
    ml3_table = md_table(
        ["Epoch", "Model", "Weight", "Voting power", "Confirmation", "Nodes"],
        [
            [
                r["epoch"],
                r["model"],
                r["weight"],
                r["voting_power"],
                r["confirmation_weight"],
                r["nodes"],
            ]
            for r in ml3_rows
        ],
    )

    (OUT / "case5_timeline.md").write_text(
        "# P3-CAND-05 Timeline\n\n"
        "Participant: `gonka15munkmx6x7k6rqqeexjet4556p7at39ks9qgr5`.\n\n"
        "Node notation is `node_id:poc_weight:throughput:timeslot_bits`, where `1` in "
        "`timeslot_bits` means that the node was allocated for that slot in the epoch "
        "group row exposed by the chain. Slot index `0` is `PRE_POC_SLOT`; slot index "
        "`1` is `POC_SLOT`. Only `POC_SLOT=true` is treated by the pre-fix chain code "
        "as preserved for PoC/inference service.\n\n"
        + table
        + "\n\n## Model Rows\n\n"
        + ml3_table
        + "\n"
    )


if __name__ == "__main__":
    sys.exit(main())
