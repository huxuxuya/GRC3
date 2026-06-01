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
