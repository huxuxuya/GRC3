# GRC Compensation Tracker

Public status tracker for proposals under preparation. Amounts are calculated estimates until approved by governance.

## Proposal #3 Candidates

| ID | Case | Epochs | Status | Reported By | Affected / Detail Contact | Investigated By / Result | Further Analysis | Estimate | Sources |
|---|---|---:|---|---|---|---|---|---:|---|
| [`P3-CAND-01`](public_cases/P3-CAND-01-devshard-miss-rate.md) | High miss rate / devshard issue | 269-272 | Investigation | Votkon; Nik | 6 addresses identified for epoch 272; Nik; claimant `A` | Fedor estimated losses; Nik identified reward omission / high miss rate | Required: devshard proofs and root cause | TBD | [Case](public_cases/P3-CAND-01-devshard-miss-rate.md); [DevOps evidence](public_cases/sources/P3-CAND-01-devops-chat.md) |
| [`P3-CAND-02`](public_cases/P3-CAND-02-negative-coin-balance.md) | Negative coin balance / settle-drop | 1-274 | Calculated; inclusion pending | Evgenii Maksimenkov | 19 miners; Evgenii Maksimenkov | Evgenii identified deterministic affected set | Required: independent validation and decision | 1,075.336 GNK | [Calculation](https://github.com/gonkavip/unclaimed) |
| [`P3-CAND-03`](public_cases/P3-CAND-03-failed-cpoc-epoch-267.md) | Failed cPoC / preserved Kimi shortfall | 267 | Scope decision required | Nik; Votkon | 1 known claimant; Nik; Evgenii Maksimenkov | DevOps discussion identifies Kimi validation shortfall and preserved-node condition | Required: victim set and methodology | TBD | [Case](public_cases/P3-CAND-03-failed-cpoc-epoch-267.md); [DevOps evidence](public_cases/sources/P3-CAND-03-devops-chat.md) |
| [`P3-CAND-04`](public_cases/P3-CAND-04-upgrade-cpoc-misfire-epoch-276.md) | UpgradeProtectionWindow / CPoC misfire | 276 | Calculated; inclusion pending | Votkon; Evgenii Maksimenkov | 19 miners; Vas Ily identified one affected address | Evgenii calculated; Nik reproduced result; Egor documented root cause | Required: independent validation and decision | 36,209.451 GNK | [Calculation](https://github.com/gonkavip/payout276); [DevOps evidence](public_cases/sources/P3-CAND-04-devops-chat.md) |
| [`P3-CAND-05`](public_cases/P3-CAND-05-ml3-reregistration.md) | `ml3` hardware re-registration | ~269 | Scope decision required | SegovChik from `@gonkstein` | 1 claimant; `@gonkstein` via SegovChik | Arturs noted no on-chain HW proof | Required: policy/scope decision first | TBD | [Log](public_cases/P3-CAND-05-ml3-reregistration.md) |

## Proposal #4 Candidate

| ID | Case | Epochs | Status | Reported By | Affected / Detail Contact | Investigated By / Result | Further Analysis | Estimate | Sources |
|---|---|---:|---|---|---|---|---|---:|---|
| [`P4-CAND-01`](public_cases/P4-CAND-01-kimi-restitution.md) | Kimi restitution: CPoC, nonce exclusion, ComputeGroupCap | 265-276 | Calculated; eligibility under discussion | Votkon; DevOps reporters | 52 unique addresses; Votkon; Evgenii Maksimenkov | Votkon calculated full period; DevOps evidence identifies epoch 266 exclusions and cap effects | Required: 3-5 validations and eligibility decision | 710,772.72 GNK | [Calculation](https://github.com/votkon/gonka-kimi-restitution); [DevOps evidence](public_cases/sources/P4-CAND-01-devops-chat.md) |

## Additional Observations - Not Proposed for Compensation

| ID | Observation | Epoch / Date | Reported By | Known Affected | Evidence Status | Action Status | Sources |
|---|---|---|---|---|---|---|---|
| [`OBS-01`](public_cases/OBS-01-governance-zero-voting-weight.md) | Governance votes recorded with zero weight for some nodes | Identified 2026-05-15; referenced again 2026-05-25 | Evgenii Maksimenkov; Gleb Morgachev; Mitch | At least 2 participant addresses cited | Chat evidence and tracker link; no reward loss asserted | Review only; not proposed for compensation | [Observation](public_cases/OBS-01-governance-zero-voting-weight.md) |
| [`OBS-02`](public_cases/OBS-02-post-cpoc-reentry-failure.md) | Node reportedly did not re-enter after cPoC removal | 2026-05-27 | Mykola | Not identified | Single report; no address or loss amount | Triage only; not proposed for compensation | [Observation](public_cases/OBS-02-post-cpoc-reentry-failure.md) |

## Mitigation / Fix Status

Status verified from public Gonka pull requests and the attributed DevOps evidence available on 2026-05-27.

| ID | Code Mitigation / Fix Evidence | Current Status | Known Timing |
|---|---|---|---|
| `P3-CAND-01` | PR [`#1143`](https://github.com/gonka-ai/gonka/pull/1143) includes devshard storage/stats and settlement-limit changes, but no confirmed fix for the reported high miss-rate cause. | Case-specific fix not identified. | `v0.2.13` deployed; root-cause fix unknown. |
| `P3-CAND-02` | PR [`#550`](https://github.com/gonka-ai/gonka/pull/550), `Negative coin balance for settle`; PR [`#826`](https://github.com/gonka-ai/gonka/pull/826), partial claim payment loss. | `#550` merged; `#826` closed without merge. | `#550` merged 2026-01-13; no deployed timing established here for the distinct `#826` path. |
| `P3-CAND-03` | PR [`#1143`](https://github.com/gonka-ai/gonka/pull/1143) fixes confirmation PoC weight loss during new-model bootstrap; DevOps discussion states a preserved-node fix was added in `0.2.13`. | Mitigation merged and reported live on mainnet. | `v0.2.13` executed at block `4267300` on 2026-05-26. |
| `P3-CAND-04` | The incident occurred because the `v0.2.13` protection window did not apply when `LastUpgradeHeight` was not recorded. | No public corrective PR identified for this misfire. | Fix schedule unknown. |
| `P3-CAND-05` | PR [`#1089`](https://github.com/gonka-ai/gonka/pull/1089), included through upgrade PR [`#948`](https://github.com/gonka-ai/gonka/pull/948), replaces epoch-long preserved scheduling with episode-scoped snapshots. | General preserved-node mitigation merged; this individual hardware claim is not proven fixed by it. | `v0.2.12` PR merged 2026-04-30. |
| `P4-CAND-01` | PR [`#1143`](https://github.com/gonka-ai/gonka/pull/1143) changes confirmation-weight snapshots and recalibrates Kimi; it does not remove the intended `ComputeGroupCap` rule. | Partial mechanism mitigation merged and reported live; compensation eligibility remains separate. | `v0.2.13` executed at block `4267300` on 2026-05-26. |
| `OBS-01` | DevOps discussion identifies consensus-module flow and proposes prioritising a fix for `0.2.14`. | No public merged PR or deployed fix identified. | Proposed target only: `0.2.14`; no confirmed release date. |
| `OBS-02` | No address or confirmed root cause available. | No mapped code fix. | Unknown. |

## Status Definitions

| Status | Meaning |
|---|---|
| Investigation | Cause and compensation eligibility are not established. |
| Scope decision required | The claim exists, but GRC has not decided whether it is eligible. |
| Calculated; inclusion pending | A calculation exists; validation and proposal inclusion are pending. |
| Review only / Triage only | Recorded for transparency; not included in a compensation proposal. |
