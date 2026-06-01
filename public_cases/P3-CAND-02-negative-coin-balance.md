# P3-CAND-02: Negative Coin Balance / Settle-Drop

| Field | Value |
|---|---|
| Proposal | Proposal #3 candidate |
| Epochs | 1-274 in the published calculation |
| Status | Calculated; inclusion pending |
| Reported by | Evgenii Maksimenkov |
| Affected / detail contact | 19 miners; Evgenii Maksimenkov |
| Case investigator | @maksimenkoff; calculation: [gonkavip/unclaimed](https://github.com/gonkavip/unclaimed) |
| Case validator | @dem_ww |
| Result so far | Deterministic affected set and payout calculated |
| Further analysis | Required: independent validation and inclusion decision |
| Compensation | 1,075.336 GNK |
| Lost reward destination | Rewards were computed but no `SettleAmount` claim ticket was written; the published calculation states they were eventually swept into the gov module account. |

## Message Log

| Date | Author | Fact / short quote | Meaning |
|---|---|---|---|
| 2026-05-26 06:54 UTC+03 | Evgenii Maksimenkov | Introduced a recovery proposal initially covering unclaimed rewards. | Initial submission; scope later narrowed. |
| 2026-05-26 08:22 UTC+03 | Votkon | GRC should restitute rewards lost due to confirmed protocol issues. | Scope requirement: exclude normal unclaimed cases. |
| 2026-05-26 08:31 UTC+03 | Evgenii Maksimenkov | Scope filters would keep only participants assigned rewards whose claim failed with "No rewards for this address". | Method narrowed to the settle-drop path. |
| 2026-05-26 09:23 UTC+03 | Evgenii Maksimenkov | "only 19 participants remain" affected by the specific bug. | Narrow deterministic affected set. |
| 2026-05-26 16:21 UTC+03 | Evgenii Maksimenkov | Shared PR #826 and PR #550. | Referenced issue/fix sources. |

## Findings

- A participant is included when rewards were calculated but no `SettleAmount` entry existed at settlement.
- The broader first-pass scan found 576 participants with assigned but unclaimed rewards for any reason; after checking for a missing post-settlement `SettleAmount`, 19 remained in the deterministic bug scope.
- Published result: `19` miners and `1,075.336 GNK`.
- The method uses historical on-chain state from an archive node.

## Mitigation / Fix Status

| Item | Status |
|---|---|
| Direct settle fix | PR [`#550`](https://github.com/gonka-ai/gonka/pull/550), `Negative coin balance for settle`, changes settlement handling for negative balances and was merged on 2026-01-13. |
| Related reward-loss fix | PR [`#826`](https://github.com/gonka-ai/gonka/pull/826) proposes retaining `SettleAmount` after partial claim payment failures; it was closed on 2026-04-27 without merge. |
| Timing | The negative-balance settlement fix is merged. No deployed correction is established here for the separate unmerged partial-payment path in `#826`. |

## Reward Flow

This case is not redistribution through reduced reward weight. The chain recorded positive `rewarded_coins` but skipped creation of the claimant's `SettleAmount`. The calculation repository states that such inaccessible rewards are eventually swept into the governance module account by `TransferOldSettleAmountsToGovernance`.

## Sources

- [Calculation repository](https://github.com/gonkavip/unclaimed)
- [GRC chat update export index](sources/GRC-chat-update-2026-06-01.md)
- [PR #826](https://github.com/gonka-ai/gonka/pull/826)
- [PR #550](https://github.com/gonka-ai/gonka/pull/550)
