# Compensation Results Ledger

Last updated: 2026-06-07.

This file is the working table of compensation amounts produced or tracked by
this repository. It separates final/accepted amounts from locally validated
recommendations and from disputed source totals. Do not sum rows across
different status groups without checking overlap notes.

Machine-readable summary: [`compensation_results.csv`](compensation_results.csv).
Address/epoch ledger:
[`compensation_address_epoch_ledger.csv`](compensation_address_epoch_ledger.csv).
Overlap matrix:
[`COMPENSATION_OVERLAP_MATRIX.md`](COMPENSATION_OVERLAP_MATRIX.md) and
[`compensation_overlap_matrix.csv`](compensation_overlap_matrix.csv).
Case/epoch crosstab:
[`COMPENSATION_EPOCH_CROSSTAB.md`](COMPENSATION_EPOCH_CROSSTAB.md) and
[`compensation_epoch_crosstab.csv`](compensation_epoch_crosstab.csv).

## Status Groups

| Status group | Meaning |
|---|---|
| `accepted_compensated` | Included in an accepted governance proposal according to the public tracker. |
| `local_validated_recommended` | Locally validated or recommended by our review, but still requires explicit governance/committee acceptance. |
| `pending_estimate` | Calculation exists, but validation, scope, or overlap review is not final. |
| `scope_required` | Claim exists, but no compensable amount is established. |
| `disputed_not_aggregate` | Useful evidence, but not valid as one aggregate payout. |
| `rejected` | Rejected or should not be paid under the current finding. |

## Main Table

| Case / Track | Epochs | Affected | Amount, GONKA | Status group | Current local position | Overlap / notes |
|---|---:|---:|---:|---|---|---|
| `P2-C01` Inactive status mid-epoch | `247` | 9 claimed participants | `0` | `rejected` | Rejected in Proposal #2 preparation. | No payout. |
| `P2-C02` Preserver weight double-scaling | n/a | 34 participant/node pairs | `30318.50` | `accepted_compensated` | Accepted / compensated in Proposal #2. | Historical tracker amount. |
| `P2-C03` Epoch loss restitution | n/a | subpackage-based | `217612.83` | `accepted_compensated` | Accepted / compensated in Proposal #2. | Do not use for deduped address count. |
| `P2-C04` API startup blocking | n/a | 14 addresses | `58375.96` | `accepted_compensated` | Accepted / compensated in Proposal #2. | Historical tracker amount. |
| `P3-CAND-01` Devshard / high miss rate | `272` | 6 confirmed addresses; 1 manual-review row | `35040.581153560` | `pending_estimate` | Current calculation repo reports this confirmed-six amount; devshard/root-cause validation still required. | Current repo also reports `35109.923355683` GONKA if the manual-review row is included. |
| `P3-CAND-02` Negative coin balance / settle-drop | `1..274` | 19 miners | `1075.336150923` | `local_validated_recommended` | Coordinator validated; inclusion decision still required. | Exact independent archive match. |
| `P3-CAND-03` strict Case 3 Kimi cPoC shortfall | `267` | 1 address | `10262.057515369` | `local_validated_recommended` | Independently validated. | Same claimant also has an epoch `265` Case-3-like row. |
| `P3-CAND-03-EXT` Case 3 same-address epoch 265 extension | `265` | 1 address | `20896.527179100` | `local_validated_recommended` | Recommended to include with Case 3 as the same Kimi cPoC failure class. | Same amount/class appears inside P4 e265 source package; do not double pay. |
| `P3-CAND-03-TOTAL` Case 3 recommended total | `265,267` | 1 address / 2 rows | `31158.584694469` | `local_validated_recommended` | Working recommended Case 3 amount after adding epoch `265`. | This is `P3-CAND-03` + `P3-CAND-03-EXT`; do not sum all three rows together. |
| `P3-CAND-04` UpgradeProtectionWindow / cPoC misfire | `276` | 19 miners | `32429.966254822` | `pending_estimate` | Current calculation repo reports this amount; our older local validation matched a previous published CSV total of `36209.451291351` GONKA, so the new source amount requires revalidation. | Same-address overlap exists with P4 epoch `276`; reconcile before any P4 payout. |
| `P3-CAND-05` `ml3` hardware re-registration | `263..283` focus `269` | 1 known claimant | `0` | `scope_required` | No compensable on-chain loss or formula established. | Keep as observation/scope item unless committee defines off-chain evidence and formula. |
| `P3-CAND-06` Pre-fix confirmation accounting candidates | `262..276` | 19 unique participants / 24 rows | `120822.324371792` | `pending_estimate` | Gross candidate set only; eligibility and overlap review required. | Includes epoch `276` rows that must be reconciled with Case 4. |
| `P4-CAND-01` source aggregate Kimi restitution | `265..276` | 53 unique addresses | `946509.925002` | `disputed_not_aggregate` | Do not approve as one aggregate payout. Split into tracks. | Mixes direct cPoC, e266 nonce/delegation, rewarded top-ups, and GroupCap. |
| `P4-e265` source cPoC / attack-attributed rows | `265` | 3 rows | `30592.104861828` | `disputed_not_aggregate` | Mixed scope: only the `gonka1j7...` row belongs with Case 3 under current local recommendation. | Case 3 part is `20896.527179100`; other e265 rows remain separate/unconfirmed for strict Case 3. |
| `P4-e266` nonce + delegation source package | `266` | 27 rows / 26 unique addresses | `188698.468968749` | `pending_estimate` | Chain facts partly confirmed; compensability must be split by sub-track. | Contains 9 absent operators, 5 zero-reward rows, 4 rewarded top-up rows, 9 delegation rows. |
| `P4-GroupCap-source` source top-up model | `267..276` | source rows | `727219.351170981` | `disputed_not_aggregate` | Reproducible model, but compensability and denominator are policy choices. | Options also include alternate denominator models or rejection. |
| `P4-GroupCap-all-confirmation` alternate denominator model | `267..276` | source rows | `503653.983658046` | `disputed_not_aggregate` | Alternative model for committee comparison, not a recommendation yet. | Do not combine with source top-up model. |
| `P4-GroupCap-replace-affected` alternate denominator model | `267..276` | source rows | `360858.547914700` | `disputed_not_aggregate` | Alternative model for committee comparison, not a recommendation yet. | Do not combine with source top-up model. |

