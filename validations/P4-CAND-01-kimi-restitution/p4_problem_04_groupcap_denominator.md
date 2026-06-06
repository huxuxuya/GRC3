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
