# P3-CAND-06 Epoch 276 Overlap Deep Dive

This note isolates the four P3-CAND-06 rows from epoch `276`.

Epoch `276` is not a normal pre-fix-only window. It overlaps `P3-CAND-04`,
where the local case dossier describes a `v0.2.13` upgrade-protection/cPoC
misfire affecting `19` miners.

## Current Classification

| Participant | Pass model(s) | Loss, GONKA | Old formula match | Bounded v0.2.13-style pass alpha | Local overlap status |
|---|---|---:|---|---|---|
| `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | Qwen+Kimi | `17,356.095656742` | False | False | Known P3-CAND-04 same-address overlap |
| `gonka14tqh62mangwzrma2lgg2dm375rcjzn2ydy8ttm` | Kimi | `11,765.489995489` | False | False | Epoch-level P3-CAND-04 overlap unresolved |
| `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e` | Qwen | `3,557.528990032` | True | False | Epoch-level P3-CAND-04 overlap unresolved |
| `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | Kimi | `10,120.274911440` | True | False | Epoch-level P3-CAND-04 overlap unresolved |

## Why Epoch 276 Is Blocked

- The P3-CAND-04 dossier says epoch `276` has a separate upgrade-protection
  cPoC misfire calculation with `19` affected miners and `36,209.451 GNK`.
- The P3-CAND-06 local evidence has only one known same-address overlap:
  `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09`.
- The full `payout276` address list is not normalized in this repository, so
  the other three epoch `276` rows cannot be cleared locally.
- One epoch `276` row has both Qwen and Kimi `pass_weight`, but the old-formula
  replay does not match the stored ratio. That is a technical reason to keep it
  separate from the formula-reconciled single-model rows.

## Working Rule

All four epoch `276` rows are blocked from P3-CAND-06 payout until P3-CAND-04
is independently validated and duplicate risk is resolved.

They should be handled as:

```text
P3-CAND-06 technical evidence: keep
P3-CAND-06 payout eligibility: blocked pending P3-CAND-04 overlap
```

## Required External Input

To clear or reject these rows, import or reproduce the normalized P3-CAND-04
`payout276` table with:

- participant address;
- dropped/reduced category;
- lost confirmation weight;
- compensation amount;
- source block heights.

Then compare by:

```text
participant + epoch + loss source
```

Rows with the same economic loss source must not be paid twice.
