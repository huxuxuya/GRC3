# P3-CAND-01: High Miss Rate / Devshard Issue

| Field | Value |
|---|---|
| Proposal | Proposal #3 candidate |
| Epochs | 269-272; main reported incident: 272 |
| Status | Investigation |
| Reported by | Votkon; technical reports by Nik |
| Affected / detail contact | Six epoch 272 addresses identified below; Nik; claimant `A` |
| Investigated by | Fedor Tmkhv; shard-proof audit outputs |
| Result so far | On-chain reward outcomes identified; protocol bug not established |
| Further analysis | Required: retained devshard proof/stat data and root-cause determination |
| Compensation | Not approved; preliminary estimates only |
| Lost reward destination | Under fixed-reward settlement logic, downtime / miss-rate reductions remain undistributed and are transferred to governance rather than redistributed to other participants. |

## Message Log

| Date | Author | Fact / short quote | Meaning |
|---|---|---|---|
| 2026-05-23 13:12 UTC+03 | Votkon | "another potential case... add it to proposal #3" | Case proposed for Proposal #3 review. |
| 2026-05-24 00:12 UTC+03 | Fedor Tmkhv | Estimated losses across epochs 269-272 by failure category. | Preliminary magnitude only; not an approved calculation. |
| 2026-05-24 00:14 UTC+03 | Fedor Tmkhv | "I don't know the true cause" | Root cause was unresolved. |
| 2026-05-24 07:10 UTC+03 | Nik | Reported abnormal miss rate and a long-input validation error example. | Operator-level evidence and investigation hypothesis. |
| 2026-05-23 11:53 UTC+03 | Nik, DevOps chat | Reported six epoch 272 addresses that received `work_coins` but no `reward_coins`; updated cause as high miss rate. | Direct address-level evidence for the reported incident. |
| 2026-05-23 12:02 UTC+03 | `A`, DevOps chat | Reported that their address was in the list and that there were no outages. | Claimant statement; does not establish protocol liability. |

## Findings

- An audit of epochs 269-272 found several epoch 272 participants with work/signatures but zero rewards through the downtime/binomial-test outcome.
- The audit does not establish incorrect protocol behaviour.
- Devshard-level retained data is required before compensation eligibility can be determined.
- DevOps evidence identifies these epoch 272 addresses: `gonka1wt8sr9jxzpec65j7zkxsgh6edk3m6r8nlf5za4`, `gonka10079cnl3nuh2k82mhkm04dj0slhtw9kmjewwau`, `gonka1007g0ut3u4wjkay9hegqfev4pj90qgexwskmcw`, `gonka1007dchuqgdnute4qam70kmn56j2vfw38mhyrqv`, `gonka15munkmx6x7k6rqqeexjet4556p7at39ks9qgr5`, and `gonka1ce02jjduga8jvwj8jx39mxn0jr345vgkx7lk2n`.

## Mitigation / Fix Status

| Item | Status |
|---|---|
| Related code changes | PR [`#1143`](https://github.com/gonka-ai/gonka/pull/1143) includes devshard storage, stats and settlement-limit changes in `v0.2.13`. |
| Case-specific remediation | Not confirmed. The available evidence does not identify a code change that fixes the cause of this high miss-rate outcome. |
| Timing | `v0.2.13` is reported deployed on mainnet on 2026-05-26; a root-cause fix schedule for this case is unknown. |

## Reward Flow

The report concerns epoch 272 participants with `rewarded_coins = 0`. Gonka fixed-reward settlement keeps pre-punishment weight in the denominator; downtime reductions are therefore undistributed remainder sent to the governance module, rather than additional rewards for other participants.

## Sources

- [Audit/calculation repository](https://github.com/huxuxuya/gonka_248_and_250_-epoch_loss/)
- [DevOps chat evidence log](sources/P3-CAND-01-devops-chat.md)
- [PR #1143: v0.2.13 microrelease](https://github.com/gonka-ai/gonka/pull/1143)
- [Settlement logic: `accountsettle.go`](https://github.com/gonka-ai/gonka/blob/17808620293b57112896bcbb7f99c4c2f554d6c8/inference-chain/x/inference/keeper/accountsettle.go)
- [Reward remainder logic: `bitcoin_rewards.go`](https://github.com/gonka-ai/gonka/blob/17808620293b57112896bcbb7f99c4c2f554d6c8/inference-chain/x/inference/keeper/bitcoin_rewards.go)
