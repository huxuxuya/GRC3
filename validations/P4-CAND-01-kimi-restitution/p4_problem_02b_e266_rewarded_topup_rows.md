# P4 Problem 02b: Epoch 266 Rewarded Top-Up Rows

This note separates the 4 in-final-group rewarded reconstruction rows
from the 9 absent final-set operators in the epoch `266` nonce claim.

## Question

Should participants who entered the final group and already received
epoch `266` rewards receive an additional reconstruction top-up?

## Rows

| Address | Source models | Raw commits | Validation rows | Final weight | Confirmation weight | Actual reward | Source top-up | Top-up / actual | Conclusion |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu` | `Qwen/Qwen3-235B-A22B-Instruct-2507-FP8+moonshotai/Kimi-K2.6` | `212704` | `28` | `16888` | `19868` | `14350.368017242` | `42339.8862` | `2.9504` | `rewarded_in_final_group_reconstruction_topup_policy_required` |
| `gonka1wthc28t25pg63hzvl07rl8e8r6km6hesl6jhsz` | `Qwen/Qwen3-235B-A22B-Instruct-2507-FP8+moonshotai/Kimi-K2.6` | `90112` | `26` | `2528` | `2973` | `2148.136567242` | `26783.8997` | `12.4684` | `rewarded_in_final_group_reconstruction_topup_policy_required` |
| `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6` | `moonshotai/Kimi-K2.6` | `57532` | `9` | `282` | `331` | `239.625993655` | `18913.1494` | `78.9278` | `rewarded_in_final_group_reconstruction_topup_policy_required` |
| `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | `moonshotai/Kimi-K2.6` | `50880` | `17` | `6908` | `8127` | `5869.987107005` | `11068.2944` | `1.8856` | `rewarded_in_final_group_reconstruction_topup_policy_required` |

## Totals

| Quantity | GONKA |
|---|---:|
| Actual rewards already paid | `22608.117685144` |
| Source proposed top-up | `99105.2297` |
| Source implied post-top-up total | `121713.347385144` |

## Findings

- Rows checked: `4`
- All 4 rows were present in the final epoch group.
- All 4 rows already received non-zero rewards.
- None of the 4 rows is in `excluded_participants/266`.
- These rows are not final-set-exclusion victims. They are a
  reconstruction/top-up policy claim.

## Audit Remark

`P4-E266-TOPUP-01`: these rows should not be approved together with
the 9 absent operators unless the committee explicitly accepts
reconstruction top-ups for already rewarded participants.
