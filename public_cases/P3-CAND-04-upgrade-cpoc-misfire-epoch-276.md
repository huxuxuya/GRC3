# P3-CAND-04: UpgradeProtectionWindow / CPoC Misfire

| Field | Value |
|---|---|
| Proposal | Proposal #3 candidate |
| Epochs | 276 |
| Status | Calculated; inclusion pending |
| Reported by | Votkon; calculation by Evgenii Maksimenkov |
| Affected / detail contact | 19 miners; Evgenii Maksimenkov |
| Investigated by | Evgenii Maksimenkov; initial reproduction by Nik |
| Result so far | Calculation published and reproduced once |
| Further analysis | Required: independent validation and inclusion decision |
| Compensation | 36,209.451 GNK |

## Message Log

| Date | Author | Fact / short quote | Meaning |
|---|---|---|---|
| 2026-05-26 21:54 UTC+03 | Votkon | `LastUpgradeHeight` was not recorded after v0.2.13. | Stated root cause for unintended cPoC execution. |
| 2026-05-27 06:18 UTC+03 | Evgenii Maksimenkov | "7 participants were affected and dropped out" | Initial dropped-participant scope. |
| 2026-05-27 10:12 UTC+03 | Evgenii Maksimenkov | Published the calculation script and total. | Calculation available for review. |
| 2026-05-27 12:09 UTC+03 | Nik | Script ran without errors and amount matched. | One reproduction reported. |

## Findings

- Published calculation includes `7` dropped miners and `12` miners with reduced confirmation weight.
- Total calculated payout: `36,209.451 GNK`.
- Inputs are archive-node snapshots at fixed historical block heights.

## Sources

- [Calculation repository](https://github.com/gonkavip/payout276)
- [Upgrade proposal #54](https://gonka.gg/network/proposals/54)
