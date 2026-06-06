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
| e266 nonce-submission proof | Blocked on current `node1` LCD: current commit endpoint returns empty commits, and historical-height queries return a state-load error. |
| e267/e275 `ComputeGroupCap` effect | Confirmed as a real chain-state pattern: Kimi model rows materially exceed root settlement group weights/confirmation-weight proportions. |
| Compensation eligibility | Not decided in this pass. |

## e266: Nine Listed Submitters

The DevOps evidence lists nine addresses as PoC submitters that did not enter
the final epoch `266` set. The saved final group/performance data confirms the
absence part of that statement:

| Address | In `epoch_group_data_266` final group | In `epoch_performance_summary_266` |
|---|---:|---:|
| `gonka125n6kr5gvdup0lndfkps7t6rd6592panhrg3np` | no | no |
| `gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d` | no | no |
| `gonka1c6fwzedfsmpu4jnjekv4cn7mvr7x7fuqd6uqt9` | no | no |
| `gonka1jrgm47v5eg876udmzg6j6glqcsd5x0vk6crpax` | no | no |
| `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | no | no |
| `gonka1qa90tgczc0k5dvk4l5nvlf5y6phgm6mg22sfjv` | no | no |
| `gonka1wkgawwdzj623ss8eywayzdj6qcgr2llygactje` | no | no |
| `gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds` | no | no |
| `gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw` | no | no |

Interpretation:

- Confirmed: these nine addresses are not present in the saved final epoch
  `266` group and not present in saved epoch `266` performance rows.
- Not confirmed yet from our node data: that these nine submitted Kimi PoC
  nonces at epoch start `4105361`.
- Current blocker: `node1_all_poc_v2_store_commits_4105361.json` has an empty
  `commits` array, and the historical-height version returns a state-load
  error. This looks like endpoint/history availability, not a substantive
  disproof of the claim.

Next action: add an archive raw source for
`all_poc_v2_store_commits/4105361` at epoch-end height `4120751`, then compare
commit submitters against the final group.

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
| 7 | `Partially confirmed` | Final-set absence is confirmed for the nine listed addresses; nonce-submission proof remains blocked pending archive commit data. |
| 12 | `Confirmed` | Saved root and Kimi model-group data for e267/e275 show the cap/weight-pressure pattern directly. |
| 14 | `Partially confirmed` | Confirmed work/weight pressure exists, but underpayment still depends on accepted counterfactual reward model. |
| 15 | `Policy required` | The top-up denominator remains a methodology choice, not a chain-only fact. |

## Next Checks

1. Obtain archive raw data for epoch `266` PoC commits at start height
   `4105361` and epoch-end height `4120751`.
2. Build an address-level e266 commit-vs-final-group table from saved raw data.
3. Build an e265 row classifier separating strict Case 3-like cPoC failure
   from broader confirmation-weight-drop rows.
4. Build a P4 overlap matrix against Case 3, Case 4, Case 6, and prior payout
   records.
