# P3-CAND-06 Gross Compensation Calculation

This table calculates the gross candidate amount for every P3-CAND-06 row
before overlap review. All `24` candidate rows are included in the gross
sum. Overlap status is shown only as a reference column and is not used to
filter this calculation.

This is not an approved payout table. Final payout still requires:

- committee policy decision for single-model `pass_weight` rows;
- duplicate-payment review against P3-CAND-04 and P4-CAND-01;
- final recipient/contact mapping if this candidate is promoted.

## Summary

| Metric | Value |
|---|---:|
| Candidate rows included | `24` |
| Unique participants | `19` |
| Gross compensation before overlap review | `120,822.324371792 GONKA` |

## Totals By Epoch

| Epoch | Rows | Unique participants | Gross compensation, GONKA |
|---:|---:|---:|---:|
| `263` | `3` | `3` | `8,719.070532944` |
| `264` | `3` | `3` | `6,010.126484192` |
| `265` | `1` | `1` | `335.927643572` |
| `268` | `1` | `1` | `25,309.087745610` |
| `269` | `2` | `2` | `2,764.396118755` |
| `271` | `1` | `1` | `139.200061369` |
| `272` | `4` | `4` | `31,070.826328522` |
| `273` | `2` | `2` | `3,237.649981278` |
| `274` | `2` | `2` | `310.429493665` |
| `275` | `1` | `1` | `126.220428182` |
| `276` | `4` | `4` | `42,799.389553703` |

## Totals By Passing Model Set

| Passing model(s) | Rows | Unique participants | Gross compensation, GONKA |
|---|---:|---:|---:|
| `Kimi` | `10` | `9` | `81,823.296078745` |
| `Qwen` | `13` | `10` | `21,642.932636305` |
| `Qwen+Kimi` | `1` | `1` | `17,356.095656742` |

## Totals By Overlap Status

These buckets are reference-only for this calculation; no rows are removed
from the gross sum.

| Overlap status | Rows | Gross compensation, GONKA |
|---|---:|---:|
| `known_p3_cand_04_same_address` | `1` | `17,356.095656742` |
| `no_known_overlap_in_local_repo` | `6` | `14,729.197017136` |
| `p3_cand_04_epoch_overlap_unresolved` | `3` | `25,443.293896961` |
| `p4_cand_01_epoch_range_overlap` | `14` | `63,293.737800953` |

## Totals By Participant

| Participant | Rows | Epochs | Passing model(s) | Gross compensation, GONKA | Overlap reference |
|---|---:|---|---|---:|---|
| `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `2` | `268, 272` | `Kimi` | `47,830.124048154` | `p4_cand_01_epoch_range_overlap` |
| `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | `1` | `276` | `Qwen+Kimi` | `17,356.095656742` | `known_p3_cand_04_same_address` |
| `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | `2` | `263, 276` | `Kimi, Qwen` | `14,970.660343414` | `no_known_overlap_in_local_repo, p3_cand_04_epoch_overlap_unresolved` |
| `gonka14tqh62mangwzrma2lgg2dm375rcjzn2ydy8ttm` | `1` | `276` | `Kimi` | `11,765.489995489` | `p3_cand_04_epoch_overlap_unresolved` |
| `gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p` | `1` | `272` | `Qwen` | `8,037.485696859` | `p4_cand_01_epoch_range_overlap` |
| `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e` | `1` | `276` | `Qwen` | `3,557.528990032` | `p3_cand_04_epoch_overlap_unresolved` |
| `gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx` | `1` | `273` | `Qwen` | `3,018.788733411` | `p4_cand_01_epoch_range_overlap` |
| `gonka1007py6y2qfn2vaqrthqhtchkwx64hgzc6w544w` | `1` | `269` | `Kimi` | `2,228.595538500` | `p4_cand_01_epoch_range_overlap` |
| `gonka14g78ez2zy08k8sssue483zmfpgd4qut8zcwlqc` | `1` | `264` | `Kimi` | `2,019.930762224` | `no_known_overlap_in_local_repo` |
| `gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d` | `1` | `264` | `Kimi` | `2,019.930762224` | `no_known_overlap_in_local_repo` |
| `gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds` | `1` | `264` | `Kimi` | `1,970.264959744` | `no_known_overlap_in_local_repo` |
| `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` | `1` | `263` | `Kimi` | `1,953.032509538` | `no_known_overlap_in_local_repo` |
| `gonka19cjm4c5mt3j3qdr8vhytmm4hef3pnkvkm0x7m2` | `1` | `263` | `Kimi` | `1,915.652591432` | `no_known_overlap_in_local_repo` |
| `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `4` | `272, 273, 274, 275` | `Qwen` | `847.691711099` | `p4_cand_01_epoch_range_overlap` |
| `gonka1naxyjmun6kl23htjdujwd6c5z5avgwapsrmfk3` | `1` | `269` | `Qwen` | `535.800580255` | `p4_cand_01_epoch_range_overlap` |
| `gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww` | `1` | `265` | `Qwen` | `335.927643572` | `p4_cand_01_epoch_range_overlap` |
| `gonka1qwfrtz9c7kcrfkrrlne2pkcye74mj6ce33xdkl` | `1` | `274` | `Qwen` | `173.159717563` | `p4_cand_01_epoch_range_overlap` |
| `gonka1nku7u6d5mz80h35ty8ydeh0k5xydesvt9w0vjr` | `1` | `272` | `Qwen` | `146.964070171` | `p4_cand_01_epoch_range_overlap` |
| `gonka16xa2sdc8qe2289nzr4e6vmdyzlke8g8fn8e75s` | `1` | `271` | `Qwen` | `139.200061369` | `p4_cand_01_epoch_range_overlap` |

## Row-Level Gross Calculation

