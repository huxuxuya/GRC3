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

## Archive-State Validation

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

A separate local archive LCD configured through `.env` was later validated on 2026-06-01. The endpoint and API key are intentionally not tracked in git. The script derives the direct Cosmos LCD URL locally, stores its resumable cache outside the repository at `/tmp/grc3-case2-audit/cache.db`, and writes only sanitized review artifacts to `artifacts/case2_archive`.

The archive validation script is [`scripts/verify_case2_archive.py`](../../scripts/verify_case2_archive.py). It independently builds the candidate set from chain state and uses the published `gonkavip/unclaimed` CSV only as a comparison target.

| Scan | Epochs | Candidate pairs | Affected addresses | Total, ngonka | Total, GNK | Nonzero epochs | Published comparison |
|---|---|---:|---:|---:|---:|---|---|
| Smoke | `97`, `112`, `116`, `129`, `132`, `240`, `275-280` | 19 | 19 | 1,075,336,150,923 | 1,075.336150923 | `97`, `112`, `116`, `129`, `132` | Exact match; 0 mismatches |
| Focused | `87-142`, `275-280` | 19 | 19 | 1,075,336,150,923 | 1,075.336150923 | `97`, `112`, `116`, `129`, `132` | Exact match; 0 mismatches |
| Full | `1-274` | 19 | 19 | 1,075,336,150,923 | 1,075.336150923 | `97`, `112`, `116`, `129`, `132` | Exact match; 0 mismatches |

Tracked artifacts:

- [`case2_full_candidates.csv`](../../artifacts/case2_archive/case2_full_candidates.csv) - final independently derived address-by-epoch matrix.
- [`case2_full_summary.json`](../../artifacts/case2_archive/case2_full_summary.json) - scanned epoch range, totals, per-epoch summary stats, and failure list.
- [`case2_full_published_compare.json`](../../artifacts/case2_archive/case2_full_published_compare.json) - exact comparison against the published CSV.

Control checks from the archive source:

| Check | Address | Epoch | Rewarded coins | Historical `SettleAmount` result |
|---|---|---:|---:|---|
| Candidate row | `gonka19nd876302m3ll2h7sd55hp9pqzv2hpqalh8pjj` | 97 | 8,432,384,134 | No record at settlement height `1519978`; included. |
| Non-candidate control | `gonka1qqpsxmrmk99lw0xaychamatvydd8uw49qw2pga` | 97 | 83,253,062,409 | Record exists at settlement height `1519978`; excluded. |

The full independent archive scan confirms the published 19-row set and did not find additional settle-drop candidates in epochs `1-274`. The focused and smoke windows also confirm that no new candidates appear in the checked tail `275-280`.

## Coordinator Validation

Proposal coordinator `@OpenMindedPerson` validated the Case 2 result after the independent archive pass. The validated result is:

- full archive scan coverage: `274/274` epochs in `1-274`, with `0` recorded failures;
- confirmed affected set: `19` `(epoch, address)` pairs and `19` unique addresses;
- confirmed compensation: `1,075,336,150,923 ngonka` / `1,075.336150923 GNK`;
- comparison with the published `gonkavip/unclaimed` calculation: exact match, `0` mismatches;
- additional Case 2 settle-drop candidates in the full `1-274` scan and checked `275-280` tail: `0`.

This coordinator validation applies to the settlement-time `#550` / negative-balance settle-drop case. PR `#826` remains documented as a separate claim-time partial-payout risk and is not included in the confirmed Case 2 compensation result.

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
- Full independent archive validation confirms the published 19 affected rows exactly: `1,075,336,150,923 ngonka` / `1,075.336150923 GNK`, with no mismatches against the published calculation and no additional candidates in the scanned `1-274` range.
- Proposal coordinator `@OpenMindedPerson` validated this Case 2 result; governance inclusion remains the only open decision recorded for this case.
