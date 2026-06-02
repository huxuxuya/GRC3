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

Start with `case6_decision_summary.md` for the one-page conclusion and
`case6_evidence_ledger.md` for row-by-row evidence. The ledger combines each
candidate row's trigger/exclusion heights, Qwen/Kimi commit and validator
evidence, strict `2/3` threshold comparison, old-formula replay, bounded
v0.2.13-style replay, loss amount, technical status, overlap status, and
decision boundary.

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

## Root-Cause Replay

`case6_root_cause_replay.md` replays the `24` candidate rows against the
normalized archive-chain scan data and the strict chain threshold:

```text
validWeight > TotalNetworkWeight * 2 / 3
```

Current result:

| Check | Result |
|---|---:|
| Rows with at least one Qwen/Kimi `pass_weight` model and durable `failed_confirmation_poc` state | `24` |
| Rows with exactly one `pass_weight` model | `23` |
| Rows with both Qwen and Kimi `pass_weight` | `1` |
| Rows where simple `confirmation_weight_at_exclusion / confirmation_weight_before / 0.909` matches stored ratio | `18` |
| Rows where that simple ratio does not match stored ratio | `6` |
| Simple-ratio mismatch rows reconciled by full coefficient replay | `5` |
| Remaining mismatch after coefficient replay | `1` |

Classification:

| Classification | Rows | Interpretation |
|---|---:|---|
| `single_model_pass_expected_capacity_failed` | `18` | One model reached `pass_weight`; the stored ratio reconciles with the observed confirmation-weight reduction. |
| `single_model_pass_coefficient_replayed` | `5` | One model reached `pass_weight`; full replay matches the stored ratio once historical coefficients, time normalization, and preserved snapshots are used. |
| `strong_signal_but_epoch276_overlap` | `1` | Both Qwen and Kimi reached `pass_weight`, but the row is in epoch `276` and overlaps the `P3-CAND-04` review window. |

The strongest contradiction is epoch `276`
`gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09`: Qwen had `86.9859%`
valid weight, Kimi had `78.7207%` valid weight, yet the stored confirmation
ratio was only `35.2638%` and the participant received zero reward. This row
must still be reconciled with `P3-CAND-04` before any payout decision.

`case6_coefficient_replay.md` closes the `5` non-epoch-276 simple-ratio
mismatch rows. The apparent mismatch was from using the current
`ConfirmationWeight` as a diagnostic denominator, while the pre-fix chain
formula used full `preserved + notPreserved` expected weight. The same replay
does not reconcile the epoch `276` overlap row, so that row remains separate.

