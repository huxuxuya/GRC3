# P3-CAND-06 Root-Cause Replay

This replay checks the `24` pass-weight-but-failed-ratio candidate rows
against normalized archive-chain artifacts. It is independent from
external compensation repositories.

## Result

| Metric | Value |
|---|---:|
| Candidate rows | `24` |
| Unique participants | `19` |
| Estimated zero-reward loss | `120822.324371792` GONKA |
| Rows with both Qwen and Kimi `pass_weight` | `1` |
| Rows with exactly one `pass_weight` model | `23` |
| Rows where simple `at/before/0.909` ratio matches stored ratio | `18` |
| Rows where simple `at/before/0.909` ratio does not match stored ratio | `6` |
| Simple-ratio mismatch rows reconciled by coefficient replay | `5` |
| Remaining mismatch after coefficient replay | `1` |

## Classification

| Classification | Rows | Meaning |
|---|---:|---|
| `single_model_pass_coefficient_replayed` | `5` | One model passed; coefficient-adjusted replay matches the stored ratio once historical coefficients, time normalization, and preserved snapshots are used. |
| `single_model_pass_expected_capacity_failed` | `18` | One model passed, the other had no submission; observed confirmation-weight reduction already reconciles with stored ratio. |
| `strong_signal_but_epoch276_overlap` | `1` | Both tracked models passed, but the row is in upgrade epoch 276 and overlaps P3-CAND-04 review. |

## Epoch Distribution

| Epoch | Rows | Estimated loss, GONKA |
|---:|---:|---:|
| `263` | `3` | `8719.070532944` |
| `264` | `3` | `6010.126484192` |
| `265` | `1` | `335.927643572` |
| `268` | `1` | `25309.087745610` |
| `269` | `2` | `2764.396118755` |
| `271` | `1` | `139.200061369` |
| `272` | `4` | `31070.826328522` |
| `273` | `2` | `3237.649981278` |
| `274` | `2` | `310.429493665` |
| `275` | `1` | `126.220428182` |
| `276` | `4` | `42799.389553703` |

## Chain Mechanism Checked

For every row, the raw model result is checked against the chain rule:

```text
validWeight > TotalNetworkWeight * 2 / 3
```

All `24` candidate rows still have at least one model with `pass_weight`
under that strict rule, while the durable chain state records
`failed_confirmation_poc`, zero reward, and `ConfirmationPoCRatio < 0.5`.

The likely fix family is PR #1143 / `v0.2.13`, whose PR text says the
microrelease fixes confirmation PoC weight loss during new-model
bootstrap by using one epoch snapshot of confirmable models and
weight-scale factors for confirmation and reward-weight calculations:

```text
https://github.com/gonka-ai/gonka/pull/1143
```

`case6_coefficient_replay.md` replays the `6` simple-ratio mismatch rows with
historical coefficients, cPoC time normalization, preserved snapshots, and ML
node distributions. It reconciles `5/6`; the remaining non-match is the epoch
`276` overlap row.

`case6_full_old_formula_replay.md` extends that formula replay to all `24`
candidate rows. It matches stored ratios for `22/24`; the two non-matches are
both in epoch `276`. `case6_new_algorithm_replay.md` applies a bounded
v0.2.13-style counterfactual over the available Qwen/Kimi data and keeps
`24/24` rows below alpha.

However, this replay does not mark the full `24` rows as confirmed
compensation rows. A single model reaching `pass_weight` does not by itself
prove that all expected confirmation capacity should have been preserved.

## Strongest Current Signal

The strongest pass-weight contradiction is:

| Epoch | Participant | Qwen | Kimi | Ratio | Loss, GONKA | Caveat |
|---:|---|---|---|---:|---:|---|
| `276` | `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | `86.9859% pass_weight` | `78.7207% pass_weight` | `35.2638%` | `17356.095656742` | Epoch 276 overlaps the upgrade cPoC-misfire case. |

## Current Conclusion

- `P3-CAND-06` is real as a chain-state anomaly set: pass-weight evidence and
  failed confirmation state coexist in `24` rows.
- It is not yet proven that all `24` rows are protocol-bug compensation rows;
  `20` non-epoch-276 rows are formula-reconciled but still require a
  single-model-service eligibility decision.
- PR `#1143` is the main fix reference to inspect; PRs `#550` and `#826`
  are currently treated as unrelated settlement/claim-path fixes unless a
  direct confirmation-PoC code link is later found.
- Epoch `276` rows must be reconciled with `P3-CAND-04` before any payout
  decision.

Detailed row data is in `case6_row_formula_replay.csv` and
`case6_row_formula_replay.json`. Coefficient replay data is in
`case6_coefficient_replay.csv` and `case6_coefficient_replay.json`. Full old
formula and bounded new-algorithm replay data are in
`case6_full_old_formula_replay.csv` and `case6_new_algorithm_replay.csv`.
