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
| `P3-CAND-03` | [`P3-CAND-03-failed-cpoc-epoch-267`](P3-CAND-03-failed-cpoc-epoch-267/) | Epoch 267 confirmation PoC events, zero-reward exclusions, claimant trace, root-cause trace, amount reconciliation, hardware/config vs chain/protocol evidence, and pre-fix neighbor scan through epoch `276`. | Independently validated for epoch `267`: `1` strict Case-3-like candidate, `10,262.057515369 GNK`; extended scan `262..276` finds the same claimant in epoch `265` and separates `24` broader pass-weight-but-failed-ratio rows into `P3-CAND-06`. |
| `P3-CAND-06` | [`P3-CAND-06-pre-fix-confirmation-accounting`](P3-CAND-06-pre-fix-confirmation-accounting/) | Standalone extraction of broader pre-fix `failed_confirmation_poc` rows where at least one submitted model reached `pass_weight`, but the final confirmation ratio failed. | Root-cause, raw stage replay, coefficient replay, bounded new-algorithm replay, `v0.2.13` code-diff proof, one-page decision summary, row-by-row evidence ledger, gross compensation calculation, epoch/upgrade timestamp table, and post-upgrade regression scan added: pre-fix `24` rows, `19` unique participants, gross before overlap `120,822.324371792 GONKA`; old formula matches `22/24`; bounded new-style replay has `0/24` pass alpha; upgrade applied in epoch `276`, epoch `277` is first clean start; post-upgrade `277..283` has `8` broad single-model-pass hits and `0` both-model-pass hits. |
