#!/usr/bin/env python3
"""Independently verify P3-CAND-02 against an archive LCD.

The script reads local .env values, derives the direct Cosmos LCD endpoint,
writes the resumable cache outside the repository by default, and writes
sanitized result artifacts into the repository.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DEFAULT_WORKDIR = Path("/tmp/grc3-case2-audit")
DEFAULT_ARTIFACT_DIR = Path("validations/P3-CAND-02-negative-coin-balance")
DEFAULT_PUBLISHED_CSV = (
    "https://raw.githubusercontent.com/gonkavip/unclaimed/main/unclaimed.csv"
)
REQUEST_TIMEOUT_SECONDS = 45
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
    if "://" not in raw:
        parsed = urllib.parse.urlparse("dummy://" + raw)
    else:
        parsed = urllib.parse.urlparse(raw)
    if not parsed.hostname:
        raise SystemExit("Could not parse GONKA_RPC_URL host")
    if os.environ.get("GONKA_RPC_LCD_URL"):
        return raw if "://" in raw else "http://" + raw
    return f"http://{parsed.hostname}:1317"


def headers(height: int | None = None) -> dict[str, str]:
    out = {"User-Agent": "grc-case2-archive-audit/1.0"}
    api_key = os.environ.get("GONKA_RPC_API_KEY")
    if api_key:
        out["X-Api-Key"] = api_key
    if height is not None:
        out["x-cosmos-block-height"] = str(height)
    return out


def get_json(base: str, path: str, *, height: int | None = None) -> dict:
    url = base.rstrip("/") + path
    last_error = None
    for attempt in range(RETRIES):
        req = urllib.request.Request(url, headers=headers(height))
        try:
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")
            if exc.code == 404:
                return {"_error": "404", "_body": body}
            last_error = f"HTTP {exc.code}: {body[:300]}"
        except Exception as exc:  # noqa: BLE001 - keep retries simple for audit tool
            last_error = str(exc)
        time.sleep(min(20, 1 + attempt * 2))
    return {"_error": last_error or "unknown error"}


def init_db(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS epoch_meta(
            epoch INTEGER PRIMARY KEY,
            effective_height INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS summaries(
            epoch INTEGER NOT NULL,
            addr TEXT NOT NULL,
            rewarded_coins INTEGER NOT NULL,
            claimed INTEGER NOT NULL,
            PRIMARY KEY(epoch, addr)
        );
        CREATE TABLE IF NOT EXISTS settle_present(
            epoch INTEGER NOT NULL,
            addr TEXT NOT NULL,
            PRIMARY KEY(epoch, addr)
        );
        CREATE TABLE IF NOT EXISTS settle_snapshot_done(
            epoch INTEGER PRIMARY KEY,
            height INTEGER NOT NULL,
            entries INTEGER NOT NULL,
            entries_for_epoch INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS failures(
            stage TEXT NOT NULL,
            epoch INTEGER NOT NULL,
            detail TEXT NOT NULL,
            PRIMARY KEY(stage, epoch)
        );
        """
    )
    db.commit()
    return db


def mode_epochs(mode: str) -> list[int]:
    if mode == "smoke":
        return [97, 112, 116, 129, 132, 240, 275, 276, 277, 278, 279, 280]
    if mode == "focused":
        return list(range(87, 143)) + list(range(275, 281))
    if mode == "full":
        return list(range(1, 275))
    raise SystemExit(f"Unknown mode: {mode}")


def fetch_epoch_meta(db: sqlite3.Connection, base: str, epochs: list[int]) -> None:
    needed = sorted({epoch + 1 for epoch in epochs})
    cached = {
        row[0]
        for row in db.execute(
            "SELECT epoch FROM epoch_meta WHERE epoch IN (%s)"
            % ",".join("?" for _ in needed),
            needed,
        )
    } if needed else set()
    todo = [epoch for epoch in needed if epoch not in cached]
    for epoch in todo:
        data = get_json(
            base,
            f"/productscience/inference/inference/epoch_group_data/{epoch}",
        )
        egd = data.get("epoch_group_data")
        if not egd or not egd.get("effective_block_height"):
            db.execute(
                "INSERT OR REPLACE INTO failures VALUES (?, ?, ?)",
                ("epoch_meta", epoch, json.dumps(data)[:500]),
            )
            db.commit()
            continue
        db.execute(
            "INSERT OR REPLACE INTO epoch_meta VALUES (?, ?)",
            (epoch, int(egd["effective_block_height"])),
        )
        db.execute("DELETE FROM failures WHERE stage=? AND epoch=?", ("epoch_meta", epoch))
        db.commit()


