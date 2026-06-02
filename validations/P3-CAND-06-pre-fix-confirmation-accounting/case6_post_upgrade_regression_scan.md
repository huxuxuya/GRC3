# P3-CAND-06 Post-v0.2.13 Regression Scan

Range checked: epochs `277` through `283`.
`v0.2.13` was installed at block `4267300` during epoch `276`; epoch `277` is the first clean start after the upgrade.

The scan looks for recurrence of the P3-CAND-06 signature:

1. participant excluded with `failed_confirmation_poc`;
2. actual epoch reward is zero;
3. `ConfirmationPoCRatio` is below `AlphaThreshold`;
4. at least one tracked model (`Qwen` or `Kimi`) has strict `pass_weight` using `validWeight > TotalNetworkWeight * 2 / 3`.

The requested end epoch was `287`, but epoch `284`
was not available from the archive LCD during this run, so the artifact records the complete available range.

## Result

| Metric | Value |
|---|---:|
| Epochs checked | `7` |
| failed_confirmation_poc rows | `50` |
| Rows with pass-weight model and failed ratio | `8` |
| Case-6-like rows with exactly one passing tracked model | `8` |
| Case-6-like rows with both tracked models passing | `0` |

Interpretation: this is a recurrence scan for the broad signal, not a
standalone proof that the pre-`v0.2.13` root cause still exists. Rows
where exactly one tracked model passes and the other has `no_submission`
can be ordinary post-upgrade multi-model accounting unless formula replay
proves otherwise.

## Epoch Summary

| Epoch | Participants | Total weight | >2/3 min | cPoC events | Excluded | failed_confirmation_poc | pass-weight failed rows | single pass | both pass | Case-6-like rows | Participants |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 277 | 56 | 502534 | 335023 | 1 | 6 | 6 | 0 | 0 | 0 | 0 |  |
| 278 | 57 | 444033 | 296023 | 4 | 12 | 12 | 2 | 2 | 0 | 2 | gonka1zfj67rvrz86q4uu2vdyt24gwf06yl9cqmy58np;gonka1tlvg4kjx7ljd5thgd5fkgh39q6lu8cmxupktgg |
| 279 | 57 | 546414 | 364277 | 1 | 8 | 8 | 1 | 1 | 0 | 1 | gonka19ghzvgfr065s3fr5awuvs3nhy9fq4n7wrr9kel |
| 280 | 53 | 570437 | 380292 | 5 | 2 | 2 | 0 | 0 | 0 | 0 |  |
| 281 | 59 | 704835 | 469891 | 2 | 2 | 2 | 0 | 0 | 0 | 0 |  |
| 282 | 62 | 555014 | 370010 | 5 | 14 | 14 | 4 | 4 | 0 | 4 | gonka1qnj39ysxpzknvrr5dw9rdl7cx5q7dpkwerryrs;gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx;gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e;gonka10egxskdvc0a5w2r5q44wvuxmjyplx6yn8l97fd |
| 283 | 55 | 548622 | 365749 | 2 | 6 | 6 | 1 | 1 | 0 | 1 | gonka10egxskdvc0a5w2r5q44wvuxmjyplx6yn8l97fd |

## Case-6-like Rows

| Epoch | Participant | Ratio | Alpha | Pass model(s) | Qwen valid | Kimi valid | Loss, GONKA |
|---:|---|---:|---:|---|---:|---:|---:|
| 278 | `gonka1zfj67rvrz86q4uu2vdyt24gwf06yl9cqmy58np` | 34.1490% | 0.5 | Qwen | 363287 (81.8153%) | 0 (0.0000%) | 1110.308716928 |
| 278 | `gonka1tlvg4kjx7ljd5thgd5fkgh39q6lu8cmxupktgg` | 19.9807% | 0.5 | Kimi | 0 (0.0000%) | 346519 (78.0390%) | 1200.230330418 |
| 279 | `gonka19ghzvgfr065s3fr5awuvs3nhy9fq4n7wrr9kel` | 42.5330% | 0.5 | Qwen | 470600 (86.1252%) | 0 (0.0000%) | 2837.619407556 |
| 282 | `gonka1qnj39ysxpzknvrr5dw9rdl7cx5q7dpkwerryrs` | 19.3024% | 0.5 | Qwen | 486890 (87.7257%) | 0 (0.0000%) | 311.151814857 |
| 282 | `gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx` | 13.6374% | 0.5 | Qwen | 484908 (87.3686%) | 0 (0.0000%) | 1401.456292125 |
| 282 | `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e` | 38.3916% | 0.5 | Qwen | 489774 (88.2453%) | 0 (0.0000%) | 10564.393452088 |
| 282 | `gonka10egxskdvc0a5w2r5q44wvuxmjyplx6yn8l97fd` | 7.4869% | 0.5 | Qwen | 486890 (87.7257%) | 0 (0.0000%) | 838.225674723 |
| 283 | `gonka10egxskdvc0a5w2r5q44wvuxmjyplx6yn8l97fd` | 36.1887% | 0.5 | Qwen | 440208 (80.2389%) | 0 (0.0000%) | 576.731377435 |

## All failed_confirmation_poc Rows

