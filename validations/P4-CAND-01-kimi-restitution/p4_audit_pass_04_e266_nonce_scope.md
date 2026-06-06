# P4 Conceptual Audit Pass 04: Epoch 266 Nonce Scope

This pass checks the conceptual scope of the epoch `266` nonce claim.
It does not reproduce the investigator arithmetic and does not approve
the compensation amount.

## Raw And Source Inputs

- Raw chain commit store: `archive_cli_height_4120751_all_poc_v2_store_commits_4105361_stdout.json`
- Raw chain validation records: `archive_cli_height_4120751_poc_v2_validations_for_stage_4105361_stdout_retry2.json`
- Raw final epoch group/performance/exclusion files for epoch `266`
- Source claim artifacts copied from the pinned Votkon repository under `source_cache/`

Important limitation: the independent raw archive CLI commit output has
`participant_address`, `count`, `root_hash`, and `hex_pub_key`, but no
`model_id`. The source artifact has `model_id`; those labels are treated
as source claims, not chain-only proof.

## Commit Artifact Match

- Raw commit rows: `44`
- Source commit rows: `44`
- Source rows with exact raw match by address/count/root/pubkey: `44`
- Raw rows with exact source match by address/count/root/pubkey: `44`

## Source Nonce Compensation Rows

- Source nonce-compensation rows: `18`
- Rows also listed as excluded operators: `9`
- Rows that were in the final group and already rewarded: `4`
- Rows that were in the final group but zero reward: `5`

## Excluded Operators

| Address | Source Kimi commits | Raw commit count | Raw validation rows | Final group | Performance row | Source compensation |
|---|---:|---:|---:|---|---|---:|
| `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `89984` | `89984` | `17` | no | no | `29956.2563` |
| `gonka1qa90tgczc0k5dvk4l5nvlf5y6phgm6mg22sfjv` | `55552` | `55552` | `17` | no | no | `18493.6205` |
| `gonka1jrgm47v5eg876udmzg6j6glqcsd5x0vk6crpax` | `25664` | `25664` | `17` | no | no | `8543.7118` |
| `gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds` | `12896` | `12896` | `17` | no | no | `4293.1619` |
| `gonka1c6fwzedfsmpu4jnjekv4cn7mvr7x7fuqd6uqt9` | `12384` | `12384` | `17` | no | no | `4122.7138` |
| `gonka1wkgawwdzj623ss8eywayzdj6qcgr2llygactje` | `6496` | `6496` | `17` | no | no | `2162.5605` |
| `gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d` | `6080` | `6080` | `17` | no | no | `2024.0714` |
| `gonka125n6kr5gvdup0lndfkps7t6rd6592panhrg3np` | `6048` | `6048` | `17` | no | no | `2013.4184` |
| `gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw` | `5664` | `5664` | `17` | no | no | `1885.5823` |

## Non-Excluded Top-Up Rows

| Address | Source models | Final weight | Actual rewards (GONKA) | Source compensation | Classification |
|---|---|---:|---:|---:|---|
| `gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu` | `Qwen/Qwen3-235B-A22B-Instruct-2507-FP8+moonshotai/Kimi-K2.6` | `16888` | `14350.368017242` | `42339.8862` | `in_final_group_rewarded_reconstruction_top_up` |
| `gonka1wthc28t25pg63hzvl07rl8e8r6km6hesl6jhsz` | `Qwen/Qwen3-235B-A22B-Instruct-2507-FP8+moonshotai/Kimi-K2.6` | `2528` | `2148.136567242` | `26783.8997` | `in_final_group_rewarded_reconstruction_top_up` |
| `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6` | `moonshotai/Kimi-K2.6` | `282` | `239.625993655` | `18913.1494` | `in_final_group_rewarded_reconstruction_top_up` |
| `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | `moonshotai/Kimi-K2.6` | `6908` | `5869.987107005` | `11068.2944` | `in_final_group_rewarded_reconstruction_top_up` |

## In-Final-Group Zero-Reward Rows

| Address | Source models | Final weight | Source compensation | Status |
|---|---|---:|---:|---|
| `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | `moonshotai/Kimi-K2.6` | `2009` | `7414.4930` | `needs_cause_policy` |
| `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e` | `Qwen/Qwen3-235B-A22B-Instruct-2507-FP8+moonshotai/Kimi-K2.6` | `1538` | `2529.4500` | `needs_cause_policy` |
| `gonka13a4v8gxxjav5t4xq5y9cv9d8rfnvkjfw5adqz3` | `Qwen/Qwen3-235B-A22B-Instruct-2507-FP8` | `1568` | `521.6378` | `needs_cause_policy` |
| `gonka1myu058axjs62mc3e7na9krwvqpfl9z3gtcw9es` | `Qwen/Qwen3-235B-A22B-Instruct-2507-FP8` | `709` | `279.0156` | `needs_cause_policy` |
| `gonka14ef2pxjge75gflqftn7m2wy0xv59gq9uc7qnct` | `Qwen/Qwen3-235B-A22B-Instruct-2507-FP8` | `156` | `260.8189` | `needs_cause_policy` |

## Interpretation

- The narrow e266 claim that nine listed addresses submitted PoC commits
  and were absent from the final epoch group remains confirmed by raw
  chain data.
- The Kimi-specific label for those commits is not proven by the raw CLI
  output alone. The Votkon source artifact labels the matching commit
  rows as Kimi, and those rows match our raw commit rows exactly by
  address/count/root/pubkey, but that is source-backed evidence rather
  than a chain-only model-id proof.
- The source nonce-compensation table contains more than the nine excluded
  operators: it also compensates participants that were in the final group
  and already received rewards. Those rows are reconstruction/top-up policy
  rows, not final-set-exclusion victims.
- Delegation compensation is a separate policy track. It depends on accepting
  the excluded-operator event as compensable and on accepting indirect
  delegator losses.