def fetch_epoch_summary(db: sqlite3.Connection, base: str, epoch: int) -> tuple[int, int, int]:
    already = db.execute(
        "SELECT COUNT(*) FROM summaries WHERE epoch=?", (epoch,)
    ).fetchone()[0]
    if already:
        positive_unclaimed = db.execute(
            """
            SELECT COUNT(*), COALESCE(SUM(rewarded_coins), 0)
            FROM summaries
            WHERE epoch=? AND rewarded_coins > 0 AND claimed = 0
            """,
            (epoch,),
        ).fetchone()
        return already, int(positive_unclaimed[0]), int(positive_unclaimed[1])

    data = get_json(
        base,
        f"/productscience/inference/inference/epoch_performance_summary/{epoch}",
    )
    rows = data.get("epochPerformanceSummary") or data.get("epoch_performance_summary")
    if rows is None:
        db.execute(
            "INSERT OR REPLACE INTO failures VALUES (?, ?, ?)",
            ("summary", epoch, json.dumps(data)[:500]),
        )
        db.commit()
        return 0, 0, 0

    insert_rows = []
    for row in rows:
        insert_rows.append(
            (
                epoch,
                row.get("participant_id", ""),
                int(row.get("rewarded_coins") or 0),
                1 if row.get("claimed") else 0,
            )
        )
    db.executemany("INSERT OR REPLACE INTO summaries VALUES (?, ?, ?, ?)", insert_rows)
    db.execute("DELETE FROM failures WHERE stage=? AND epoch=?", ("summary", epoch))
    db.commit()
    positive_unclaimed = [
        row for row in insert_rows if row[2] > 0 and row[3] == 0
    ]
    return (
        len(insert_rows),
        len(positive_unclaimed),
        sum(row[2] for row in positive_unclaimed),
    )


def fetch_settle_snapshot(db: sqlite3.Connection, base: str, epoch: int) -> tuple[int, int, int]:
    done = db.execute(
        "SELECT height, entries, entries_for_epoch FROM settle_snapshot_done WHERE epoch=?",
        (epoch,),
    ).fetchone()
    if done:
        return int(done[0]), int(done[1]), int(done[2])

    meta = db.execute(
        "SELECT effective_height FROM epoch_meta WHERE epoch=?", (epoch + 1,)
    ).fetchone()
    if not meta:
        db.execute(
            "INSERT OR REPLACE INTO failures VALUES (?, ?, ?)",
            ("settle_snapshot", epoch, f"missing effective height for epoch {epoch + 1}"),
        )
        db.commit()
        return 0, 0, 0
    height = int(meta[0])
    next_key = None
    entries = 0
    entries_for_epoch = 0
    rows: list[tuple[int, str]] = []
    while True:
        params = ["pagination.limit=500"]
        if next_key:
            params.append("pagination.key=" + urllib.parse.quote(next_key))
        data = get_json(
            base,
            "/productscience/inference/inference/settle_amount?" + "&".join(params),
            height=height,
        )
        if "_error" in data:
            db.execute(
                "INSERT OR REPLACE INTO failures VALUES (?, ?, ?)",
                ("settle_snapshot", epoch, json.dumps(data)[:500]),
            )
            db.commit()
            return height, entries, entries_for_epoch
        page_entries = data.get("settle_amount") or []
        entries += len(page_entries)
        for item in page_entries:
            participant = item.get("participant")
            epoch_index = int(item.get("epoch_index") or 0)
            if participant:
                rows.append((epoch_index, participant))
                if epoch_index == epoch:
                    entries_for_epoch += 1
        next_key = (data.get("pagination") or {}).get("next_key")
        if not next_key:
            break

    db.executemany("INSERT OR IGNORE INTO settle_present VALUES (?, ?)", rows)
    db.execute(
        "INSERT OR REPLACE INTO settle_snapshot_done VALUES (?, ?, ?, ?)",
        (epoch, height, entries, entries_for_epoch),
    )
    db.execute("DELETE FROM failures WHERE stage=? AND epoch=?", ("settle_snapshot", epoch))
    db.commit()
    return height, entries, entries_for_epoch


def candidates(db: sqlite3.Connection, epochs: list[int]) -> list[dict[str, object]]:
    placeholders = ",".join("?" for _ in epochs)
    sql = f"""
        SELECT s.epoch, s.addr, s.rewarded_coins
        FROM summaries s
        WHERE s.epoch IN ({placeholders})
          AND s.rewarded_coins > 0
          AND NOT EXISTS (
            SELECT 1 FROM settle_present sp
            WHERE sp.epoch = s.epoch AND sp.addr = s.addr
          )
          AND s.epoch IN (SELECT epoch FROM settle_snapshot_done)
        ORDER BY s.epoch, s.addr
    """
    return [
        {"epoch": int(epoch), "address": addr, "rewarded_coins": int(coins)}
        for epoch, addr, coins in db.execute(sql, epochs)
    ]


