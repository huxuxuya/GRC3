# P3-CAND-06 Overlap Matrix

This matrix classifies duplicate-payment risk using only evidence
available in this repository.

## Summary

| Overlap status | Rows |
|---|---:|
| `known_p3_cand_04_same_address` | `1` |
| `no_known_overlap_in_local_repo` | `6` |
| `p3_cand_04_epoch_overlap_unresolved` | `3` |
| `p4_cand_01_epoch_range_overlap` | `14` |

## Rows

| Epoch | Participant | Pass model(s) | Loss, GONKA | Status | Action |
|---:|---|---|---:|---|---|
| 263 | `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` | Kimi | 1953.032509538 | `no_known_overlap_in_local_repo` | `clear` |
| 263 | `gonka19cjm4c5mt3j3qdr8vhytmm4hef3pnkvkm0x7m2` | Kimi | 1915.652591432 | `no_known_overlap_in_local_repo` | `clear` |
| 263 | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | Qwen | 4850.385431974 | `no_known_overlap_in_local_repo` | `clear` |
| 264 | `gonka14g78ez2zy08k8sssue483zmfpgd4qut8zcwlqc` | Kimi | 2019.930762224 | `no_known_overlap_in_local_repo` | `clear` |
| 264 | `gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d` | Kimi | 2019.930762224 | `no_known_overlap_in_local_repo` | `clear` |
| 264 | `gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds` | Kimi | 1970.264959744 | `no_known_overlap_in_local_repo` | `clear` |
| 265 | `gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww` | Qwen | 335.927643572 | `p4_cand_01_epoch_range_overlap` | `review` |
| 268 | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | Kimi | 25309.087745610 | `p4_cand_01_epoch_range_overlap` | `review` |
| 269 | `gonka1007py6y2qfn2vaqrthqhtchkwx64hgzc6w544w` | Kimi | 2228.595538500 | `p4_cand_01_epoch_range_overlap` | `review` |
| 269 | `gonka1naxyjmun6kl23htjdujwd6c5z5avgwapsrmfk3` | Qwen | 535.800580255 | `p4_cand_01_epoch_range_overlap` | `review` |
| 271 | `gonka16xa2sdc8qe2289nzr4e6vmdyzlke8g8fn8e75s` | Qwen | 139.200061369 | `p4_cand_01_epoch_range_overlap` | `review` |
| 272 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | Qwen | 365.340258948 | `p4_cand_01_epoch_range_overlap` | `review` |
| 272 | `gonka1nku7u6d5mz80h35ty8ydeh0k5xydesvt9w0vjr` | Qwen | 146.964070171 | `p4_cand_01_epoch_range_overlap` | `review` |
| 272 | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | Kimi | 22521.036302544 | `p4_cand_01_epoch_range_overlap` | `review` |
| 272 | `gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p` | Qwen | 8037.485696859 | `p4_cand_01_epoch_range_overlap` | `review` |
| 273 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | Qwen | 218.861247867 | `p4_cand_01_epoch_range_overlap` | `review` |
| 273 | `gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx` | Qwen | 3018.788733411 | `p4_cand_01_epoch_range_overlap` | `review` |
| 274 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | Qwen | 137.269776102 | `p4_cand_01_epoch_range_overlap` | `review` |
| 274 | `gonka1qwfrtz9c7kcrfkrrlne2pkcye74mj6ce33xdkl` | Qwen | 173.159717563 | `p4_cand_01_epoch_range_overlap` | `review` |
| 275 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | Qwen | 126.220428182 | `p4_cand_01_epoch_range_overlap` | `review` |
| 276 | `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | Qwen+Kimi | 17356.095656742 | `known_p3_cand_04_same_address` | `blocked` |
| 276 | `gonka14tqh62mangwzrma2lgg2dm375rcjzn2ydy8ttm` | Kimi | 11765.489995489 | `p3_cand_04_epoch_overlap_unresolved` | `blocked` |
| 276 | `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e` | Qwen | 3557.528990032 | `p3_cand_04_epoch_overlap_unresolved` | `blocked` |
| 276 | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | Kimi | 10120.274911440 | `p3_cand_04_epoch_overlap_unresolved` | `blocked` |

## Rule

- `blocked` rows must not be paid from P3-CAND-06 until duplicate risk is
  resolved.
- `review` rows need same-address comparison against a normalized external
  table before payout.
- `clear` rows have no local overlap signal, but still need eligibility
  decision.

Machine-readable versions are in `case6_overlap_matrix.csv` and
`case6_overlap_matrix.json`.
