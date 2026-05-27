# GRC Compensation Tracker

Public status tracker for proposals under preparation. Amounts are calculated estimates until approved by governance.

## Proposal #3 Candidates

| ID | Case | Epochs | Status | Affected | Estimated Compensation | Evidence / Calculation | Next Step |
|---|---|---:|---|---:|---:|---|---|
| `P3-CAND-01` | High miss rate / devshard issue | 269-272 | Investigation | TBD | TBD | On-chain audit completed; node devshard proof data required | Establish root cause and eligibility |
| `P3-CAND-02` | Negative coin balance / settle-drop | 1-274 | Calculated; inclusion pending | 19 | 1,075.336 GNK | [Calculation](https://github.com/gonkavip/unclaimed), fixes [#826](https://github.com/gonka-ai/gonka/pull/826) / [#550](https://github.com/gonka-ai/gonka/pull/550) | Independent validation and inclusion decision |
| `P3-CAND-03` | Failed cPoC / preserved Kimi validation shortfall | 267 | Scope decision required | 1 known claimant | TBD | On-chain failure identified; historical preserved-node evidence required | Define evidence and eligibility |
| `P3-CAND-04` | UpgradeProtectionWindow / CPoC misfire | 276 | Calculated; inclusion pending | 19 | 36,209.451 GNK | [Calculation](https://github.com/gonkavip/payout276) | Independent validation and inclusion decision |
| `P3-CAND-05` | `ml3` hardware re-registration | ~269 | Scope decision required | 1 known claimant | TBD | [Tracker record](https://tracker.gonka.hyperfusion.io/?epoch=269&participant=gonka15munkmx6x7k6rqqeexjet4556p7at39ks9qgr5); hardware change not verifiable on-chain | Decide whether claim is eligible |

## Proposal #4 Candidate

| ID | Case | Epochs | Status | Affected | Estimated Compensation | Evidence / Calculation | Next Step |
|---|---|---:|---|---:|---:|---|---|
| `P4-CAND-01` | Kimi restitution: CPoC, nonce exclusion, ComputeGroupCap | 265-276 | Calculated; GRC eligibility under discussion | 52 unique addresses | 710,772.72 GNK | [Calculation](https://github.com/votkon/gonka-kimi-restitution) | Independent validations and scope decision |

## Status Definitions

| Status | Meaning |
|---|---|
| Investigation | Cause and compensation eligibility are not established. |
| Scope decision required | The claim exists, but GRC has not decided whether it is eligible. |
| Calculated; inclusion pending | A calculation exists; validation and proposal inclusion are pending. |

