# OBS-02: Post-cPoC Re-Entry Failure Report

| Field | Value |
|---|---|
| Classification | Additional observation; not proposed for compensation |
| Date reported | 2026-05-27 |
| Reported by | Mykola |
| Known affected | Not identified in the reviewed message |
| Reported impact | A node removed during cPoC did not return at the start of the next epoch |
| Compensation evidence | No address, amount or proven relation to an existing case |
| Action status | Triage only |

## Evidence

| Message ID | Date (UTC+03) | Author | Fact |
|---|---|---|---|
| `16120` | 2026-05-27 16:47:29 | Mykola | Reported that a node removed from an epoch during cPoC did not return in the next epoch despite previously operating for many epochs. |

## Key Excerpt

**Message `16120`, Mykola - original Russian**

> Вчера выпала из эпохи вместе с другими участниками на cPoC. Я ожидал что она вернется с началом новой эпохи, потому что там стояла только квен мл нода отработавшая десятки эпох, но нет. Разбираюсь в чем дело.

**English translation**

> Yesterday it dropped out of the epoch together with other participants during cPoC. I expected it to return at the beginning of the new epoch because it only had a Qwen ML node that had operated for dozens of epochs, but it did not. I am investigating the cause.

## Assessment

This may be related to the epoch 276 cPoC incident or may be separate. No participant address, loss amount or root cause is provided, so it remains an observation pending triage.

## Mitigation / Fix Status

No code mitigation can be linked until the participant address and root cause are identified. If this is shown to result from the epoch 276 `LastUpgradeHeight` misfire, it should be connected to `P3-CAND-04`; no separate fix schedule is currently established.