## Rollups

| Rollup | Amount, GONKA | Contents | Notes |
|---|---:|---|---|
| Accepted / compensated historical tracker total | `306307.29` | `P2-C02 + P2-C03 + P2-C04` | Proposal #2 accepted amounts from public tracker; `P2-C01` rejected. |
| Local validated/recommended open total | `32233.920845392` | `P3-CAND-02 + P3-CAND-03-TOTAL` | Requires governance/committee acceptance. Case 4 is excluded from this rollup until the changed source amount is revalidated. |
| Pending estimate total, not final | `188292.871780174` | `P3-CAND-01 + P3-CAND-04 current source + P3-CAND-06` | Do not treat as payout until validation/scope/revalidation is complete. |
| P4 source aggregate | `946509.925002` | Full source package | Recorded for comparison only; current local position is to reject aggregate approval. |

## Source Pointers

- Calculation repo reconciliation: [`CALCULATION_REPO_RECONCILIATION.md`](CALCULATION_REPO_RECONCILIATION.md).
- Address/epoch overlap matrix: [`COMPENSATION_OVERLAP_MATRIX.md`](COMPENSATION_OVERLAP_MATRIX.md).
- Case/epoch crosstab: [`COMPENSATION_EPOCH_CROSSTAB.md`](COMPENSATION_EPOCH_CROSSTAB.md).
- Main public tracker: [`PUBLIC_COMPENSATION_TRACKER.md`](PUBLIC_COMPENSATION_TRACKER.md).
- Case 3 validation: [`validations/P3-CAND-03-failed-cpoc-epoch-267/README.md`](validations/P3-CAND-03-failed-cpoc-epoch-267/README.md).
- Case 4 validation: [`validations/P3-CAND-04-upgrade-protection-cpoc-misfire-epoch-276/README.md`](validations/P3-CAND-04-upgrade-protection-cpoc-misfire-epoch-276/README.md).
- Case 6 validation: [`validations/P3-CAND-06-pre-fix-confirmation-accounting/README.md`](validations/P3-CAND-06-pre-fix-confirmation-accounting/README.md).
- P4 split recommendation: [`validations/P4-CAND-01-kimi-restitution/p4_recommendation_draft.md`](validations/P4-CAND-01-kimi-restitution/p4_recommendation_draft.md).
- P4 attack summary: [`validations/P4-CAND-01-kimi-restitution/p4_attack_summary.md`](validations/P4-CAND-01-kimi-restitution/p4_attack_summary.md).
