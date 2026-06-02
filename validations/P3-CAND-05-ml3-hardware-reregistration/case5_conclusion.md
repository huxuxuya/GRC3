# P3-CAND-05 Conclusion

## Decision State

Validation result: scope decision still required.

This case should not be marked as independently confirmed compensation until a
committee/policy decision accepts off-chain hardware replacement claims and
defines the compensation formula.

## Evidence Summary

On-chain data confirms a real node/weight transition around the reported epoch:

- epochs `263..265`: `ml3` appears as Qwen node with `poc_weight = 16235`;
- epoch `266`: `ml3` appears as Kimi node with `poc_weight = 16235`;
- epochs `267..269`: `ml3` appears as Kimi node with `poc_weight = 5219`;
- epoch `270+`: `ml3` disappears from the claimant's checked model rows and
  other node IDs appear;
- the claimant is not listed as excluded in the checked `263..283` range;
- the claimant receives non-zero rewards in epochs `263..271`, zero rewards in
  `272..273`, then non-zero rewards again after later node IDs appear.
- regular PoC evidence endpoints for epochs `266..269` did not expose raw
  batch, validation, V2 validation, or V2 commit rows; the ML node weight
  distribution route returned `Not Implemented`.

## Root-Cause Status

Confirmed code area:

- pre-`v0.2.12` preserved-node scheduling used static epoch-level
  `timeslot_allocation[POC_SLOT]`;
- preserved nodes stayed in inference service and were excluded from PoC
  validation/generation flow;
- `v0.2.12` introduced episode-scoped preserved snapshots through PR `#1089`.

Claimant-specific root cause is not confirmed:

- the visible `ml3` rows in epochs `263..269` have `timeslot_allocation = 10`;
- chain code defines index `0` as `PRE_POC_SLOT` and index `1` as `POC_SLOT`;
- therefore those rows mean `PRE_POC_SLOT=true`, `POC_SLOT=false`;
- no generated claimant row shows `POC_SLOT=true`, so the archive trace does
  not prove that `ml3` was preserved out of PoC by the old mechanism.
- the available LCD data does not expose the raw PoC evidence needed to
  independently explain why the chain measured `ml3 = 5219`.

Not confirmed:

- actual physical hardware change from `4xB200` to `8xB200`;
- that the old behavior caused a specific measurable reward loss for this
  claimant;
- whether `5219` resulted from submitted nonce count, validator behavior,
  local operator setup, or another chain-side mechanism;
- an on-chain-only compensation amount.

## Weight / Amount Caution

The `poc_weight` and model `weight` rows used in this validation are raw model
weights. They are enough to show that `ml3` was present, later changed raw
weight, and then disappeared from the checked model rows. They are not enough to
calculate compensation directly.

To calculate a chain-style amount, a separate policy/formula pass would need to:

- define the counterfactual raw node/model weight for every affected epoch;
- apply the model `weight_scale_factor` used by the chain for that epoch/model;
- use the chain payout formula with the epoch reward denominator;
- compare the resulting counterfactual reward with actual `rewarded_coins`.

## Practical Conclusion

The case is best described as:

> A real on-chain `ml3` weight/node transition with an unproven off-chain
> hardware claim. It is adjacent to the old `timeslot_allocation` area discussed
> in PR `#1089`, but the checked rows do not show `ml3` as `POC_SLOT=true`
> preserved and do not independently prove a compensable protocol-loss case.

If this claim type is accepted by policy, the next required evidence is
off-chain operator proof of the hardware replacement time plus an agreed
counterfactual weight/reward formula.
