# Epoch 265 Chain Reward-State Table

Participant:

`gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6`

This note tracks chain reward state for epoch `265`. It intentionally separates
raw model PoC weights from the chain reward numerator. The main table below is
chain-state emulation only: if the epoch ended at each checkpoint, it shows the
stored participant status, the stored chain `confirmation_weight`, and the
reward that the chain formula would pay from that state.

## Fixed Constants

| Metric | Value |
|---|---:|
| Epoch | `265` |
| Reward/root total weight | `904,177` |
| Inferred fixed epoch reward, ngonka | `284,932,503,735,690` |
| Final cPoC stage | `4,102,890` |
| Final cPoC snapshot `TotalNetworkWeight` | `732,828` |
| Strict `>2/3` threshold at final cPoC | `488,553` |
| Alpha threshold | `0.5` |

## Participant Model Weights

Chain facts for epoch `265`:

- historical `confirmation_weight_scales` in both Kimi and Qwen
  `epoch_group_data` are empty (`[]`);
- the chain stores the participant/model-row `confirmation_weight` as `66,311`
  before the cPoC failure;
- that `66,311` is the chain reward/confirmation weight. It is not the raw
  Kimi `52,279` weight, and it must not be multiplied by another policy scale
  factor when calculating the normal chain payout.

| Field | Kimi | Qwen | Meaning |
|---|---:|---:|---|
| Raw model `weight` | `52,279` | `923` | Sum of participant node PoC weights for that model. Kimi nodes: `kimi30..kimi33`; Qwen node: `node1`. |
| Model `voting_power` | `66,311` | `66,311` | Voting power used when summing validator power for cPoC validation. |
| Model `confirmation_weight` before failure | `66,311` | `66,311` | Model row confirmation weight before the failed cPoC transition. |
| Full root/participant weight before exclusion | `66,311` | `66,311` | Full reward numerator if the whole participant row is restored. |
| Chain confirmation weight after exclusion | `323` | `323` | Stored participant weight after `failed_confirmation_poc` at block `4,103,171`. |
| External policy factor | not chain state | not chain state | No external Kimi-only factor is used in the chain-state table below. |

## cPoC Progression

The first two rows come from the existing epoch `265` timeline scan. The final
row is the archive-confirmed failure stage and uses the cPoC snapshot denominator
`732,828`.

| cPoC | Trigger height | Kimi submitted count | Kimi validating voting power | Kimi result | Qwen submitted count | Qwen validating voting power | Qwen result | Denominator used here | Strict `>2/3` threshold | Guardian result | Chain confirmation weight |
|---:|---:|---:|---:|---|---:|---:|---|---:|---:|---|---:|
| `0` | `4,095,682` | `43,360` | `677,518` | passes diagnostic | `960` | `509,938` | short by `92,847` diagnostic | `904,177` diagnostic | `602,785` diagnostic | not reconstructed in local raw cache | not finalized |
| `1` | `4,098,879` | `43,328` | `535,847` | short by `66,938` diagnostic | `960` | `406,730` | short by `196,055` diagnostic | `904,177` diagnostic | `602,785` diagnostic | not reconstructed in local raw cache | not finalized |
| `2` | `4,102,890` | `52,028` | `256,727` | short by `231,826` | `960` | `35,370` | short by `453,183` | `732,828` cPoC snapshot | `488,553` | Kimi: `1 valid / 1 invalid / 1 no_vote`, no guardian pass; Qwen: `2 valid / 0 invalid / 1 no_vote`, guardian pass | `66,311 -> 323` at block `4,103,171` |

## Chain Reward-State Emulation By Checkpoint

This table uses only chain-applicable state:

- raw model weight is shown only as context for Kimi/Qwen;
- chain `confirmation_weight` is the reward numerator while the participant is
  active;
- if the participant is `INACTIVE` because of `failed_confirmation_poc`, the
  actual chain payout is `0` even if a residual `confirmation_weight` remains.

The reward formula amount is shown as:

```text
floor(confirmation_weight * 284,932,503,735,690 / 904,177)
```

For checkpoints before the exclusion block, the participant is still `ACTIVE`,
so the payable amount equals the formula amount. After the exclusion block, the
stored residual weight `323` is useful for explaining the failure, but the actual
epoch reward is `0` because the participant is inactive/excluded.

Rows `cPoC 0` and `cPoC 1` are diagnostic because the local archive does not
contain the raw guardian/final-reading cache for those two intermediate stages.
The final chain-applied stage is `cPoC 2`.

| Checkpoint | Height | Status at checkpoint | Kimi raw model weight | Qwen raw model weight | Chain `confirmation_weight` / reward numerator | Formula reward from numerator, GONKA | Would chain pay if epoch ended here? | Notes |
|---|---:|---|---:|---:|---:|---:|---:|---|
| Epoch entry | before cPoC | `ACTIVE` | `52,279` | `923` | `66,311` | `20,896.527179100` | `20,896.527179100` | `52,279` is raw Kimi PoC weight, not the reward numerator. Chain reward uses `66,311`. |
| After `cPoC 0` trigger | `4,095,682` | `ACTIVE` | `52,279` | `923` | `66,311` | `20,896.527179100` | `20,896.527179100` | Kimi passes the diagnostic weight check; Qwen is short. For this participant, no chain failure is applied at this checkpoint. |
| After `cPoC 1` trigger | `4,098,879` | `ACTIVE` | `52,279` | `923` | `66,311` | `20,896.527179100` | `20,896.527179100` | Both model diagnostics are short, but this participant remains active; no reward-weight cut is stored yet. |
| After `cPoC 2` trigger, before exclusion | `4,102,890` to `4,103,170` | `ACTIVE` | `52,279` | `923` | `66,311` | `20,896.527179100` | `20,896.527179100` | Final cPoC failure window has started, but immediately before exclusion the stored chain weight is still `66,311`. |
| After `failed_confirmation_poc` is applied | `4,103,171` | `INACTIVE` | `52,279` | `923` | `323` residual | `101.786706260` if active | `0.000000000000` | Chain records `failed_confirmation_poc`; status becomes inactive, so actual epoch reward is zero. |

## Chain Formula Interpretations

| Interpretation | Reward numerator | Formula | Amount, GONKA | What it compensates |
|---|---:|---|---:|---|
| Active chain state before exclusion | `66,311` | `floor(66,311 * fixedEpochReward / 904,177)` | `20,896.527179100` | This is what the chain would pay if the epoch ended while the participant was still active. |
| Residual weight after failure, formula only | `323` | `floor(323 * fixedEpochReward / 904,177)` | `101.786706260` | This is not paid in the real chain state because the participant is already inactive. |
| Actual final epoch state | inactive/excluded | not payable | `0.000000000000` | The participant is `INACTIVE` with reason `failed_confirmation_poc`. |

## Conclusion

For chain-state emulation, there is no stage where the chain changes reward
weight from `52,279` to `40,777`. The chain-applicable reward numerator stays
`66,311` while the participant is active, then the participant becomes inactive
at block `4,103,171` and the actual payable reward becomes `0`.

Therefore, if the epoch had ended at any checkpoint before the exclusion block,
the chain-calculated reward would be `20,896.527179100 GONKA`. If it ends after
the exclusion is applied, the actual chain reward is `0`.