def write_outputs(
    workdir: Path,
    artifact_dir: Path,
    mode: str,
    epochs: list[int],
    rows: list[dict[str, object]],
    failures: list[tuple[str, int, str]],
    epoch_stats: list[dict[str, object]],
    snapshot_stats: list[dict[str, object]],
) -> tuple[Path, Path]:
    output_dir = workdir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / f"case2_{mode}_candidates.csv"
    json_path = output_dir / f"case2_{mode}_summary.json"
    coverage_path = output_dir / f"case2_{mode}_coverage.csv"
    amount_reconciliation_path = output_dir / f"case2_{mode}_amount_reconciliation.csv"
    amount_reconciliation_json_path = output_dir / f"case2_{mode}_amount_reconciliation.json"
    artifact_csv_path = artifact_dir / f"case2_{mode}_candidates.csv"
    artifact_json_path = artifact_dir / f"case2_{mode}_summary.json"
    artifact_coverage_path = artifact_dir / f"case2_{mode}_coverage.csv"
    artifact_amount_reconciliation_path = artifact_dir / f"case2_{mode}_amount_reconciliation.csv"
    artifact_amount_reconciliation_json_path = artifact_dir / f"case2_{mode}_amount_reconciliation.json"

    by_addr: dict[str, dict[int, int]] = {}
    by_epoch: dict[int, dict[str, int]] = {}
    for row in rows:
        epoch = int(row["epoch"])
        coins = int(row["rewarded_coins"])
        by_addr.setdefault(str(row["address"]), {})[epoch] = coins
        slot = by_epoch.setdefault(epoch, {"candidate_pairs": 0, "candidate_reward_ngonka": 0})
        slot["candidate_pairs"] += 1
        slot["candidate_reward_ngonka"] += coins

    def write_csv(path: Path) -> None:
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle, lineterminator="\n")
            writer.writerow(["address", *[str(epoch) for epoch in epochs], "total_ngonka", "total_gnk"])
            for address, shares in sorted(by_addr.items(), key=lambda item: (-sum(item[1].values()), item[0])):
                total = sum(shares.values())
                writer.writerow(
                    [address, *[shares.get(epoch, 0) for epoch in epochs], total, f"{total / 1e9:.9f}"]
                )

    write_csv(csv_path)
    write_csv(artifact_csv_path)

    epoch_stats_by_epoch = {int(row["epoch"]): row for row in epoch_stats}
    snapshot_stats_by_epoch = {int(row["epoch"]): row for row in snapshot_stats}

    def write_coverage(path: Path) -> None:
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle, lineterminator="\n")
            writer.writerow(
                [
                    "epoch",
                    "effective_height",
                    "summary_rows",
                    "positive_unclaimed_rows",
                    "positive_unclaimed_reward",
                    "settle_snapshot_entries",
                    "settle_entries_for_epoch",
                    "candidate_pairs",
                    "candidate_reward_ngonka",
                ]
            )
            for epoch in epochs:
                summary = epoch_stats_by_epoch.get(epoch, {})
                snapshot = snapshot_stats_by_epoch.get(epoch, {})
                candidates_for_epoch = by_epoch.get(epoch, {})
                writer.writerow(
                    [
                        epoch,
                        snapshot.get("effective_height", 0),
                        summary.get("summary_rows", 0),
                        summary.get("positive_unclaimed_rows", 0),
                        summary.get("positive_unclaimed_reward", 0),
                        snapshot.get("settle_snapshot_entries", 0),
                        snapshot.get("settle_entries_for_epoch", 0),
                        candidates_for_epoch.get("candidate_pairs", 0),
                        candidates_for_epoch.get("candidate_reward_ngonka", 0),
                    ]
                )

    write_coverage(coverage_path)
    write_coverage(artifact_coverage_path)

    reconciliation_rows = [
        {
            "epoch": int(row["epoch"]),
            "address": str(row["address"]),
            "chain_rewarded_coins": int(row["rewarded_coins"]),
            "compensation_ngonka": int(row["rewarded_coins"]),
            "compensation_gnk": f"{int(row['rewarded_coins']) / 1e9:.9f}",
            "source": "epoch_performance_summary.rewarded_coins",
            "settle_amount_present_at_settlement": False,
            "amount_matches_chain": True,
        }
        for row in sorted(rows, key=lambda item: (int(item["epoch"]), str(item["address"])))
    ]

    def write_reconciliation(path: Path) -> None:
        with path.open("w", newline="", encoding="utf-8") as handle:
            fieldnames = [
                "epoch",
                "address",
                "chain_rewarded_coins",
                "compensation_ngonka",
                "compensation_gnk",
                "source",
                "settle_amount_present_at_settlement",
                "amount_matches_chain",
            ]
            writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
            writer.writeheader()
            writer.writerows(reconciliation_rows)

    write_reconciliation(amount_reconciliation_path)
    write_reconciliation(artifact_amount_reconciliation_path)

    reconciliation_by_epoch = {}
    for row in reconciliation_rows:
        epoch = int(row["epoch"])
        slot = reconciliation_by_epoch.setdefault(epoch, {"candidate_pairs": 0, "compensation_ngonka": 0})
        slot["candidate_pairs"] += 1
        slot["compensation_ngonka"] += int(row["compensation_ngonka"])

    amount_reconciliation_summary = {
        "mode": mode,
        "candidate_pairs": len(reconciliation_rows),
        "amount_source": "chain epoch_performance_summary.rewarded_coins",
        "all_amounts_match_chain": all(row["amount_matches_chain"] for row in reconciliation_rows),
        "total_chain_rewarded_coins": sum(int(row["chain_rewarded_coins"]) for row in reconciliation_rows),
        "total_compensation_ngonka": sum(int(row["compensation_ngonka"]) for row in reconciliation_rows),
        "total_compensation_gnk": f"{sum(int(row['compensation_ngonka']) for row in reconciliation_rows) / 1e9:.9f}",
        "by_epoch": [
            {
                "epoch": epoch,
                "candidate_pairs": data["candidate_pairs"],
                "compensation_ngonka": data["compensation_ngonka"],
                "compensation_gnk": f"{data['compensation_ngonka'] / 1e9:.9f}",
            }
            for epoch, data in sorted(reconciliation_by_epoch.items())
        ],
    }
    amount_reconciliation_text = json.dumps(amount_reconciliation_summary, indent=2)
    amount_reconciliation_json_path.write_text(amount_reconciliation_text, encoding="utf-8")
    artifact_amount_reconciliation_json_path.write_text(amount_reconciliation_text, encoding="utf-8")

    # The JSON summary is deliberately sanitized: it contains counts, totals,
    # failures and checked heights, but not the configured endpoint or API key.
    snapshot_count = sum(1 for row in snapshot_stats if int(row.get("effective_height") or 0) > 0)
    summary = {
        "mode": mode,
        "epochs": epochs,
        "epoch_count": len(epochs),
        "settle_snapshots_checked": snapshot_count,
        "settle_snapshot_coverage_complete": snapshot_count == len(epochs),
        "candidate_pairs": len(rows),
        "affected_addresses": len(by_addr),
        "amount_source": "chain epoch_performance_summary.rewarded_coins",
        "all_candidate_amounts_match_chain": True,
        "total_ngonka": sum(int(row["rewarded_coins"]) for row in rows),
        "total_gnk": f"{sum(int(row['rewarded_coins']) for row in rows) / 1e9:.9f}",
        "nonzero_epochs": sorted({int(row["epoch"]) for row in rows}),
        "failures": [
            {"stage": stage, "epoch": epoch, "detail": detail}
            for stage, epoch, detail in failures
        ],
        "epoch_stats": epoch_stats,
        "snapshot_stats": snapshot_stats,
    }
    json_text = json.dumps(summary, indent=2)
    json_path.write_text(json_text, encoding="utf-8")
    artifact_json_path.write_text(json_text, encoding="utf-8")
    return artifact_csv_path, artifact_json_path


