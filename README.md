# GRC3 Compensation Review

Working repository for GRC compensation case tracking, validation notes, and
overlap review.

Main entry points:

- [`PUBLIC_COMPENSATION_TRACKER.md`](PUBLIC_COMPENSATION_TRACKER.md) - public
  case/status tracker and high-level compensation table.
- [`COMPENSATION_RESULTS.md`](COMPENSATION_RESULTS.md) - working compensation
  results ledger split by status group.
- [`PLANNED_COMPENSATION_SETTLEMENT.md`](PLANNED_COMPENSATION_SETTLEMENT.md) -
  planned payout table with P4 overlap adjustments and final payout amounts.
- [`CALCULATION_REPO_RECONCILIATION.md`](CALCULATION_REPO_RECONCILIATION.md) -
  comparison against current external calculation repositories.
- [`COMPENSATION_OVERLAP_MATRIX.md`](COMPENSATION_OVERLAP_MATRIX.md) -
  address/epoch overlap matrix for duplicate-compensation review.
- [`COMPENSATION_EPOCH_CROSSTAB.md`](COMPENSATION_EPOCH_CROSSTAB.md) -
  case/epoch crosstab for epoch-level overlap review.
- [`COMPENSATION_ADDRESS_CROSSTAB.md`](COMPENSATION_ADDRESS_CROSSTAB.md) -
  address/case crosstab for recipient-level overlap review.
- [`COMPENSATION_ADDRESS_EPOCH_CROSSTAB.md`](COMPENSATION_ADDRESS_EPOCH_CROSSTAB.md)
  - address/epoch/case crosstab for participant-level epoch review.
- [`compensation_address_epoch_ledger.csv`](compensation_address_epoch_ledger.csv)
  - machine-readable per-address, per-epoch compensation component ledger.
- [`compensation_overlap_matrix.csv`](compensation_overlap_matrix.csv) -
  machine-readable repeated `(epoch,address)` keys.
- [`compensation_epoch_crosstab.csv`](compensation_epoch_crosstab.csv) -
  machine-readable case/epoch crosstab.
- [`compensation_address_case_crosstab.csv`](compensation_address_case_crosstab.csv)
  - machine-readable address/case crosstab.
- [`compensation_address_epoch_case_crosstab.csv`](compensation_address_epoch_case_crosstab.csv)
  - machine-readable address/epoch/case crosstab.
- [`planned_compensation_settlement.csv`](planned_compensation_settlement.csv)
  - machine-readable planned payout rows with P4 overlap adjustments.

Generated address/epoch files are rebuilt with:

```sh
python3 scripts/build_compensation_address_epoch_ledger.py
```