| Epoch | Participant | Trigger -> Exclusion | Passing model(s) | Stored ratio | Old formula match | New-style pass alpha | Gross compensation, GONKA | Overlap reference |
|---:|---|---|---|---:|---|---|---:|---|
| `263` | `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` | `4073650` -> `4073931` | `Kimi` | `35.0447%` | `True` | `False` | `1,953.032509538` | `no_known_overlap_in_local_repo` |
| `263` | `gonka19cjm4c5mt3j3qdr8vhytmm4hef3pnkvkm0x7m2` | `4073650` -> `4073931` | `Kimi` | `2.7391%` | `True` | `False` | `1,915.652591432` | `no_known_overlap_in_local_repo` |
| `263` | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | `4073650` -> `4073931` | `Qwen` | `14.7717%` | `True` | `False` | `4,850.385431974` | `no_known_overlap_in_local_repo` |
| `264` | `gonka14g78ez2zy08k8sssue483zmfpgd4qut8zcwlqc` | `4075202` -> `4075483` | `Kimi` | `6.0014%` | `True` | `False` | `2,019.930762224` | `no_known_overlap_in_local_repo` |
| `264` | `gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d` | `4075202` -> `4075483` | `Kimi` | `49.2523%` | `True` | `False` | `2,019.930762224` | `no_known_overlap_in_local_repo` |
| `264` | `gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds` | `4075202` -> `4075483` | `Kimi` | `39.8189%` | `True` | `False` | `1,970.264959744` | `no_known_overlap_in_local_repo` |
| `265` | `gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww` | `4102890` -> `4103171` | `Qwen` | `20.7038%` | `True` | `False` | `335.927643572` | `p4_cand_01_epoch_range_overlap` |
| `268` | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `4144898` -> `4145179` | `Kimi` | `17.3837%` | `True` | `False` | `25,309.087745610` | `p4_cand_01_epoch_range_overlap` |
| `269` | `gonka1007py6y2qfn2vaqrthqhtchkwx64hgzc6w544w` | `4164861` -> `4165142` | `Kimi` | `45.1393%` | `True` | `False` | `2,228.595538500` | `p4_cand_01_epoch_range_overlap` |
| `269` | `gonka1naxyjmun6kl23htjdujwd6c5z5avgwapsrmfk3` | `4153434` -> `4153715` | `Qwen` | `45.8992%` | `True` | `False` | `535.800580255` | `p4_cand_01_epoch_range_overlap` |
| `271` | `gonka16xa2sdc8qe2289nzr4e6vmdyzlke8g8fn8e75s` | `4184386` -> `4184667` | `Qwen` | `33.0943%` | `True` | `False` | `139.200061369` | `p4_cand_01_epoch_range_overlap` |
| `272` | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `4202293` -> `4202574` | `Qwen` | `28.7372%` | `True` | `False` | `365.340258948` | `p4_cand_01_epoch_range_overlap` |
| `272` | `gonka1nku7u6d5mz80h35ty8ydeh0k5xydesvt9w0vjr` | `4202293` -> `4202574` | `Qwen` | `19.6229%` | `True` | `False` | `146.964070171` | `p4_cand_01_epoch_range_overlap` |
| `272` | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `4209686` -> `4209967` | `Kimi` | `40.2573%` | `True` | `False` | `22,521.036302544` | `p4_cand_01_epoch_range_overlap` |
| `272` | `gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p` | `4202293` -> `4202574` | `Qwen` | `19.0604%` | `True` | `False` | `8,037.485696859` | `p4_cand_01_epoch_range_overlap` |
| `273` | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `4215427` -> `4215708` | `Qwen` | `49.0130%` | `True` | `False` | `218.861247867` | `p4_cand_01_epoch_range_overlap` |
| `273` | `gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx` | `4215427` -> `4215708` | `Qwen` | `31.5761%` | `True` | `False` | `3,018.788733411` | `p4_cand_01_epoch_range_overlap` |
| `274` | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `4231815` -> `4232096` | `Qwen` | `29.0542%` | `True` | `False` | `137.269776102` | `p4_cand_01_epoch_range_overlap` |
| `274` | `gonka1qwfrtz9c7kcrfkrrlne2pkcye74mj6ce33xdkl` | `4232787` -> `4233068` | `Qwen` | `30.4095%` | `True` | `False` | `173.159717563` | `p4_cand_01_epoch_range_overlap` |
| `275` | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `4258197` -> `4258478` | `Qwen` | `33.4816%` | `True` | `False` | `126.220428182` | `p4_cand_01_epoch_range_overlap` |
| `276` | `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | `4267778` -> `4268059` | `Qwen+Kimi` | `35.2638%` | `False` | `False` | `17,356.095656742` | `known_p3_cand_04_same_address` |
| `276` | `gonka14tqh62mangwzrma2lgg2dm375rcjzn2ydy8ttm` | `4264130` -> `4264411` | `Kimi` | `37.1301%` | `False` | `False` | `11,765.489995489` | `p3_cand_04_epoch_overlap_unresolved` |
| `276` | `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e` | `4265965` -> `4266246` | `Qwen` | `16.9861%` | `True` | `False` | `3,557.528990032` | `p3_cand_04_epoch_overlap_unresolved` |
| `276` | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | `4264130` -> `4264411` | `Kimi` | `36.3655%` | `True` | `False` | `10,120.274911440` | `p3_cand_04_epoch_overlap_unresolved` |

Machine-readable versions:

- `case6_gross_compensation_calculation.csv`
- `case6_gross_compensation_calculation.json`
- `case6_gross_compensation_by_epoch.csv`
- `case6_gross_compensation_by_participant.csv`
- `case6_gross_compensation_by_pass_models.csv`
- `case6_gross_compensation_by_overlap_reference.csv`
