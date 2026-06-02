# Pre-Fix Window Review

The `v0.2.13` fix was installed on-chain during epoch `276`, at block
`4,267,300`. The new confirmation snapshot logic starts cleanly from epoch
`277`, because confirmation PoC is disabled for the rest of the upgrade epoch.

For that reason, the neighbor scan was extended through epoch `276`.

## Scope

```text
epochs checked: 262..276
fix installed:  epoch 276, block 4,267,300
clean start:    epoch 277, block 4,275,062
```

## Result Summary

The table keeps the original neighbor-scan loss totals as full-root estimates.
For epoch `265`, the narrower chain-style counterfactual is lower because the
lost raw Kimi model weight must be scaled before it is used as a reward
numerator. See `case3_epoch265_timeline.md` for the detailed amount split.

| Class | Rows | Estimated zero-reward loss, GONKA | Interpretation |
|---|---:|---:|---|
| Strict Case-3-like Kimi submitted below `2/3` | `2` | `31,158.584694469` full-root scan estimate; `23,213.864411072` if epoch `265` uses the narrower `12,951.806895703` counterfactual | Same narrow symptom family; epoch `265` amount needs scope/source decision. |
| Submitted and `pass_weight`, but still failed ratio | `24` | `120,822.324371792` | Broader suspicious confirmation-accounting candidates; not the same Kimi-shortfall signature. |
| Qwen submitted below `2/3` | `3` | `4,917.314529158` | Different model-side shortfall. |
| No Qwen/Kimi submission on selected cPoC event | `90` | `260,371.420615124` | Broad `failed_confirmation_poc`, but not enough evidence for the Case 3 mechanism. |
| **Total failed_confirmation_poc zero-reward rows** | **`119`** | **`417,269.644210543`** | All failed-cPoC rows found in epochs `262..276`. |

The `24` broader suspicious rows are extracted into standalone candidate
`P3-CAND-06`:

```text
validations/P3-CAND-06-pre-fix-confirmation-accounting/
```

## Strict Case-3-Like Rows

Only one participant appears under the strict Case 3 signature, but it appears
in two epochs:

| Epoch | Participant | Exclusion height | Trigger height | Kimi submitted | Kimi validating weight | Max preserved Kimi weight | Amount interpretation, GONKA |
|---:|---|---:|---:|---:|---:|---:|---:|
| `265` | `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6` | `4,103,171` | `4,102,890` | `52,028` | `256,727` / `35.0324%` of cPoC #2 snapshot total | `189,884` / `21.0008%` diagnostic share of epoch reward/root total | `12,951.806895703` conditional chain-style counterfactual; `20,896.527179100` full-root upper bound |
| `267` | `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6` | `4,122,552` | `4,122,271` | `57,664` | `171,571` / `31.6894%` | `159,432` / `29.4473%` | `10,262.057515369` |

The strict signature requires:

1. `failed_confirmation_poc`;
2. zero epoch reward;
3. `ConfirmationPoCRatio < AlphaThreshold`;
4. Kimi submission exists;
5. Kimi validation weight is below the strict `>2/3` line;
6. Kimi preserved-node voting power is present.

## Broader Suspicious Rows

There are `24` rows where at least one submitted model reached `pass_weight`,
but the participant still received `failed_confirmation_poc` and zero reward.
These rows are not the same Kimi-shortfall signature, but they are relevant to
the broader `v0.2.13` confirmation-accounting fix and should not be silently
treated as ordinary no-submission cases.

| Epoch | Participant | Ratio | Qwen result | Kimi result | Loss, GONKA |
|---:|---|---:|---|---|---:|
| `263` | `gonka19cjm4c5mt3j3qdr8vhytmm4hef3pnkvkm0x7m2` | `2.7391%` | `no_submission` | `pass_weight` | `1,915.652591432` |
| `263` | `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` | `35.0447%` | `no_submission` | `pass_weight` | `1,953.032509538` |
| `263` | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | `14.7717%` | `pass_weight` | `no_submission` | `4,850.385431974` |
| `264` | `gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds` | `39.8189%` | `no_submission` | `pass_weight` | `1,970.264959744` |
| `264` | `gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d` | `49.2523%` | `no_submission` | `pass_weight` | `2,019.930762224` |
| `264` | `gonka14g78ez2zy08k8sssue483zmfpgd4qut8zcwlqc` | `6.0014%` | `no_submission` | `pass_weight` | `2,019.930762224` |
| `265` | `gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww` | `20.7038%` | `pass_weight` | `no_submission` | `335.927643572` |
| `268` | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `17.3837%` | `no_submission` | `pass_weight` | `25,309.087745610` |
| `269` | `gonka1007py6y2qfn2vaqrthqhtchkwx64hgzc6w544w` | `45.1393%` | `no_submission` | `pass_weight` | `2,228.595538500` |
| `269` | `gonka1naxyjmun6kl23htjdujwd6c5z5avgwapsrmfk3` | `45.8992%` | `pass_weight` | `no_submission` | `535.800580255` |
| `271` | `gonka16xa2sdc8qe2289nzr4e6vmdyzlke8g8fn8e75s` | `33.0943%` | `pass_weight` | `no_submission` | `139.200061369` |
| `272` | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `40.2573%` | `no_submission` | `pass_weight` | `22,521.036302544` |
| `272` | `gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p` | `19.0604%` | `pass_weight` | `no_submission` | `8,037.485696859` |
| `272` | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `28.7372%` | `pass_weight` | `no_submission` | `365.340258948` |
| `272` | `gonka1nku7u6d5mz80h35ty8ydeh0k5xydesvt9w0vjr` | `19.6229%` | `pass_weight` | `no_submission` | `146.964070171` |
| `273` | `gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx` | `31.5761%` | `pass_weight` | `no_submission` | `3,018.788733411` |
| `273` | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `49.0130%` | `pass_weight` | `no_submission` | `218.861247867` |
| `274` | `gonka1qwfrtz9c7kcrfkrrlne2pkcye74mj6ce33xdkl` | `30.4095%` | `pass_weight` | `no_submission` | `173.159717563` |
| `274` | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `29.0542%` | `pass_weight` | `no_submission` | `137.269776102` |
| `275` | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `33.4816%` | `pass_weight` | `no_submission` | `126.220428182` |
| `276` | `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e` | `16.9861%` | `pass_weight` | `no_submission` | `3,557.528990032` |
| `276` | `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | `35.2638%` | `pass_weight` | `pass_weight` | `17,356.095656742` |
| `276` | `gonka14tqh62mangwzrma2lgg2dm375rcjzn2ydy8ttm` | `37.1301%` | `no_submission` | `pass_weight` | `11,765.489995489` |
| `276` | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | `36.3655%` | `no_submission` | `pass_weight` | `10,120.274911440` |

## Interpretation

The answer depends on how narrow the definition is:

- strict Case 3 / Kimi shortfall: only
  `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6`, in epochs `265` and `267`;
- broader pre-fix confirmation-accounting suspicion: at least `24` additional
  rows need separate review;
- broad `failed_confirmation_poc`: `119` rows before the clean `v0.2.13`
  start.

The current Case 3 compensation package should not automatically include the
broader rows without a separate root-cause pass, because many have no submission
for one model or have a different model-side pattern.
