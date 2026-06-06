#!/usr/bin/env python3
"""Build address/epoch compensation ledger and overlap matrix.

The generated files are intentionally derived from raw/source CSVs. This keeps
the overlap review reproducible and avoids hand-maintained per-address totals.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
NGONKA = Decimal("1000000000")
EXCLUDED_FROM_CURRENT_CROSSTAB = {"P3-CAND-06"}
PAID_REFERENCE_FAMILIES = {"P4-CAND-01"}


@dataclass(frozen=True)
class Row:
    case_track: str
    case_family: str
    status_group: str
    source_scope: str
    epoch: int
    address: str
    amount_ngonka: int
    source_file: str
    source_repo_head: str
    note: str

    @property
    def amount_gonka(self) -> str:
        return format_gonka(self.amount_ngonka)


def format_gonka(amount_ngonka: int) -> str:
    return f"{Decimal(amount_ngonka) / NGONKA:.9f}"


def gonka_to_ngonka(value: str) -> int:
    return int((Decimal(value) * NGONKA).to_integral_value(rounding=ROUND_HALF_UP))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh))


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(BASE))
    except ValueError:
        return str(path)


def add(
    rows: list[Row],
    *,
    case_track: str,
    case_family: str,
    status_group: str,
    source_scope: str,
    epoch: int,
    address: str,
    amount_ngonka: int,
    source_file: Path,
    source_repo_head: str,
    note: str,
) -> None:
    if amount_ngonka <= 0:
        return
    rows.append(
        Row(
            case_track=case_track,
            case_family=case_family,
            status_group=status_group,
            source_scope=source_scope,
            epoch=epoch,
            address=address,
            amount_ngonka=amount_ngonka,
            source_file=rel(source_file),
            source_repo_head=source_repo_head,
            note=note,
        )
    )


def load_p3_cand01(rows: list[Row]) -> None:
    path = Path("/private/tmp/grc-p3-cand01-check/artifacts/epoch_272_reported_and_claimed_zero_reward.csv")
    for row in read_csv(path):
        reported = row["reported_address"] == "True"
        scope = "confirmed_six" if reported else "manual_review_not_in_confirmed_total"
        add(
            rows,
            case_track="P3-CAND-01-confirmed" if reported else "P3-CAND-01-manual-review",
            case_family="P3-CAND-01",
            status_group="pending_estimate",
            source_scope=scope,
            epoch=int(row["epoch"]),
            address=row["participant_id"],
            amount_ngonka=int(row["preliminary_exposure"]),
            source_file=path,
            source_repo_head="huxuxuya/grc-p3-cand01@d2fe976",
            note="Devshard/high miss-rate zero-reward row; manual-review row is not in confirmed-six total.",
        )


def load_p3_cand02(rows: list[Row]) -> None:
    path = Path("/private/tmp/unclaimed-check/unclaimed.csv")
    for row in read_csv(path):
        address = row["address"]
        for epoch_text, value in row.items():
            if not epoch_text.isdigit():
                continue
            add(
                rows,
                case_track="P3-CAND-02",
                case_family="P3-CAND-02",
                status_group="local_validated_recommended",
                source_scope="settle_drop_epoch_cell",
                epoch=int(epoch_text),
                address=address,
                amount_ngonka=int(value),
                source_file=path,
                source_repo_head="gonkavip/unclaimed@658d62b",
                note="Negative-balance settle-drop amount from nonzero epoch cell.",
            )


def load_p3_cand03(rows: list[Row]) -> None:
    source = Path("/private/tmp/GRC-e267-kimi_shortfall-check/BROADER_REVIEW.md")
    address = "gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6"
    add(
        rows,
        case_track="P3-CAND-03-EXT",
        case_family="P3-CAND-03",
        status_group="local_validated_recommended",
        source_scope="same_address_epoch_265_extension",
        epoch=265,
        address=address,
        amount_ngonka=20_896_527_179_100,
        source_file=source,
        source_repo_head="gonkalabs/GRC-e267-kimi_shortfall@9e372ae",
        note="Same-address Kimi cPoC shortfall extension recommended for Case 3.",
    )
    add(
        rows,
        case_track="P3-CAND-03",
        case_family="P3-CAND-03",
        status_group="local_validated_recommended",
        source_scope="strict_epoch_267_kimi",
        epoch=267,
        address=address,
        amount_ngonka=10_262_057_515_369,
        source_file=source,
        source_repo_head="gonkalabs/GRC-e267-kimi_shortfall@9e372ae",
        note="Strict Case 3 Kimi cPoC shortfall row.",
    )


def load_p3_cand04(rows: list[Row]) -> None:
    path = Path("/private/tmp/payout276-check/payout_276.csv")
    for row in read_csv(path):
        add(
            rows,
            case_track="P3-CAND-04",
            case_family="P3-CAND-04",
            status_group="pending_estimate_revalidation_required",
            source_scope=row["reason"],
            epoch=276,
            address=row["address"],
            amount_ngonka=int(row["compensation_ngonka"]),
            source_file=path,
            source_repo_head="gonkavip/payout276@b393de8",
            note="Current payout276 source amount; changed from older locally validated CSV.",
        )


def load_p3_cand06(rows: list[Row]) -> None:
    path = BASE / "validations/P3-CAND-06-pre-fix-confirmation-accounting/case6_gross_compensation_calculation.csv"
    for row in read_csv(path):
        add(
            rows,
            case_track="P3-CAND-06",
            case_family="P3-CAND-06",
            status_group="pending_estimate",
            source_scope=row["calculation_scope"],
            epoch=int(row["epoch"]),
            address=row["participant"],
            amount_ngonka=gonka_to_ngonka(row["gross_compensation_gonka"]),
            source_file=path,
            source_repo_head="local validation package",
            note=row["note"],
        )


def load_p4(rows: list[Row]) -> None:
    root = BASE / "validations/P4-CAND-01-kimi-restitution/source_cache"
    head = "votkon/gonka-kimi-restitution@5462c55"

    e265 = root / "votkon_e265_compensation_265.csv"
    for row in read_csv(e265):
        add(
            rows,
            case_track="P4-e265-source-cpoc",
            case_family="P4-CAND-01",
            status_group="disputed_not_aggregate",
            source_scope="e265_cpoc_attack_attributed",
            epoch=265,
            address=row["address"],
            amount_ngonka=int(row["compensation_ngonka"]),
            source_file=e265,
            source_repo_head=head,
            note="P4 source e265 cPoC/attack-attributed row; aggregate is disputed.",
        )

    e266_nonce = root / "votkon_e266_compensation_266_nonces.csv"
    for row in read_csv(e266_nonce):
        add(
            rows,
            case_track="P4-e266-nonce",
            case_family="P4-CAND-01",
            status_group="pending_estimate",
            source_scope="e266_nonce_scope",
            epoch=266,
            address=row["address"],
            amount_ngonka=int(row["compensation_ngonka"]),
            source_file=e266_nonce,
            source_repo_head=head,
            note="P4 source e266 nonce-scope row; compensability split still under review.",
        )

    e266_delegation = root / "votkon_e266_compensation_266_delegation.csv"
    for row in read_csv(e266_delegation):
        add(
            rows,
            case_track="P4-e266-delegation",
            case_family="P4-CAND-01",
            status_group="pending_estimate",
            source_scope="e266_delegation_scope",
            epoch=266,
            address=row["address"],
            amount_ngonka=int(row["compensation_ngonka"]),
            source_file=e266_delegation,
            source_repo_head=head,
            note="P4 source e266 delegation row; compensability split still under review.",
        )

    for epoch in range(267, 277):
        path = root / f"votkon_e{epoch}_compensation_{epoch}.csv"
        for row in read_csv(path):
            add(
                rows,
                case_track="P4-GroupCap-source",
                case_family="P4-CAND-01",
                status_group="disputed_not_aggregate",
                source_scope="groupcap_source_topup_model",
                epoch=epoch,
                address=row["address"],
                amount_ngonka=int(row["compensation_ngonka"]),
                source_file=path,
                source_repo_head=head,
                note="P4 GroupCap source top-up model; committee must choose/reject model before payout.",
            )


def overlap_action(group: list[Row]) -> str:
    families = {row.case_family for row in group}
    tracks = {row.case_track for row in group}
    if "P4-CAND-01" in families and len(families) > 1:
        return "dedupe_against_p4_before_any_p4_vote_or_payout"
    if tracks == {"P4-e266-nonce", "P4-e266-delegation"}:
        return "internal_p4_e266_component_overlap_review"
    if {"P3-CAND-04", "P3-CAND-06"} <= families:
        return "case4_case6_overlap_review"
    if len(families) > 1:
        return "cross_case_overlap_review"
    return "same_case_component_review"


def write_ledger(rows: list[Row], path: Path) -> None:
    fieldnames = [
        "case_track",
        "case_family",
        "status_group",
        "source_scope",
        "epoch",
        "address",
        "amount_gonka",
        "amount_ngonka",
        "source_file",
        "source_repo_head",
        "note",
    ]
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in sorted(rows, key=lambda r: (r.epoch, r.address, r.case_track, r.source_scope)):
            writer.writerow(
                {
                    "case_track": row.case_track,
                    "case_family": row.case_family,
                    "status_group": row.status_group,
                    "source_scope": row.source_scope,
                    "epoch": row.epoch,
                    "address": row.address,
                    "amount_gonka": row.amount_gonka,
                    "amount_ngonka": row.amount_ngonka,
                    "source_file": row.source_file,
                    "source_repo_head": row.source_repo_head,
                    "note": row.note,
                }
            )


def build_overlaps(rows: list[Row]) -> list[dict[str, str]]:
    by_key = group_by_epoch_address(rows)

    overlaps: list[dict[str, str]] = []
    for (epoch, address), group in sorted(by_key.items()):
        if len(group) < 2:
            continue
        group = sorted(group, key=lambda r: (r.case_track, r.source_scope))
        total = sum(row.amount_ngonka for row in group)
        overlaps.append(
            {
                "epoch": str(epoch),
                "address": address,
                "row_count": str(len(group)),
                "case_family_count": str(len({row.case_family for row in group})),
                "total_amount_gonka_if_naively_summed": format_gonka(total),
                "case_tracks": "; ".join(row.case_track for row in group),
                "amounts_gonka": "; ".join(row.amount_gonka for row in group),
                "status_groups": "; ".join(row.status_group for row in group),
                "source_scopes": "; ".join(row.source_scope for row in group),
                "recommended_action": overlap_action(group),
                "notes": " | ".join(row.note for row in group),
            }
        )
    return overlaps


def group_by_epoch_address(rows: list[Row]) -> dict[tuple[int, str], list[Row]]:
    by_key: dict[tuple[int, str], list[Row]] = defaultdict(list)
    for row in rows:
        by_key[(row.epoch, row.address)].append(row)
    return by_key


def is_current_case_family(case_family: str) -> bool:
    return case_family not in EXCLUDED_FROM_CURRENT_CROSSTAB and case_family not in PAID_REFERENCE_FAMILIES


def paid_reference_intersection_groups(rows: list[Row]) -> list[list[Row]]:
    groups = []
    for group in group_by_epoch_address(rows).values():
        families = {row.case_family for row in group}
        if families & PAID_REFERENCE_FAMILIES and any(is_current_case_family(family) for family in families):
            groups.append(sorted(group, key=lambda r: (r.epoch, r.address, r.case_track, r.source_scope)))
    return sorted(groups, key=lambda group: (group[0].epoch, group[0].address))


def paid_reference_intersection_summary(rows: list[Row]) -> list[dict[str, str]]:
    summary = []
    for group in paid_reference_intersection_groups(rows):
        current_rows = [row for row in group if is_current_case_family(row.case_family)]
        paid_reference_rows = [row for row in group if row.case_family in PAID_REFERENCE_FAMILIES]
        current_total = sum(row.amount_ngonka for row in current_rows)
        paid_reference_total = sum(row.amount_ngonka for row in paid_reference_rows)
        summary.append(
            {
                "epoch": str(group[0].epoch),
                "address": group[0].address,
                "current_tracks": "; ".join(row.case_track for row in current_rows),
                "current_amount_gonka": format_gonka(current_total),
                "paid_reference_tracks": "; ".join(row.case_track for row in paid_reference_rows),
                "paid_reference_amount_gonka": format_gonka(paid_reference_total),
                "naive_total_gonka": format_gonka(current_total + paid_reference_total),
            }
        )
    return summary


def write_overlap_csv(overlaps: list[dict[str, str]], path: Path) -> None:
    fieldnames = [
        "epoch",
        "address",
        "row_count",
        "case_family_count",
        "total_amount_gonka_if_naively_summed",
        "case_tracks",
        "amounts_gonka",
        "status_groups",
        "source_scopes",
        "recommended_action",
        "notes",
    ]
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(overlaps)


def format_cell(amount_ngonka: int) -> str:
    return format_gonka(amount_ngonka) if amount_ngonka else ""


def current_crosstab_rows(rows: list[Row]) -> list[Row]:
    current_addresses = {row.address for row in rows if is_current_case_family(row.case_family)}
    return [
        row
        for row in rows
        if row.case_family not in EXCLUDED_FROM_CURRENT_CROSSTAB
        and (row.case_family not in PAID_REFERENCE_FAMILIES or row.address in current_addresses)
    ]


def sum_by(rows: list[Row], key_name: str) -> dict[str, dict[int, int]]:
    result: dict[str, dict[int, int]] = defaultdict(lambda: defaultdict(int))
    for row in rows:
        key = getattr(row, key_name)
        result[key][row.epoch] += row.amount_ngonka
    return result


def write_epoch_crosstab_csv(rows: list[Row], path: Path) -> None:
    epochs = sorted({row.epoch for row in rows})
    by_track = sum_by(rows, "case_track")
    rows_by_track: dict[str, list[Row]] = defaultdict(list)
    for row in rows:
        rows_by_track[row.case_track].append(row)

    fieldnames = [
        "case_track",
        "case_family",
        "status_groups",
        "component_rows",
        "unique_positive_addresses",
        "epochs_present",
        *[f"epoch_{epoch}_gonka" for epoch in epochs],
        "total_gonka",
    ]
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for track in sorted(by_track):
            group = rows_by_track[track]
            amounts = by_track[track]
            out = {
                "case_track": track,
                "case_family": ",".join(sorted({row.case_family for row in group})),
                "status_groups": ",".join(sorted({row.status_group for row in group})),
                "component_rows": str(len(group)),
                "unique_positive_addresses": str(len({row.address for row in group})),
                "epochs_present": ",".join(str(epoch) for epoch in sorted(amounts)),
                "total_gonka": format_gonka(sum(amounts.values())),
            }
            for epoch in epochs:
                out[f"epoch_{epoch}_gonka"] = format_cell(amounts.get(epoch, 0))
            writer.writerow(out)


def epoch_overlap_summary(rows: list[Row], overlaps: list[dict[str, str]]) -> list[dict[str, str]]:
    by_epoch: dict[int, list[Row]] = defaultdict(list)
    exact_overlap_count: dict[int, int] = defaultdict(int)
    for row in rows:
        by_epoch[row.epoch].append(row)
    for row in overlaps:
        exact_overlap_count[int(row["epoch"])] += 1

    result: list[dict[str, str]] = []
    for epoch in sorted(by_epoch):
        group = by_epoch[epoch]
        families = sorted({row.case_family for row in group})
        tracks = sorted({row.case_track for row in group})
        if len(families) < 2 and len(tracks) < 2:
            continue
        result.append(
            {
                "epoch": str(epoch),
                "case_families": "; ".join(families),
                "case_family_count": str(len(families)),
                "case_tracks": "; ".join(tracks),
                "case_track_count": str(len(tracks)),
                "component_rows": str(len(group)),
                "unique_addresses": str(len({row.address for row in group})),
                "total_amount_gonka_if_naively_summed": format_gonka(sum(row.amount_ngonka for row in group)),
                "exact_address_epoch_overlap_keys": str(exact_overlap_count.get(epoch, 0)),
            }
        )
    return result


def append_crosstab_section(
    lines: list[str],
    *,
    title: str,
    grouped_amounts: dict[str, dict[int, int]],
    row_counts: dict[str, int],
    address_counts: dict[str, int],
    statuses: dict[str, str],
    epochs: list[int],
) -> None:
    lines += [
        "",
        f"## {title}",
        "",
        "| Case / track | Status | Rows | Addresses | " + " | ".join(str(epoch) for epoch in epochs) + " | Total |",
        "|---|---|---:|---:|" + "|".join("---:" for _ in epochs) + "|---:|",
    ]
    for key in sorted(grouped_amounts):
        amounts = grouped_amounts[key]
        cells = [format_cell(amounts.get(epoch, 0)) for epoch in epochs]
        lines.append(
            f"| `{key}` | `{statuses[key]}` | {row_counts[key]} | {address_counts[key]} | "
            + " | ".join(f"`{cell}`" if cell else "" for cell in cells)
            + f" | `{format_gonka(sum(amounts.values()))}` |"
        )


def write_epoch_crosstab_markdown(rows: list[Row], overlaps: list[dict[str, str]], path: Path) -> None:
    epochs = sorted({row.epoch for row in rows})
    by_family = sum_by(rows, "case_family")
    by_track = sum_by(rows, "case_track")

    family_rows: dict[str, list[Row]] = defaultdict(list)
    track_rows: dict[str, list[Row]] = defaultdict(list)
    for row in rows:
        family_rows[row.case_family].append(row)
        track_rows[row.case_track].append(row)

    family_statuses = {
        family: ",".join(sorted({row.status_group for row in group}))
        for family, group in family_rows.items()
    }
    track_statuses = {
        track: ",".join(sorted({row.status_group for row in group}))
        for track, group in track_rows.items()
    }
    family_row_counts = {family: len(group) for family, group in family_rows.items()}
    track_row_counts = {track: len(group) for track, group in track_rows.items()}
    family_address_counts = {
        family: len({row.address for row in group})
        for family, group in family_rows.items()
    }
    track_address_counts = {
        track: len({row.address for row in group})
        for track, group in track_rows.items()
    }

    summary = epoch_overlap_summary(rows, overlaps)
    lines = [
        "# Compensation Epoch Crosstab",
        "",
        "Generated by `scripts/build_compensation_address_epoch_ledger.py` from the address/epoch ledger inputs.",
        "",
        "Machine-readable file: `compensation_epoch_crosstab.csv`.",
        "",
        "Current crosstab scope excludes `P3-CAND-06`; that case remains in the raw address/epoch ledger as reference data, but is not part of this payout-scope view.",
        "`P4-CAND-01` is already paid and rejected as a case; this crosstab keeps only P4 rows whose recipient address also appears in a current case.",
        "",
        "The crosstab shows epoch-level overlap only. Exact duplicate-risk review still uses `COMPENSATION_OVERLAP_MATRIX.md`, because duplicate payout risk requires the same `epoch + address`, not just the same epoch.",
        "",
        "## Epoch Overlap Summary",
        "",
        "| Epoch | Families | Tracks | Component rows | Unique addresses | Naive total, GONKA | Exact address/epoch overlap keys |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for item in summary:
        lines.append(
            "| {epoch} | {case_family_count}: {case_families} | {case_track_count}: {case_tracks} | {component_rows} | {unique_addresses} | `{total_amount_gonka_if_naively_summed}` | {exact_address_epoch_overlap_keys} |".format(
                **item
            )
        )
    if not summary:
        lines.append("| | | | | | | |")

    append_crosstab_section(
        lines,
        title="Case-Family Crosstab",
        grouped_amounts=by_family,
        row_counts=family_row_counts,
        address_counts=family_address_counts,
        statuses=family_statuses,
        epochs=epochs,
    )
    append_crosstab_section(
        lines,
        title="Track-Level Crosstab",
        grouped_amounts=by_track,
        row_counts=track_row_counts,
        address_counts=track_address_counts,
        statuses=track_statuses,
        epochs=epochs,
    )
    path.write_text("\n".join(lines) + "\n")


def address_overlap_counts(overlaps: list[dict[str, str]]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for row in overlaps:
        counts[row["address"]] += 1
    return counts


def address_case_rows(rows: list[Row], overlaps: list[dict[str, str]]) -> list[dict[str, object]]:
    families = sorted({row.case_family for row in rows})
    by_address: dict[str, list[Row]] = defaultdict(list)
    exact_counts = address_overlap_counts(overlaps)
    for row in rows:
        by_address[row.address].append(row)

    result: list[dict[str, object]] = []
    for address, group in by_address.items():
        family_amounts = {family: 0 for family in families}
        for row in group:
            family_amounts[row.case_family] += row.amount_ngonka
        result.append(
            {
                "address": address,
                "case_family_count": len({row.case_family for row in group}),
                "case_track_count": len({row.case_track for row in group}),
                "component_rows": len(group),
                "epochs_present": ",".join(str(epoch) for epoch in sorted({row.epoch for row in group})),
                "exact_address_epoch_overlap_keys": exact_counts.get(address, 0),
                "status_groups": ",".join(sorted({row.status_group for row in group})),
                "case_tracks": "; ".join(sorted({row.case_track for row in group})),
                "family_amounts": family_amounts,
                "total_ngonka": sum(row.amount_ngonka for row in group),
            }
        )
    return sorted(
        result,
        key=lambda row: (
            -int(row["exact_address_epoch_overlap_keys"]),
            -int(row["case_family_count"]),
            -int(row["case_track_count"]),
            str(row["address"]),
        ),
    )


def write_address_crosstab_csv(rows: list[Row], overlaps: list[dict[str, str]], path: Path) -> None:
    families = sorted({row.case_family for row in rows})
    fieldnames = [
        "address",
        "case_family_count",
        "case_track_count",
        "component_rows",
        "epochs_present",
        "exact_address_epoch_overlap_keys",
        "status_groups",
        "case_tracks",
        *[f"{family}_gonka" for family in families],
        "total_gonka_if_naively_summed",
    ]
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in address_case_rows(rows, overlaps):
            family_amounts = row["family_amounts"]
            assert isinstance(family_amounts, dict)
            out = {
                "address": row["address"],
                "case_family_count": row["case_family_count"],
                "case_track_count": row["case_track_count"],
                "component_rows": row["component_rows"],
                "epochs_present": row["epochs_present"],
                "exact_address_epoch_overlap_keys": row["exact_address_epoch_overlap_keys"],
                "status_groups": row["status_groups"],
                "case_tracks": row["case_tracks"],
                "total_gonka_if_naively_summed": format_gonka(int(row["total_ngonka"])),
            }
            for family in families:
                out[f"{family}_gonka"] = format_cell(int(family_amounts[family]))
            writer.writerow(out)


def append_address_table(lines: list[str], rows_for_table: list[dict[str, object]], families: list[str]) -> None:
    lines += [
        "| Address | Families | Tracks | Rows | Epochs | Exact overlap keys | "
        + " | ".join(families)
        + " | Naive total |",
        "|---|---:|---:|---:|---|---:|"
        + "|".join("---:" for _ in families)
        + "|---:|",
    ]
    for row in rows_for_table:
        family_amounts = row["family_amounts"]
        assert isinstance(family_amounts, dict)
        family_cells = [format_cell(int(family_amounts[family])) for family in families]
        lines.append(
            f"| `{row['address']}` | {row['case_family_count']} | {row['case_track_count']} | {row['component_rows']} | `{row['epochs_present']}` | {row['exact_address_epoch_overlap_keys']} | "
            + " | ".join(f"`{cell}`" if cell else "" for cell in family_cells)
            + f" | `{format_gonka(int(row['total_ngonka']))}` |"
        )


def append_case_family_recipients(lines: list[str], rows_for_table: list[dict[str, object]], family: str) -> None:
    recipients = []
    for row in rows_for_table:
        family_amounts = row["family_amounts"]
        assert isinstance(family_amounts, dict)
        amount = int(family_amounts.get(family, 0))
        if amount > 0:
            recipients.append((row, amount))

    lines += [
        f"## {family} Recipients",
        "",
        "| Address | Epochs | Amount, GONKA | Other case families | Exact overlap keys |",
        "|---|---|---:|---:|---:|",
    ]
    for row, amount in sorted(recipients, key=lambda item: str(item[0]["address"])):
        other_families = int(row["case_family_count"]) - 1
        lines.append(
            f"| `{row['address']}` | `{row['epochs_present']}` | `{format_gonka(amount)}` | {other_families} | {row['exact_address_epoch_overlap_keys']} |"
        )
    if not recipients:
        lines.append("| | | | | |")
    lines.append("")


def write_address_crosstab_markdown(rows: list[Row], overlaps: list[dict[str, str]], path: Path) -> None:
    families = sorted({row.case_family for row in rows})
    address_rows = address_case_rows(rows, overlaps)
    review_rows = [
        row
        for row in address_rows
        if int(row["case_family_count"]) > 1
        or int(row["case_track_count"]) > 1
        or int(row["exact_address_epoch_overlap_keys"]) > 0
    ]

    lines = [
        "# Compensation Address/Case Crosstab",
        "",
        "Generated by `scripts/build_compensation_address_epoch_ledger.py` from the address/epoch ledger inputs.",
        "",
        "Machine-readable file: `compensation_address_case_crosstab.csv`.",
        "",
        "Current crosstab scope excludes `P3-CAND-06`; that case remains in the raw address/epoch ledger as reference data, but is not part of this payout-scope view.",
        "`P4-CAND-01` is already paid and rejected as a case; this crosstab keeps only P4 rows whose recipient address also appears in a current case.",
        "",
        "Amounts are grouped by address and case family. `Naive total` is useful for review, but it must not be treated as final payout when a row has multiple case families, multiple tracks, or exact address/epoch overlap keys.",
        "",
        "## Summary",
        "",
        f"- Unique addresses in current crosstab scope: `{len(address_rows)}`",
        f"- Addresses with more than one case family: `{sum(1 for row in address_rows if int(row['case_family_count']) > 1)}`",
        f"- Addresses with more than one case track: `{sum(1 for row in address_rows if int(row['case_track_count']) > 1)}`",
        f"- Addresses with exact address/epoch overlap keys: `{sum(1 for row in address_rows if int(row['exact_address_epoch_overlap_keys']) > 0)}`",
        "",
        "## All Recipients Address/Case Crosstab",
        "",
    ]
    append_address_table(lines, address_rows, families)

    lines += [
        "",
        "## Addresses Requiring Review",
        "",
    ]
    append_address_table(lines, review_rows, families)

    lines += [
        "",
    ]
    append_case_family_recipients(lines, address_rows, "P3-CAND-02")
    while lines and lines[-1] == "":
        lines.pop()
    path.write_text("\n".join(lines) + "\n")


def write_markdown(rows: list[Row], overlaps: list[dict[str, str]], path: Path) -> None:
    by_track: dict[str, list[Row]] = defaultdict(list)
    by_status: dict[str, list[Row]] = defaultdict(list)
    paid_reference_summary = paid_reference_intersection_summary(rows)
    for row in rows:
        by_track[row.case_track].append(row)
        by_status[row.status_group].append(row)

    lines = [
        "# Compensation Address/Epoch Ledger And Overlap Matrix",
        "",
        "Generated by `scripts/build_compensation_address_epoch_ledger.py` from source CSVs.",
        "",
        "Primary machine-readable files:",
        "- `compensation_address_epoch_ledger.csv` - one compensation component per address and epoch.",
        "- `compensation_overlap_matrix.csv` - repeated `(epoch,address)` keys across compensation components.",
        "",
        "## Summary",
        "",
        f"- Ledger rows: `{len(rows)}`",
        f"- Unique `(epoch,address)` keys: `{len({(row.epoch, row.address) for row in rows})}`",
        f"- Overlap keys: `{len(overlaps)}`",
        f"- Current-case exact overlaps with paid P4 rows: `{len(paid_reference_summary)}`",
        "",
        "## Totals By Track",
        "",
        "| Track | Rows | Unique addresses | Epochs | Amount, GONKA | Status group |",
        "|---|---:|---:|---|---:|---|",
    ]

    for track in sorted(by_track):
        group = by_track[track]
        epochs = ",".join(str(epoch) for epoch in sorted({row.epoch for row in group}))
        total = sum(row.amount_ngonka for row in group)
        statuses = ",".join(sorted({row.status_group for row in group}))
        lines.append(
            f"| `{track}` | {len(group)} | {len({row.address for row in group})} | `{epochs}` | `{format_gonka(total)}` | `{statuses}` |"
        )

    lines += [
        "",
        "## Totals By Status",
        "",
        "| Status group | Rows | Amount, GONKA |",
        "|---|---:|---:|",
    ]
    for status in sorted(by_status):
        group = by_status[status]
        lines.append(f"| `{status}` | {len(group)} | `{format_gonka(sum(row.amount_ngonka for row in group))}` |")

    lines += [
        "",
        "## Current Case / Paid P4 Exact Intersections",
        "",
        "`P4-CAND-01` was rejected as a case but was fully paid. This table isolates exact `epoch + address` intersections between current case candidates and paid P4 rows.",
        "",
        "| Epoch | Address | Current tracks | Current amount, GONKA | Paid P4 tracks | Paid P4 amount, GONKA | Naive total, GONKA |",
        "|---:|---|---|---:|---|---:|---:|",
    ]
    current_total = 0
    paid_reference_total = 0
    for row in paid_reference_summary:
        current_total += int(Decimal(row["current_amount_gonka"]) * NGONKA)
        paid_reference_total += int(Decimal(row["paid_reference_amount_gonka"]) * NGONKA)
        lines.append(
            "| {epoch} | `{address}` | {current_tracks} | `{current_amount_gonka}` | {paid_reference_tracks} | `{paid_reference_amount_gonka}` | `{naive_total_gonka}` |".format(
                **row
            )
        )
    if paid_reference_summary:
        lines.append(
            f"| **Total** |  |  | `{format_gonka(current_total)}` |  | `{format_gonka(paid_reference_total)}` | `{format_gonka(current_total + paid_reference_total)}` |"
        )
    else:
        lines.append("| | | | | | | |")

    lines += [
        "",
        "## Overlap Keys",
        "",
        "These are exact same `epoch + address` collisions. They are not all duplicate payouts by themselves, but each row must be reconciled before summing case totals.",
        "",
        "| Epoch | Address | Rows | Families | Naive total, GONKA | Tracks | Amounts, GONKA | Action |",
        "|---:|---|---:|---:|---:|---|---|---|",
    ]
    for row in overlaps:
        lines.append(
            "| {epoch} | `{address}` | {row_count} | {case_family_count} | `{total_amount_gonka_if_naively_summed}` | {case_tracks} | {amounts_gonka} | `{recommended_action}` |".format(
                **row
            )
        )

    if not overlaps:
        lines.append("| | | | | | | | |")

    path.write_text("\n".join(lines) + "\n")


def main() -> None:
    rows: list[Row] = []
    load_p3_cand01(rows)
    load_p3_cand02(rows)
    load_p3_cand03(rows)
    load_p3_cand04(rows)
    load_p3_cand06(rows)
    load_p4(rows)

    overlaps = build_overlaps(rows)
    crosstab_rows = current_crosstab_rows(rows)
    crosstab_overlaps = build_overlaps(crosstab_rows)
    write_ledger(rows, BASE / "compensation_address_epoch_ledger.csv")
    write_overlap_csv(overlaps, BASE / "compensation_overlap_matrix.csv")
    write_epoch_crosstab_csv(crosstab_rows, BASE / "compensation_epoch_crosstab.csv")
    write_address_crosstab_csv(crosstab_rows, crosstab_overlaps, BASE / "compensation_address_case_crosstab.csv")
    write_markdown(rows, overlaps, BASE / "COMPENSATION_OVERLAP_MATRIX.md")
    write_epoch_crosstab_markdown(crosstab_rows, crosstab_overlaps, BASE / "COMPENSATION_EPOCH_CROSSTAB.md")
    write_address_crosstab_markdown(crosstab_rows, crosstab_overlaps, BASE / "COMPENSATION_ADDRESS_CROSSTAB.md")

    print(f"ledger_rows={len(rows)}")
    print(f"current_crosstab_rows={len(crosstab_rows)}")
    print(f"unique_epoch_address={len({(row.epoch, row.address) for row in rows})}")
    print(f"unique_addresses={len({row.address for row in rows})}")
    print(f"overlap_keys={len(overlaps)}")
    print(f"current_crosstab_unique_addresses={len({row.address for row in crosstab_rows})}")
    print(f"current_crosstab_overlap_keys={len(crosstab_overlaps)}")
    print(f"epoch_overlap_rows={len(epoch_overlap_summary(crosstab_rows, crosstab_overlaps))}")
    print(f"address_review_rows={len([row for row in address_case_rows(crosstab_rows, crosstab_overlaps) if int(row['case_family_count']) > 1 or int(row['case_track_count']) > 1 or int(row['exact_address_epoch_overlap_keys']) > 0])}")


if __name__ == "__main__":
    main()
