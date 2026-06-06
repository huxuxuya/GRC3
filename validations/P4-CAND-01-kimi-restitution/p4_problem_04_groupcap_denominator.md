# P4 Problem 04: Epochs 267-276 GroupCap Denominator

## Question

If `ComputeGroupCap` is considered compensable, which counterfactual denominator
should be used for epochs `267..276`?

## Current Evidence

Primary local evidence:

- [`p4_audit_pass_06_e267_e276_groupcap.md`](p4_audit_pass_06_e267_e276_groupcap.md)
- [`p4_e267_e276_groupcap_denominator_check.csv`](p4_e267_e276_groupcap_denominator_check.csv)
- raw root group, Kimi model group, and performance summaries for epochs
  `267..276`
- copied source `GROUP_CAP.md` and compensation JSON/CSV files

## Findings

| Model | Total, GONKA | Meaning |
|---|---:|---|
| Source top-up / capped root denominator | `727,219.351170981` | Uses `confirmation_weight` as numerator but keeps the already-capped `root_total_weight` denominator. |
| All root confirmation denominator | `503,653.983658046` | Uses root `confirmation_weight` as both numerator basis and denominator basis. |
| Replace affected denominator | `360,858.547914700` | Replaces affected capped Kimi weight with affected confirmation weight and leaves the rest of the root denominator unchanged. |

## What Is Proven

- `ComputeGroupCap` / Kimi weight pressure is real chain state.
- The source affected rows match raw root `weight`, raw root
  `confirmation_weight`, and raw performance `rewarded_coins`.
- The source top-up formula is reproducible from saved raw data.

## What Is Not Proven

- That the source top-up denominator is the only chain-correct counterfactual.
- That an intended protocol cap should be treated as a compensable bug.
- That Qwen or non-Kimi paid rewards should be ignored when constructing the
  counterfactual denominator.

## Audit Remarks

| Remark | Issue | Impact |
|---|---|---|
| `P4-GC-01` | `ComputeGroupCap` appears to be an intended protocol rule, not a simple accidental accounting bug. | Compensability must be a committee policy decision before any amount is discussed. |
| `P4-GC-02` | The source denominator model is reproducible, but not unique. Pass 06 shows totals of `727,219.351170981`, `503,653.983658046`, or `360,858.547914700` GONKA under three defensible denominator choices. | The source total cannot be called the only chain-style settlement result. |
| `P4-GC-03` | Epoch `276` includes upgrade block `4,267,300` inside the epoch window. | Full-epoch e276 compensation is not automatically justified; full, prorated, or excluded treatment must be explicit. |

## Epoch 276 Proration Issue

Raw epoch `276` group data:

| Field | Value |
|---|---:|
| `effective_block_height` | `4,259,671` |
| upgrade block | `4,267,300` |
| `last_block_height` | `4,275,061` |
| pre-upgrade effective block share | `0.4957` |

The upgrade happened inside epoch `276`, so full-epoch e276 treatment needs an
explicit policy/proration decision.

## Recommended Handling

Do not approve the e267-e276 source total by default. First decide:

1. Is intended `ComputeGroupCap` compensable at all?
2. If yes, which denominator model is accepted?
3. Should epoch `276` be full, prorated, or excluded?

## Voting-Ready Options

| Option | Meaning |
|---|---|
| Reject GroupCap compensation | Treat `ComputeGroupCap` as intended protocol behavior and exclude e267-e276 from P4 payout. |
| Approve source top-up model | Accept capped-root denominator and source e267-e276 amount `727,219.351170981` GONKA, subject to e276 treatment. |
| Approve alternate denominator model | Accept compensation in principle but require a different denominator, such as all-root-confirmation or replace-affected denominator. |
| Defer GroupCap decision | Keep raw facts confirmed but postpone payout until compensability, denominator, and e276 proration are explicitly defined. |
