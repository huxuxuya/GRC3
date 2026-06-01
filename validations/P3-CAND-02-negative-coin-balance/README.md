# P3-CAND-02 Validation

This folder contains the independent validation package for Case 2: negative
coin balance / settle-drop. It includes the archive validation script and
sanitized outputs, so reviewers can inspect the result without querying the
archive node on every pass.

The archive endpoint and API key are loaded from local `.env` and are not stored
in git. The resumable raw cache is also outside the repository at
`/tmp/grc3-case2-audit/cache.db`.

## What Was Checked

The validation independently rebuilt the affected set from chain state rather
than using the published payout CSV as the calculation source.

| Check | Method | Result |
|---|---|---|
| Archive coverage | Full scan of epochs `1-274`; for every epoch, query the full historical `settle_amount` snapshot at the next epoch's `effective_block_height`. | `274/274` snapshots checked; `0` failures. |
| Affected-set criterion | Include only rows with positive `epoch_performance_summary.rewarded_coins` and no historical `(epoch, address)` `SettleAmount` at settlement. | `19` candidate pairs / `19` addresses. |
| Amount reconciliation | For each candidate, compare compensation to chain `epoch_performance_summary.rewarded_coins`. | All `19` amounts match chain exactly. |
| Published comparison | Compare independent chain-derived candidates with `gonkavip/unclaimed`. | Exact match; `0` mismatches. |
| Tail sanity check | Re-run focused/smoke checks including epochs `275-280`. | No additional settle-drop candidates found. |

## How To Re-run

From the repository root, with local `.env` configured:

```sh
python3 validations/P3-CAND-02-negative-coin-balance/verify_archive.py --mode full --compare-published yes
```

The script writes sanitized outputs back into this folder by default. It keeps
the raw resumable cache at `/tmp/grc3-case2-audit/cache.db`.

| File | Meaning |
|---|---|
| `verify_archive.py` | Independent archive validation script for this case. |
| `case2_full_candidates.csv` | Final independently derived address-by-epoch compensation matrix for epochs `1-274`. |
| `case2_full_amount_reconciliation.csv` | Per-candidate amount proof: compensation equals chain `epoch_performance_summary.rewarded_coins`. |
| `case2_full_amount_reconciliation.json` | Amount totals by epoch and all-amounts-match-chain flag. |
| `case2_full_coverage.csv` | Per-epoch coverage proof: settlement height, summary rows, snapshot size, and candidate count. |
| `case2_full_summary.json` | Full scan metadata, totals, nonzero epochs, per-epoch summary stats, and failures. |
| `case2_full_published_compare.json` | Exact comparison with the published `gonkavip/unclaimed` CSV. |
| `case2_focused_*` | Focused rerun for epochs `87-142` plus tail `275-280`. |
| `case2_smoke_*` | Small control rerun for known affected epochs, epoch `240`, and tail `275-280`. |

Current confirmed result:

| Scan | Epochs | Candidate pairs | Affected addresses | Total, ngonka | Total, GNK | Published compare |
|---|---|---:|---:|---:|---:|---|
| Full | `1-274` | 19 | 19 | 1,075,336,150,923 | 1,075.336150923 | Exact; 0 mismatches |
| Focused | `87-142`, `275-280` | 19 | 19 | 1,075,336,150,923 | 1,075.336150923 | Exact; 0 mismatches |
| Smoke | known affected epochs, `240`, `275-280` | 19 | 19 | 1,075,336,150,923 | 1,075.336150923 | Exact; 0 mismatches |

Confirmed nonzero epochs: `97`, `112`, `116`, `129`, and `132`.
