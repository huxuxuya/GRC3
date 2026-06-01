# P3-CAND-02: Negative Coin Balance / Settle-Drop

| Field | Value |
|---|---|
| Proposal | Proposal #3 candidate |
| Epochs | 1-274 in the published calculation |
| Status | Coordinator validated; inclusion pending |
| Reported by | Evgenii Maksimenkov |
| Affected / detail contact | 19 miners; Evgenii Maksimenkov |
| Case investigator | @maksimenkoff; calculation: [gonkavip/unclaimed](https://github.com/gonkavip/unclaimed) |
| Case validator | @dem_ww |
| Result so far | Proposal coordinator validated the independent archive result: 19 affected rows, exact match to the published calculation |
| Further analysis | Required: governance inclusion decision |
| Compensation | 1,075.336150923 GNK |
| Lost reward destination | Rewards were computed but no `SettleAmount` claim ticket was written; the published calculation states they were eventually swept into the gov module account. |

## Message Log

| Date | Author | Fact / short quote | Meaning |
|---|---|---|---|
| 2026-05-26 06:54 UTC+03 | Evgenii Maksimenkov | Introduced a recovery proposal initially covering unclaimed rewards. | Initial submission; scope later narrowed. |
| 2026-05-26 08:22 UTC+03 | Votkon | GRC should restitute rewards lost due to confirmed protocol issues. | Scope requirement: exclude normal unclaimed cases. |
| 2026-05-26 08:31 UTC+03 | Evgenii Maksimenkov | Scope filters would keep only participants assigned rewards whose claim failed with "No rewards for this address". | Method narrowed to the settle-drop path. |
| 2026-05-26 09:23 UTC+03 | Evgenii Maksimenkov | "only 19 participants remain" affected by the specific bug. | Narrow deterministic affected set. |
| 2026-05-26 16:21 UTC+03 | Evgenii Maksimenkov | Shared PR #826 and PR #550. | Referenced issue/fix sources. |
| 2026-06-01 | @OpenMindedPerson | Proposal coordinator validated Case 2 archive-check result: 19 affected addresses, `1,075.336150923 GNK`, and no additional settle-drop candidates in the checked range. | Coordinator validation confirms the independently reproduced result; governance inclusion decision remains. |

## Findings

- A participant is included when rewards were calculated but no `SettleAmount` entry existed at settlement.
- The broader first-pass scan found 576 participants with assigned but unclaimed rewards for any reason; after checking for a missing post-settlement `SettleAmount`, 19 remained in the deterministic bug scope.
- Published result: `19` miners and `1,075.336150923 GNK`.
- The method uses historical on-chain state from an archive node.
- Independent first-pass scan on 2026-06-01 did not use the published script or CSV. It queried `epoch_performance_summary` directly for epochs `1-280`.
- That independent first pass found `823` rows with `rewarded_coins > 0` and `claimed = false` in epochs `1-274`, including ordinary missed claims. The broad result confirms that `EpochPerformanceSummary` alone cannot identify Case 2 compensation recipients.
- In the current tail `275-280`, the independent scan found `0` rows with positive unclaimed rewards.
- Public `node1`, `node2`, and `node3` did not retain the required old `SettleAmount` state, and authenticated `rpc.gonka.gg` gateway access did not expose it either.
- A local archive LCD configured through `.env` was validated on 2026-06-01. The endpoint and key are not tracked in git; sanitized results are stored in `validations/P3-CAND-02-negative-coin-balance`.
- Independent archive validation scanned the full published range `1-274`, checking each epoch's positive rewards against the complete historical `SettleAmount` snapshot at the next epoch's `effective_block_height`.
- The full scan found exactly `19` candidate `(epoch, address)` pairs, `19` affected addresses, total `1,075.336150923 GNK`, with nonzero epochs `97`, `112`, `116`, `129`, and `132`.
- Amount reconciliation confirms every candidate payout equals the on-chain `epoch_performance_summary.rewarded_coins` value for that `(epoch, address)`. Total chain rewarded coins and total compensation both equal `1,075,336,150,923 ngonka`.
- The independent result matched the published `gonkavip/unclaimed` CSV exactly: `19` pairs, `1,075.336150923 GNK`, `0` mismatches.
- Proposal coordinator `@OpenMindedPerson` validated the Case 2 result: the confirmed compensation set remains the 19 settle-drop rows, and no additional Case 2 candidates were found in the full `1-274` archive scan or the checked `275-280` tail.

## Independent Audit Snapshot

| Scan | Epochs | Candidate pairs | Affected addresses | Total | Nonzero epochs | Published compare |
|---|---|---:|---:|---:|---|---|
| Smoke | `97`, `112`, `116`, `129`, `132`, `240`, `275-280` | 19 | 19 | 1,075.336150923 GNK | `97`, `112`, `116`, `129`, `132` | Exact |
| Focused | `87-142`, `275-280` | 19 | 19 | 1,075.336150923 GNK | `97`, `112`, `116`, `129`, `132` | Exact |
| Full | `1-274` | 19 | 19 | 1,075.336150923 GNK | `97`, `112`, `116`, `129`, `132` | Exact |

The earlier broad summary scan remains useful as a sanity check: `EpochPerformanceSummary` contains many normal positive-unclaimed rows, so the final compensation set must be isolated by historical `SettleAmount` absence, not by `claimed = false` alone.

## Mitigation / Fix Status

| Item | Status |
|---|---|
| Direct settle fix | PR [`#550`](https://github.com/gonka-ai/gonka/pull/550), `Negative coin balance for settle`, was merged on 2026-01-13 as commit [`8184fe3`](https://github.com/gonka-ai/gonka/commit/8184fe3501629d1051d1d14b31e7c47c01f7615d) into milestone `v0.2.8`. |
| Current code status | Current `main` subtracts negative `CoinBalance` debt from `RewardCoins` when the reward covers the debt. If debt exceeds reward, `RewardCoins` becomes `0` and `ErrNegativeCoinBalance` remains. |
| Related claim-time path | PR [`#826`](https://github.com/gonka-ai/gonka/pull/826) describes partial claim payment failure and was closed on 2026-04-27 without merge. Current `main` uses `CacheContext` in `payoutClaim`, so payout failure does not commit `finishSettle`; this is separate from the settlement-time Case 2 path. |
| Timing | The negative-balance settlement fix is present in current code. Full archive validation through epoch `274` and tail checks through `280` found no additional settle-drop candidates outside the published set. |

## Reward Flow

This case is not redistribution through reduced reward weight. The chain recorded positive `rewarded_coins` but skipped creation of the claimant's `SettleAmount`. The calculation repository states that such inaccessible rewards are eventually swept into the governance module account by `TransferOldSettleAmountsToGovernance`.

## Sources

- [Calculation repository](https://github.com/gonkavip/unclaimed)
- [Independent audit notes](sources/P3-CAND-02-independent-audit.md)
- [Validation package](../validations/P3-CAND-02-negative-coin-balance/README.md)
- [Archive validation script](../validations/P3-CAND-02-negative-coin-balance/verify_archive.py)
- [Full candidate artifact](../validations/P3-CAND-02-negative-coin-balance/case2_full_candidates.csv)
- [Full amount reconciliation CSV](../validations/P3-CAND-02-negative-coin-balance/case2_full_amount_reconciliation.csv)
- [Full amount reconciliation summary](../validations/P3-CAND-02-negative-coin-balance/case2_full_amount_reconciliation.json)
- [Full summary artifact](../validations/P3-CAND-02-negative-coin-balance/case2_full_summary.json)
- [Published comparison artifact](../validations/P3-CAND-02-negative-coin-balance/case2_full_published_compare.json)
- [GRC chat update export index](sources/GRC-chat-update-2026-06-01.md)
- [PR #826](https://github.com/gonka-ai/gonka/pull/826)
- [PR #550](https://github.com/gonka-ai/gonka/pull/550)
