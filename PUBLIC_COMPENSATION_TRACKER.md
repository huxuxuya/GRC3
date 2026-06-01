# GRC Compensation Tracker

Public status tracker for proposals under preparation. Amounts are calculated estimates until approved by governance.

## Governance Reward Destination Balance

Lost-reward destinations in the case tables below refer to the chain `gov` module account used by settlement logic for undistributed or expired rewards. This account is distinct from the Cosmos distribution `community_pool`.

| Account | Address | Balance | Snapshot Block / Time | Sources |
|---|---|---:|---|---|
| `gov` module account | `gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33` | **1,078,335.309119497 GNK** (`1,078,335,309,119,497 ngonka`) | `4,286,541`; 2026-05-27 19:12:25 UTC | [Account balance](http://node1.gonka.ai:8000/chain-api/cosmos/bank/v1beta1/balances/gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33/by_denom?denom=ngonka); [Module accounts](http://node1.gonka.ai:8000/chain-api/cosmos/auth/v1beta1/module_accounts) |

## Proposal #3 Candidates

| Case | Epochs | Status | Reported By | Affected / Detail Contact | Investigator / Result | Validator(s) / Further Analysis | Estimate | Lost Reward Destination | Fix |
|---|---:|---|---|---|---|---|---:|---|---|
| [`P3-CAND-01`](public_cases/P3-CAND-01-devshard-miss-rate.md)<br>High miss rate / devshard issue<br>[Investigation](https://github.com/huxuxuya/grc-p3-cand01); [DevOps evidence](public_cases/sources/P3-CAND-01-devops-chat.md) | 272 | Ready for validation | Votkon; Nik | 6 addresses identified for epoch 272; Nik; claimant `A` | @OpenMindedPerson; investigation ready, same pattern not found in epochs 273-280 | @mikenosov; required: devshard-data validation | 30,715.491 GNK | Zeroed downtime/miss-rate reward share is not redistributed; it goes to governance remainder under fixed-reward settlement. | Likely mitigated by `v0.2.13`; validation pending |
| [`P3-CAND-02`](public_cases/P3-CAND-02-negative-coin-balance.md)<br>Negative coin balance / settle-drop<br>[Calculation](https://github.com/gonkavip/unclaimed); [independent audit](public_cases/sources/P3-CAND-02-independent-audit.md) | 1-274; tail 275-280 checked | Calculated; archive validation required | Evgenii Maksimenkov | 19 miners; Evgenii Maksimenkov | @maksimenkoff; deterministic affected set calculated in [gonkavip/unclaimed](https://github.com/gonkavip/unclaimed); independent first-pass/code audit completed | @dem_ww; required: archive `SettleAmount` validation and decision | 1,075.336 GNK | Calculated but no `SettleAmount` was written; rewards were eventually swept into the gov module account. Independent summary scan found 823 broad positive-unclaimed rows in 1-274, proving archive state is required to isolate the 19 bug rows. | [#550](https://github.com/gonka-ai/gonka/pull/550) (`v0.2.8`) present in current code; current tail 275-280 has no positive-unclaimed rows; [#826](https://github.com/gonka-ai/gonka/pull/826) is a separate claim-time path |
| [`P3-CAND-03`](public_cases/P3-CAND-03-failed-cpoc-epoch-267.md)<br>Failed cPoC / preserved Kimi shortfall<br>[Investigation](https://github.com/gonkalabs/GRC-e267-kimi_shortfall); [DevOps evidence](public_cases/sources/P3-CAND-03-devops-chat.md) | 267 | Calculated; eligibility disputed | Votkon; Nik | 1 primary claimant; Nik; Evgenii Maksimenkov | @mikenosov; report identifies one fully valid restitution address | @dem_ww; @votkon; required: eligibility vote / validation | ~10.2k GNK | cPoC-reduced / zero reward share is not redistributed; it goes to governance remainder under fixed-reward settlement. | [#1143](https://github.com/gonka-ai/gonka/pull/1143) (`v0.2.13`); proxy-config responsibility disputed |
| [`P3-CAND-04`](public_cases/P3-CAND-04-upgrade-cpoc-misfire-epoch-276.md)<br>UpgradeProtectionWindow / CPoC misfire<br>[Calculation](https://github.com/gonkavip/payout276); [DevOps evidence](public_cases/sources/P3-CAND-04-devops-chat.md) | 276 | Calculated; inclusion pending | Votkon; Evgenii Maksimenkov | 19 miners; Vas Ily identified one affected address | @maksimenkoff; calculation published in [gonkavip/payout276](https://github.com/gonkavip/payout276); Egor documented root cause | @votkon; @OpenMindedPerson; required: independent validation and decision | 36,209.451 GNK | cPoC-lost confirmation-weight share is not redistributed; under fixed-reward settlement it is transferred to governance remainder. | No public corrective fix identified |

## Other / Not In Current GRC Proposal

| Case | Epochs | Status | Reported By | Affected / Detail Contact | Investigated By / Result | Further Analysis | Estimate | Lost Reward Destination | Fix |
|---|---:|---|---|---|---|---|---:|---|---|
| [`P3-CAND-05`](public_cases/P3-CAND-05-ml3-reregistration.md)<br>`ml3` hardware re-registration | ~269 | Scope decision required; not in the current five assigned Proposal #3 cases | SegovChik from `@gonkstein` | 1 claimant; `@gonkstein` via SegovChik | Arturs noted no on-chain HW proof | Required: policy/scope decision first | TBD | Not established: compensable lost reward is not yet proven. | [#1089](https://github.com/gonka-ai/gonka/pull/1089) (`v0.2.12`, related mitigation) |
| [`P4-CAND-01`](public_cases/P4-CAND-01-kimi-restitution.md)<br>Kimi restitution: CPoC, nonce exclusion, ComputeGroupCap<br>[Calculation](https://github.com/votkon/gonka-kimi-restitution); [DevOps evidence](public_cases/sources/P4-CAND-01-devops-chat.md) | 265-276 | Not included in GRC; community proposal possible | Votkon; DevOps reporters | 52 unique addresses; Votkon; Evgenii Maksimenkov | @votkon; full-period calculation published; @maksimenkoff reviewed numbers as generally correct | @mikenosov raised scope, denominator and reproducibility objections; GRC voted against inclusion | 710,772.72 GNK published; contested | Disputed: chat notes some losses may have been redistributed by network rules, while fixed-reward reduced weights can leave governance remainder. | [#1143](https://github.com/gonka-ai/gonka/pull/1143) (`v0.2.13`, partial mitigation) |

## Compensation By Epoch / Overlap Matrix

Amounts are in GNK and are calculated estimates from the linked public repositories. Empty cells mean no compensation amount was found for that case and epoch.

| Case | Source | 97 | 112 | 116 | 129 | 132 | 265 | 266 | 267 | 268 | 269 | 270 | 271 | 272 | 273 | 274 | 275 | 276 | Total | Overlap Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `P3-CAND-01` | [grc-p3-cand01](https://github.com/huxuxuya/grc-p3-cand01) |  |  |  |  |  |  |  |  |  |  |  |  | 30,715.490666 |  |  |  |  | 30,715.490666 | Epoch 272 overlaps `P4-CAND-01` by epoch only; no same-address overlap found in checked aggregate data. |
| `P3-CAND-02` | [unclaimed](https://github.com/gonkavip/unclaimed) | 8.432384 | 7.993577 | 1,037.343140 | 7.470361 | 14.096690 |  |  |  |  |  |  |  |  |  |  |  |  | 1,075.336151 | No overlap with other current case epochs. |
| `P3-CAND-03` | [GRC-e267-kimi_shortfall](https://github.com/gonkalabs/GRC-e267-kimi_shortfall) |  |  |  |  |  |  |  | 10,262.057515 |  |  |  |  |  |  |  |  |  | 10,262.057515 | Epoch 267 overlaps `P4-CAND-01` by epoch only; no same-address overlap found in checked aggregate data. |
| `P3-CAND-04` | [payout276](https://github.com/gonkavip/payout276) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 36,209.451291 | 36,209.451291 | Epoch 276 has same-address overlap with `P4-CAND-01`; duplicate-compensation handling required. |
| `P4-CAND-01` | [gonka-kimi-restitution](https://github.com/votkon/gonka-kimi-restitution) |  |  |  |  |  | 30,592.104862 | 188,698.468970 | 88,917.163953 | 65,241.369805 | 48,012.518034 | 30,965.834116 | 38,178.788158 | 32,434.442996 | 50,077.516007 | 47,718.948918 | 33,938.754950 | 55,996.808384 | 710,772.719154 | Not in current GRC proposal; overlaps `P3-CAND-04` by address+epoch in epoch 276. |

### Overlap Findings

- Epoch-level overlaps exist at epoch `267` (`P3-CAND-03` / `P4-CAND-01`), epoch `272` (`P3-CAND-01` / `P4-CAND-01`) and epoch `276` (`P3-CAND-04` / `P4-CAND-01`).
- Epoch-level overlap is only a review signal; it does not by itself prove duplicate payment risk.
- Confirmed address+epoch overlap was found only for epoch `276`, between `P3-CAND-04` and `P4-CAND-01`.
- The overlapping epoch `276` addresses are `gonka10079cnl3nuh2k82mhkm04dj0slhtw9kmjewwau`, `gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2`, `gonka1gvrrhjmy4w4mayvs2s5l23edj8ertcmtd2v4zr`, `gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5`, `gonka1scskt6wpnjnumsah6kjphmdu87vjgvcxmn4rxv`, and `gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw`.
- Before any `P4-CAND-01` community payout, validators should subtract or otherwise reconcile any approved `P3-CAND-04` epoch `276` compensation for the overlapping addresses.

## Additional Observations - Not Proposed for Compensation

| Observation | Epoch / Date | Reported By | Known Affected | Evidence Status | Action Status | Fix |
|---|---|---|---|---|---|---|
| [`OBS-01`](public_cases/OBS-01-governance-zero-voting-weight.md)<br>Governance votes recorded with zero weight for some nodes | Identified 2026-05-15; referenced again 2026-05-25 | Evgenii Maksimenkov; Gleb Morgachev; Mitch | At least 2 participant addresses cited | Chat evidence and tracker link; no reward loss asserted | Review only; not proposed for compensation | No public PR; `v0.2.14` proposed in chat |
| [`OBS-02`](public_cases/OBS-02-post-cpoc-reentry-failure.md)<br>Node reportedly did not re-enter after cPoC removal | 2026-05-27 | Mykola | Not identified | Single report; no address or loss amount | Triage only; not proposed for compensation | No mapped fix |

## Status Definitions

| Status | Meaning |
|---|---|
| Investigation | Cause and compensation eligibility are not established. |
| Ready for validation | Investigator has published a calculation/report; independent validation remains open. |
| Scope decision required | The claim exists, but GRC has not decided whether it is eligible. |
| Calculated; inclusion pending | A calculation exists; validation and proposal inclusion are pending. |
| Calculated; eligibility disputed | A calculation exists, but committee members have raised material scope or responsibility objections. |
| Not included in GRC; community proposal possible | GRC has voted or decided not to include the case in a GRC proposal, but the materials may still support a direct community proposal. |
| Review only / Triage only | Recorded for transparency; not included in a compensation proposal. |
