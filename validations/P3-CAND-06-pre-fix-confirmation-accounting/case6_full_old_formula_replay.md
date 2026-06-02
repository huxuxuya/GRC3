# P3-CAND-06 Full Old Formula Replay

This artifact replays the reviewed pre-`v0.2.13` cPoC formula for all
`24` candidate rows using historical params, cPoC time normalization,
preserved snapshots, MLNode distributions, and raw submission evidence.

## Result

| Check | Value |
|---|---:|
| Rows replayed | `24` |
| Rows matching stored ratio | `22` |
| Rows below alpha in replay | `24` |

## Rows

| Epoch | Participant | Pass model(s) | Preserved | Measured | Not preserved | Total expected | Reading | Stored ratio | Replay ratio | Match |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 263 | `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` | Kimi | 0 | 2400 | 7534 | 7534 | 2400 | 0.3504465126629466 | 0.3504465126629467 | True |
| 263 | `gonka19cjm4c5mt3j3qdr8vhytmm4hef3pnkvkm0x7m2` | Kimi | 0 | 184 | 7390 | 7390 | 184 | 0.0273911017624090 | 0.0273911017624090 | True |
| 263 | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | Qwen | 0 | 2387 | 17777 | 17777 | 2387 | 0.1477168586521700 | 0.1477168586521700 | True |
| 264 | `gonka14g78ez2zy08k8sssue483zmfpgd4qut8zcwlqc` | Kimi | 0 | 411 | 7534 | 7534 | 411 | 0.0600139652935296 | 0.0600139652935296 | True |
| 264 | `gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d` | Kimi | 0 | 3373 | 7534 | 7534 | 3373 | 0.4925233696717163 | 0.4925233696717163 | True |
| 264 | `gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds` | Kimi | 0 | 2660 | 7349 | 7349 | 2660 | 0.3981892270054329 | 0.3981892270054329 | True |
| 265 | `gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww` | Qwen | 0 | 236 | 1254 | 1254 | 236 | 0.2070382476844176 | 0.2070382476844176 | True |
| 268 | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | Kimi | 0 | 14477 | 91616 | 91616 | 14477 | 0.1738374588419373 | 0.1738374588419373 | True |
| 269 | `gonka1007py6y2qfn2vaqrthqhtchkwx64hgzc6w544w` | Kimi | 0 | 3182 | 7755 | 7755 | 3182 | 0.4513926569961960 | 0.4513926569961961 | True |
| 269 | `gonka1naxyjmun6kl23htjdujwd6c5z5avgwapsrmfk3` | Qwen | 0 | 562 | 1347 | 1347 | 562 | 0.4589917046641561 | 0.4589917046641561 | True |
| 271 | `gonka16xa2sdc8qe2289nzr4e6vmdyzlke8g8fn8e75s` | Qwen | 0 | 691 | 2297 | 2297 | 691 | 0.3309429767530519 | 0.3309429767530519 | True |
| 272 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | Qwen | 0 | 291 | 1114 | 1114 | 291 | 0.2873716456026213 | 0.2873716456026213 | True |
| 272 | `gonka1nku7u6d5mz80h35ty8ydeh0k5xydesvt9w0vjr` | Qwen | 0 | 447 | 2506 | 2506 | 447 | 0.1962287210365091 | 0.1962287210365091 | True |
| 272 | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | Kimi | 0 | 27426 | 74947 | 74947 | 27426 | 0.4025727135404508 | 0.4025727135404509 | True |
| 272 | `gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p` | Qwen | 0 | 4249 | 24524 | 24524 | 4249 | 0.1906037937018298 | 0.1906037937018298 | True |
| 273 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | Qwen | 0 | 274 | 615 | 615 | 274 | 0.4901303138443925 | 0.4901303138443926 | True |
| 273 | `gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx` | Qwen | 378 | 2684 | 10290 | 10668 | 3062 | 0.3157608599255127 | 0.3157608599255126 | True |
| 274 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | Qwen | 0 | 103 | 390 | 390 | 103 | 0.2905418747002905 | 0.2905418747002905 | True |
| 274 | `gonka1qwfrtz9c7kcrfkrrlne2pkcye74mj6ce33xdkl` | Qwen | 0 | 136 | 492 | 492 | 136 | 0.3040954501954261 | 0.3040954501954260 | True |
| 275 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | Qwen | 0 | 105 | 345 | 345 | 105 | 0.3348160903046826 | 0.3348160903046826 | True |
| 276 | `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | Qwen+Kimi | 3906 | 12411 | 40862 | 44768 | 16317 | 0.3526384050777585 | 0.4009670981394065 | False |
| 276 | `gonka14tqh62mangwzrma2lgg2dm375rcjzn2ydy8ttm` | Kimi | 0 | 17150 | 50810 | 50810 | 17150 | 0.3713006608671101 | 0.3713223123138923 | False |
| 276 | `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e` | Qwen | 0 | 1343 | 8698 | 8698 | 1343 | 0.1698606282794295 | 0.1698606282794295 | True |
| 276 | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | Kimi | 0 | 16147 | 48847 | 48847 | 16147 | 0.3636554209600337 | 0.3636554209600336 | True |

## Interpretation

- The replay proves that the durable failed ratios are internally
  reproducible from chain data for the formula-reconciled rows.
- Rows that remain non-matching are treated as overlap/upgrade review
  candidates rather than forced into the generic pre-fix formula bucket.
- Formula reconciliation is technical evidence, not automatic payout
  eligibility for single-model service rows.

Machine-readable versions are in `case6_full_old_formula_replay.csv` and
`case6_full_old_formula_replay.json`.
