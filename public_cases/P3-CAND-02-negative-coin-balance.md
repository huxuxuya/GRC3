# P3-CAND-02: Negative Coin Balance / Settle-Drop

| Field | Value |
|---|---|
| Proposal | Proposal #3 candidate |
| Epochs | 1-274 in the published calculation |
| Status | Calculated; inclusion pending |
| Reported by | Evgenii Maksimenkov |
| Affected / detail contact | 19 miners; Evgenii Maksimenkov |
| Investigated by | Evgenii Maksimenkov |
| Result so far | Deterministic affected set and payout calculated |
| Further analysis | Required: independent validation and inclusion decision |
| Compensation | 1,075.336 GNK |

## Message Log

| Date | Author | Fact / short quote | Meaning |
|---|---|---|---|
| 2026-05-26 06:54 UTC+03 | Evgenii Maksimenkov | Introduced a recovery proposal initially covering unclaimed rewards. | Initial submission; scope later narrowed. |
| 2026-05-26 08:22 UTC+03 | Votkon | GRC should restitute rewards lost due to confirmed protocol issues. | Scope requirement: exclude normal unclaimed cases. |
| 2026-05-26 09:23 UTC+03 | Evgenii Maksimenkov | "only 19 participants remain" affected by the specific bug. | Narrow deterministic affected set. |
| 2026-05-26 16:21 UTC+03 | Evgenii Maksimenkov | Shared PR #826 and PR #550. | Referenced issue/fix sources. |

## Findings

- A participant is included when rewards were calculated but no `SettleAmount` entry existed at settlement.
- Published result: `19` miners and `1,075.336 GNK`.
- The method uses historical on-chain state from an archive node.

## Sources

- [Calculation repository](https://github.com/gonkavip/unclaimed)
- [PR #826](https://github.com/gonka-ai/gonka/pull/826)
- [PR #550](https://github.com/gonka-ai/gonka/pull/550)
