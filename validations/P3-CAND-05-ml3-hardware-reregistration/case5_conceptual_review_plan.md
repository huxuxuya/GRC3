# P3-CAND-05 Conceptual Review Plan

This document is a step-by-step review plan for Case 5. It focuses on
conceptual validity, not arithmetic. Each item tracks whether the claim is
supported by chain data, off-chain evidence, or still requires a committee
policy decision.

## Status Labels

| Status | Meaning |
|---|---|
| `Confirmed` | Evidence is sufficient for the claim. |
| `Partially confirmed` | Some facts are proven, but the full claim is not. |
| `Not confirmed` | Current evidence does not support the claim. |
| `Pending` | Evidence or a formula still needs to be collected. |
| `Blocked` | The required evidence is not available from current archive/LCD data. |
| `Policy required` | The committee must decide scope before technical validation can finish. |

## Case Scope

| Field | Value |
|---|---|
| Candidate | `P3-CAND-05` |
| Claimant | `gonka15munkmx6x7k6rqqeexjet4556p7at39ks9qgr5` |
| Claimed node | `ml3` |
| Reported issue | `ml3` allegedly moved from `4xB200` to `8xB200` under the same node name, but chain weight did not increase as expected. |
| Current high-level state | Chain confirms node/weight transitions, but not the physical hardware change, exact protocol cause, or compensable loss. |

## Review Checklist

| # | Question / claim to validate | Evidence required | Current evidence | Status | Next action |
|---:|---|---|---|---|---|
| 1 | Did the claimant actually replace `ml3` hardware from `4xB200` to `8xB200`? | Operator proof, hardware inventory, deployment logs, photos/serials if accepted by policy, or other committee-approved off-chain evidence. | Chain data has no hardware inventory field. It only records node IDs, model rows, `poc_weight`, `throughput`, and `timeslot_allocation`. | `Not confirmed` | Ask claimant/operator for off-chain proof and define acceptable evidence standard. |
| 2 | Is `ml3` the same node identity across the relevant epochs? | Stable node ID in claimant model rows, plus evidence that the node name maps to the same operational entity. | Chain confirms `ml3` appears for claimant in epochs `263..269`, then disappears from checked model rows from epoch `270`. | `Partially confirmed` | Treat node ID continuity as chain-confirmed, but do not infer physical hardware continuity without off-chain proof. |
| 3 | Did chain weight materially change around the reported period? | Epoch group model rows by epoch. | `ml3` has Qwen `poc_weight = 16,235` in epochs `263..265`; Kimi `16,235` in epoch `266`; Kimi `5,219` in epochs `267..269`; from epoch `270`, `ml3` is absent. | `Confirmed` | Keep this as the core on-chain fact, not as proof of cause. |
| 4 | Was the lower `ml3 = 5,219` weight caused by a protocol defect rather than normal PoC measurement, local setup, validator behavior, or submission count? | Raw PoC submissions, nonce counts, validator rows, weight distributions, DAPI/operator logs. | Current public/archive endpoints did not expose raw PoC submissions, validations, V2 store commits, or ML node weight distributions for epochs `266..269`. | `Blocked` | Need deeper archive, node logs, or claimant/operator evidence. |
| 5 | Was `ml3` preserved out of PoC by the old `POC_SLOT=true` mechanism? | `timeslot_allocation[1] == true` for `ml3`, or preserved-node snapshot evidence showing `ml3` was excluded from PoC. | Checked `ml3` rows show `timeslot_bits = 10`: `PRE_POC_SLOT=true`, `POC_SLOT=false`. Pre-fix code treats index `1` / `POC_SLOT` as preserved-for-PoC. | `Not confirmed` | Do not use preserved-node mechanism as proven root cause unless new evidence shows `POC_SLOT=true` or equivalent preservation. |
| 6 | Does PR `#1089` / `v0.2.12` prove this specific claim? | Direct link between the fix and the claimant's observed node behavior. | PR `#1089` fixes broader preserved-node scheduling, but does not prove that this operator replaced hardware or that `ml3` was affected by `POC_SLOT=true`. | `Not confirmed` | Use PR `#1089` only as related context, not as case-specific proof. |
| 7 | Was the claimant excluded or explicitly slashed by a known chain reason? | `excluded_participants`, participant status, failure reason. | Claimant is not listed as excluded in checked epochs `263..283`. | `Not confirmed` as an exclusion/slash case | Do not classify this with cPoC/exclusion cases unless new failure evidence appears. |
| 8 | Did the claimant receive rewards during the alleged loss window? | `epoch_performance_summary` for claimant. | Claimant received non-zero rewards in epochs `263..271`, zero in `272..273`, then non-zero again after later node IDs appear. | `Confirmed` | Separate "reduced reward" analysis from "zero reward" claims; zero rewards in `272..273` are not currently linked to `ml3`. |
| 9 | Is there a measurable reward shortfall from chain data alone? | Counterfactual weight, model scale factors, epoch reward denominator, actual reward comparison. | No agreed counterfactual weight/formula exists. Raw `poc_weight` changes alone do not define a chain reward shortfall. | `Not confirmed` | Define a compensation formula only after root cause and counterfactual weight are accepted. |
| 10 | Can raw `poc_weight` be used directly as compensation weight? | Chain reward formula and model scale factors. | No. Raw model `poc_weight` is not a reward numerator. Chain-style calculation must apply model `weight_scale_factor` and epoch payout denominator. | `Confirmed` | Any proposed amount must show raw weight -> scaled/effective weight -> reward formula. |
| 11 | Is the loss destination known? | Proven reward shortfall and chain settlement path. | No compensable shortfall is established, so reward destination cannot be determined. | `Pending` | Revisit only if a concrete shortfall formula is accepted. |
| 12 | Is this eligible as a GRC compensation case without on-chain proof? | Committee policy on off-chain hardware claims. | Current technical evidence is insufficient for independent protocol-loss confirmation. | `Policy required` | Committee must decide whether off-chain hardware evidence can establish eligibility. |

## Working Order

1. Confirm the exact claim wording and affected epoch range.
2. Request/collect off-chain proof for the alleged hardware replacement.
3. Re-check chain rows for claimant/node/model continuity across the proposed range.
4. Verify whether any evidence shows `POC_SLOT=true` or preserved snapshot inclusion for `ml3`.
5. Try to obtain raw PoC submissions, validation rows, or node weight distributions for epochs `266..269`.
6. Decide whether the root cause is protocol-side, operator-side, or unproven.
7. If protocol-side cause is confirmed, define the counterfactual weight per epoch.
8. Apply model `weight_scale_factor` and chain reward formula per epoch.
9. Compare counterfactual rewards against actual `rewarded_coins`.
10. Check overlap with other cases and prior payments.
11. Draft committee decision: reject, defer pending evidence, or approve with a defined formula.

## Current Working Conclusion

At the current evidence level, Case 5 should not be treated as an independently
confirmed compensation case.

The chain confirms a real `ml3` node/weight transition, but it does not confirm:

- the physical hardware replacement;
- that `ml3` was preserved out of PoC by `POC_SLOT=true`;
- the exact reason why `ml3` measured `5,219` in epochs `267..269`;
- a protocol-caused reward shortfall;
- a chain-style compensation formula.

The next useful work is evidence collection and policy clarification, not
amount calculation.
