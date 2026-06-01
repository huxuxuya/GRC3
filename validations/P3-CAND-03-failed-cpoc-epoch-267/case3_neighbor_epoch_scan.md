# Case 3 Neighbor Epoch Scan

Range checked: epochs `262` through `272`.

The scan looks for the same durable chain signature as Case 3:

1. participant excluded with `failed_confirmation_poc`;
2. `ConfirmationPoCRatio` below `AlphaThreshold`;
3. zero actual epoch reward;
4. Kimi submission exists but Kimi validation weight does not exceed the two-thirds weight line;
5. Kimi preserved-node voting power is present at the exclusion height.

## Epoch Summary

| Epoch | Participants | Excluded | failed_confirmation_poc | Case-3-like | Participants |
|---:|---:|---:|---:|---:|---|
| 262 | 54 | 0 | 0 | 0 |  |
| 263 | 55 | 6 | 6 | 0 |  |
| 264 | 54 | 3 | 3 | 0 |  |
| 265 | 51 | 14 | 14 | 1 | gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6 |
| 266 | 46 | 7 | 7 | 0 |  |
| 267 | 51 | 3 | 2 | 1 | gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6 |
| 268 | 57 | 11 | 11 | 0 |  |
| 269 | 58 | 11 | 11 | 0 |  |
| 270 | 49 | 4 | 4 | 0 |  |
| 271 | 49 | 7 | 7 | 0 |  |
| 272 | 50 | 7 | 6 | 0 |  |

## Case-3-like Rows

| Epoch | Participant | Ratio | Alpha | Kimi submitted | Kimi valid weight | Preserved Kimi weight | Loss, GONKA |
|---:|---|---:|---:|---:|---:|---:|---:|
| 265 | `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6` | 0.5359% | 0.5 | 52028 | 256727 (28.3934%) | 189884 (21.0008%) | 20896.527179100 |
| 267 | `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6` | 0.5742% | 0.5 | 57664 | 171571 (31.6894%) | 159432 (29.4473%) | 10262.057515369 |

## All failed_confirmation_poc Rows

