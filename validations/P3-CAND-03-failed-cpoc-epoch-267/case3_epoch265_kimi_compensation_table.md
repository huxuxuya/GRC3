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

## Participant Kimi Weight

| Field | Value | Meaning |
|---|---:|---|
| Kimi raw model `weight` | `52,279` | Sum of participant Kimi node PoC weights: `kimi30..kimi33`. |
| Kimi `voting_power` | `66,311` | Voting power used when summing validator power for Kimi cPoC validation. |
| Kimi `confirmation_weight` | `66,311` | Model row confirmation weight before the failed cPoC transition. |
| Full root/participant weight before exclusion | `66,311` | Full reward numerator if the whole participant row is restored. |
| Chain confirmation weight after exclusion | `323` | Stored weight after `failed_confirmation_poc` at block `4,103,171`. |
| Proposed Kimi scale factor | `0.780` | Policy/input assumption used by the narrower Kimi-only counterfactual. |
| Scaled Kimi weight, floor(`52,279 * 0.780`) | `40,777` | Kimi-only restored contribution in reward scale. |
| Chain-style restored weight, `323 + 40,777` | `41,100` | Narrow counterfactual: keep measured non-Kimi residual and restore scaled Kimi. |

## cPoC Progression

The first two rows come from the existing epoch `265` timeline scan. The final
row is the archive-confirmed failure stage and uses the cPoC snapshot denominator
`732,828`.

| cPoC | Trigger height | Kimi submitted count | Kimi validating voting power | Denominator used here | Strict `>2/3` threshold | Weight result | Guardian result | Chain confirmation weight |
|---:|---:|---:|---:|---:|---:|---|---|---:|
| `0` | `4,095,682` | `43,360` | `677,518` | `904,177` diagnostic | `602,785` diagnostic | passes diagnostic | not reconstructed in local raw cache | not finalized |
| `1` | `4,098,879` | `43,328` | `535,847` | `904,177` diagnostic | `602,785` diagnostic | short by `66,938` diagnostic | not reconstructed in local raw cache | not finalized |
| `2` | `4,102,890` | `52,028` | `256,727` | `732,828` cPoC snapshot | `488,553` | short by `231,826` | `1 valid / 1 invalid / 1 no_vote`; no guardian pass | `66,311 -> 323` at block `4,103,171` |

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
