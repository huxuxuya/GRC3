#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CASE3 = ROOT / "validations/P3-CAND-03-failed-cpoc-epoch-267"
CASE5_RAW = ROOT / "validations/P3-CAND-05-ml3-hardware-reregistration/raw_cache"
CASE6_RAW = ROOT / "validations/P3-CAND-06-pre-fix-confirmation-accounting/raw_stage_cache"

KIMI_ADDR = "gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6"
QWEN_ADDR = "gonka1myu058axjs62mc3e7na9krwvqpfl9z3gtcw9es"
KIMI = "moonshotai/Kimi-K2.6"
QWEN = "Qwen/Qwen3-235B-A22B-Instruct-2507-FP8"


def load(path: Path):
    with path.open() as f:
        return json.load(f)


def ngonka_to_gonka(value: int) -> str:
    whole = value // 1_000_000_000
    frac = value % 1_000_000_000
    return f"{whole}.{frac:09d}"


def performance(epoch: int, participant: str) -> dict:
    matches = sorted(CASE5_RAW.glob(f"productscience_inference_inference_epoch_performance_summary_{epoch}.*.json"))
    if not matches:
        raise FileNotFoundError(f"no performance summary for epoch {epoch}")
    rows = load(matches[0])["epochPerformanceSummary"]
    row = next((r for r in rows if r["participant_id"] == participant), None)
    if row is None:
        raise KeyError(f"{participant} not in epoch {epoch} performance summary")
    return row


def excluded(epoch: int, participant: str) -> dict | None:
    matches = sorted(CASE5_RAW.glob(f"productscience_inference_inference_excluded_participants_{epoch}.*.json"))
    if not matches:
        return None
    rows = load(matches[0])["items"]
    return next((r for r in rows if r["address"] == participant), None)


def case3_row(epoch: int, participant: str) -> dict:
    with (CASE3 / "case3_neighbor_failed_cpoc_rows.csv").open() as f:
        rows = csv.DictReader(f)
        row = next((r for r in rows if int(r["epoch"]) == epoch and r["participant"] == participant), None)
    if row is None:
        raise KeyError(f"{participant} not in local case3 neighbor rows for epoch {epoch}")
    return row


def cpoc_stage_rows(stage: int, participant: str) -> list[dict]:
    matches = sorted(CASE6_RAW.glob(f"productscience_inference_inference_poc_v2_validations_for_stage_{stage}.*.json"))
    if not matches:
        raise FileNotFoundError(f"no cPoC validation file for stage {stage}")
    outer = load(matches[0])["poc_validation"]
    return [r for r in outer if r.get("participant") == participant]


def cpoc_snapshot_total(stage: int) -> int:
    matches = sorted(CASE6_RAW.glob(f"height_*_productscience_inference_inference_poc_validation_snapshot_{stage}.*.json"))
    if not matches:
        raise FileNotFoundError(f"no cPoC snapshot file for stage {stage}")
    return int(load(matches[0])["snapshot"]["total_network_weight"])


def main() -> None:
    rows = [
        ("strict_epoch267_kimi", 267, KIMI_ADDR, KIMI),
        ("extension_epoch265_kimi", 265, KIMI_ADDR, KIMI),
        ("extension_epoch265_qwen", 265, QWEN_ADDR, QWEN),
    ]

    selected = []
    for label, epoch, addr, model in rows:
        perf = performance(epoch, addr)
        excl = excluded(epoch, addr)
        scan = case3_row(epoch, addr)
        loss = int(scan["loss_ngonka"])
        selected.append((label, epoch, addr, model, loss))
        print(f"{label}:")
        print(f"  participant: {addr}")
        print(f"  model_scope: {model}")
        print(f"  claimed: {perf['claimed']}")
        print(f"  actual_reward_ngonka: {perf['rewarded_coins']}")
        print(f"  excluded: {bool(excl)}")
        if excl:
            print(f"  exclusion: height={excl['exclusion_block_height']} reason={excl['reason']}")
        print(f"  root_weight: {scan['root_weight']}")
        print(f"  root_total_weight: {scan['total_network_weight']}")
        print(f"  expected_loss_ngonka: {loss}")
        print(f"  expected_loss_gonka: {ngonka_to_gonka(loss)}")
        print(f"  event_stage: {scan['event_trigger_height']}")
        print(f"  qwen: submitted={scan['qwen_submitted_count']} valid_weight={scan['qwen_valid_weight']} result={scan['qwen_result']}")
        print(f"  kimi: submitted={scan['kimi_submitted_count']} valid_weight={scan['kimi_valid_weight']} result={scan['kimi_result']}")

        if epoch == 265:
            snapshot_total = cpoc_snapshot_total(int(scan["event_trigger_height"]))
            threshold = snapshot_total * 2 // 3 + 1
            print(f"  raw_snapshot_total_network_weight: {snapshot_total}")
            print(f"  strict_gt_2_3_threshold: {threshold}")
            print(f"  qwen_passes_weight: {int(scan['qwen_valid_weight']) >= threshold}")
            print(f"  kimi_passes_weight: {int(scan['kimi_valid_weight']) >= threshold}")
        print()

    kimi_only = sum(loss for _, _, _, model, loss in selected if model == KIMI)
    broader = sum(loss for *_, loss in selected)
    print(f"kimi_only_total_ngonka: {kimi_only}")
    print(f"kimi_only_total_gonka: {ngonka_to_gonka(kimi_only)}")
    print(f"broader_total_ngonka: {broader}")
    print(f"broader_total_gonka: {ngonka_to_gonka(broader)}")


if __name__ == "__main__":
    main()
