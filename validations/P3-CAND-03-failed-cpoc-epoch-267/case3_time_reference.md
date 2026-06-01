# Case 3 Time Reference

Block timestamps were read from the configured archive LCD via:

```text
/cosmos/base/tendermint/v1beta1/blocks/{height}
```

The chain block header time is UTC. MSK is shown as UTC+03:00.

## Epoch Boundaries

`poc_start_block_height` and `effective_block_height` are both included because
they mark different chain fields in `epoch_group_data`.

| Epoch | Boundary | Height | UTC | MSK |
|---:|---|---:|---|---|
| `265` | PoC start | `4,089,970` | `2026-05-15 22:48:39 UTC` | `2026-05-16 01:48:39 MSK` |
| `265` | Effective start | `4,090,370` | `2026-05-15 23:22:59 UTC` | `2026-05-16 02:22:59 MSK` |
| `265` | Last block | `4,105,760` | `2026-05-16 21:04:58 UTC` | `2026-05-17 00:04:58 MSK` |
| `267` | PoC start | `4,120,752` | `2026-05-17 18:17:36 UTC` | `2026-05-17 21:17:36 MSK` |
| `267` | Effective start | `4,121,152` | `2026-05-17 18:51:44 UTC` | `2026-05-17 21:51:44 MSK` |
| `267` | Last block | `4,136,542` | `2026-05-18 16:48:56 UTC` | `2026-05-18 19:48:56 MSK` |

## Case Events

| Epoch | Event | Height | UTC | MSK |
|---:|---|---:|---|---|
| `265` | cPoC #0 trigger | `4,095,682` | `2026-05-16 06:55:01 UTC` | `2026-05-16 09:55:01 MSK` |
| `265` | cPoC #1 trigger | `4,098,879` | `2026-05-16 11:26:01 UTC` | `2026-05-16 14:26:01 MSK` |
| `265` | cPoC #2 trigger / failure window | `4,102,890` | `2026-05-16 17:05:17 UTC` | `2026-05-16 20:05:17 MSK` |
| `265` | Same-claimant exclusion | `4,103,171` | `2026-05-16 17:29:07 UTC` | `2026-05-16 20:29:07 MSK` |
| `267` | cPoC #1 trigger / episode anchor | `4,122,271` | `2026-05-17 20:27:55 UTC` | `2026-05-17 23:27:55 MSK` |
| `267` | cPoC #1 validation snapshot | `4,122,312` | `2026-05-17 20:31:29 UTC` | `2026-05-17 23:31:29 MSK` |
| `267` | Claimant exclusion | `4,122,552` | `2026-05-17 20:52:06 UTC` | `2026-05-17 23:52:06 MSK` |
| `267` | cPoC #2 trigger | `4,130,085` | `2026-05-18 07:36:38 UTC` | `2026-05-18 10:36:38 MSK` |
| `267` | cPoC #3 trigger | `4,133,665` | `2026-05-18 12:43:06 UTC` | `2026-05-18 15:43:06 MSK` |
| `267` | cPoC #4 trigger | `4,134,529` | `2026-05-18 13:56:57 UTC` | `2026-05-18 16:56:57 MSK` |

## Fix Deployment

The applied on-chain upgrade plan reports:

```text
/cosmos/upgrade/v1beta1/applied_plan/v0.2.13 -> height 4,267,300
```

| Item | Height | UTC | MSK |
|---|---:|---|---|
| Epoch `276` effective start | `4,259,671` | `2026-05-26 03:34:34 UTC` | `2026-05-26 06:34:34 MSK` |
| `v0.2.13` applied on-chain | `4,267,300` | `2026-05-26 14:39:41 UTC` | `2026-05-26 17:39:41 MSK` |
| Epoch `276` last block | `4,275,061` | `2026-05-27 02:12:27 UTC` | `2026-05-27 05:12:27 MSK` |
| Epoch `277` effective start | `4,275,062` | `2026-05-27 02:12:33 UTC` | `2026-05-27 05:12:33 MSK` |

The fix was installed on-chain at block `4,267,300`, during epoch `276`.
The `v0.2.13` upgrade disables confirmation PoC triggers for the rest of the
upgrade epoch, so the new confirmation snapshot logic starts cleanly from epoch
`277`.
