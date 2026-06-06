# P4 Recommendation Draft

## Verdict

Do not approve P4 as a single aggregate payout of `946,509.925002 GONKA`.

The source package is useful evidence, but it combines different technical and
policy classes:

- epoch `265` direct cPoC / attack-attributed rows;
- epoch `266` nonce exclusion, zero-reward rows, rewarded top-up rows, and
  delegation loss;
- epochs `267..276` `ComputeGroupCap` top-up.

These tracks need separate decisions.

## Confirmed Technical Facts

| Track | Confirmed facts |
|---|---|
| e265 | One row, `gonka1j7x6...`, matches the Case 3 direct Kimi cPoC shortfall class. |
| e266 excluded operators | 9 source-listed operators had raw PoC commits and raw validation records, but no final epoch-group or performance row. |
| e266 delegation | 9 source-listed delegators had raw Kimi delegation to excluded operator `gonka1q5xt54...`; chain params support the `0.15 - 0.05 = 0.10` mechanical delta. |
| e267-e276 GroupCap | Cap effect and source rows are confirmed from raw chain data; source top-up formula is reproducible. |

## Blocking Remarks

| Remark | Meaning |
|---|---|
| `P4-E266-ZR-01` | 5 e266 zero-reward rows are in-final-group `failed_confirmation_poc`, not absent final-set operators. |
| `P4-E266-TOPUP-01` | 4 e266 rows already received rewards and are reconstruction/top-up policy rows, not exclusion victims. |
| `P4-GC-01` | `ComputeGroupCap` appears to be intended protocol behavior; compensability must be decided. |
| `P4-GC-02` | GroupCap denominator model is unresolved; checked totals vary materially by model. |
| `P4-GC-03` | Epoch `276` upgrade was inside the epoch; full/prorated/excluded treatment must be explicit. |

## Recommended Committee Decision Shape

Do not vote on "P4 total yes/no" as one number.

Use separate decisions:

1. Keep the confirmed e265 `gonka1j7...` row in Case 3 scope.
2. Vote separately on whether the 9 e266 absent operators are compensable.
3. Vote separately on whether e266 zero-reward rows are compensable.
4. Vote separately on whether e266 rewarded reconstruction top-ups are
   compensable.
5. Vote separately on whether e266 indirect delegator losses are compensable.
6. Vote separately on whether e267-e276 intended GroupCap effects are
   compensable.
7. If GroupCap is compensable, select a denominator model and e276 treatment.

## GroupCap Options

| Option | Meaning |
|---|---|
| Reject GroupCap compensation | Treat `ComputeGroupCap` as intended protocol behavior and exclude e267-e276 from payout. |
| Approve source top-up model | Accept capped-root denominator and source e267-e276 amount `727,219.351170981` GONKA, subject to e276 treatment. |
| Approve alternate denominator model | Accept compensation in principle but require a different denominator, such as all-root-confirmation or replace-affected denominator. |
| Defer GroupCap decision | Keep raw facts confirmed but postpone payout until compensability, denominator, and e276 proration are defined. |

## Recommended Public Summary

The P4 source repository contains real evidence and several reproducible
components, but the package is too broad to approve as one compensation case.
The aggregate amount depends on unresolved policy decisions: external-attack
scope, indirect delegator eligibility, already-rewarded top-ups, intended
`ComputeGroupCap` compensability, denominator choice, and epoch `276` proration.

Recommended position: confirm the evidence, reject aggregate approval, and split
P4 into separate committee decisions.
