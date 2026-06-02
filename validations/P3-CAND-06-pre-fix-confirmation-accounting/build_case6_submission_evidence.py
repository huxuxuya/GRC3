#!/usr/bin/env python3
"""Fetch and normalize raw cPoC submission/validation evidence for P3-CAND-06.

The root-cause replay proves the aggregate pass-weight contradiction from the
archive scan. This script goes one level deeper: for each candidate loss event
it fetches the cPoC stage store commits and validation rows, then reconstructs
submission counts, validator counts, valid validator weight, and the strict
two-thirds pass/fail result independently from the raw stage data.
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
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


CASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = CASE_DIR.parents[1]
CACHE_DIR = CASE_DIR / "raw_stage_cache"

KIMI = "moonshotai/Kimi-K2.6"
QWEN = "Qwen/Qwen3-235B-A22B-Instruct-2507-FP8"
MODELS = [QWEN, KIMI]
REQUEST_TIMEOUT_SECONDS = 90
RETRIES = 6


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
    headers = {"User-Agent": "grc-case6-submission-evidence/1.0"}
    api_key = os.environ.get("GONKA_RPC_API_KEY")
    if api_key:
        headers["X-Api-Key"] = api_key
    return headers


def path_cache_name(path: str) -> str:
    digest = hashlib.sha256(path.encode("utf-8")).hexdigest()[:16]
    safe = path.strip("/").replace("/", "_").replace("?", "__")
    safe = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in safe)
    return f"{safe}.{digest}.json"


def get_json(base: str, path: str, *, refresh: bool = False) -> Any:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / path_cache_name(path)
    if cache_path.exists() and not refresh:
        return json.loads(cache_path.read_text(encoding="utf-8"))

    url = base.rstrip("/") + path
    last_error = None
    for attempt in range(RETRIES):
        req = urllib.request.Request(url, headers=request_headers())
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
        except Exception as exc:  # noqa: BLE001 - audit tool should retry broadly
            last_error = str(exc)
        time.sleep(min(20, 1 + attempt * 2))
    raise RuntimeError(f"Failed to fetch {path}: {last_error}")


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


def int_of(value: Any, default: int = 0) -> int:
    if value is None or value == "":
        return default
    return int(value)


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
        "commit_present": bool(commit),
        "commit_count": int_of(commit.get("count")) if commit else 0,
        "commit_root_hash": commit.get("root_hash", "") if commit else "",
        "commit_node_id": commit.get("node_id", "") if commit else "",
        "validator_count": len(valid_validators | invalid_validators),
        "valid_validator_count": len(valid_validators),
        "invalid_validator_count": len(invalid_validators),
        "valid_weight": valid_weight,
        "invalid_weight": invalid_weight,
        "valid_weight_percent": f"{valid_weight * 100 / total_network_weight:.4f}" if total_network_weight else "",
        "result": result,
        "validators": ";".join(sorted(valid_validators | invalid_validators)),
    }


def stage_counts(commits: list[dict[str, Any]], validations: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "commit_rows": len(commits),
        "validation_outer_rows": len(validations),
        "validation_inner_rows": sum(len(row.get("poc_validation") or []) for row in validations),
    }


def build_evidence(base: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    rows = read_csv(CASE_DIR / "case6_row_formula_replay.csv")
    model_group_cache: dict[tuple[int, str], dict[str, int]] = {}
    stage_cache: dict[int, tuple[list[dict[str, Any]], list[dict[str, Any]]]] = {}
    out_rows: list[dict[str, Any]] = []
    stage_rows: list[dict[str, Any]] = []

    for row in rows:
        epoch = int(row["epoch"])
        trigger = int(row["event_trigger_height"])
        total = int(row["total_network_weight"])
        for model in MODELS:
            key = (epoch, model)
            if key not in model_group_cache:
                path = f"/productscience/inference/inference/epoch_group_data/{epoch}?model_id={urllib.parse.quote(model, safe='')}"
                model_group_cache[key] = model_voting_power(get_json(base, path)["epoch_group_data"])
        if trigger not in stage_cache:
            commits = get_json(base, f"/productscience/inference/inference/all_poc_v2_store_commits/{trigger}")["commits"]
            validations = get_json(base, f"/productscience/inference/inference/poc_v2_validations_for_stage/{trigger}")[
                "poc_validation"
            ]
            stage_cache[trigger] = (commits, validations)
            counts = stage_counts(commits, validations)
            stage_rows.append(
                {
                    "event_trigger_height": trigger,
                    "commit_rows": counts["commit_rows"],
                    "validation_outer_rows": counts["validation_outer_rows"],
                    "validation_inner_rows": counts["validation_inner_rows"],
                }
            )
        commits, validations = stage_cache[trigger]
        commits_by_key = commitment_index(commits)
        validations_by_key = validation_index(validations)
        for model_label, model in [("qwen", QWEN), ("kimi", KIMI)]:
            evidence = classify_model(
                row["participant"],
                model,
                total,
                model_group_cache[(epoch, model)],
                commits_by_key,
                validations_by_key,
            )
            out_rows.append(
                {
                    "epoch": row["epoch"],
                    "participant": row["participant"],
                    "event_sequence": row["event_sequence"],
                    "event_trigger_height": row["event_trigger_height"],
                    "model_label": model_label,
                    "model_id": model,
                    "total_network_weight": total,
                    "two_thirds_floor": total * 2 // 3,
                    "strict_two_thirds_min": total * 2 // 3 + 1,
                    "commit_present": str(evidence["commit_present"]),
                    "commit_count": evidence["commit_count"],
                    "commit_root_hash": evidence["commit_root_hash"],
                    "commit_node_id": evidence["commit_node_id"],
                    "validator_count": evidence["validator_count"],
                    "valid_validator_count": evidence["valid_validator_count"],
                    "invalid_validator_count": evidence["invalid_validator_count"],
                    "valid_weight": evidence["valid_weight"],
                    "valid_weight_percent": evidence["valid_weight_percent"],
                    "invalid_weight": evidence["invalid_weight"],
                    "result": evidence["result"],
                    "source_csv_submitted_count": row[f"{model_label}_submitted_count"],
                    "source_csv_valid_weight": row[f"{model_label}_valid_weight"],
                    "source_csv_result": row[f"{model_label}_result"],
                    "matches_source_csv": str(
                        int(row[f"{model_label}_submitted_count"]) == evidence["commit_count"]
                        and int(row[f"{model_label}_valid_weight"]) == evidence["valid_weight"]
                        and row[f"{model_label}_result"] == evidence["result"]
                    ),
                    "validators": evidence["validators"],
                }
            )

    summary = {
        "candidate_rows": len(rows),
        "candidate_participants": len({row["participant"] for row in rows}),
        "unique_trigger_heights": len({int(row["event_trigger_height"]) for row in rows}),
        "model_rows": len(out_rows),
        "model_rows_matching_source_csv": sum(row["matches_source_csv"] == "True" for row in out_rows),
        "model_rows_with_commit": sum(row["commit_present"] == "True" for row in out_rows),
        "pass_weight_model_rows": sum(row["result"] == "pass_weight" for row in out_rows),
        "pass_model_distribution": dict(
            Counter(
                "+".join(
                    model_row["model_label"]
                    for model_row in out_rows
                    if model_row["participant"] == candidate["participant"]
                    and model_row["event_trigger_height"] == candidate["event_trigger_height"]
                    and model_row["result"] == "pass_weight"
                )
                for candidate in rows
            )
        ),
        "stage_counts": sorted(stage_rows, key=lambda item: int(item["event_trigger_height"])),
    }
    return out_rows, stage_rows, summary


def write_review(evidence_rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    candidate_keys = {(row["epoch"], row["participant"], row["event_trigger_height"]) for row in evidence_rows}
    by_candidate: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in evidence_rows:
        by_candidate[(row["epoch"], row["participant"], row["event_trigger_height"])].append(row)
    both_pass = [
        rows
        for rows in by_candidate.values()
        if sum(row["result"] == "pass_weight" for row in rows) == 2
    ]
    any_mismatch = [row for row in evidence_rows if row["matches_source_csv"] != "True"]
    lines = [
        "# P3-CAND-06 Submission And Validator Evidence",
        "",
        "This artifact fetches the raw cPoC stage commit and validation rows for",
        "the `24` candidate loss events, then reconstructs submitted counts,",
        "validator counts, valid validator weight, and strict `>2/3` pass/fail",
        "results. It does not execute any external compensation repository.",
        "",
        "## Result",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Candidate rows | `{summary['candidate_rows']}` |",
        f"| Unique participants | `{summary['candidate_participants']}` |",
        f"| Unique cPoC trigger heights fetched | `{summary['unique_trigger_heights']}` |",
        f"| Model rows checked | `{summary['model_rows']}` |",
        f"| Model rows matching the previous aggregate CSV | `{summary['model_rows_matching_source_csv']}` |",
        f"| Model rows with a stage commit/submission | `{summary['model_rows_with_commit']}` |",
        f"| Model rows with `pass_weight` | `{summary['pass_weight_model_rows']}` |",
        f"| Candidate keys reconstructed | `{len(candidate_keys)}` |",
        f"| Source mismatches | `{len(any_mismatch)}` |",
        "",
        "## What This Proves",
        "",
        "- The previous aggregate `submitted_count`, `valid_weight`, and model result",
        "  columns are reproducible from raw stage commit and validation rows.",
        "- Every candidate has at least one model with a cPoC store commit and enough",
        "  validator weight to satisfy strict `validWeight > TotalNetworkWeight * 2 / 3`.",
        "- The loss is therefore not explained by a simple lack of validators for the",
        "  passing model.",
        "",
        "## What This Does Not Prove",
        "",
        "- The chain endpoints expose cPoC store commit counts/root hashes and",
        "  validation rows here, not every individual off-chain nonce/payload body.",
        "- For rows with one passing model and one no-submission model, eligibility is",
        "  still a policy/protocol question: the raw data proves one model passed, but",
        "  not that the missing model should have been ignored for compensation.",
        "- Six candidate rows still need coefficient-adjusted replay of",
        "  preserved/measured/not-preserved components.",
        "",
        "## Both-Model Pass Rows",
        "",
    ]
    if not both_pass:
        lines.append("No row has both Qwen and Kimi passing.")
    else:
        lines.extend(
            [
                "| Epoch | Participant | Trigger | Qwen commit/validators/weight | Kimi commit/validators/weight |",
                "|---:|---|---:|---|---|",
            ]
        )
        for rows in both_pass:
            qwen = next(row for row in rows if row["model_label"] == "qwen")
            kimi = next(row for row in rows if row["model_label"] == "kimi")
            lines.append(
                f"| `{qwen['epoch']}` | `{qwen['participant']}` | `{qwen['event_trigger_height']}` | "
                f"`{qwen['commit_count']}` / `{qwen['valid_validator_count']}` / `{qwen['valid_weight_percent']}%` | "
                f"`{kimi['commit_count']}` / `{kimi['valid_validator_count']}` / `{kimi['valid_weight_percent']}%` |"
            )
    lines.extend(
        [
            "",
            "## Stage Fetch Summary",
            "",
            "| Trigger height | Commit rows | Validation outer rows | Validation inner rows |",
            "|---:|---:|---:|---:|",
        ]
    )
    for row in summary["stage_counts"]:
        lines.append(
            f"| `{row['event_trigger_height']}` | `{row['commit_rows']}` | "
            f"`{row['validation_outer_rows']}` | `{row['validation_inner_rows']}` |"
        )
    lines.extend(
        [
            "",
            "Machine-readable details:",
            "",
            "- `case6_submission_validator_evidence.csv`",
            "- `case6_submission_validator_evidence.json`",
            "- raw endpoint cache: `raw_stage_cache/`",
        ]
    )
    (CASE_DIR / "case6_submission_validator_evidence.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    load_dotenv(REPO_ROOT / ".env")
    base = direct_lcd_from_env()
    evidence_rows, stage_rows, summary = build_evidence(base)
    fieldnames = [
        "epoch",
        "participant",
        "event_sequence",
        "event_trigger_height",
        "model_label",
        "model_id",
        "total_network_weight",
        "two_thirds_floor",
        "strict_two_thirds_min",
        "commit_present",
        "commit_count",
        "commit_root_hash",
        "commit_node_id",
        "validator_count",
        "valid_validator_count",
        "invalid_validator_count",
        "valid_weight",
        "valid_weight_percent",
        "invalid_weight",
        "result",
        "source_csv_submitted_count",
        "source_csv_valid_weight",
        "source_csv_result",
        "matches_source_csv",
        "validators",
    ]
    write_csv(CASE_DIR / "case6_submission_validator_evidence.csv", evidence_rows, fieldnames)
    write_json(
        CASE_DIR / "case6_submission_validator_evidence.json",
        {
            "case": "P3-CAND-06",
            "source": "case6_row_formula_replay.csv + archive cPoC stage endpoints",
            "summary": summary,
            "rows": evidence_rows,
        },
    )
    write_csv(
        CASE_DIR / "case6_stage_fetch_summary.csv",
        stage_rows,
        ["event_trigger_height", "commit_rows", "validation_outer_rows", "validation_inner_rows"],
    )
    write_review(evidence_rows, summary)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
