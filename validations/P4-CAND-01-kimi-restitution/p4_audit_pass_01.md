# P4 Conceptual Audit Pass 01

This pass starts closing the conceptual audit checklist using independently
saved raw node data. It does not run the investigator's scripts and does not
approve any payout amount.

Raw inputs for this pass are listed in
[`raw_chain_cache_manifest.md`](raw_chain_cache_manifest.md).

## Summary

| Area | Result |
|---|---|
| Raw data retention | Confirmed: all node responses fetched in this pass are stored under `raw_chain_cache/`. |
| e266 final-set absence for the nine DevOps-listed addresses | Confirmed from saved `epoch_group_data_266` and `epoch_performance_summary_266`: all nine are absent from final group and performance rows. |
| e266 PoC commit proof for the nine DevOps-listed addresses | Confirmed from archive CLI query at height `4120751`: all nine have PoC v2 store commits at stage start `4105361`. |
| e267/e275 `ComputeGroupCap` effect | Confirmed as a real chain-state pattern: Kimi model rows materially exceed root settlement group weights/confirmation-weight proportions. |
| Compensation eligibility | Not decided in this pass. |

## e266: Nine Listed Submitters

The DevOps evidence lists nine addresses as PoC submitters that did not enter
the final epoch `266` set. The saved final group/performance data confirms the
absence part of that statement:

| Address | PoC commit count | In `epoch_group_data_266` final group | In `epoch_performance_summary_266` |
|---|---:|---:|---:|
| `gonka125n6kr5gvdup0lndfkps7t6rd6592panhrg3np` | `6,048` | no | no |
| `gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d` | `6,080` | no | no |
| `gonka1c6fwzedfsmpu4jnjekv4cn7mvr7x7fuqd6uqt9` | `12,384` | no | no |
| `gonka1jrgm47v5eg876udmzg6j6glqcsd5x0vk6crpax` | `25,664` | no | no |
| `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `89,984` | no | no |
| `gonka1qa90tgczc0k5dvk4l5nvlf5y6phgm6mg22sfjv` | `55,552` | no | no |
| `gonka1wkgawwdzj623ss8eywayzdj6qcgr2llygactje` | `6,496` | no | no |
| `gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds` | `12,896` | no | no |
| `gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw` | `5,664` | no | no |

Interpretation:

- Confirmed: archive CLI query
  `all-poc-v2-store-commits 4105361 --height 4120751` returns `44` PoC commit
  rows and `41` unique submitters.
- Confirmed: all nine DevOps-listed addresses have positive PoC commit counts
  and are absent from the final epoch `266` group.
- Confirmed: these nine addresses are not present in saved epoch `266`
  performance rows.
- Current limitation: the CLI output contains `participant_address`, `count`,
  `root_hash`, and `hex_pub_key`, but not `model_id`. Therefore this pass
  confirms PoC commit submission and final-set absence; the "Kimi submitter"
  label still depends on DevOps/source context or a richer raw commit extract.

Derived files:

- `p4_e266_commit_final_group_check.csv`
- `p4_e266_commit_final_group_check.json`

## e267: Kimi Model Rows vs Root Settlement Rows

Saved raw files:

- `node1_epoch_group_data_267.json`
- `node1_epoch_group_data_267_model_kimi.json`

Observed values:

| Metric | Value |
|---|---:|
| Root epoch group rows | `51` |
| Root `total_weight` | `541,415` |
| Root summed `weight` | `541,415` |
| Root summed `confirmation_weight` | `948,169` |
| Kimi model rows | `27` |
| Kimi model-row `weight` sum | `658,820` |
| Kimi model-row `confirmation_weight` sum | `915,743` |
| Same-address root `weight` sum for Kimi rows | `334,289` |
| Same-address root `confirmation_weight` sum for Kimi rows | `738,372` |

Interpretation:

- Confirmed: Kimi model-specific rows in epoch `267` materially exceed the
  root settlement weights for the same participants.
- Confirmed: the cap/settlement state is not equivalent to raw Kimi model-row
  weight.
- Still policy/methodology: whether the difference should be compensated using
  the source repo's top-up formula or a full uncapped settlement replay.

## e275: Kimi Model Rows vs Root Epoch State

Saved raw files:

- `node1_epoch_group_data_275.json`
- `node1_epoch_group_data_275_model_kimi.json`

Observed values:

| Metric | Value |
|---|---:|
| Root epoch group rows | `55` |
| Root `total_weight` | `736,925` |
| Root summed `weight` | `736,925` |
| Root summed `confirmation_weight` | `945,908` |
| Kimi model rows | `24` |
| Kimi model-row `weight` sum | `589,904` |
| Kimi model-row `confirmation_weight` sum | `763,391` |

Interpretation:

- Confirmed: Kimi remains a dominant model group in epoch `275`, and
  model-row confirmation weight remains larger than the root epoch total
  weight.
- This supports the existence of a later Kimi cap/weight-pressure pattern.
- It does not by itself prove restitution eligibility.

## Checklist Updates From This Pass

| Checklist item | Updated status | Reason |
|---:|---|---|
| 7 | `Confirmed` | Archive CLI raw data confirms PoC commits for all nine listed addresses at stage `4105361`; final group/performance raw data confirms all nine are absent from the epoch `266` final set. |
| 12 | `Confirmed` | Saved root and Kimi model-group data for e267/e275 show the cap/weight-pressure pattern directly. |
| 14 | `Partially confirmed` | Confirmed work/weight pressure exists, but underpayment still depends on accepted counterfactual reward model. |
| 15 | `Policy required` | The top-up denominator remains a methodology choice, not a chain-only fact. |

## Next Checks

1. Add richer e266 commit evidence if available, ideally including `model_id`,
   to independently confirm the Kimi-specific part of the submitter claim.
2. Build an e265 row classifier separating strict Case 3-like cPoC failure
   from broader confirmation-weight-drop rows.
3. Build a P4 overlap matrix against Case 3, Case 4, Case 6, and prior payout
   records.
