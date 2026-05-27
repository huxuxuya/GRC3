# GRC Compensation Tracker

Public status tracker for proposals under preparation. Amounts are calculated estimates until approved by governance.

## Proposal #3 Candidates

| ID | Case | Epochs | Status | Reported By | Affected / Detail Contact | Investigated By / Result | Further Analysis | Estimate | Sources |
|---|---|---:|---|---|---|---|---|---:|---|
| [`P3-CAND-01`](public_cases/P3-CAND-01-devshard-miss-rate.md) | High miss rate / devshard issue | 269-272 | Investigation | Votkon; Nik | TBD; Nik | Fedor estimated losses; audit confirmed outcome, not bug | Required: devshard proofs and root cause | TBD | [Log](public_cases/P3-CAND-01-devshard-miss-rate.md) |
| [`P3-CAND-02`](public_cases/P3-CAND-02-negative-coin-balance.md) | Negative coin balance / settle-drop | 1-274 | Calculated; inclusion pending | Evgenii Maksimenkov | 19 miners; Evgenii Maksimenkov | Evgenii identified deterministic affected set | Required: independent validation and decision | 1,075.336 GNK | [Calculation](https://github.com/gonkavip/unclaimed) |
| [`P3-CAND-03`](public_cases/P3-CAND-03-failed-cpoc-epoch-267.md) | Failed cPoC / preserved Kimi shortfall | 267 | Scope decision required | Nik; Votkon | 1 known claimant; Nik | Mike excluded it from P2 scope | Required: victim set and methodology | TBD | [Log](public_cases/P3-CAND-03-failed-cpoc-epoch-267.md) |
| [`P3-CAND-04`](public_cases/P3-CAND-04-upgrade-cpoc-misfire-epoch-276.md) | UpgradeProtectionWindow / CPoC misfire | 276 | Calculated; inclusion pending | Votkon; Evgenii Maksimenkov | 19 miners; Evgenii Maksimenkov | Evgenii calculated; Nik reproduced result | Required: independent validation and decision | 36,209.451 GNK | [Calculation](https://github.com/gonkavip/payout276) |
| [`P3-CAND-05`](public_cases/P3-CAND-05-ml3-reregistration.md) | `ml3` hardware re-registration | ~269 | Scope decision required | SegovChik from `@gonkstein` | 1 claimant; `@gonkstein` via SegovChik | Arturs noted no on-chain HW proof | Required: policy/scope decision first | TBD | [Log](public_cases/P3-CAND-05-ml3-reregistration.md) |

## Proposal #4 Candidate

| ID | Case | Epochs | Status | Reported By | Affected / Detail Contact | Investigated By / Result | Further Analysis | Estimate | Sources |
|---|---|---:|---|---|---|---|---|---:|---|
| [`P4-CAND-01`](public_cases/P4-CAND-01-kimi-restitution.md) | Kimi restitution: CPoC, nonce exclusion, ComputeGroupCap | 265-276 | Calculated; eligibility under discussion | Votkon | 52 unique addresses; Votkon | Votkon calculated full period | Required: 3-5 validations and eligibility decision | 710,772.72 GNK | [Calculation](https://github.com/votkon/gonka-kimi-restitution) |

## Status Definitions

| Status | Meaning |
|---|---|
| Investigation | Cause and compensation eligibility are not established. |
| Scope decision required | The claim exists, but GRC has not decided whether it is eligible. |
| Calculated; inclusion pending | A calculation exists; validation and proposal inclusion are pending. |
