#!/usr/bin/env python3
"""Build a provenance manifest for P3-CAND-06 raw cache files."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any


CASE_DIR = Path(__file__).resolve().parent
CACHE_DIR = CASE_DIR / "raw_stage_cache"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def infer_height(name: str) -> str:
    block_match = re.search(r"blocks_(\d+)", name)
    if block_match:
        return block_match.group(1)
    if not name.startswith("height_"):
        return "latest"
    parts = name.split("_", 2)
    return parts[1] if len(parts) >= 3 else ""


def infer_consumer(name: str) -> str:
    if "post_upgrade_scan/" in name:
        return "post_upgrade_regression_scan"
    if "cosmos_base_tendermint_v1beta1_blocks" in name:
        return "epoch_upgrade_timeline"
    if "all_poc_v2_store_commits" in name:
        return "submission_validator_evidence;old_formula_replay"
    if "poc_v2_validations_for_stage" in name:
        return "submission_validator_evidence"
    if "all_mlnode_weight_distributions" in name:
        return "old_formula_replay;new_algorithm_replay"
    if "poc_validation_snapshot" in name:
        return "old_formula_replay;new_algorithm_replay"
    if "preserved_nodes_snapshot" in name:
        return "old_formula_replay;new_algorithm_replay"
    if "epoch_group_data" in name:
        return "submission_validator_evidence;old_formula_replay;new_algorithm_replay"
    if "params" in name:
        return "old_formula_replay;new_algorithm_replay"
    return "unknown"


def infer_endpoint(name: str) -> str:
    base = name
    if base.startswith("height_"):
        base = base.split("_", 2)[2]
    base = base.rsplit(".", 2)[0]

    block_match = re.match(r"^cosmos_base_tendermint_v1beta1_blocks_(\d+)$", base)
    if block_match:
        return f"/cosmos/base/tendermint/v1beta1/blocks/{block_match.group(1)}"

    prefix = "productscience_inference_inference_"
    if not base.startswith(prefix):
        return "unknown"

    suffix = base.removeprefix(prefix)
    simple_endpoints = {
        "params": "/productscience/inference/inference/params",
        "preserved_nodes_snapshot": "/productscience/inference/inference/preserved_nodes_snapshot",
    }
    if suffix in simple_endpoints:
        return simple_endpoints[suffix]

    endpoint_patterns = [
        (
            r"^all_poc_v2_store_commits_(\d+)$",
            "/productscience/inference/inference/all_poc_v2_store_commits/{0}",
        ),
        (
            r"^poc_v2_validations_for_stage_(\d+)$",
            "/productscience/inference/inference/poc_v2_validations_for_stage/{0}",
        ),
        (
            r"^poc_validation_snapshot_(\d+)$",
            "/productscience/inference/inference/poc_validation_snapshot/{0}",
        ),
        (
            r"^all_mlnode_weight_distributions_(\d+)$",
            "/productscience/inference/inference/all_mlnode_weight_distributions/{0}",
        ),
        (
            r"^epoch_group_data_(\d+)$",
            "/productscience/inference/inference/epoch_group_data/{0}",
        ),
        (
            r"^epoch_performance_summary_(\d+)$",
            "/productscience/inference/inference/epoch_performance_summary/{0}",
        ),
        (
            r"^excluded_participants_(\d+)$",
            "/productscience/inference/inference/excluded_participants/{0}",
        ),
        (
            r"^confirmation_poc_events_(\d+)$",
            "/productscience/inference/inference/confirmation_poc_events/{0}",
        ),
        (
            r"^participant_(gonka[0-9a-z]+)$",
            "/productscience/inference/inference/participant/{0}",
        ),
    ]
    for pattern, endpoint in endpoint_patterns:
        match = re.match(pattern, suffix)
        if match:
            return endpoint.format(*match.groups())

    match = re.match(r"^epoch_group_data_(\d+)__model_id_(.+)$", suffix)
    if match:
        epoch, model = match.groups()
        return f"/productscience/inference/inference/epoch_group_data/{epoch}?model_id={model.replace('_2F', '/')}"

    return "unknown"


def build_rows() -> list[dict[str, Any]]:
    rows = []
    for path in sorted(CACHE_DIR.rglob("*.json")):
        stat = path.stat()
        name = path.name
        cache_file = str(path.relative_to(CASE_DIR))
        rows.append(
            {
                "cache_file": cache_file,
                "requested_block_height": infer_height(name),
                "size_bytes": stat.st_size,
                "sha256": sha256(path),
                "inferred_endpoint": infer_endpoint(name),
                "consumer": infer_consumer(cache_file),
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = ["cache_file", "requested_block_height", "size_bytes", "sha256", "inferred_endpoint", "consumer"]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, rows: list[dict[str, Any]]) -> None:
    by_consumer: dict[str, int] = {}
    for row in rows:
        for consumer in row["consumer"].split(";"):
            by_consumer[consumer] = by_consumer.get(consumer, 0) + 1
    total_size = sum(int(row["size_bytes"]) for row in rows)
    lines = [
        "# P3-CAND-06 Raw Data Manifest",
        "",
        "This manifest records the cached raw LCD responses used by the P3-CAND-06",
        "validation artifacts. It intentionally stores file hashes and inferred",
        "request metadata, not RPC URLs or API keys.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Cache files | `{len(rows)}` |",
        f"| Total cache size | `{total_size}` bytes (`{total_size / 1_000_000:.1f} MB`) |",
        "",
        "## Files By Consumer",
        "",
        "| Consumer | Files |",
        "|---|---:|",
    ]
    for consumer, count in sorted(by_consumer.items()):
        lines.append(f"| `{consumer}` | `{count}` |")
    lines.extend(
        [
            "",
            "Machine-readable versions are in `case6_raw_data_manifest.csv` and",
            "`case6_raw_data_manifest.json`.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = build_rows()
    write_csv(CASE_DIR / "case6_raw_data_manifest.csv", rows)
    write_json(CASE_DIR / "case6_raw_data_manifest.json", {"cache_files": rows})
    write_md(CASE_DIR / "case6_raw_data_manifest.md", rows)
    print(json.dumps({"cache_files": len(rows), "size_bytes": sum(int(r["size_bytes"]) for r in rows)}, sort_keys=True))


if __name__ == "__main__":
    main()
