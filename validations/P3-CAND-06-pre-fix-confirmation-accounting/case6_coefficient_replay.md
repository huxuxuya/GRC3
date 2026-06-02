# P3-CAND-06 Coefficient Replay

This replay focuses on the `6` rows where the simple diagnostic ratio did
not match stored `ConfirmationPoCRatio`.

The pre-`v0.2.13` chain formula reviewed from `confirmation_poc.go` was:

```text
reading = preserved + measured
totalExpected = preserved + notPreserved
ratio = min((reading / totalExpected) / 0.909, 1)
ConfirmationWeight = min(previous ConfirmationWeight, reading)
```

The important point is that `totalExpected` is not necessarily the current
`ConfirmationWeight`. If earlier cPoC events already lowered
`ConfirmationWeight`, a simple `after / before / 0.909` check uses the
wrong denominator.

## Result

| Check | Value |
|---|---:|
| Rows replayed | `6` |
| Rows matching stored ratio | `5` |

## Rows

| Epoch | Participant | Trigger | Snapshot anchor | Pass model(s) | Preserved | Measured | Not preserved | Total expected | Reading | Stored ratio | Replay ratio | Match |
|---:|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| 268 | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | 4144898 | 4144898 | Kimi | 0 | 14477 | 91616 | 91616 | 14477 | 0.1738374588419373 | 0.1738374588419373 | True |
| 272 | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | 4209686 | 4209686 | Kimi | 0 | 27426 | 74947 | 74947 | 27426 | 0.4025727135404508 | 0.4025727135404509 | True |
| 273 | `gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx` | 4215427 | 4215427 | Qwen | 378 | 2684 | 10290 | 10668 | 3062 | 0.3157608599255127 | 0.3157608599255126 | True |
| 274 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | 4231815 | 4231815 | Qwen | 0 | 103 | 390 | 390 | 103 | 0.2905418747002905 | 0.2905418747002905 | True |
| 275 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | 4258197 | 4258197 | Qwen | 0 | 105 | 345 | 345 | 105 | 0.3348160903046826 | 0.3348160903046826 | True |
| 276 | `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | 4267778 | 4267778 | Qwen+Kimi | 3906 | 12411 | 40862 | 44768 | 16317 | 0.3526384050777585 | 0.4009670981394065 | False |

## Interpretation

- `5/6` prior mismatch rows reconcile against the reviewed pre-fix
  chain formula.
- For those `5` rows, the mismatch was caused by using
  `confirmation_weight_before` as a
  diagnostic denominator even though the chain ratio denominator was
  `preserved + notPreserved`.
- The remaining non-match is epoch `276`
  `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09`, which is already
  marked as an upgrade/`P3-CAND-04` overlap row.
- This does not automatically approve payout eligibility. It proves that
  the stored ratios for `5` single-model rows are internally consistent
  with the pre-fix formula once historical coefficients, time
  normalization, and preserved snapshots are used.
- The economic eligibility question remains whether a single passing model
  should count as enough service for compensation, and whether epoch `276`
  overlaps another case.

Machine-readable details are in `case6_coefficient_replay.csv` and
`case6_coefficient_replay.json`.
