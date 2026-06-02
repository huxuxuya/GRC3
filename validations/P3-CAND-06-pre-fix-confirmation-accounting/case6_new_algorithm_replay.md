# P3-CAND-06 v0.2.13-Style Counterfactual Replay

This replay applies the v0.2.13-style idea of using one confirmation
snapshot model set for measured, preserved, and total expected weight.
It is limited to the Qwen/Kimi data available in this case folder.

## Result

| Check | Value |
|---|---:|
| Rows replayed | `24` |
| Rows that would pass alpha in this counterfactual | `0` |
| Rows still below alpha in this counterfactual | `24` |

## Rows

| Epoch | Participant | Pass model(s) | Snapshot models | Stored ratio | New ratio | Would pass alpha |
|---:|---|---|---|---:|---:|---|
| 263 | `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` | Kimi | Qwen+Kimi | 0.3504465126629466 | 0.3504465126629467 | False |
| 263 | `gonka19cjm4c5mt3j3qdr8vhytmm4hef3pnkvkm0x7m2` | Kimi | Qwen+Kimi | 0.0273911017624090 | 0.0273911017624090 | False |
| 263 | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | Qwen | Qwen+Kimi | 0.1477168586521700 | 0.1477168586521700 | False |
| 264 | `gonka14g78ez2zy08k8sssue483zmfpgd4qut8zcwlqc` | Kimi | Qwen+Kimi | 0.0600139652935296 | 0.0600139652935296 | False |
| 264 | `gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d` | Kimi | Qwen+Kimi | 0.4925233696717163 | 0.4925233696717163 | False |
| 264 | `gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds` | Kimi | Qwen+Kimi | 0.3981892270054329 | 0.3981892270054329 | False |
| 265 | `gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww` | Qwen | Qwen+Kimi | 0.2070382476844176 | 0.2070382476844176 | False |
| 268 | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | Kimi | Qwen+Kimi | 0.1738374588419373 | 0.1738374588419373 | False |
| 269 | `gonka1007py6y2qfn2vaqrthqhtchkwx64hgzc6w544w` | Kimi | Qwen+Kimi | 0.4513926569961960 | 0.4513926569961961 | False |
| 269 | `gonka1naxyjmun6kl23htjdujwd6c5z5avgwapsrmfk3` | Qwen | Qwen+Kimi | 0.4589917046641561 | 0.4589917046641561 | False |
| 271 | `gonka16xa2sdc8qe2289nzr4e6vmdyzlke8g8fn8e75s` | Qwen | Qwen+Kimi | 0.3309429767530519 | 0.3309429767530519 | False |
| 272 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | Qwen | Qwen+Kimi | 0.2873716456026213 | 0.2873716456026213 | False |
| 272 | `gonka1nku7u6d5mz80h35ty8ydeh0k5xydesvt9w0vjr` | Qwen | Qwen+Kimi | 0.1962287210365091 | 0.1962287210365091 | False |
| 272 | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | Kimi | Qwen+Kimi | 0.4025727135404508 | 0.4025727135404509 | False |
| 272 | `gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p` | Qwen | Qwen+Kimi | 0.1906037937018298 | 0.1906037937018298 | False |
| 273 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | Qwen | Qwen+Kimi | 0.4901303138443925 | 0.4901303138443926 | False |
| 273 | `gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx` | Qwen | Qwen+Kimi | 0.3157608599255127 | 0.3157608599255126 | False |
| 274 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | Qwen | Qwen+Kimi | 0.2905418747002905 | 0.2905418747002905 | False |
| 274 | `gonka1qwfrtz9c7kcrfkrrlne2pkcye74mj6ce33xdkl` | Qwen | Qwen+Kimi | 0.3040954501954261 | 0.3040954501954260 | False |
| 275 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | Qwen | Qwen+Kimi | 0.3348160903046826 | 0.3348160903046826 | False |
| 276 | `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | Qwen+Kimi | Qwen+Kimi | 0.3526384050777585 | 0.4009670981394065 | False |
| 276 | `gonka14tqh62mangwzrma2lgg2dm375rcjzn2ydy8ttm` | Kimi | Qwen+Kimi | 0.3713006608671101 | 0.3713223123138923 | False |
| 276 | `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e` | Qwen | Qwen+Kimi | 0.1698606282794295 | 0.1698606282794295 | False |
| 276 | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | Kimi | Qwen+Kimi | 0.3636554209600337 | 0.3636554209600336 | False |

## Interpretation

- This is a bounded counterfactual, not a claim that the exact production
  upgrade state can be reconstructed without the final stored
  `ConfirmationWeightScales` field.
- If a single-model row remains below alpha here, it supports keeping
  payout eligibility as a policy decision rather than automatically
  treating every single-model pass as compensable.
- Epoch `276` rows remain overlap-sensitive because the upgrade window
  changed params and cPoC behavior.

Machine-readable versions are in `case6_new_algorithm_replay.csv` and
`case6_new_algorithm_replay.json`.
