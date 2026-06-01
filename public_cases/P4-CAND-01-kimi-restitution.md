# P4-CAND-01: Kimi Restitution, Epochs 265-276

| Field | Value |
|---|---|
| **Case** | `P4-CAND-01` - Kimi Restitution |
| Proposal | Not included in current GRC proposal; external/community proposal possible |
| Epochs affected | 265-276 |
| Affected participants | 52 unique addresses |
| Estimated compensation | 710,772.72 GNK |
| **Cause and evidence** | CPoC degradation in epoch 265, nonce/delegation losses in epoch 266, and ComputeGroupCap underpayment in epochs 267-276. Evidence: [calculation repository](https://github.com/votkon/gonka-kimi-restitution) and [DevOps chat log](sources/P4-CAND-01-devops-chat.md). |
| **Can it happen again?** | Reduced risk after `v0.2.13`; `ComputeGroupCap` still exists as an intended protocol rule, so recurrence risk should be reviewed. |
| **Mitigation / fix** | Partially mitigated by PR [#1143](https://github.com/gonka-ai/gonka/pull/1143) in `v0.2.13`: confirmation PoC weight loss during new-model bootstrap was fixed, and Kimi `WeightScaleFactor` was recalibrated to `0.78`. |
| **Compensation overlap** | Overlaps by epoch with `P3-CAND-03` at epoch 267, `P3-CAND-01` at epoch 272, and `P3-CAND-04` at epoch 276. Confirmed same-address overlap was found only with `P3-CAND-04` in epoch 276; validators must ensure no duplicate compensation for those addresses. |
| **Current decision** | GRC voted against including this case in a GRC proposal; published findings remain usable for a community proposal. |
| **Review focus** | Investigator: @votkon. @maksimenkoff reviewed the numbers as generally correct but questioned GroupCap compensation; @mikenosov raised scope, denominator, epoch-276 proration and reproducibility objections. |

## Message Log

| Date | Author | Fact / short quote | Meaning |
|---|---|---|---|
| 2026-05-24 09:02 UTC+03 | Votkon | Kimi issue was initially listed for Proposal #3 work. | Earlier planning context. |
| 2026-05-27 17:03 UTC+03 | Votkon | Clarified period as epochs 265-276. | Calculation scope. |
| 2026-05-27 17:50 UTC+03 | Votkon | Proposed voting whether to include the case in Proposal #4. | Earlier proposal-positioning and eligibility context. |
| 2026-05-27 18:04 UTC+03 | Votkon | "We'd probably need 3-5 validations." | Review requirement due to amount. |
| 2026-05-29 08:29 UTC+03 | Evgenii Maksimenkov | Numbers appear correct; direct attack impact can be compensated, but GroupCap effects across later epochs are less convincing. | Validator view: calculation broadly reproducible, scope contested. |
| 2026-05-29 08:37 UTC+03 | Votkon | GRC voted against including this case; he would record the GRC position and GroupCap view in the repo. | GRC inclusion decision. |
| 2026-06-01 00:54 UTC+03 | Mike | Suggested excluding e265-e266 from GRC scope, questioned e267-e276 denominator correctness, noted e276 proration and e266 script/output mismatch. | Validator objections requiring resolution outside GRC inclusion. |
| 2026-05-17 00:56 UTC+03 | Evgenii Maksimenkov, DevOps chat | Identified 9 PoC submitters that did not enter the epoch 266 final set. | Address-level evidence for nonce exclusion. |
| 2026-05-17 22:30 UTC+03 | David Liberman, DevOps chat | Identified `ComputeGroupCap` and its `75%` cap as the cause of reduced Kimi weight. | Protocol-rule evidence for later Kimi weight reduction. |
| 2026-05-25 13:52 UTC+03 | Evgenii Maksimenkov, DevOps chat | Calculated an epoch 275 Kimi scale of approximately `0.659`. | Independent contemporaneous explanation of cap effect. |

## Findings

- The published package covers epoch 265 CPoC degradation, epoch 266 nonce/delegation losses, and epochs 267-276 ComputeGroupCap underpayment.
- It reports `52` unique affected addresses and `710,772.72 GNK`.
- GRC voted against including the case in a GRC proposal because the root event was framed as a third-party attack / operator-disruption case.
- Evgenii Maksimenkov reviewed the numbers as generally correct, but did not support compensating all later GroupCap effects without qualification.
- Mike raised additional methodological concerns: scope exclusion for e265-e266, denominator correctness for e267-e276, proration for e276, and an e266 script/output mismatch.
- Any approval must check overlap with the separate epoch 276 CPoC-misfire candidate. The checked data shows six same-address epoch-276 overlaps with `P3-CAND-04`.
- DevOps evidence includes named addresses and publicly described methods for recovering PoC/validation evidence.

## Mitigation / Fix Status

| Item | Status |
|---|---|
| Chain mitigation | PR [`#1143`](https://github.com/gonka-ai/gonka/pull/1143) fixes confirmation PoC weight loss during new-model bootstrap and recalibrates the Kimi `WeightScaleFactor` to `0.78`. |
| Protocol rule distinction | The PR does not remove `ComputeGroupCap`; the `75%` cap discussed in the evidence remains an intended protocol rule. The recalibration limits the circumstances producing a Kimi cap breach. |
| Deployment timing | DevOps announcement reports that `v0.2.13` executed on mainnet at block `4267300` on 2026-05-26. |
| Remaining status | Not in the current GRC proposal. Historical restitution may still be proposed directly to the community, but scope and methodology objections should be resolved first. |

## Reward Flow

The restitution package calculates shortfalls from zeroed or reduced effective weight. Reward destination is contested in the latest discussion: Arturs Plisko stated that attack-related losses were redistributed among active participants under network rules, while the fixed-reward settlement logic still leaves some reduced-weight remainders for governance. This destination question is separate from whether the case is eligible for GRC compensation.

## Sources

- [Calculation repository](https://github.com/votkon/gonka-kimi-restitution)
- [GRC chat update export index](sources/GRC-chat-update-2026-06-01.md)
- [DevOps chat evidence log](sources/P4-CAND-01-devops-chat.md)
- [PR #1143: v0.2.13 microrelease](https://github.com/gonka-ai/gonka/pull/1143)
- [Settlement logic: `accountsettle.go`](https://github.com/gonka-ai/gonka/blob/17808620293b57112896bcbb7f99c4c2f554d6c8/inference-chain/x/inference/keeper/accountsettle.go)
- [Reward remainder logic: `bitcoin_rewards.go`](https://github.com/gonka-ai/gonka/blob/17808620293b57112896bcbb7f99c4c2f554d6c8/inference-chain/x/inference/keeper/bitcoin_rewards.go)
