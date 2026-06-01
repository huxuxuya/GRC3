# P3-CAND-06 Validation: Pre-Fix Confirmation Accounting Candidates

This folder contains a standalone extraction of the broader suspicious rows
found while validating `P3-CAND-03`.

The source scan is:

```text
validations/P3-CAND-03-failed-cpoc-epoch-267/case3_neighbor_failed_cpoc_rows.csv
```

The rows were discovered by an independent archive LCD scan. The published Case
3 repository was not executed or imported.

## Why This Is Separate From Case 3

Strict Case 3 is a Kimi validation-shortfall case:

```text
Kimi submitted
Kimi validating weight below strict >2/3
Kimi preserved voting power present
failed_confirmation_poc
zero reward
```

This candidate is broader. It contains rows where a participant was excluded
with `failed_confirmation_poc`, had zero epoch reward, and at least one
submitted model reached `pass_weight`, but the final confirmation ratio was
still below alpha.

That means these rows may be related to the pre-`v0.2.13`
confirmation-accounting bug, but they are not automatically the same mechanism
as strict Case 3.

## Selection Rule

Included rows satisfy all of:

1. epoch in `262..276`;
2. exclusion reason is `failed_confirmation_poc`;
3. actual epoch reward is `0`;
4. `ConfirmationPoCRatio < AlphaThreshold`;
5. `qwen_result = pass_weight` or `kimi_result = pass_weight`;
6. not already classified as strict Case-3-like Kimi-shortfall.

Excluded from this candidate:

- strict Case 3 rows for `gonka1j7x6...` in epochs `265` and `267`;
- rows with no Qwen/Kimi submission on the selected cPoC event;
- rows where the only evidence is broad `failed_confirmation_poc` without a
  submitted model reaching `pass_weight`.

## Current Result

| Metric | Value |
|---|---:|
| Epoch range checked | `262..276` |
| Candidate rows | `24` |
| Unique participants | `19` |
| Estimated zero-reward loss | `120,822.324371792 GNK` |
| Epoch `276` rows | `4` |
| Epoch `276` estimated loss | `42,799.389553703 GNK` |

Distribution by epoch:

| Epoch | Rows |
|---:|---:|
| `263` | `3` |
| `264` | `3` |
| `265` | `1` |
| `268` | `1` |
| `269` | `2` |
| `271` | `1` |
| `272` | `4` |
| `273` | `2` |
| `274` | `2` |
| `275` | `1` |
| `276` | `4` |

## Candidate Rows

The full row list is in `candidate_rows.csv`.
The expanded per-participant timeline is in `participant_epoch_timeline.md`;
the machine-readable version is `participant_epoch_timeline.csv`.

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

## What Still Needs Review

- Confirm whether `pass_weight` on one model should have preserved enough
  confirmation capacity under the historical pre-fix formula.
- Reconcile each row against coefficient-adjusted `foldEventReadings`, not only
  raw model voting power.
- Check overlap with `P3-CAND-04` for epoch `276` so the same economic loss is
  not paid twice.
- Check overlap with `P4-CAND-01` Kimi restitution before assigning this
  candidate to a proposal.

## Related Artifacts

- `participant_epoch_timeline.md`
- `participant_epoch_timeline.csv`
- `candidate_rows.csv`
- `../P3-CAND-03-failed-cpoc-epoch-267/case3_neighbor_failed_cpoc_rows.csv`
- `../P3-CAND-03-failed-cpoc-epoch-267/case3_pre_fix_window_review.md`
- `../P3-CAND-03-failed-cpoc-epoch-267/case3_chain_formula_reconciliation.md`
- `../../cases/P3-CAND-06-pre-fix-confirmation-accounting.md`
