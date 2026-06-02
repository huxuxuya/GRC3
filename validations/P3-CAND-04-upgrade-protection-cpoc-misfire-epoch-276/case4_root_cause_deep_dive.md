# P3-CAND-04 Root-Cause Deep Dive

## Conclusion

The compensation set is independently proven by archive-chain replay.
The most likely root cause is also strongly supported: the `v0.2.13`
upgrade was intended to suppress confirmation PoC through the upgrade
epoch, but the `LastUpgradeHeight` state key was not populated, so the
skip condition did not activate and two post-upgrade cPoC stages ran in
epoch 276.

## Evidence Chain

| Link | Evidence |
|---|---|
| Expected behavior | PR #1143: https://github.com/gonka-ai/gonka/pull/1143 |
| Release-note behavior | https://gonka.ai/release-announcements/ describes skipping confirmation PoC from upgrade height through the upgrade epoch |
| Chain execution | Post-upgrade cPoC triggers `4267778` and `4270605` ran inside epoch `276` |
| State key | `LastUpgradeHeight` key `0x1b` is queried directly through `abci_query` |
| Code fix | PR #1268: https://github.com/gonka-ai/gonka/pull/1268 tracks `LastUpgradeHeight` from upgrade handlers and adds tests on branch https://github.com/gonka-ai/gonka/tree/upgrade-v0.2.14 |

## LastUpgradeHeight State Query

| Requested height | Response height | Key base64 | Value base64 | Null | Status | RPC source |
|---:|---:|---|---|---:|---|---|
| `latest` | `4377778` | `Gw==` | `` | `1` | `ok` | `default_node1` |
| `4267299` | `4267299` | `Gw==` | `` | `1` | `ok` | `default_node1` |
| `4267300` | `4267300` | `Gw==` | `` | `1` | `ok` | `default_node1` |
| `4267778` | `4267778` | `Gw==` | `` | `1` | `ok` | `default_node1` |
| `4270605` | `4270605` | `Gw==` | `` | `1` | `ok` | `default_node1` |
| `4274661` | `4274661` | `Gw==` | `` | `1` | `ok` | `default_node1` |

Latest-chain null proof:
`latest_null_confirmed = True`.

Historical null proof for all checked heights: `True`.

## Why Epoch 276 Only

`v0.2.13` was applied at block `4267300`, while epoch `276` spans
`4259271..4275061`. That makes epoch `276` the only upgrade epoch.
Epochs before it were pre-upgrade controls. Epoch `277` and later are
post-upgrade clean epochs; cPoC there is not the same upgrade-window
misfire.

| Epoch | Trigger | Blocks after upgrade | Case4-like misfire | Interpretation |
|---:|---:|---:|---:|---|
| `276` | `4267778` | `478` | `1` | post-upgrade cPoC inside upgrade epoch; expected skip under release-note behavior |
| `276` | `4270605` | `3305` | `1` | post-upgrade cPoC inside upgrade epoch; expected skip under release-note behavior |

## Strength And Remaining Limits

- Strong: affected rows and amounts match the published CSV exactly from independent archive-chain state.
- Strong: two post-upgrade cPoC stages are directly visible inside the upgrade epoch.
- Strong: historical and current chain state return null for the `LastUpgradeHeight` key at all checked heights.
- Strong: PR #1268 changes future full upgrades to record `LastUpgradeHeight` from the upgrade handler and tests full/partial upgrade tracking.
- Limit: PR #1268 is merged to `upgrade-v0.2.14`; public releases checked still showed latest release `v0.2.13`, so on-chain deployment must be confirmed separately.
