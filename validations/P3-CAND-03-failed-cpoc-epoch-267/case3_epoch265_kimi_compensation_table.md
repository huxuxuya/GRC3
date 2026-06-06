# Epoch 265 Kimi Weight Compensation Table

Participant:

`gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6`

This note separates the epoch `265` Kimi-only compensation interpretation from
the full-root zero-reward upper bound.

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

| Field | Kimi | Qwen | Meaning |
|---|---:|---:|---|
| Raw model `weight` | `52,279` | `923` | Sum of participant node PoC weights for that model. Kimi nodes: `kimi30..kimi33`; Qwen node: `node1`. |
| Model `voting_power` | `66,311` | `66,311` | Voting power used when summing validator power for cPoC validation. |
| Model `confirmation_weight` before failure | `66,311` | `66,311` | Model row confirmation weight before the failed cPoC transition. |
| Full root/participant weight before exclusion | `66,311` | `66,311` | Full reward numerator if the whole participant row is restored. |
| Chain confirmation weight after exclusion | `323` | `323` | Stored participant weight after `failed_confirmation_poc` at block `4,103,171`. |
| Proposed scale factor for narrow model-only restitution | `0.780` | not used | Policy/input assumption used by the narrower Kimi-only counterfactual. |
| Scaled restored model weight | `40,777` | not restored | `floor(52,279 * 0.780)` for Kimi-only restitution. |
| Chain-style restored weight | `41,100` | not restored | `323 + 40,777`; keep measured residual and restore scaled Kimi. |

## cPoC Progression

The first two rows come from the existing epoch `265` timeline scan. The final
row is the archive-confirmed failure stage and uses the cPoC snapshot denominator
`732,828`.

| cPoC | Trigger height | Kimi submitted count | Kimi validating voting power | Kimi result | Qwen submitted count | Qwen validating voting power | Qwen result | Denominator used here | Strict `>2/3` threshold | Guardian result | Chain confirmation weight |
|---:|---:|---:|---:|---|---:|---:|---|---:|---:|---|---:|
| `0` | `4,095,682` | `43,360` | `677,518` | passes diagnostic | `960` | `509,938` | short by `92,847` diagnostic | `904,177` diagnostic | `602,785` diagnostic | not reconstructed in local raw cache | not finalized |
| `1` | `4,098,879` | `43,328` | `535,847` | short by `66,938` diagnostic | `960` | `406,730` | short by `196,055` diagnostic | `904,177` diagnostic | `602,785` diagnostic | not reconstructed in local raw cache | not finalized |
| `2` | `4,102,890` | `52,028` | `256,727` | short by `231,826` | `960` | `35,370` | short by `453,183` | `732,828` cPoC snapshot | `488,553` | Kimi: `1 valid / 1 invalid / 1 no_vote`, no guardian pass; Qwen: `2 valid / 0 invalid / 1 no_vote`, guardian pass | `66,311 -> 323` at block `4,103,171` |

## Reward-Weight Projection By Stage

This table separates three different layers:

- raw model weight: the participant's model-specific PoC weight entering the epoch;
- confirmed raw model weight: which model row would be treated as confirmed at that stage;
- reward numerator: the weight used in the epoch reward formula after applying the
  Kimi-only scale/residual interpretation. For Kimi-only restitution this is not
  the raw Kimi model weight; it is `floor(52,279 * 0.780) = 40,777`.

Rows `cPoC 0` and `cPoC 1` are diagnostic because the local archive does not
contain the raw guardian/final-reading cache for those two intermediate stages.
The final chain-applied stage is `cPoC 2`.

| Stage | Height | Kimi input raw weight | Qwen input raw weight | Kimi confirmed raw weight | Qwen confirmed raw weight | Kimi scaled reward numerator | Qwen/residual reward numerator | Total reward numerator | Calculated reward, GONKA | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Epoch entry, full-root view | before cPoC | `52,279` | `923` | not applicable | not applicable | not decomposed | not decomposed | `66,311` | `20,896.527179100` | Full active participant/root weight on epoch entry. This is the full-root upper bound, not Kimi-only. |
| Epoch entry, Kimi-only projection | before cPoC | `52,279` | `923` | `52,279` projected | not restored | `40,777` | `0` | `40,777` | `12,850.020189443` | Narrow model-only view at epoch entry: raw Kimi weight `52,279` is converted to the scaled reward numerator `floor(52,279 * 0.780) = 40,777`. |
| `cPoC 0` diagnostic | `4,095,682` | `52,279` | `923` | `52,279` | `0` by weight diagnostic | `40,777` | `0` | `40,777` | `12,850.020189443` | Kimi validating power clears the diagnostic threshold. `40,777` is not another cPoC weight; it is the scaled reward numerator from `floor(52,279 * 0.780)`. Qwen validating power is short. Guardian outcome was not reconstructed locally. |
| `cPoC 1` diagnostic | `4,098,879` | `52,279` | `923` | `0` by weight diagnostic | `0` by weight diagnostic | `0` | `0` | `0` | `0.000000000000` | Both Kimi and Qwen are short by voting-power diagnostic. Guardian outcome was not reconstructed locally. |
| `cPoC 2` chain-applied result | `4,102,890` | `52,279` | `923` | `0` | `923` by guardian pass | `0` | `323` | `323` | `101.786706260` | Kimi has voting shortfall and no guardian pass. Qwen has voting shortfall but `2 valid / 0 invalid / 1 no_vote`; chain stores residual confirmation weight `323` after exclusion. |
| `cPoC 2` Kimi-restored counterfactual | `4,102,890` | `52,279` | `923` | `52,279` restored | `923` retained by guardian pass | `40,777` | `323` | `41,100` | `12,951.806895703` | Narrow Kimi-only compensation view: keep the chain-observed residual and add scaled Kimi weight. |
| Full-row restore counterfactual | `4,102,890` | `52,279` | `923` | full participant row | full participant row | not decomposed | not decomposed | `66,311` | `20,896.527179100` | Broader policy view: restore the whole failed participant epoch row. This is not model-only compensation. |

## Compensation Interpretations

| Interpretation | Reward numerator | Formula | Amount, GONKA | What it compensates |
|---|---:|---|---:|---|
| Full-root restore | `66,311` | `floor(66,311 * fixedEpochReward / 904,177)` | `20,896.527179100` | Treats the whole participant epoch row as if it should have remained fully active. This includes more than the Kimi-only lost contribution. |
| Kimi-only restored contribution | `40,777` | `floor(40,777 * fixedEpochReward / 904,177)` | `12,850.020189443` | Restores only scaled Kimi weight using the proposed `0.780` factor. |
| Chain-style Kimi counterfactual | `41,100` | `floor((323 + 40,777) * fixedEpochReward / 904,177)` | `12,951.806895703` | Keeps the chain-observed residual `323` and adds scaled Kimi. This is the narrowest practical Kimi-only row-level payout if actual reward is zero. |
| Chain-observed residual only | `323` | `floor(323 * fixedEpochReward / 904,177)` | `101.786706260` | Not a restitution amount by itself; shown to explain the `41,100` counterfactual. |

## Conclusion

For epoch `265`, `20,896.527179100 GONKA` is a full-root upper bound, not a
Kimi-only amount.

If the policy is **Kimi-only restitution**, the cleaner chain-style number is
`12,951.806895703 GONKA` for this epoch, subject to accepting the `0.780` Kimi
scale factor. If the policy is **full failed-confirmation-poc row restoration**,
then `20,896.527179100 GONKA` is the corresponding full-root amount.
