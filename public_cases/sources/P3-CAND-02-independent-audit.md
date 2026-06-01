# P3-CAND-02 Independent Audit Notes

Audit date: 2026-06-01.

This note records an independent pass over Case 2. It does not use the published `gonkavip/unclaimed` script or CSV as the calculation source. That repository remains useful only as a comparison target after independent evidence is collected.

## Independent Data Pass

Data source used for the first-pass scan:

- `http://node1.gonka.ai:8000/chain-api/productscience/inference/inference/epoch_performance_summary/{epoch}`

Criterion for the first pass:

- `rewarded_coins > 0`
- `claimed == false`

This is intentionally broader than the Case 2 compensation criterion. It identifies all positive, unclaimed rewards visible in `EpochPerformanceSummary`, including ordinary missed claims. It does not prove settle-drop by itself.

| Range | Epochs with API errors | Positive unclaimed rows | Positive unclaimed reward, ngonka | Meaning |
|---|---:|---:|---:|---|
| `1-274` | 0 | 823 | 1,427,305,676,768,877 | Broad unclaimed-positive universe; includes normal missed claims. |
| `87-142` | 0 | 471 | 127,838,757,295,576 | Wide window around the published Case 2 epochs. |
| `133-274` | 0 | 185 | 131,513,967,332,046 | Post-fix published window still has unclaimed-positive rows, so summary data alone is not enough to classify bug recurrence. |
| `275-280` | 0 | 0 | 0 | Current tail scan found no positive unclaimed rows. |

Spot checks in the published Case 2 epochs:

| Epoch | Participants in summary | Participants with positive reward | Positive unclaimed rows | Positive unclaimed reward, ngonka |
|---:|---:|---:|---:|---:|
| 97 | 415 | 385 | 6 | 8,125,070,579,633 |
| 112 | 573 | 515 | 6 | 731,602,580,169 |
| 116 | 594 | 552 | 57 | 2,751,905,731,625 |
| 129 | 597 | 509 | 7 | 218,739,570,224 |
| 132 | 613 | 513 | 31 | 5,776,580,606,544 |

These spot checks show why the final Case 2 list cannot be derived from summary data alone: the broad first-pass rows in the relevant epochs are much larger than the published 19 settle-drop rows.

## Archive-State Requirement

The independent compensation criterion requires historical `SettleAmount` state at the settlement height of the next epoch:

- fetch `epoch_group_data/{N+1}`;
- take `effective_block_height`;
- query `settle_amount/{address}` and the full paginated `settle_amount` snapshot at that height;
- classify a candidate only when positive `rewarded_coins` exists but no `(epoch, address)` `SettleAmount` existed at settlement.

Public nodes checked on 2026-06-01 did not provide the needed historical state:

| Node | Historical query tested | Result |
|---|---|---|
| `node1.gonka.ai` | `settle_amount` at height `1519978` for epoch 97 settlement | `no commit info found`, latest height reported around `4364758+`. |
| `node2.gonka.ai` | same height and endpoint | `no commit info found`, latest height reported around `4364799+`. |
| `node3.gonka.ai` | same height and endpoint | empty reply from server. |
| `rpc.gonka.gg` | same endpoint without credentials | `unauthorized`; endpoint reference states an API key is required. |
| `rpc.gonka.gg` | same endpoint with API-key authentication | authenticated request reached the chain API, but `settle_amount` at height `1519978` still returned `no commit info found`. |

Therefore the independent data audit is complete only through the broad first-pass and current-tail check. The final 19-row compensation list and `1,075.336150923 GNK` total still require a true archive node or indexed historical `SettleAmount` dataset to independently verify missing historical `SettleAmount` entries. Authentication to `rpc.gonka.gg` is not sufficient for this specific old-state query.

## Code Audit

PR #550, `Negative coin balance for settle`, was merged on 2026-01-13 as commit `8184fe3501629d1051d1d14b31e7c47c01f7615d` into milestone `v0.2.8`.

The merged change removed the unconditional negative-balance settlement error and added debt subtraction from `RewardCoins`:

- if `RewardCoins >= -CoinBalance`, the debt is subtracted and no settle error is returned;
- if debt exceeds reward, `RewardCoins` is set to `0` and `ErrNegativeCoinBalance` remains.

Current `main` still contains that logic in `inference-chain/x/inference/keeper/bitcoin_rewards.go`. Current `SettleAccounts` still writes `EpochPerformanceSummary` before writing `SettleAmount`, and skips `SettleAmount` when `amount.Error != nil`. This explains the historical Case 2 signature: positive `RewardedCoins` could be recorded while the claim ticket was not written.

Current `main` also uses `CacheContext` in `payoutClaim` in `msg_server_claim_rewards.go`, making payout mutations atomic: if escrow or reward payment fails, `finishSettle` is not committed and the settle record persists for retry. This means the partial-payment concern described in PR #826 is a separate claim-time path, not the same settlement-time Case 2 path. PR #826 itself was closed on 2026-04-27 without merge, but the current code path already contains the atomic behavior relevant to that risk.

## Current Conclusion

- The settlement-time negative-balance bug is fixed in current code for the reward-covers-debt case.
- The remaining `debt > reward` path intentionally returns `ErrNegativeCoinBalance` with zero reward, so it does not match the positive-reward compensation signature.
- No positive unclaimed rows were found in epochs `275-280`.
- A full independent confirmation of the published 19 affected rows remains blocked until historical `settle_amount` state is available from an archive node.
