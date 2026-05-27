# P4-CAND-01: Kimi Restitution, Epochs 265-276

| Field | Value |
|---|---|
| Proposal | Proposal #4 candidate |
| Epochs | 265-276 |
| Status | Calculated; GRC eligibility under discussion |
| Reported by | Votkon; DevOps chat reporters including Evgenii Maksimenkov |
| Affected / detail contact | 52 unique addresses; Votkon; Evgenii Maksimenkov for chat evidence |
| Investigated by | Votkon; DevOps technical discussion |
| Result so far | Full-period calculation published; contemporaneous epoch 266 exclusion and ComputeGroupCap evidence located |
| Further analysis | Required: 3-5 independent validations and eligibility decision |
| Compensation | 710,772.72 GNK |

## Message Log

| Date | Author | Fact / short quote | Meaning |
|---|---|---|---|
| 2026-05-24 09:02 UTC+03 | Votkon | Kimi issue was initially listed for Proposal #3 work. | Earlier planning context. |
| 2026-05-27 17:03 UTC+03 | Votkon | Clarified period as epochs 265-276. | Calculation scope. |
| 2026-05-27 17:50 UTC+03 | Votkon | Proposed voting whether to include the case in Proposal #4. | Current proposal classification. |
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

## Sources

- [Calculation repository](https://github.com/votkon/gonka-kimi-restitution)
- [DevOps chat evidence log](sources/P4-CAND-01-devops-chat.md)
- [PR #1143: v0.2.13 microrelease](https://github.com/gonka-ai/gonka/pull/1143)
