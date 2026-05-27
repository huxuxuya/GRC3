# P3-CAND-05: `ml3` Hardware Re-Registration

| Field | Value |
|---|---|
| Proposal | Proposal #3 candidate |
| Epochs | Around epoch 269 |
| Status | Scope decision required |
| Reported by | SegovChik from `@gonkstein` and technical contact |
| Affected / detail contact | One known claimant: `gonka15munkmx6x7k6rqqeexjet4556p7at39ks9qgr5`; `@gonkstein` via SegovChik |
| Investigated by | Arturs Plisko provided initial scope assessment |
| Result so far | No on-chain proof of hardware change identified |
| Further analysis | Required only if committee accepts this claim type as eligible |
| Compensation | Not calculated |

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

## Mitigation / Fix Status

| Item | Status |
|---|---|
| Related preserved-node redesign | PR [`#1089`](https://github.com/gonka-ai/gonka/pull/1089) replaces epoch-long preserved scheduling with episode-scoped preserved snapshots; it was merged into the `v0.2.12` upgrade branch. |
| Deployment evidence | Upgrade PR [`#948`](https://github.com/gonka-ai/gonka/pull/948), which includes the preserved-node redesign, was merged into `main` on 2026-04-30. |
| Case-specific conclusion | This is general mitigation for predictable preserved-node behaviour; it does not prove that the reported hardware re-registration claim was a defect or that it was cured. |

## Sources

- [Participant tracker record](https://tracker.gonka.hyperfusion.io/?epoch=269&participant=gonka15munkmx6x7k6rqqeexjet4556p7at39ks9qgr5)
- [PR #1089: Random Selection of Preserved MLNodes](https://github.com/gonka-ai/gonka/pull/1089)
- [PR #948: Upgrade v0.2.12](https://github.com/gonka-ai/gonka/pull/948)