The likely fix family is PR
[`#1143`](https://github.com/gonka-ai/gonka/pull/1143) / `v0.2.13`, which
stores one epoch snapshot of confirmable models and weight-scale factors for
confirmation/reward calculations. PRs `#550` and `#826` remain treated as
unrelated settlement/claim-path fixes unless a direct confirmation-PoC code
link is found.

`case6_code_diff_root_cause.md` independently reviews the `v0.2.13` source diff
against its parent commit. It confirms that PR `#1143` added the
`ConfirmationWeightScales` epoch snapshot and then used the same snapshot for:

- initial epoch-member confirmation weight;
- cPoC measured and preserved weight;
- Bitcoin reward rescaling.

The code-diff review strengthens the root-cause finding: the current evidence
matches a pre-fix confirmation-accounting mismatch, not a simple absence of
submissions or validator weight for the passing model. It does not by itself
approve all `24` rows for payout; eligibility and overlap review remain
separate.

## Submission And Validator Evidence

`case6_submission_validator_evidence.md` fetches raw cPoC stage data for the
candidate loss triggers:

- `/productscience/inference/inference/all_poc_v2_store_commits/{trigger}`;
- `/productscience/inference/inference/poc_v2_validations_for_stage/{trigger}`;
- model-specific `epoch_group_data` for Qwen/Kimi voting power.

Result:

| Check | Result |
|---|---:|
| Unique loss trigger heights fetched | `16` |
| Submission-evidence raw endpoint files | `54` |
| Full validation raw cache files after formula/new/timeline/post-upgrade replay | `349` |
| Full validation raw cache size | `17.6 MB` |
| Model rows reconstructed | `48` |
| Model rows matching previous aggregate CSV | `48` |
| Model rows with cPoC store commit/submission | `25` |
| Model rows with strict `pass_weight` | `25` |
| Candidate rows with at least one passing model | `24` |

This confirms that submissions and enough validator weight existed for the
passing model in every candidate row. The current evidence does not expose every
individual off-chain nonce/payload body; it proves commit counts/root hashes,
validator rows, valid validator counts, and valid validator voting weight from
the chain's cPoC stage endpoints.

## Full Formula And Eligibility Review

`case6_full_old_formula_replay.md` replays all `24` rows with historical
params, cPoC time normalization, preserved snapshots, MLNode distributions, and
raw submission evidence.

| Check | Result |
|---|---:|
| Rows replayed through old formula | `24` |
| Rows matching stored ratio | `22` |
| Rows still below alpha in bounded v0.2.13-style replay | `24` |
| Rows that would pass alpha in bounded v0.2.13-style replay | `0` |

The bounded v0.2.13-style replay is intentionally limited to the Qwen/Kimi data
available in this case folder. It does not prove the exact post-upgrade state,
but it shows that the available Qwen/Kimi evidence does not automatically rescue
the single-model rows. This strengthens the decision boundary: most rows are
technically reproducible but still require a policy decision on whether
single-model service is compensable.

`case6_eligibility_matrix.md` classifies:

| Technical status | Rows |
|---|---:|
| `formula_reconciled_policy_required` | `20` |
| `blocked_epoch276_overlap` | `4` |

`case6_overlap_matrix.md` classifies duplicate-payment risk:

| Overlap status | Rows |
|---|---:|
| `no_known_overlap_in_local_repo` | `6` |
| `p4_cand_01_epoch_range_overlap` | `14` |
| `p3_cand_04_epoch_overlap_unresolved` | `3` |
| `known_p3_cand_04_same_address` | `1` |

`case6_evidence_ledger.md` provides the combined audit table. Its action split
is:

| Action | Rows | Estimated loss, GONKA |
|---|---:|---:|
| `clear` | `6` | `14,729.197017136` |
| `review` | `14` | `63,293.737800953` |
| `blocked` | `4` | `42,799.389553703` |

## Epoch And Upgrade Timeline

`case6_epoch_upgrade_timeline.md` records block-header timestamps for epoch
`263..277` boundaries and the on-chain `v0.2.13` upgrade point.

| Item | Height | UTC | MSK |
|---|---:|---|---|
| Epoch `276` PoC start | `4,259,271` | `2026-05-26 02:59:12 UTC` | `2026-05-26 05:59:12 MSK` |
| Epoch `276` effective start | `4,259,671` | `2026-05-26 03:34:34 UTC` | `2026-05-26 06:34:34 MSK` |
| `v0.2.13` applied on-chain | `4,267,300` | `2026-05-26 14:39:41 UTC` | `2026-05-26 17:39:41 MSK` |
| Epoch `277` effective start | `4,275,062` | `2026-05-27 02:12:33 UTC` | `2026-05-27 05:12:33 MSK` |

Interpretation: epochs `263..275` are pre-upgrade, epoch `276` contains the
upgrade application point, and epoch `277` is the first clean start after
`v0.2.13`.

## Post-v0.2.13 Regression Scan

`case6_post_upgrade_regression_scan.md` checks the accessible post-upgrade
epochs `277..283` for recurrence of the broad P3-CAND-06 signal:

```text
failed_confirmation_poc
zero reward
ConfirmationPoCRatio < AlphaThreshold
at least one tracked Qwen/Kimi model has strict pass_weight
```

Current result:

| Check | Result |
|---|---:|
| Epochs checked | `277..283` |
| failed_confirmation_poc rows | `50` |
| Rows matching the broad pass-weight-but-failed-ratio signal | `8` |
| Rows where exactly one tracked model passed | `8` |
| Rows where both tracked models passed | `0` |

Interpretation: the broad signal does appear after the clean `v0.2.13` start,
but every post-upgrade hit is a single-model-pass row where the other tracked
model has `no_submission`. This does not by itself prove that the pre-`v0.2.13`
root cause still exists; it strengthens the existing decision boundary that
single-model rows need a policy/formula eligibility review. No post-upgrade row
in `277..283` reproduced the stronger epoch `276` contradiction where both
tracked models passed but the stored confirmation ratio still failed.

## Gross Compensation Calculation

`case6_gross_compensation_calculation.md` is the common calculation table for
all `24` rows before overlap review. It includes every candidate row in the
gross sum and keeps overlap status only as a reference column.

| Gross calculation metric | Value |
|---|---:|
| Rows included | `24` |
| Unique participants | `19` |
| Gross compensation before overlap review | `120,822.324371792 GONKA` |

The generated machine-readable tables are:

- `case6_gross_compensation_calculation.csv`
- `case6_gross_compensation_calculation.json`
- `case6_gross_compensation_by_epoch.csv`
- `case6_gross_compensation_by_participant.csv`
- `case6_gross_compensation_by_pass_models.csv`
- `case6_gross_compensation_by_overlap_reference.csv`

## Candidate Rows

The full row list is in `candidate_rows.csv`.
The expanded per-participant timeline is in `participant_epoch_timeline.md`;
the machine-readable version is `participant_epoch_timeline.csv`.
The grouped participant -> epoch -> cPoC view is in
`participant_grouped_cpoc_timeline.md`; the machine-readable version is
`participant_grouped_cpoc_timeline.csv`.

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

- Reconcile all `4` epoch `276` rows against `P3-CAND-04` /
  upgrade-protection evidence.
- Decide whether the `20` formula-reconciled non-epoch-276 single-model rows
  are protocol-bug compensation rows or ordinary incomplete multi-model service
  rows.
- Check overlap with `P3-CAND-04` for epoch `276` so the same economic loss is
  not paid twice.
- Check overlap with `P4-CAND-01` Kimi restitution before assigning this
  candidate to a proposal.

## Related Artifacts

- `participant_epoch_timeline.md`
- `participant_epoch_timeline.csv`
- `participant_grouped_cpoc_timeline.md`
- `participant_grouped_cpoc_timeline.csv`
- `case6_decision_summary.md`
- `case6_evidence_ledger.md`
- `case6_evidence_ledger.csv`
- `case6_evidence_ledger.json`
- `case6_gross_compensation_calculation.md`
- `case6_gross_compensation_calculation.csv`
- `case6_gross_compensation_calculation.json`
- `case6_gross_compensation_by_epoch.csv`
- `case6_gross_compensation_by_participant.csv`
- `case6_gross_compensation_by_pass_models.csv`
- `case6_gross_compensation_by_overlap_reference.csv`
- `case6_epoch_upgrade_timeline.md`
- `case6_epoch_upgrade_timeline.csv`
- `case6_epoch_upgrade_timeline.json`
- `case6_post_upgrade_regression_scan.md`
- `case6_post_upgrade_regression_scan.json`
- `case6_post_upgrade_epoch_summary.csv`
- `case6_post_upgrade_failed_cpoc_rows.csv`
- `case6_root_cause_replay.md`
- `case6_row_formula_replay.csv`
- `case6_row_formula_replay.json`
- `case6_overlap_review.md`
- `case6_submission_validator_evidence.md`
- `case6_submission_validator_evidence.csv`
- `case6_submission_validator_evidence.json`
- `case6_stage_fetch_summary.csv`
- `case6_fix_review.md`
- `case6_code_diff_root_cause.md`
- `case6_coefficient_replay.md`
- `case6_coefficient_replay.csv`
- `case6_coefficient_replay.json`
- `case6_full_old_formula_replay.md`
- `case6_full_old_formula_replay.csv`
- `case6_full_old_formula_replay.json`
- `case6_new_algorithm_replay.md`
- `case6_new_algorithm_replay.csv`
- `case6_new_algorithm_replay.json`
- `case6_eligibility_matrix.md`
- `case6_eligibility_matrix.csv`
- `case6_eligibility_matrix.json`
- `case6_overlap_matrix.md`
- `case6_overlap_matrix.csv`
- `case6_overlap_matrix.json`
- `case6_epoch276_overlap_deep_dive.md`
- `case6_raw_data_manifest.md`
- `case6_raw_data_manifest.csv`
- `case6_raw_data_manifest.json`
- `build_case6_root_cause_replay.py`
- `build_case6_submission_evidence.py`
- `build_case6_coefficient_replay.py`
- `build_case6_full_old_formula_replay.py`
- `build_case6_new_algorithm_replay.py`
- `build_case6_eligibility_matrix.py`
- `build_case6_overlap_matrix.py`
- `build_case6_raw_manifest.py`
- `build_case6_evidence_ledger.py`
- `build_case6_compensation_calculation.py`
- `build_case6_epoch_upgrade_timeline.py`
- `build_case6_post_upgrade_regression_scan.py`
- `build_grouped_timeline.py`
- `candidate_rows.csv`
- `raw_stage_cache/`
- `../P3-CAND-03-failed-cpoc-epoch-267/case3_neighbor_failed_cpoc_rows.csv`
- `../P3-CAND-03-failed-cpoc-epoch-267/case3_pre_fix_window_review.md`
- `../P3-CAND-03-failed-cpoc-epoch-267/case3_chain_formula_reconciliation.md`
- `../../cases/P3-CAND-06-pre-fix-confirmation-accounting.md`
