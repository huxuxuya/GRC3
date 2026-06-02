# P3-CAND-05: `ml3` Hardware Re-Registration

| Field | Value |
|---|---|
| Proposal | Proposal #3 candidate |
| Epochs | Around epoch 269 |
| Status | Independently checked; scope decision still required |
| Reported by | SegovChik from `@gonkstein` and technical contact |
| Affected / detail contact | One known claimant: `gonka15munkmx6x7k6rqqeexjet4556p7at39ks9qgr5`; `@gonkstein` via SegovChik |
| Investigated by | Arturs Plisko provided initial scope assessment |
| Result so far | Chain confirms node/weight transitions, but no on-chain proof of the physical hardware change, `POC_SLOT=true` preservation for `ml3`, or compensable loss |
| Further analysis | Required only if committee accepts this claim type as eligible and defines off-chain evidence / formula |
| Compensation | Not calculated |
| Lost reward destination | Not established: no compensable reward shortfall has been proven for this claim. |

## Message Log

| Date | Author | Fact / short quote | Meaning |
|---|---|---|---|
| 2026-05-20 17:07 UTC+03 | SegovChik | `ml3` moved from 4xB200 to 8xB200 under the same name without weight increase. | Claim as reported by operator contact. |
| 2026-05-20 17:09 UTC+03 | SegovChik | Shared tracker entry for the participant at epoch 269. | Public observable reference. |
| 2026-05-20 17:37 UTC+03 | Arturs Plisko | "there is no onchain proof of HW change" | Key eligibility limitation. |
| 2026-05-20 17:37 UTC+03 | Arturs Plisko | Described it as known `timeslot_allocation` / preserved-node behaviour. | Potential policy rather than protocol bug. |

## Findings

- A single claimant is currently identified.
- Hardware replacement itself is not verifiable from the cited on-chain information.
- No compensation computation has been presented.
- Independent archive validation across epochs `263..283` confirms `ml3` appears for the claimant in epochs `263..269`, then disappears from the checked model rows from epoch `270`.
- The `ml3` rows in the archive trace show `timeslot_bits = 10`, i.e.
  `PRE_POC_SLOT=true` and `POC_SLOT=false`; this is not proof that `ml3` was
  preserved out of PoC by the old `POC_SLOT` mechanism.
- The claimant was not found in `excluded_participants` for the checked range.
- The Kimi/Qwen `weight` values in the trace are raw model `poc_weight`
  values. They show measurement/node history, but they are not a direct reward
  numerator; any payout formula would need model `weight_scale_factor` and the
  chain reward denominator.
- The archive trace is stored in [`validations/P3-CAND-05-ml3-hardware-reregistration`](../validations/P3-CAND-05-ml3-hardware-reregistration/).

## Independent Trace Summary

| Epoch | Nodes | `ml3` | Kimi weight | Qwen weight | Reward, GONKA | Excluded |
|---|---|---|---:|---:|---:|---|
| 263 | `ml3;ml5;ml8` | yes | 23972 | 16235 | 9745.244781111 | no |
| 265 | `ml3;ml5;ml8` | yes | 22160 | 16235 | 10553.989409830 | no |
| 266 | `ml3;ml8` | yes | 26304 |  | 26799.023361427 | no |
| 267 | `ml3;ml5;ml8` | yes | 27400 |  | 2829.715828861 | no |
| 268 | `ml3;ml5;ml8` | yes | 27639 |  | 5757.415294226 | no |
| 269 | `ml3;ml5` | yes | 17885 |  | 6276.820078853 | no |
| 270 | `ml1;ml5` | no | 23670 |  | 7880.707923174 | no |
| 272 | `ml1` | no | 11175 |  | 0.000000000 | no |

## Mitigation / Fix Status

| Item | Status |
|---|---|
| Related preserved-node redesign | PR [`#1089`](https://github.com/gonka-ai/gonka/pull/1089) replaces epoch-long preserved scheduling with episode-scoped preserved snapshots; it was merged into the `v0.2.12` upgrade branch. |
| Deployment evidence | Upgrade PR [`#948`](https://github.com/gonka-ai/gonka/pull/948), which includes the preserved-node redesign, was merged into `main` on 2026-04-30. |
| Case-specific conclusion | This is general mitigation for predictable preserved-node behaviour; the checked `ml3` rows do not show `POC_SLOT=true`, and the PR does not prove that the reported hardware re-registration claim was a defect, that physical hardware changed, or that a payout amount exists. |

## Reward Flow

No reward-destination conclusion can be made until the committee establishes that a measurable reward loss occurred and identifies its on-chain mechanism. A valid chain-style amount cannot be calculated directly from raw `poc_weight`; it would need the relevant model scale factors and the epoch payout formula.

## Sources

- [Participant tracker record](https://tracker.gonka.hyperfusion.io/?epoch=269&participant=gonka15munkmx6x7k6rqqeexjet4556p7at39ks9qgr5)
- [Validation package](../validations/P3-CAND-05-ml3-hardware-reregistration/)
- [PR #1089: Random Selection of Preserved MLNodes](https://github.com/gonka-ai/gonka/pull/1089)
- [PR #948: Upgrade v0.2.12](https://github.com/gonka-ai/gonka/pull/948)
