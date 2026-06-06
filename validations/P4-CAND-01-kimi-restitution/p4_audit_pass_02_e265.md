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
| `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` | `13,490` | `7,031` | `0` | yes, `failed_confirmation_poc` at `4,103,171` | `0` | broader failed-confirmation candidate | `needs_row_level_cpoc_model_proof` |

## Interpretation

- The `gonka1j7...` row matches the Case 3 extension already reviewed:
  epoch `265`, same participant as epoch `267`, zero reward, exclusion reason
  `failed_confirmation_poc`, and the same Kimi cPoC shortfall class.
- The `gonka17...` row is not a direct zero-reward cPoC victim in this pass.
  It had a confirmation-weight drop, but it was not excluded and it received
  `54,393.492283376 GONKA`. This row is broader policy territory, not strict
  Case 3.
- The `gonka1830...` row is a real zero-reward `failed_confirmation_poc`
  candidate, but this pass does not yet prove that it is the same Kimi cPoC
  validation-shortfall class. It needs row-level cPoC submission and validator
  evidence before being accepted as a direct Kimi restitution victim.

## Checklist Updates From This Pass

| Checklist item | Updated status | Reason |
|---:|---|---|
| 3 | `Confirmed` | The `gonka1j7...` epoch `265` row is confirmed as the Case 3-like direct cPoC shortfall row. |
| 4 | `Partially confirmed` | One additional e265 row is a real zero-reward failed-confirmation candidate; the other is a rewarded confirmation-weight-drop row. Neither is yet proven as strict Case-3-like Kimi restitution. |
| 5 | `Partially confirmed` | Chain state confirms the cW drops and exclusions, but attack causality still depends on operational evidence. |

## Next Checks

1. Pull cPoC submission/validator evidence for `gonka1830...` at epoch `265`
   before classifying it as direct Kimi restitution.
2. Decide whether rewarded confirmation-weight-drop rows like `gonka17...`
   are eligible for any P4 policy track.
3. Keep `gonka1j7...` in the Case 3 extension path to avoid duplicate P4/Case
   3 treatment.
