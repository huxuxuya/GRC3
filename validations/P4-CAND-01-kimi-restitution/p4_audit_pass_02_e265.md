# P4 Conceptual Audit Pass 02: Epoch 265 Row Classifier

This pass classifies the three epoch `265` rows included by the Votkon P4
repository. It uses independently saved archive-chain raw data and does not
approve compensation amounts.

Raw inputs are stored in `raw_chain_cache/`:

- `archive_cli_height_4103170_epoch_group_data_265_stdout.json`
- `archive_cli_height_4105360_epoch_group_data_265_stdout.json`
- `archive_cli_height_4103170_epoch_group_data_265_model_kimi_stdout.json`
- `archive_cli_height_4105360_epoch_group_data_265_model_kimi_stdout.json`
- `archive_cli_epoch265_performance_*_stdout.json`
- `archive_cli_excluded_participants_265_stdout_retry1.json`

Derived table:

- `p4_e265_row_classifier.csv`

## Result

| Address | Weight | Healthy cW | End cW | Excluded | Rewarded coins | Classification | Status |
|---|---:|---:|---:|---|---:|---|---|
| `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6` | `66,311` | `66,311` | `323` | yes, `failed_confirmation_poc` at `4,103,171` | `0` | strict Case-3-like direct cPoC shortfall | `confirmed` |
| `gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu` | `189,884` | `186,719` | `172,607` | no | `54,393,492,283,376` | broader confirmation-weight drop | `policy_required` |
| `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` | `13,490` | `7,031` | `0` | yes, `failed_confirmation_poc` at `4,103,171` | `0` | zero-reward failed confirmation with no cPoC submission at final checked stage | `not_confirmed_as_direct_kimi_shortfall` |

## Interpretation

- The `gonka1j7...` row matches the Case 3 extension already reviewed:
  epoch `265`, same participant as epoch `267`, zero reward, exclusion reason
  `failed_confirmation_poc`, and the same Kimi cPoC shortfall class.
- The `gonka17...` row is not a direct zero-reward cPoC victim in this pass.
  It had a confirmation-weight drop, but it was not excluded and it received
  `54,393.492283376 GONKA`. This row is broader policy territory, not strict
  Case 3.
- Follow-up pass 03 checked `gonka1830...` at cPoC stage `4102890`. It has
  Kimi model voting power `13,490` and appears in the Kimi model group, but it
  has zero raw commit rows and zero validation records for both Kimi and Qwen
  on that final checked stage. This is not confirmed as the same direct Kimi
  cPoC shortfall class as `gonka1j7...`.

## Checklist Updates From This Pass

| Checklist item | Updated status | Reason |
|---:|---|---|
| 3 | `Confirmed` | The `gonka1j7...` epoch `265` row is confirmed as the Case 3-like direct cPoC shortfall row. |
| 4 | `Not confirmed` | `gonka1830...` is a real zero-reward failed-confirmation row, but pass 03 does not confirm it as a direct Kimi cPoC shortfall; `gonka17...` is a rewarded confirmation-weight-drop row. |
| 5 | `Partially confirmed` | Chain state confirms the cW drops and exclusions, but attack causality still depends on operational evidence. |

## Next Checks

1. Decide whether zero-reward no-submission failed-confirmation rows like
   `gonka1830...` are eligible under a broader policy track.
2. Decide whether rewarded confirmation-weight-drop rows like `gonka17...`
   are eligible for any P4 policy track.
3. Keep `gonka1j7...` in the Case 3 extension path to avoid duplicate P4/Case
   3 treatment.