| Epoch | Participant | Reward | Ratio | Kimi result | Reason |
|---:|---|---:|---:|---|---|
| 263 | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | 0 | 27.2752% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 263 | `gonka19cjm4c5mt3j3qdr8vhytmm4hef3pnkvkm0x7m2` | 0 | 2.7391% | pass_weight | zero_reward,ratio_below_alpha,kimi_submitted,kimi_preserved_power_present |
| 263 | `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` | 0 | 35.0447% | pass_weight | zero_reward,ratio_below_alpha,kimi_submitted,kimi_preserved_power_present |
| 263 | `gonka125n6kr5gvdup0lndfkps7t6rd6592panhrg3np` | 0 | 42.9329% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 263 | `gonka1w29nvdy6caqtrw30whz9h6ghl0xszwh3egndah` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 263 | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | 0 | 14.7717% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 264 | `gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds` | 0 | 39.8189% | pass_weight | zero_reward,ratio_below_alpha,kimi_submitted,kimi_preserved_power_present |
| 264 | `gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d` | 0 | 49.2523% | pass_weight | zero_reward,ratio_below_alpha,kimi_submitted,kimi_preserved_power_present |
| 264 | `gonka14g78ez2zy08k8sssue483zmfpgd4qut8zcwlqc` | 0 | 6.0014% | pass_weight | zero_reward,ratio_below_alpha,kimi_submitted,kimi_preserved_power_present |
| 265 | `gonka1qnj39ysxpzknvrr5dw9rdl7cx5q7dpkwerryrs` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 265 | `gonka1zsvl7ujlc8z3a35v2q6e3nml7ftyk23v76jqgl` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 265 | `gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 265 | `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 265 | `gonka187tn9y92ur6tu0zf69u94hwl0q77m47y0k36hv` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 265 | `gonka1famtxh54kad6ylwtm60j6d7h6unpc08d4vdqnk` | 0 | 8.9349% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 265 | `gonka125n6kr5gvdup0lndfkps7t6rd6592panhrg3np` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 265 | `gonka1tl5m3vuqsx333v7095ymwjdc4vdk2wd9r5hqws` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 265 | `gonka1wt8sr9jxzpec65j7zkxsgh6edk3m6r8nlf5za4` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 265 | `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6` | 0 | 0.5359% | weight_shortfall | zero_reward,ratio_below_alpha,kimi_submitted,kimi_below_2_3,kimi_preserved_power_present |
| 265 | `gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww` | 0 | 20.7038% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 265 | `gonka1myu058axjs62mc3e7na9krwvqpfl9z3gtcw9es` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 265 | `gonka1mmlyd5xxu5l68yx8wzclrkxkxvm88mhq5tp5s0` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 265 | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | 0 | 25.7867% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 266 | `gonka1qnj39ysxpzknvrr5dw9rdl7cx5q7dpkwerryrs` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 266 | `gonka187tn9y92ur6tu0zf69u94hwl0q77m47y0k36hv` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 266 | `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 266 | `gonka13a4v8gxxjav5t4xq5y9cv9d8rfnvkjfw5adqz3` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 266 | `gonka14ef2pxjge75gflqftn7m2wy0xv59gq9uc7qnct` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 266 | `gonka1myu058axjs62mc3e7na9krwvqpfl9z3gtcw9es` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 266 | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 267 | `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6` | 0 | 0.5742% | weight_shortfall | zero_reward,ratio_below_alpha,kimi_submitted,kimi_below_2_3,kimi_preserved_power_present |
| 267 | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 268 | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | 0 | 17.3837% | pass_weight | zero_reward,ratio_below_alpha,kimi_submitted,kimi_preserved_power_present |
| 268 | `gonka18x5f3q6g0r3n7rgslwq66d2hd6tp5mgxwxnmc3` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 268 | `gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 268 | `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 268 | `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e` | 0 | 16.7727% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 268 | `gonka125n6kr5gvdup0lndfkps7t6rd6592panhrg3np` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 268 | `gonka1tl5m3vuqsx333v7095ymwjdc4vdk2wd9r5hqws` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 268 | `gonka1wt8sr9jxzpec65j7zkxsgh6edk3m6r8nlf5za4` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 268 | `gonka14g78ez2zy08k8sssue483zmfpgd4qut8zcwlqc` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 268 | `gonka1mmlyd5xxu5l68yx8wzclrkxkxvm88mhq5tp5s0` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 268 | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 269 | `gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 269 | `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 269 | `gonka125n6kr5gvdup0lndfkps7t6rd6592panhrg3np` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 269 | `gonka1tl5m3vuqsx333v7095ymwjdc4vdk2wd9r5hqws` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 269 | `gonka1w29nvdy6caqtrw30whz9h6ghl0xszwh3egndah` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 269 | `gonka1007py6y2qfn2vaqrthqhtchkwx64hgzc6w544w` | 0 | 45.1393% | pass_weight | zero_reward,ratio_below_alpha,kimi_submitted,kimi_preserved_power_present |
| 269 | `gonka1naxyjmun6kl23htjdujwd6c5z5avgwapsrmfk3` | 0 | 45.8992% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 269 | `gonka14g78ez2zy08k8sssue483zmfpgd4qut8zcwlqc` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 269 | `gonka1c6fwzedfsmpu4jnjekv4cn7mvr7x7fuqd6uqt9` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 269 | `gonka1mmlyd5xxu5l68yx8wzclrkxkxvm88mhq5tp5s0` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 269 | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 270 | `gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx` | 0 | 13.1539% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 270 | `gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 270 | `gonka125n6kr5gvdup0lndfkps7t6rd6592panhrg3np` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 270 | `gonka1mmlyd5xxu5l68yx8wzclrkxkxvm88mhq5tp5s0` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 271 | `gonka1qu9mna5xlvlnw9455ygtjq92wuzkzm237w8l08` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 271 | `gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 271 | `gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 271 | `gonka1c6fwzedfsmpu4jnjekv4cn7mvr7x7fuqd6uqt9` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 271 | `gonka16xa2sdc8qe2289nzr4e6vmdyzlke8g8fn8e75s` | 0 | 33.0943% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 271 | `gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2` | 0 | 3.5450% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 271 | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 272 | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | 0 | 40.2573% | pass_weight | zero_reward,ratio_below_alpha,kimi_submitted,kimi_preserved_power_present |
| 272 | `gonka1qu9mna5xlvlnw9455ygtjq92wuzkzm237w8l08` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 272 | `gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p` | 0 | 19.0604% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 272 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | 0 | 28.7372% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 272 | `gonka1nku7u6d5mz80h35ty8ydeh0k5xydesvt9w0vjr` | 0 | 19.6229% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
| 272 | `gonka1mmlyd5xxu5l68yx8wzclrkxkxvm88mhq5tp5s0` | 0 | 0.0000% | no_submission | zero_reward,ratio_below_alpha,kimi_below_2_3,kimi_preserved_power_present |
