# P3-CAND-04 Upgrade Protection Evidence

`v0.2.13` upgrade height: `4267300` / `2026-05-26 17:39:41 MSK`.

| Item | Value |
|---|---:|
| Chain `confirmation_poc_params.upgrade_protection_window` at upgrade height | `500` blocks |
| Reported release-note protection window | `10000` blocks |

## Post-Upgrade cPoC Stages

| cPoC trigger | Blocks after upgrade | Inside chain-param window | Inside reported 10000-block window | Excluded at stage |
|---:|---:|---|---|---:|
| `4267778` | `478` | `True` | `True` | `5` |
| `4270605` | `3305` | `False` | `True` | `2` |

DevOps evidence states `LastUpgradeHeight` was not written after the
upgrade, so the cPoC skip did not apply. The chain evidence above
confirms cPoC stages did run after the upgrade inside epoch 276.
