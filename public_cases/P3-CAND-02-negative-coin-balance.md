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
| Result so far | Published affected set and payout calculated; independent first-pass and code audit completed |
| Further analysis | Required: archive-node validation of historical `SettleAmount` state and inclusion decision |
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
- Independent first-pass scan on 2026-06-01 did not use the published script or CSV. It queried `epoch_performance_summary` directly for epochs `1-280`.
- That independent first pass found `823` rows with `rewarded_coins > 0` and `claimed = false` in epochs `1-274`, including ordinary missed claims. The broad result confirms that `EpochPerformanceSummary` alone cannot identify Case 2 compensation recipients.
- In the current tail `275-280`, the independent scan found `0` rows with positive unclaimed rewards.
- Independent historical `SettleAmount` validation is currently blocked because public `node1`, `node2`, and `node3` do not retain the required old state; `rpc.gonka.gg` requires an API key.

## Independent Audit Snapshot

| Range | Positive unclaimed rows from direct summary scan | Positive unclaimed reward | Interpretation |
|---|---:|---:|---|
| `1-274` | 823 | 1,427,305.676769 GNK | Broad unclaimed-positive universe; not the compensation set. |
| `87-142` | 471 | 127,838.757296 GNK | Wide window around known Case 2 epochs. |
| `133-274` | 185 | 131,513.967332 GNK | Post-fix summary rows exist, but summary data alone cannot classify them as bug recurrence. |
| `275-280` | 0 | 0 GNK | No positive unclaimed rows in the current tail checked. |

The independent compensation criterion still requires an archive-node lookup of `settle_amount` at the `effective_block_height` of epoch `N+1`. Without that historical state, the published 19-row set remains a calculated claim requiring independent archive validation rather than a fully independently confirmed result.

## Mitigation / Fix Status

| Item | Status |
|---|---|
| Direct settle fix | PR [`#550`](https://github.com/gonka-ai/gonka/pull/550), `Negative coin balance for settle`, was merged on 2026-01-13 as commit [`8184fe3`](https://github.com/gonka-ai/gonka/commit/8184fe3501629d1051d1d14b31e7c47c01f7615d) into milestone `v0.2.8`. |
| Current code status | Current `main` subtracts negative `CoinBalance` debt from `RewardCoins` when the reward covers the debt. If debt exceeds reward, `RewardCoins` becomes `0` and `ErrNegativeCoinBalance` remains. |
| Related claim-time path | PR [`#826`](https://github.com/gonka-ai/gonka/pull/826) describes partial claim payment failure and was closed on 2026-04-27 without merge. Current `main` uses `CacheContext` in `payoutClaim`, so payout failure does not commit `finishSettle`; this is separate from the settlement-time Case 2 path. |
| Timing | The negative-balance settlement fix is present in current code. No positive unclaimed rows were found in epochs `275-280`; full post-fix settle-drop exclusion still requires archive `SettleAmount` state. |

## Reward Flow

This case is not redistribution through reduced reward weight. The chain recorded positive `rewarded_coins` but skipped creation of the claimant's `SettleAmount`. The calculation repository states that such inaccessible rewards are eventually swept into the governance module account by `TransferOldSettleAmountsToGovernance`.

## Sources

- [Calculation repository](https://github.com/gonkavip/unclaimed)
- [Independent audit notes](sources/P3-CAND-02-independent-audit.md)
- [GRC chat update export index](sources/GRC-chat-update-2026-06-01.md)
- [PR #826](https://github.com/gonka-ai/gonka/pull/826)
- [PR #550](https://github.com/gonka-ai/gonka/pull/550)
