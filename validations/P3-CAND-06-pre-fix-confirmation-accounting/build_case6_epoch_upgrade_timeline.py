#!/usr/bin/env python3
"""Build epoch boundary timestamps and v0.2.13 upgrade timing for P3-CAND-06."""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


CASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = CASE_DIR.parents[1]
CACHE_DIR = CASE_DIR / "raw_stage_cache" / "block_headers"
REQUEST_TIMEOUT_SECONDS = 45
RETRIES = 4
UPGRADE_HEIGHT = 4_267_300
UPGRADE_VERSION = "v0.2.13"


def load_dotenv() -> None:
    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


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


def request_headers() -> dict[str, str]:
    headers = {"User-Agent": "grc-case6-epoch-upgrade-timeline/1.0"}
    api_key = os.environ.get("GONKA_RPC_API_KEY")
    if api_key:
        headers["X-Api-Key"] = api_key
    return headers


def cache_name(path: str) -> str:
    digest = hashlib.sha256(path.encode("utf-8")).hexdigest()[:16]
    safe = path.strip("/").replace("/", "_")
    return f"{safe}.{digest}.json"


def get_json_from_base(base: str, path: str, *, refresh: bool = False) -> Any:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / cache_name(path)
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
        except Exception as exc:  # noqa: BLE001 - audit scripts retry broadly
            last_error = str(exc)
        time.sleep(min(20, 1 + attempt * 2))
    raise RuntimeError(f"Failed to fetch {path}: {last_error}")


def get_json(base_urls: list[str], path: str, *, refresh: bool = False) -> Any:
    errors = []
    for base in base_urls:
        try:
            return get_json_from_base(base, path, refresh=refresh)
        except Exception as exc:  # noqa: BLE001 - try next configured LCD
            errors.append(str(exc))
    raise RuntimeError(f"Failed to fetch {path} from configured LCDs: {errors[-1] if errors else 'no base URLs'}")


def normalize_base_url(value: str) -> str:
    if not value.startswith(("http://", "https://")):
        value = "http://" + value
    parsed = urllib.parse.urlparse(value)
    if parsed.hostname and parsed.port is None:
        netloc = f"{parsed.hostname}:8000"
        return urllib.parse.urlunparse((parsed.scheme, netloc, parsed.path, "", "", ""))
    return value


def base_urls() -> list[str]:
    urls = ["http://node1.gonka.ai:8000/chain-api"]
    env_base = os.environ.get("GONKA_RPC_URL")
    if env_base:
        urls.append(normalize_base_url(env_base))
        urls.append(normalize_base_url(env_base).rstrip("/") + "/chain-api")
    return list(dict.fromkeys(urls))


def block_time(urls: list[str], height: int) -> tuple[str, str, str]:
    payload = get_json(urls, f"/cosmos/base/tendermint/v1beta1/blocks/{height}")
    raw = payload["block"]["header"]["time"]
    utc = dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
    msk = utc.astimezone(dt.timezone(dt.timedelta(hours=3)))
    return raw, utc.strftime("%Y-%m-%d %H:%M:%S UTC"), msk.strftime("%Y-%m-%d %H:%M:%S MSK")


def known_boundaries() -> dict[int, dict[str, int]]:
    rows = read_csv(CASE_DIR / "participant_epoch_timeline.csv")
    by_epoch: dict[int, dict[str, int]] = {}
    for row in rows:
        epoch = int(row["epoch"])
        by_epoch.setdefault(
            epoch,
            {
                "poc_start_height": int(row["poc_start_height"]),
                "effective_start_height": int(row["epoch_effective_height"]),
                "last_height": int(row["epoch_last_height"]),
                "next_epoch_height": int(row["next_epoch_height"]),
            },
        )
    return by_epoch


def interpolate_boundaries() -> dict[int, dict[str, int]]:
    known = known_boundaries()
    epoch_step = known[264]["poc_start_height"] - known[263]["poc_start_height"]
    effective_offset = known[263]["effective_start_height"] - known[263]["poc_start_height"]
    last_offset = known[263]["last_height"] - known[263]["poc_start_height"]
    next_offset = known[263]["next_epoch_height"] - known[263]["poc_start_height"]

    first_poc = known[263]["poc_start_height"]
    boundaries: dict[int, dict[str, int]] = {}
    for epoch in range(263, 278):
        poc = first_poc + (epoch - 263) * epoch_step
        boundaries[epoch] = {
            "poc_start_height": poc,
            "effective_start_height": poc + effective_offset,
            "last_height": poc + last_offset,
            "next_epoch_height": poc + next_offset,
        }
    for epoch, values in known.items():
        boundaries[epoch] = values
    return boundaries


