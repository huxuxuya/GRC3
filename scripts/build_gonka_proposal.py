#!/usr/bin/env python3
"""Build Gonka governance proposal JSON from settlement and role config."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
NGONKA = Decimal("1000000000")
DENOM = "ngonka"


def gonka_to_ngonka(value: str) -> int:
    return int((Decimal(str(value or "0")) * NGONKA).to_integral_value(rounding=ROUND_HALF_UP))


def format_gonka(amount_ngonka: int) -> str:
    return f"{Decimal(amount_ngonka) / NGONKA:.9f}"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def is_gonka_address(value: str) -> bool:
    return isinstance(value, str) and value.startswith("gonka1") and len(value) >= 40


def role_entries(role_config: dict) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for case in role_config.get("cases", []):
        family = case.get("case_family", "")
        rejected_by_coordinator = case.get("status") == "rejected_by_coordinator"
        for role_name in ("investigators", "validators"):
            singular = role_name[:-1]
            for person in case.get(role_name, []):
                amount = 0 if rejected_by_coordinator else gonka_to_ngonka(person.get("amount_gonka", "0"))
                entries.append(
                    {
                        "case_family": family,
                        "role": singular,
                        "name": person.get("name", ""),
                        "address": person.get("address", ""),
                        "amount_ngonka": amount,
                        "amount_gonka": format_gonka(amount),
                        "comment": person.get("comment", ""),
                    }
                )
        organizer = case.get("organizer") or {}
        amount = 0 if rejected_by_coordinator else gonka_to_ngonka(organizer.get("amount_gonka", "0"))
        entries.append(
            {
                "case_family": family,
                "role": "organizer",
                "name": organizer.get("name", ""),
                "address": organizer.get("address", ""),
                "amount_ngonka": amount,
                "amount_gonka": format_gonka(amount),
                "comment": organizer.get("comment", ""),
            }
        )
    return entries


def validate_role_entries(entries: list[dict[str, object]]) -> list[str]:
    errors = []
    for entry in entries:
        if int(entry["amount_ngonka"]) <= 0:
            continue
        address = str(entry.get("address", ""))
        if not is_gonka_address(address):
            errors.append(
                f"{entry['case_family']} {entry['role']} {entry['name']} has non-zero amount {entry['amount_gonka']} but no valid gonka address"
            )
    return errors


def build_victim_outputs(settlement: dict) -> tuple[list[dict], list[dict]]:
    by_address: dict[str, int] = defaultdict(int)
    breakdown: list[dict] = []
    for row in settlement["rows"]:
        amount = int(row["final_payout_ngonka"])
        if amount <= 0:
            continue
        address = row["address"]
        by_address[address] += amount
        breakdown.append(
            {
                "category": "victim",
                "case_family": row["case_family"],
                "epoch": row["epoch"],
                "address": address,
                "amount_ngonka": amount,
                "amount_gonka": format_gonka(amount),
                "source_row": row,
            }
        )
    outputs = [
        {
            "recipient": address,
            "amount": [{"denom": DENOM, "amount": str(amount)}],
        }
        for address, amount in sorted(by_address.items())
        if amount > 0
    ]
    return outputs, breakdown


def build_role_messages(entries: list[dict[str, object]], authority: str) -> tuple[list[dict], list[dict]]:
    messages = []
    breakdown = []
    for entry in entries:
        amount = int(entry["amount_ngonka"])
        if amount <= 0:
            continue
        messages.append(
            {
                "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
                "authority": authority,
                "recipient": entry["address"],
                "amount": [{"denom": DENOM, "amount": str(amount)}],
            }
        )
        breakdown.append(
            {
                "category": "role",
                "case_family": entry["case_family"],
                "role": entry["role"],
                "name": entry["name"],
                "address": entry["address"],
                "amount_ngonka": amount,
                "amount_gonka": format_gonka(amount),
                "comment": entry["comment"],
            }
        )
    return messages, breakdown


def build_proposal(settlement: dict, role_config: dict) -> tuple[dict, dict]:
    settings = role_config["settings"]
    authority = settings["authority"]
    victim_outputs, victim_breakdown = build_victim_outputs(settlement)

    entries = role_entries(role_config)
    errors = validate_role_entries(entries)
    if errors:
        raise SystemExit("Cannot build proposal JSON:\n- " + "\n- ".join(errors))

    role_messages, role_breakdown = build_role_messages(entries, authority)
    messages = [
        {
            "@type": "/inference.streamvesting.MsgBatchTransferWithVesting",
            "sender": authority,
            "outputs": victim_outputs,
            "vesting_epochs": str(settings.get("vesting_epochs", "150")),
        },
        *role_messages,
    ]
    proposal = {
        "messages": messages,
        "metadata": settings.get("metadata", ""),
        "deposit": settings.get("deposit", "50000000ngonka"),
        "title": settings.get("title", "GRC Proposal #3 - Restitution"),
        "summary": settings.get("summary", ""),
    }

    victim_total = sum(int(item["amount_ngonka"]) for item in victim_breakdown)
    role_total = sum(int(item["amount_ngonka"]) for item in role_breakdown)
    breakdown = {
        "totals": {
            "victim_payout_ngonka": victim_total,
            "victim_payout_gonka": format_gonka(victim_total),
            "role_payout_ngonka": role_total,
            "role_payout_gonka": format_gonka(role_total),
            "proposal_total_ngonka": victim_total + role_total,
            "proposal_total_gonka": format_gonka(victim_total + role_total),
            "victim_recipient_count": len(victim_outputs),
            "role_message_count": len(role_messages),
        },
        "entries": [*victim_breakdown, *role_breakdown],
    }
    return proposal, breakdown


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--settlement", type=Path, default=BASE / "docs/data/settlement.json")
    parser.add_argument("--roles", type=Path, default=BASE / "docs/data/role_config.json")
    parser.add_argument("--proposal-out", type=Path, default=BASE / "docs/data/proposal.json")
    parser.add_argument("--breakdown-out", type=Path, default=BASE / "docs/data/payout_breakdown.json")
    args = parser.parse_args()

    proposal, breakdown = build_proposal(load_json(args.settlement), load_json(args.roles))
    args.proposal_out.parent.mkdir(parents=True, exist_ok=True)
    args.breakdown_out.parent.mkdir(parents=True, exist_ok=True)
    args.proposal_out.write_text(json.dumps(proposal, indent=2, sort_keys=True) + "\n")
    args.breakdown_out.write_text(json.dumps(breakdown, indent=2, sort_keys=True) + "\n")
    print(f"victim_total={breakdown['totals']['victim_payout_gonka']}")
    print(f"role_total={breakdown['totals']['role_payout_gonka']}")
    print(f"proposal_total={breakdown['totals']['proposal_total_gonka']}")


if __name__ == "__main__":
    main()
