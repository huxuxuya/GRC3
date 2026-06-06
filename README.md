# GRC3 Compensation Review

Working repository for GRC compensation case tracking, validation notes, and
overlap review.

Main entry points:

- [`PUBLIC_COMPENSATION_TRACKER.md`](PUBLIC_COMPENSATION_TRACKER.md) - public
  case/status tracker and high-level compensation table.
- [`COMPENSATION_RESULTS.md`](COMPENSATION_RESULTS.md) - working compensation
  results ledger split by status group.
- [`CALCULATION_REPO_RECONCILIATION.md`](CALCULATION_REPO_RECONCILIATION.md) -
  comparison against current external calculation repositories.
- [`COMPENSATION_OVERLAP_MATRIX.md`](COMPENSATION_OVERLAP_MATRIX.md) -
  address/epoch overlap matrix for duplicate-compensation review.
- [`compensation_address_epoch_ledger.csv`](compensation_address_epoch_ledger.csv)
  - machine-readable per-address, per-epoch compensation component ledger.
- [`compensation_overlap_matrix.csv`](compensation_overlap_matrix.csv) -
  machine-readable repeated `(epoch,address)` keys.

Generated address/epoch files are rebuilt with:

```sh
python3 scripts/build_compensation_address_epoch_ledger.py
```
