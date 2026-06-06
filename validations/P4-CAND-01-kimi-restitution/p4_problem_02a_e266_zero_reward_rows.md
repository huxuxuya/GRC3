# P4 Problem 02a: Epoch 266 Zero-Reward Rows

This note separates the 5 in-final-group zero-reward rows from the 9
absent final-set operators in the epoch `266` nonce claim.

## Question

Are these rows direct victims of the e266 nonce incident, or ordinary
`failed_confirmation_poc` rows that need separate policy/cause proof?

## Evidence Inputs

- Raw e266 commit store at stage `4105361`
- Raw e266 validation records at stage `4105361`
- Raw final epoch group `266`
- Raw epoch performance summary `266`
- Raw excluded participants `266`
- Source commit labels and source nonce compensation table from pinned
  Votkon repository

## Rows

| Address | Source models | Raw commits | Validation rows | Full commit-count validations | Final weight | Confirmation weight | Excluded reason | Reward | Source comp | Conclusion |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|---|
| `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | `moonshotai/Kimi-K2.6` | `22272` | `17` | `1` | `2009` | `0` | `failed_confirmation_poc` | `0.000000000` | `7414.4930` | `kimi_zero_reward_row_not_absent_operator_needs_cause_policy` |
| `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e` | `Qwen/Qwen3-235B-A22B-Instruct-2507-FP8+moonshotai/Kimi-K2.6` | `10528` | `45` | `2` | `1538` | `0` | `failed_confirmation_poc` | `0.000000000` | `2529.4500` | `mixed_kimi_qwen_zero_reward_row_not_same_as_absent_operator` |
| `gonka13a4v8gxxjav5t4xq5y9cv9d8rfnvkjfw5adqz3` | `Qwen/Qwen3-235B-A22B-Instruct-2507-FP8` | `5504` | `29` | `1` | `1568` | `0` | `failed_confirmation_poc` | `0.000000000` | `521.6378` | `not_kimi_zero_reward_row_qwen_only_policy_required_if_broadened` |
| `gonka1myu058axjs62mc3e7na9krwvqpfl9z3gtcw9es` | `Qwen/Qwen3-235B-A22B-Instruct-2507-FP8` | `2944` | `1` | `1` | `709` | `0` | `failed_confirmation_poc` | `0.000000000` | `279.0156` | `not_kimi_zero_reward_row_qwen_only_policy_required_if_broadened` |
| `gonka14ef2pxjge75gflqftn7m2wy0xv59gq9uc7qnct` | `Qwen/Qwen3-235B-A22B-Instruct-2507-FP8` | `2752` | `27` | `1` | `156` | `0` | `failed_confirmation_poc` | `0.000000000` | `260.8189` | `not_kimi_zero_reward_row_qwen_only_policy_required_if_broadened` |

## Findings

- Rows checked: `5`
- Kimi or mixed Kimi rows by source label: `2`
- Qwen-only rows by source label: `3`
- All 5 rows are present in final epoch group `266`.
- All 5 rows have `confirmation_weight=0`, `rewarded_coins=0`, and
  excluded reason `failed_confirmation_poc`.
- These rows are not the same class as the 9 absent operators: they
  reached the final group and then failed confirmation.

## Interpretation

The raw data confirms submissions and validation records, but does not
prove that these zero-reward rows are direct victims of the same incident
as the absent operators. They should remain a separate row-level cause
and policy question.
