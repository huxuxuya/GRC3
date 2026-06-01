# P3-CAND-06 Participant Epoch Timeline

This timeline expands the `24` pass-weight-but-failed-ratio candidate rows.
It shows where the normal epoch PoC window started, which confirmation PoC
event produced the exclusion, how far the participant was from the next
epoch, and how much confirmation weight remained after the failure.

Column notes:

- `PoC start` is `epoch_group_data.poc_start_block_height`.
- `cPoC` is the confirmation PoC trigger height selected by the scan.
- `next epoch in` is `next_epoch_height - exclusion_height` in blocks.
- `CW before -> confirmed` is confirmation weight before exclusion and at
  exclusion; `lost` is the difference.
- Model result cells show whether Qwen/Kimi reached `pass_weight` and the
  raw validating-weight percentage where a submission existed.

## Timeline

| Epoch | Participant | PoC start | cPoC | Exclusion | Next epoch in | Root weight | CW before -> confirmed | Lost CW | Ratio | Model results | Loss, GONKA |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| `263` | `gonka19cjm4c5mt3j3qdr8vhytmm4hef3pnkvkm0x7m2` | `4,059,188` | `#0 @ 4,073,650` | `4,073,931` | `1,048` blocks | `7,021` | `7,390 -> 184` | `7,206` | `2.7391%` | Qwen no_submission; Kimi pass_weight 76% | `1,915.652591432` |
| `263` | `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` | `4,059,188` | `#0 @ 4,073,650` | `4,073,931` | `1,048` blocks | `7,158` | `7,534 -> 2,400` | `5,134` | `35.0447%` | Qwen no_submission; Kimi pass_weight 76% | `1,953.032509538` |
| `263` | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | `4,059,188` | `#0 @ 4,073,650` | `4,073,931` | `1,048` blocks | `17,777` | `17,777 -> 2,387` | `15,390` | `14.7717%` | Qwen pass_weight 69%; Kimi no_submission | `4,850.385431974` |
| `264` | `gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds` | `4,074,579` | `#0 @ 4,075,202` | `4,075,483` | `14,887` blocks | `6,982` | `7,349 -> 2,660` | `4,689` | `39.8189%` | Qwen no_submission; Kimi pass_weight 70% | `1,970.264959744` |
| `264` | `gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d` | `4,074,579` | `#0 @ 4,075,202` | `4,075,483` | `14,887` blocks | `7,158` | `7,534 -> 3,373` | `4,161` | `49.2523%` | Qwen no_submission; Kimi pass_weight 70% | `2,019.930762224` |
| `264` | `gonka14g78ez2zy08k8sssue483zmfpgd4qut8zcwlqc` | `4,074,579` | `#0 @ 4,075,202` | `4,075,483` | `14,887` blocks | `7,158` | `7,534 -> 411` | `7,123` | `6.0014%` | Qwen no_submission; Kimi pass_weight 70% | `2,019.930762224` |
| `265` | `gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww` | `4,089,970` | `#2 @ 4,102,890` | `4,103,171` | `2,590` blocks | `1,066` | `1,254 -> 236` | `1,018` | `20.7038%` | Qwen pass_weight 69%; Kimi no_submission | `335.927643572` |
| `268` | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `4,136,143` | `#3 @ 4,144,898` | `4,145,179` | `6,755` blocks | `62,145` | `89,030 -> 14,477` | `74,553` | `17.3837%` | Qwen no_submission; Kimi pass_weight 88% | `25,309.087745610` |
| `269` | `gonka1007py6y2qfn2vaqrthqhtchkwx64hgzc6w544w` | `4,151,534` | `#5 @ 4,164,861` | `4,165,142` | `2,183` blocks | `5,324` | `7,755 -> 3,182` | `4,573` | `45.1393%` | Qwen no_submission; Kimi pass_weight 83% | `2,228.595538500` |
| `269` | `gonka1naxyjmun6kl23htjdujwd6c5z5avgwapsrmfk3` | `4,151,534` | `#0 @ 4,153,434` | `4,153,715` | `13,610` blocks | `1,280` | `1,347 -> 562` | `785` | `45.8992%` | Qwen pass_weight 87%; Kimi no_submission | `535.800580255` |
| `271` | `gonka16xa2sdc8qe2289nzr4e6vmdyzlke8g8fn8e75s` | `4,182,316` | `#0 @ 4,184,386` | `4,184,667` | `13,440` blocks | `390` | `2,297 -> 691` | `1,606` | `33.0943%` | Qwen pass_weight 78%; Kimi no_submission | `139.200061369` |
| `272` | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `4,197,707` | `#3 @ 4,209,686` | `4,209,967` | `3,531` blocks | `65,281` | `44,078 -> 27,426` | `16,652` | `40.2573%` | Qwen no_submission; Kimi pass_weight 90% | `22,521.036302544` |
| `272` | `gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p` | `4,197,707` | `#0 @ 4,202,293` | `4,202,574` | `10,924` blocks | `23,298` | `24,524 -> 4,249` | `20,275` | `19.0604%` | Qwen pass_weight 96%; Kimi no_submission | `8,037.485696859` |
| `272` | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `4,197,707` | `#0 @ 4,202,293` | `4,202,574` | `10,924` blocks | `1,059` | `1,114 -> 291` | `823` | `28.7372%` | Qwen pass_weight 96%; Kimi no_submission | `365.340258948` |
| `272` | `gonka1nku7u6d5mz80h35ty8ydeh0k5xydesvt9w0vjr` | `4,197,707` | `#0 @ 4,202,293` | `4,202,574` | `10,924` blocks | `426` | `2,506 -> 447` | `2,059` | `19.6229%` | Qwen pass_weight 96%; Kimi no_submission | `146.964070171` |
| `273` | `gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx` | `4,213,098` | `#0 @ 4,215,427` | `4,215,708` | `13,181` blocks | `8,069` | `10,669 -> 3,062` | `7,607` | `31.5761%` | Qwen pass_weight 73%; Kimi no_submission | `3,018.788733411` |
| `273` | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `4,213,098` | `#0 @ 4,215,427` | `4,215,708` | `13,181` blocks | `585` | `615 -> 274` | `341` | `49.0130%` | Qwen pass_weight 74%; Kimi no_submission | `218.861247867` |
| `274` | `gonka1qwfrtz9c7kcrfkrrlne2pkcye74mj6ce33xdkl` | `4,228,489` | `#2 @ 4,232,787` | `4,233,068` | `11,212` blocks | `468` | `492 -> 136` | `356` | `30.4095%` | Qwen pass_weight 79%; Kimi no_submission | `173.159717563` |
| `274` | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `4,228,489` | `#1 @ 4,231,815` | `4,232,096` | `12,184` blocks | `371` | `312 -> 103` | `209` | `29.0542%` | Qwen pass_weight 83%; Kimi no_submission | `137.269776102` |
| `275` | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `4,243,880` | `#2 @ 4,258,197` | `4,258,478` | `1,193` blocks | `328` | `289 -> 105` | `184` | `33.4816%` | Qwen pass_weight 90%; Kimi no_submission | `126.220428182` |
| `276` | `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e` | `4,259,271` | `#1 @ 4,265,965` | `4,266,246` | `8,816` blocks | `10,016` | `8,698 -> 1,343` | `7,355` | `16.9861%` | Qwen pass_weight 76%; Kimi no_submission | `3,557.528990032` |
| `276` | `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | `4,259,271` | `#2 @ 4,267,778` | `4,268,059` | `7,003` blocks | `48,865` | `65,994 -> 21,654` | `44,340` | `35.2638%` | Qwen pass_weight 86%; Kimi pass_weight 78% | `17,356.095656742` |
| `276` | `gonka14tqh62mangwzrma2lgg2dm375rcjzn2ydy8ttm` | `4,259,271` | `#0 @ 4,264,130` | `4,264,411` | `10,651` blocks | `33,125` | `50,810 -> 17,149` | `33,661` | `37.1301%` | Qwen no_submission; Kimi pass_weight 86% | `11,765.489995489` |
| `276` | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | `4,259,271` | `#0 @ 4,264,130` | `4,264,411` | `10,651` blocks | `28,493` | `48,847 -> 16,147` | `32,700` | `36.3655%` | Qwen no_submission; Kimi pass_weight 74% | `10,120.274911440` |

## Reading The Timeline

These rows are suspicious because each participant had at least one model
reach `pass_weight`, but the chain still reduced confirmation weight below
alpha and excluded the participant before the next epoch.

This table is not yet a payout proof. The next validation step is to replay
each row through the historical `foldEventReadings` formula and decide
whether the pass-weight model should have preserved enough confirmation
capacity for that participant.