def build_rows(urls: list[str]) -> list[dict[str, Any]]:
    boundaries = interpolate_boundaries()
    rows = []
    upgrade_raw, upgrade_utc, upgrade_msk = block_time(urls, UPGRADE_HEIGHT)
    for epoch in sorted(boundaries):
        values = boundaries[epoch]
        poc_raw, poc_utc, poc_msk = block_time(urls, values["poc_start_height"])
        eff_raw, eff_utc, eff_msk = block_time(urls, values["effective_start_height"])
        last_raw, last_utc, last_msk = block_time(urls, values["last_height"])
        upgrade_relation = "pre_upgrade"
        if values["poc_start_height"] <= UPGRADE_HEIGHT <= values["last_height"]:
            upgrade_relation = "upgrade_applied_during_epoch"
        elif values["poc_start_height"] > UPGRADE_HEIGHT:
            upgrade_relation = "post_upgrade_clean_start"
        rows.append(
            {
                "epoch": epoch,
                "poc_start_height": values["poc_start_height"],
                "poc_start_utc": poc_utc,
                "poc_start_msk": poc_msk,
                "effective_start_height": values["effective_start_height"],
                "effective_start_utc": eff_utc,
                "effective_start_msk": eff_msk,
                "last_height": values["last_height"],
                "last_utc": last_utc,
                "last_msk": last_msk,
                "upgrade_version": UPGRADE_VERSION if upgrade_relation == "upgrade_applied_during_epoch" else "",
                "upgrade_height": UPGRADE_HEIGHT if upgrade_relation == "upgrade_applied_during_epoch" else "",
                "upgrade_utc": upgrade_utc if upgrade_relation == "upgrade_applied_during_epoch" else "",
                "upgrade_msk": upgrade_msk if upgrade_relation == "upgrade_applied_during_epoch" else "",
                "upgrade_relation": upgrade_relation,
                "raw_times": {
                    "poc_start": poc_raw,
                    "effective_start": eff_raw,
                    "last": last_raw,
                    "upgrade": upgrade_raw if upgrade_relation == "upgrade_applied_during_epoch" else "",
                },
            }
        )
    return rows


def write_md(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = [
        "# P3-CAND-06 Epoch Start And v0.2.13 Upgrade Timeline",
        "",
        "Block timestamps are Tendermint block header times from",
        "`/cosmos/base/tendermint/v1beta1/blocks/{height}`. UTC and MSK",
        "(UTC+03:00) are both shown.",
        "",
        f"`{UPGRADE_VERSION}` was applied on-chain at block `{UPGRADE_HEIGHT}`.",
        "It lands inside epoch `276`; epoch `277` is the first clean epoch start",
        "after the upgrade.",
        "",
        "## Epoch Timeline",
        "",
        "| Epoch | PoC start height | PoC start UTC | PoC start MSK | Effective start height | Effective start UTC | Effective start MSK | Last height | Last MSK | Upgrade marker |",
        "|---:|---:|---|---|---:|---|---|---:|---|---|",
    ]
    for row in rows:
        marker = row["upgrade_relation"]
        if row["upgrade_relation"] == "upgrade_applied_during_epoch":
            marker = f"{row['upgrade_version']} at {row['upgrade_height']} / {row['upgrade_msk']}"
        lines.append(
            f"| `{row['epoch']}` | `{row['poc_start_height']}` | `{row['poc_start_utc']}` | "
            f"`{row['poc_start_msk']}` | `{row['effective_start_height']}` | "
            f"`{row['effective_start_utc']}` | `{row['effective_start_msk']}` | "
            f"`{row['last_height']}` | `{row['last_msk']}` | `{marker}` |"
        )

    lines.extend(
        [
            "",
            "## Upgrade Point",
            "",
            "| Item | Height | UTC | MSK |",
            "|---|---:|---|---|",
        ]
    )
    upgrade_row = next(row for row in rows if row["upgrade_relation"] == "upgrade_applied_during_epoch")
    lines.append(
        f"| `{UPGRADE_VERSION}` applied on-chain | `{upgrade_row['upgrade_height']}` | "
        f"`{upgrade_row['upgrade_utc']}` | `{upgrade_row['upgrade_msk']}` |"
    )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Epochs `263..275` are before the on-chain `v0.2.13` application.",
            "- Epoch `276` contains the upgrade application point and remains overlap",
            "  sensitive with P3-CAND-04.",
            "- Epoch `277` is the first clean epoch start after the upgrade.",
            "",
            "Machine-readable versions are in",
            "`case6_epoch_upgrade_timeline.csv` and",
            "`case6_epoch_upgrade_timeline.json`.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    load_dotenv()
    rows = build_rows(base_urls())
    fieldnames = [
        "epoch",
        "poc_start_height",
        "poc_start_utc",
        "poc_start_msk",
        "effective_start_height",
        "effective_start_utc",
        "effective_start_msk",
        "last_height",
        "last_utc",
        "last_msk",
        "upgrade_version",
        "upgrade_height",
        "upgrade_utc",
        "upgrade_msk",
        "upgrade_relation",
    ]
    write_csv(CASE_DIR / "case6_epoch_upgrade_timeline.csv", rows, fieldnames)
    write_json(CASE_DIR / "case6_epoch_upgrade_timeline.json", {"rows": rows})
    write_md(CASE_DIR / "case6_epoch_upgrade_timeline.md", rows)
    print(json.dumps({"rows": len(rows), "upgrade_height": UPGRADE_HEIGHT}, sort_keys=True))


if __name__ == "__main__":
    main()