| Epoch | Participant | Reward | Ratio | Pass model(s) | Qwen result | Kimi result | Reason |
|---:|---|---:|---:|---|---|---|---|
| 277 | `gonka1pksqg5wpgqsnezrr0nw7l35y7u8v4vvjdavpem` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 277 | `gonka1zfj67rvrz86q4uu2vdyt24gwf06yl9cqmy58np` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 277 | `gonka1y7mt2r8qalzdca9eq3pvf86c0puv0xfa60wl8w` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 277 | `gonka19u92d2744vrmjg2y8wpeguz48vv52damsc5uv5` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 277 | `gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 277 | `gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2` | 0 | 5.4056% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 278 | `gonka1qnj39ysxpzknvrr5dw9rdl7cx5q7dpkwerryrs` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 278 | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 278 | `gonka1pksqg5wpgqsnezrr0nw7l35y7u8v4vvjdavpem` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 278 | `gonka1zfj67rvrz86q4uu2vdyt24gwf06yl9cqmy58np` | 0 | 34.1490% | Qwen | pass_weight | no_submission | zero_reward,ratio_below_alpha,pass_weight_model:Qwen |
| 278 | `gonka1y7mt2r8qalzdca9eq3pvf86c0puv0xfa60wl8w` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 278 | `gonka19u92d2744vrmjg2y8wpeguz48vv52damsc5uv5` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 278 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 278 | `gonka1tlvg4kjx7ljd5thgd5fkgh39q6lu8cmxupktgg` | 0 | 19.9807% | Kimi | no_submission | pass_weight | zero_reward,ratio_below_alpha,pass_weight_model:Kimi |
| 278 | `gonka10egxskdvc0a5w2r5q44wvuxmjyplx6yn8l97fd` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 278 | `gonka1scskt6wpnjnumsah6kjphmdu87vjgvcxmn4rxv` | 0 | 9.1151% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 278 | `gonka1naxyjmun6kl23htjdujwd6c5z5avgwapsrmfk3` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 278 | `gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww` | 0 | 0.0000% |  | fail_weight | no_submission | zero_reward,ratio_below_alpha |
| 279 | `gonka1pksqg5wpgqsnezrr0nw7l35y7u8v4vvjdavpem` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 279 | `gonka1zfj67rvrz86q4uu2vdyt24gwf06yl9cqmy58np` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 279 | `gonka1y7mt2r8qalzdca9eq3pvf86c0puv0xfa60wl8w` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 279 | `gonka19ghzvgfr065s3fr5awuvs3nhy9fq4n7wrr9kel` | 0 | 42.5330% | Qwen | pass_weight | no_submission | zero_reward,ratio_below_alpha,pass_weight_model:Qwen |
| 279 | `gonka19u92d2744vrmjg2y8wpeguz48vv52damsc5uv5` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 279 | `gonka10egxskdvc0a5w2r5q44wvuxmjyplx6yn8l97fd` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 279 | `gonka1naxyjmun6kl23htjdujwd6c5z5avgwapsrmfk3` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 279 | `gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 280 | `gonka1naxyjmun6kl23htjdujwd6c5z5avgwapsrmfk3` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 280 | `gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 281 | `gonka1naxyjmun6kl23htjdujwd6c5z5avgwapsrmfk3` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 281 | `gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 282 | `gonka1qnj39ysxpzknvrr5dw9rdl7cx5q7dpkwerryrs` | 0 | 19.3024% | Qwen | pass_weight | no_submission | zero_reward,ratio_below_alpha,pass_weight_model:Qwen |
| 282 | `gonka1p2lhgng7tcqju7emk989s5fpdr7k2c3ek6h26m` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 282 | `gonka1pksqg5wpgqsnezrr0nw7l35y7u8v4vvjdavpem` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 282 | `gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx` | 0 | 13.6374% | Qwen | pass_weight | no_submission | zero_reward,ratio_below_alpha,pass_weight_model:Qwen |
| 282 | `gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 282 | `gonka1y7mt2r8qalzdca9eq3pvf86c0puv0xfa60wl8w` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 282 | `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e` | 0 | 38.3916% | Qwen | pass_weight | no_submission | zero_reward,ratio_below_alpha,pass_weight_model:Qwen |
| 282 | `gonka10egxskdvc0a5w2r5q44wvuxmjyplx6yn8l97fd` | 0 | 7.4869% | Qwen | pass_weight | no_submission | zero_reward,ratio_below_alpha,pass_weight_model:Qwen |
| 282 | `gonka1naxyjmun6kl23htjdujwd6c5z5avgwapsrmfk3` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 282 | `gonka14tqh62mangwzrma2lgg2dm375rcjzn2ydy8ttm` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 282 | `gonka1ce02jjduga8jvwj8jx39mxn0jr345vgkx7lk2n` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 282 | `gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 282 | `gonka1myu058axjs62mc3e7na9krwvqpfl9z3gtcw9es` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 282 | `gonka1amlmhjym02shahjv8ldmupg4cx0qc66q6f85rj` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 283 | `gonka1qnj39ysxpzknvrr5dw9rdl7cx5q7dpkwerryrs` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 283 | `gonka1xu8fgywyg8aauydpdr2gtu30zv0x0330k249ua` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 283 | `gonka125n6kr5gvdup0lndfkps7t6rd6592panhrg3np` | 0 | 25.7493% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 283 | `gonka10egxskdvc0a5w2r5q44wvuxmjyplx6yn8l97fd` | 0 | 36.1887% | Qwen | pass_weight | no_submission | zero_reward,ratio_below_alpha,pass_weight_model:Qwen |
| 283 | `gonka1naxyjmun6kl23htjdujwd6c5z5avgwapsrmfk3` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
| 283 | `gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww` | 0 | 0.0000% |  | no_submission | no_submission | zero_reward,ratio_below_alpha |
