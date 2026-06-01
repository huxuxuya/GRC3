# Case Validation Artifacts

This directory stores reproducible validation materials grouped by case. Each
case folder should contain the scripts, sanitized outputs, and a README
describing what was checked, what data was used, and what result was confirmed.

Local secrets and raw caches stay outside git. Validation scripts may read
`.env`, but committed artifacts must not include RPC URLs, API keys, or raw
node cache databases.

| Case | Folder | What was validated | Result |
|---|---|---|---|
| `P3-CAND-02` | [`P3-CAND-02-negative-coin-balance`](P3-CAND-02-negative-coin-balance/) | Negative coin balance / settle-drop archive state, affected set, payout amounts, coverage, and published CSV comparison. | Coordinator validated: `19` addresses, `1,075.336150923 GNK`, exact match, no additional settle-drop candidates in the checked range. |
| `P3-CAND-03` | [`P3-CAND-03-failed-cpoc-epoch-267`](P3-CAND-03-failed-cpoc-epoch-267/) | Epoch 267 confirmation PoC events, zero-reward exclusions, claimant trace, root-cause trace, amount reconciliation, hardware/config vs chain/protocol evidence, and nearest five-epoch neighbor scan. | Independently validated for epoch `267`: `1` candidate, `10,262.057515369 GNK`, exact published-amount match; neighbor scan of epochs `262..272` also flags the same claimant in epoch `265` with a Case-3-like signature and estimated loss `20,896.527179100 GNK`, requiring separate scope/eligibility review. |
