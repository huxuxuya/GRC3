# P3-CAND-06 Eligibility Matrix

This matrix separates technical replay status from compensation eligibility.
It does not approve payouts.

## Summary

| Technical status | Rows |
|---|---:|
| `blocked_epoch276_overlap` | `4` |
| `formula_reconciled_policy_required` | `20` |

## Rows

| Epoch | Participant | Pass model(s) | Old formula match | New replay pass alpha | Loss, GONKA | Technical status |
|---:|---|---|---|---|---:|---|
| 263 | `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` | Kimi | True | False | 1953.032509538 | `formula_reconciled_policy_required` |
| 263 | `gonka19cjm4c5mt3j3qdr8vhytmm4hef3pnkvkm0x7m2` | Kimi | True | False | 1915.652591432 | `formula_reconciled_policy_required` |
| 263 | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | Qwen | True | False | 4850.385431974 | `formula_reconciled_policy_required` |
| 264 | `gonka14g78ez2zy08k8sssue483zmfpgd4qut8zcwlqc` | Kimi | True | False | 2019.930762224 | `formula_reconciled_policy_required` |
| 264 | `gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d` | Kimi | True | False | 2019.930762224 | `formula_reconciled_policy_required` |
| 264 | `gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds` | Kimi | True | False | 1970.264959744 | `formula_reconciled_policy_required` |
| 265 | `gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww` | Qwen | True | False | 335.927643572 | `formula_reconciled_policy_required` |
| 268 | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | Kimi | True | False | 25309.087745610 | `formula_reconciled_policy_required` |
| 269 | `gonka1007py6y2qfn2vaqrthqhtchkwx64hgzc6w544w` | Kimi | True | False | 2228.595538500 | `formula_reconciled_policy_required` |
| 269 | `gonka1naxyjmun6kl23htjdujwd6c5z5avgwapsrmfk3` | Qwen | True | False | 535.800580255 | `formula_reconciled_policy_required` |
| 271 | `gonka16xa2sdc8qe2289nzr4e6vmdyzlke8g8fn8e75s` | Qwen | True | False | 139.200061369 | `formula_reconciled_policy_required` |
| 272 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | Qwen | True | False | 365.340258948 | `formula_reconciled_policy_required` |
| 272 | `gonka1nku7u6d5mz80h35ty8ydeh0k5xydesvt9w0vjr` | Qwen | True | False | 146.964070171 | `formula_reconciled_policy_required` |
| 272 | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | Kimi | True | False | 22521.036302544 | `formula_reconciled_policy_required` |
| 272 | `gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p` | Qwen | True | False | 8037.485696859 | `formula_reconciled_policy_required` |
| 273 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | Qwen | True | False | 218.861247867 | `formula_reconciled_policy_required` |
| 273 | `gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx` | Qwen | True | False | 3018.788733411 | `formula_reconciled_policy_required` |
| 274 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | Qwen | True | False | 137.269776102 | `formula_reconciled_policy_required` |
| 274 | `gonka1qwfrtz9c7kcrfkrrlne2pkcye74mj6ce33xdkl` | Qwen | True | False | 173.159717563 | `formula_reconciled_policy_required` |
| 275 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | Qwen | True | False | 126.220428182 | `formula_reconciled_policy_required` |
| 276 | `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | Qwen+Kimi | False | False | 17356.095656742 | `blocked_epoch276_overlap` |
| 276 | `gonka14tqh62mangwzrma2lgg2dm375rcjzn2ydy8ttm` | Kimi | False | False | 11765.489995489 | `blocked_epoch276_overlap` |
| 276 | `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e` | Qwen | True | False | 3557.528990032 | `blocked_epoch276_overlap` |
| 276 | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | Kimi | True | False | 10120.274911440 | `blocked_epoch276_overlap` |

## Decision Boundary

- `formula_reconciled_policy_required` means the technical chain state is
  reproducible, but payout still depends on whether the committee treats
  single-model pass rows as compensable.
- `blocked_epoch276_overlap` must be resolved against P3-CAND-04 before
  any payout decision.
- `technical_replay_gap` requires more technical work before policy review.

Machine-readable versions are in `case6_eligibility_matrix.csv` and
`case6_eligibility_matrix.json`.
