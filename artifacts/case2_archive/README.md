# P3-CAND-02 Archive Validation Artifacts

These artifacts are sanitized outputs from `scripts/verify_case2_archive.py`.
They are tracked so reviewers can inspect the independent Case 2 result without
querying the archive node on every pass.

The archive endpoint and API key are loaded from local `.env` and are not stored
in git. The resumable raw cache is also outside the repository at
`/tmp/grc3-case2-audit/cache.db`.

| File | Meaning |
|---|---|
| `case2_full_candidates.csv` | Final independently derived address-by-epoch compensation matrix for epochs `1-274`. |
| `case2_full_amount_reconciliation.csv` | Per-candidate amount proof: compensation equals chain `epoch_performance_summary.rewarded_coins`. |
| `case2_full_amount_reconciliation.json` | Amount totals by epoch and all-amounts-match-chain flag. |
| `case2_full_coverage.csv` | Per-epoch coverage proof: settlement height, summary rows, snapshot size, and candidate count. |
| `case2_full_summary.json` | Full scan metadata, totals, nonzero epochs, per-epoch summary stats, and failures. |
| `case2_full_published_compare.json` | Exact comparison with the published `gonkavip/unclaimed` CSV. |
| `case2_focused_*` | Focused rerun for epochs `87-142` plus tail `275-280`. |
| `case2_smoke_*` | Small control rerun for known affected epochs, epoch `240`, and tail `275-280`. |

Current confirmed result:

| Scan | Candidate pairs | Affected addresses | Total, ngonka | Total, GNK | Published compare |
|---|---:|---:|---:|---:|---|
| Full | 19 | 19 | 1,075,336,150,923 | 1,075.336150923 | Exact; 0 mismatches |
| Focused | 19 | 19 | 1,075,336,150,923 | 1,075.336150923 | Exact; 0 mismatches |
| Smoke | 19 | 19 | 1,075,336,150,923 | 1,075.336150923 | Exact; 0 mismatches |
