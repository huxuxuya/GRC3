# P3-CAND-04: UpgradeProtectionWindow / CPoC Misfire

| Field | Value |
|---|---|
| Proposal | Proposal #3 candidate |
| Epochs | 276 |
| Status | Calculated; inclusion pending |
| Reported by | Votkon; calculation by Evgenii Maksimenkov |
| Affected / detail contact | 19 miners; Evgenii Maksimenkov; Vas Ily for `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` |
| Case investigator | @maksimenkoff; calculation: [gonkavip/payout276](https://github.com/gonkavip/payout276) |
| Case validators | @votkon; @OpenMindedPerson |
| Result so far | Calculation published and reproduced once; DevOps discussion confirms unintended cPoC behaviour |
| Further analysis | Required: independent validation and inclusion decision |
| Compensation | 36,209.451 GNK |
| Lost reward destination | Confirmation-weight share lost through unintended cPoC is not redistributed; under fixed-reward settlement it is transferred to governance remainder. |

## Message Log

| Date | Author | Fact / short quote | Meaning |
|---|---|---|---|
| 2026-05-26 21:54 UTC+03 | Votkon | `LastUpgradeHeight` was not recorded after v0.2.13. | Stated root cause for unintended cPoC execution. |
| 2026-05-27 06:18 UTC+03 | Evgenii Maksimenkov | "7 participants were affected and dropped out" | Initial dropped-participant scope. |
| 2026-05-27 10:12 UTC+03 | Evgenii Maksimenkov | Published the calculation script and total. | Calculation available for review. |
| 2026-05-27 12:09 UTC+03 | Nik | Script ran without errors and amount matched. | One reproduction reported. |
| 2026-05-26 18:52-18:57 UTC+03 | Arturs Plisko; Evgenii Maksimenkov; Gleb Morgachev, DevOps chat | cPoC happened although it was not expected; five participants dropped after the latest cPoC. | Contemporaneous technical confirmation. |
| 2026-05-26 21:49 UTC+03 | Egor, DevOps chat | `LastUpgradeHeight` was not written after `v0.2.13`, so the recent-upgrade cPoC skip did not apply. | Root-cause statement with chain-check commands. |

## Findings

- Published calculation includes `7` dropped miners and `12` miners with reduced confirmation weight.
- Total calculated payout: `36,209.451 GNK`.
- Inputs are archive-node snapshots at fixed historical block heights.
- DevOps chat identifies one affected address, `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09`, with reported `53.21%` confirmation ratio before dropping from the epoch.

## Mitigation / Fix Status

| Item | Status |
|---|---|
| Intended mitigation | PR [`#1143`](https://github.com/gonka-ai/gonka/pull/1143) intended to skip confirmation PoC from the upgrade height through the end of the upgrade epoch using `UpgradeProtectionWindow`. |
| Failure of mitigation | DevOps evidence states that after `v0.2.13`, `LastUpgradeHeight` was not recorded, so the skip did not apply and cPoC ran using stale scales. |
| Corrective fix | No public Gonka PR or issue specifically correcting the `LastUpgradeHeight` misfire was identified in the reviewed sources as of 2026-05-27. |
| Timing | Unknown. The affected upgrade itself was already live when this incident occurred. |

## Reward Flow

The calculation reports `7` dropped participants receiving zero reward and `12` participants receiving reduced reward because their confirmation weight fell. Gonka settlement explicitly keeps the unreduced weight in the denominator and routes cPoC-reduced undistributed rewards to governance rather than redistributing them.

## Sources

- [Calculation repository](https://github.com/gonkavip/payout276)
- [Upgrade proposal #54](https://gonka.gg/network/proposals/54)
- [DevOps chat evidence log](sources/P3-CAND-04-devops-chat.md)
- [PR #1143: v0.2.13 microrelease](https://github.com/gonka-ai/gonka/pull/1143)
- [Settlement logic: `accountsettle.go`](https://github.com/gonka-ai/gonka/blob/17808620293b57112896bcbb7f99c4c2f554d6c8/inference-chain/x/inference/keeper/accountsettle.go)
- [Reward remainder logic: `bitcoin_rewards.go`](https://github.com/gonka-ai/gonka/blob/17808620293b57112896bcbb7f99c4c2f554d6c8/inference-chain/x/inference/keeper/bitcoin_rewards.go)
