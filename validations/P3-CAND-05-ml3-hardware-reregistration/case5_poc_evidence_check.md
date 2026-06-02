# P3-CAND-05 PoC Evidence Check

This check asks whether the public/archive LCD layer exposes raw PoC evidence
that can explain why claimant node `ml3` moved from raw `poc_weight = 16235` to
`poc_weight = 5219`.

## Stage Heights Checked

The regular PoC start heights come from `epoch_group_data`:

| Epoch | PoC start block height | Claimant model row | `ml3` raw weight |
|---|---:|---|---:|
| 266 | `4105361` | Kimi | `16235` |
| 267 | `4120752` | Kimi | `5219` |
| 268 | `4136143` | Kimi | `5219` |
| 269 | `4151534` | Kimi | `5219` |

## LCD Endpoints Checked

| Endpoint | 266 | 267 | 268 | 269 | Meaning |
|---|---:|---:|---:|---:|---|
| `poc_batches_for_stage/{height}` | `0` | `0` | `0` | `0` | No V1 PoC batch rows exposed for these stage heights. |
| `poc_validations_for_stage/{height}` | `0` | `0` | `0` | `0` | No V1 PoC validation rows exposed for these stage heights. |
| `poc_v2_validations_for_stage/{height}` outer rows | `0` | `0` | `0` | `0` | No V2 PoC validation rows exposed for these stage heights. |
| `poc_v2_validations_for_stage/{height}` inner rows | `0` | `0` | `0` | `0` | No nested V2 validation rows exposed. |
| `all_poc_v2_store_commits/{height}` | `0` | `0` | `0` | `0` | No V2 store commits exposed. |
| `epoch_group_validations/{claimant}/{epoch}` | not found | not found | not found | not found | No per-claimant epoch-group validation record returned. |
| `all_ml_node_weight_distributions_for_stage/{height}` | not implemented | not implemented | not implemented | not implemented | The route exists in source but the queried node returns `Not Implemented`. |

Machine-readable counts are stored in
[`case5_poc_endpoint_check.csv`](case5_poc_endpoint_check.csv).

## Interpretation

The public/archive LCD data confirms the final model/node weights but does not
currently expose the raw PoC submissions, validator rows, or node weight
distributions needed to independently explain the `ml3 = 5219` measurement.

Therefore this validation can say:

- the chain recorded the lower raw weight in epochs `267..269`;
- the claimant was not excluded and did receive rewards in epochs `267..269`;
- the checked rows do not show `ml3` as `POC_SLOT=true` preserved;
- the currently queried public LCD routes do not provide enough raw PoC
  evidence to prove whether the low `5219` came from submitted nonce count,
  validator behavior, local operator configuration, or another chain-side
  mechanism.

This is a materially weaker evidence state than Case 3, where cPoC rows,
validation weights, exclusion reason, and reward formula can be reconstructed
directly from chain/archive data.
