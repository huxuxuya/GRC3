# P4-CAND-01: Kimi Restitution, Epochs 265-276

| Field | Value |
|---|---|
| **Case** | `P4-CAND-01` - Kimi Restitution |
| Proposal | Proposal #3 candidate |
| Epochs affected | 265-276 |
| Affected participants | 52 unique addresses |
| Estimated compensation | 710,772.72 GNK |
| **Cause and evidence** | CPoC degradation in epoch 265, nonce/delegation losses in epoch 266, and ComputeGroupCap underpayment in epochs 267-276. Evidence: [calculation repository](https://github.com/votkon/gonka-kimi-restitution) and [DevOps chat log](sources/P4-CAND-01-devops-chat.md). |
| **Can it happen again?** | Reduced risk after `v0.2.13`; `ComputeGroupCap` still exists as an intended protocol rule, so recurrence risk should be reviewed. |
| **Mitigation / fix** | Partially mitigated by PR [#1143](https://github.com/gonka-ai/gonka/pull/1143) in `v0.2.13`: confirmation PoC weight loss during new-model bootstrap was fixed, and Kimi `WeightScaleFactor` was recalibrated to `0.78`. |
| **Compensation overlap** | Overlaps epoch 276 with the separate UpgradeProtectionWindow / CPoC misfire case; validators must ensure no duplicate compensation for the same economic loss. |
| **Current decision** | Calculated; GRC must decide eligibility and Proposal #3 inclusion. |
| **Review focus** | Investigator: @votkon. Validators: @maksimenkoff and @mikenosov. Also check overlap with the separate epoch 276 CPoC-misfire candidate. |

## Message Log

| Date | Author | Fact / short quote | Meaning |
|---|---|---|---|
| 2026-05-24 09:02 UTC+03 | Votkon | Kimi issue was initially listed for Proposal #3 work. | Earlier planning context. |
| 2026-05-27 17:03 UTC+03 | Votkon | Clarified period as epochs 265-276. | Calculation scope. |
| 2026-05-27 17:50 UTC+03 | Votkon | Proposed voting whether to include the case in Proposal #4. | Earlier proposal-positioning and eligibility context. |
| 2026-05-27 18:04 UTC+03 | Votkon | "We'd probably need 3-5 validations." | Review requirement due to amount. |
| 2026-05-17 00:56 UTC+03 | Evgenii Maksimenkov, DevOps chat | Identified 9 PoC submitters that did not enter the epoch 266 final set. | Address-level evidence for nonce exclusion. |
| 2026-05-17 22:30 UTC+03 | David Liberman, DevOps chat | Identified `ComputeGroupCap` and its `75%` cap as the cause of reduced Kimi weight. | Protocol-rule evidence for later Kimi weight reduction. |
| 2026-05-25 13:52 UTC+03 | Evgenii Maksimenkov, DevOps chat | Calculated an epoch 275 Kimi scale of approximately `0.659`. | Independent contemporaneous explanation of cap effect. |

## Findings

- The published package covers epoch 265 CPoC degradation, epoch 266 nonce/delegation losses, and epochs 267-276 ComputeGroupCap underpayment.
- It reports `52` unique affected addresses and `710,772.72 GNK`.
- Eligibility remains unresolved because the underlying event involved a third-party attack.
- Any approval must check overlap with the separate epoch 276 CPoC-misfire candidate.
- DevOps evidence includes named addresses and publicly described methods for recovering PoC/validation evidence.

## Mitigation / Fix Status

| Item | Status |
|---|---|
| Chain mitigation | PR [`#1143`](https://github.com/gonka-ai/gonka/pull/1143) fixes confirmation PoC weight loss during new-model bootstrap and recalibrates the Kimi `WeightScaleFactor` to `0.78`. |
| Protocol rule distinction | The PR does not remove `ComputeGroupCap`; the `75%` cap discussed in the evidence remains an intended protocol rule. The recalibration limits the circumstances producing a Kimi cap breach. |
| Deployment timing | DevOps announcement reports that `v0.2.13` executed on mainnet at block `4267300` on 2026-05-26. |
| Remaining status | Historical restitution and eligibility still require review; the mitigation does not approve or calculate compensation by itself. |

## Reward Flow

The restitution package calculates shortfalls from zeroed or reduced effective weight. For the fixed-reward epochs in scope, settlement does not increase other participants' allocations when a participant is invalidated or reduced through cPoC/weight scaling; the undistributed remainder is transferred to governance. This is distinct from determining whether each historical shortfall is eligible for compensation.

## Sources

- [Calculation repository](https://github.com/votkon/gonka-kimi-restitution)
- [DevOps chat evidence log](sources/P4-CAND-01-devops-chat.md)
- [PR #1143: v0.2.13 microrelease](https://github.com/gonka-ai/gonka/pull/1143)
- [Settlement logic: `accountsettle.go`](https://github.com/gonka-ai/gonka/blob/17808620293b57112896bcbb7f99c4c2f554d6c8/inference-chain/x/inference/keeper/accountsettle.go)
- [Reward remainder logic: `bitcoin_rewards.go`](https://github.com/gonka-ai/gonka/blob/17808620293b57112896bcbb7f99c4c2f554d6c8/inference-chain/x/inference/keeper/bitcoin_rewards.go)