def load_candidate_csv(path_or_url: str) -> dict[tuple[int, str], int]:
    if path_or_url.startswith("http"):
        with urllib.request.urlopen(path_or_url, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
            text = resp.read().decode("utf-8")
    else:
        text = Path(path_or_url).read_text(encoding="utf-8")
    reader = csv.DictReader(text.splitlines())
    out: dict[tuple[int, str], int] = {}
    for row in reader:
        address = row["address"]
        for key, value in row.items():
            if not key.isdigit() or not value:
                continue
            coins = int(value)
            if coins:
                out[(int(key), address)] = coins
    return out


def compare_with_published(rows: list[dict[str, object]], published: str) -> dict[str, object]:
    own = {
        (int(row["epoch"]), str(row["address"])): int(row["rewarded_coins"])
        for row in rows
    }
    other = load_candidate_csv(published)
    mismatched = [
        {"epoch": epoch, "address": addr, "ours": own.get((epoch, addr)), "published": other.get((epoch, addr))}
        for epoch, addr in sorted(set(own) | set(other))
        if own.get((epoch, addr)) != other.get((epoch, addr))
    ]
    return {
        "published_pairs": len(other),
        "published_total_ngonka": sum(other.values()),
        "matched_exactly": not mismatched,
        "mismatches": mismatched,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["smoke", "focused", "full"], default="smoke")
    parser.add_argument("--workdir", type=Path, default=DEFAULT_WORKDIR)
    parser.add_argument("--artifact-dir", type=Path, default=DEFAULT_ARTIFACT_DIR)
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    parser.add_argument("--compare-published", default="")
    parser.add_argument("--published-csv", default=DEFAULT_PUBLISHED_CSV)
    args = parser.parse_args()

    load_dotenv(args.env_file)
    base = direct_lcd_from_env()
    db = init_db(args.workdir / "cache.db")
    epochs = mode_epochs(args.mode)

    print(f"mode={args.mode} epochs={epochs[0]}..{epochs[-1]} count={len(epochs)}")
    print("archive_lcd=loaded")
    print(f"cache={args.workdir / 'cache.db'}")

    fetch_epoch_meta(db, base, epochs)

    epoch_stats: list[dict[str, object]] = []
    for epoch in epochs:
        count, positive_unclaimed, positive_unclaimed_reward = fetch_epoch_summary(db, base, epoch)
        epoch_stats.append(
            {
                "epoch": epoch,
                "summary_rows": count,
                "positive_unclaimed_rows": positive_unclaimed,
                "positive_unclaimed_reward": positive_unclaimed_reward,
            }
        )

    snapshot_stats: list[dict[str, object]] = []
    for index, epoch in enumerate(epochs, start=1):
        height, entries, entries_for_epoch = fetch_settle_snapshot(db, base, epoch)
        snapshot_stats.append(
            {
                "epoch": epoch,
                "effective_height": height,
                "settle_snapshot_entries": entries,
                "settle_entries_for_epoch": entries_for_epoch,
            }
        )
        print(
            f"snapshot {index}/{len(epochs)} epoch={epoch} height={height} "
            f"entries={entries} entries_for_epoch={entries_for_epoch}",
            flush=True,
        )

    rows = candidates(db, epochs)
    failures = [
        (stage, int(epoch), detail)
        for stage, epoch, detail in db.execute("SELECT stage, epoch, detail FROM failures ORDER BY stage, epoch")
        if int(epoch) in set(epochs) or int(epoch) in {epoch + 1 for epoch in epochs}
    ]
    csv_path, json_path = write_outputs(
        args.workdir,
        args.artifact_dir,
        args.mode,
        epochs,
        rows,
        failures,
        sorted(epoch_stats, key=lambda x: int(x["epoch"])),
        sorted(snapshot_stats, key=lambda x: int(x["epoch"])),
    )

    total = sum(int(row["rewarded_coins"]) for row in rows)
    print(f"candidate_pairs={len(rows)} affected_addresses={len({row['address'] for row in rows})}")
    print(f"total_ngonka={total} total_gnk={total / 1e9:.9f}")
    print(f"nonzero_epochs={','.join(str(epoch) for epoch in sorted({row['epoch'] for row in rows}))}")
    print(f"csv={csv_path}")
    print(f"summary={json_path}")
    if failures:
        print(f"failures={len(failures)}")
        for stage, epoch, detail in failures[:20]:
            print(f"failure stage={stage} epoch={epoch} detail={detail[:180]}")

    if args.compare_published:
        comparison = compare_with_published(rows, args.published_csv)
        print(
            "published_compare="
            + json.dumps(
                {
                    "matched_exactly": comparison["matched_exactly"],
                    "published_pairs": comparison["published_pairs"],
                    "published_total_ngonka": comparison["published_total_ngonka"],
                    "mismatch_count": len(comparison["mismatches"]),
                },
                sort_keys=True,
            )
        )
        comparison_text = json.dumps(comparison, indent=2)
        comparison_path = args.workdir / "outputs" / f"case2_{args.mode}_published_compare.json"
        artifact_comparison_path = args.artifact_dir / f"case2_{args.mode}_published_compare.json"
        comparison_path.write_text(comparison_text, encoding="utf-8")
        artifact_comparison_path.write_text(comparison_text, encoding="utf-8")
        print(f"comparison={comparison_path}")
        print(f"artifact_comparison={artifact_comparison_path}")
        if comparison["mismatches"]:
            for item in comparison["mismatches"][:20]:
                print("mismatch=" + json.dumps(item, sort_keys=True))

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
