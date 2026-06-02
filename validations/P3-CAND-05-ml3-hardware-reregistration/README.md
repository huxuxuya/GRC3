# P3-CAND-05 Validation: `ml3` Hardware Re-Registration

This folder contains an independent validation package for candidate case
`P3-CAND-05`. The reported claim is that participant
`gonka15munkmx6x7k6rqqeexjet4556p7at39ks9qgr5` replaced node `ml3` hardware
from `4xB200` to `8xB200` under the same node name, but the weight did not
increase for several epochs.

## Scope

Checked independently, without running prior case solution code:

- archive LCD chain rows for epochs `263..283`;
- claimant model membership and node-level `poc_weight`;
- participant reward and exclusion status;
- old and new preserved-node mechanics in upstream Gonka code.

## Artifacts

| File | Purpose |
|---|---|
| [`build_case5_validation.py`](build_case5_validation.py) | Independent stdlib-only collector. Reads `.env` for RPC settings but does not print or store secrets. |
| [`raw_cache/`](raw_cache/) | Cached raw chain API JSON responses for reproducibility. |
| [`case5_timeline.csv`](case5_timeline.csv) | Epoch-level trace for claimant nodes, model weights, rewards, and exclusion status. |
| [`case5_timeline.md`](case5_timeline.md) | Human-readable focused timeline. |
| [`case5_ml3_model_trace.csv`](case5_ml3_model_trace.csv) | Per-model claimant rows from `epoch_group_data`. |
| [`case5_ml3_node_trace.csv`](case5_ml3_node_trace.csv) | Node-level `poc_weight` / `timeslot_allocation` rows. |
| [`case5_participant_reward_trace.csv`](case5_participant_reward_trace.csv) | Participant rewards and exclusion status by epoch. |
| [`case5_poc_evidence_check.md`](case5_poc_evidence_check.md) | Read-only check of PoC batch/validation/commit endpoints for epochs `266..269`. |
| [`case5_poc_endpoint_check.csv`](case5_poc_endpoint_check.csv) | Machine-readable endpoint counts for the PoC evidence check. |
| [`case5_chain_rules_review.md`](case5_chain_rules_review.md) | Code-level preserved-node mechanics review. |
| [`case5_conclusion.md`](case5_conclusion.md) | Validation conclusion and remaining policy decision. |

## Main On-Chain Timeline

Node notation: `node_id:poc_weight:throughput:timeslot_bits`.
`timeslot_bits = 10` means `PRE_POC_SLOT=true`, `POC_SLOT=false` in the
epoch-group row.

Important slot interpretation:

- The pre-fix chain code treats `timeslot_allocation[1]` (`POC_SLOT`) as the
  preserved-for-PoC bit.
- The claimant rows for `ml3` in epochs `263..269` show `timeslot_bits = 10`,
  so `POC_SLOT=false`.
- Therefore the checked archive rows do not prove that `ml3` itself was
  preserved by the old `POC_SLOT` mechanism.

Weight semantics:

- `poc_weight`, model `weight`, and the Kimi/Qwen `weight` columns below are
  raw model weights from `epoch_group_data`; they prove what the chain measured
  for the node/model, but they are not direct reward weights.
- `voting_power`, `confirmation_weight`, and `rewarded_coins` are chain
  accounting fields after upstream aggregation/scaling.
- Any compensation counterfactual that starts from raw `poc_weight` must apply
  the model `weight_scale_factor` and the chain reward formula before comparing
  to rewards. This validation package does not establish such a payout formula.

| Epoch | Models found | Nodes | `ml3` present | Kimi weight | Kimi voting power | Qwen weight | Reward, GONKA | Excluded |
|---|---:|---|---|---:|---:|---:|---:|---|
| 263 | 2 | `ml3;ml5;ml8` | yes | 23972 | 36087 | 16235 | 9745.244781111 | no |
| 264 | 2 | `ml3;ml5;ml8` | yes | 24324 | 36531 | 16235 | 8986.970520335 | no |
| 265 | 2 | `ml3;ml5;ml8` | yes | 22160 | 33800 | 16235 | 10553.989409830 | no |
| 266 | 1 | `ml3;ml8` | yes | 26304 | 31538 |  | 26799.023361427 | no |
| 267 | 1 | `ml3;ml5;ml8` | yes | 27400 | 9647 |  | 2829.715828861 | no |
| 268 | 1 | `ml3;ml5;ml8` | yes | 27639 | 22500 |  | 5757.415294226 | no |
| 269 | 1 | `ml3;ml5` | yes | 17885 | 15496 |  | 6276.820078853 | no |
| 270 | 1 | `ml1;ml5` | no | 23670 | 19891 |  | 7880.707923174 | no |
| 271 | 1 | `ml1;ml5` | no | 23867 | 24532 |  | 4081.774107222 | no |
| 272 | 1 | `ml1` | no | 11175 | 11782 |  | 0.000000000 | no |
| 273 | 1 | `ml1` | no | 11175 | 8777 |  | 0.000000000 | no |
| 280 | 2 | `mlnode-100;mlnode-200` | no | 6197 | 8390 | 2545 | 3937.861717621 | no |
| 282 | 2 | `mlnode-100;mlnode-103;mlnode-104` | no | 6723 | 10094 | 5444 | 4760.469992293 | no |

## What Was Confirmed

- The chain sees `ml3` for this claimant in epochs `263..269`.
- `ml3` has stable Qwen `poc_weight = 16235` in epochs `263..265`.
- `ml3` later appears under Kimi in epoch `266` with `poc_weight = 16235`,
  then under Kimi with `poc_weight = 5219` in epochs `267..269`.
- From epoch `270`, the claimant no longer has `ml3` in the checked model
  rows; Kimi rows show `ml1` / `ml5` instead.
- The claimant was not present in `excluded_participants` for checked epochs.
- The claimant received non-zero rewards in epochs `263..271`, zero rewards in
  `272..273`, then non-zero rewards again after later node IDs appear.
- In the checked `epoch_group_data` rows, `ml3` has `PRE_POC_SLOT=true` but
  `POC_SLOT=false`; no claimant node row in the generated trace has
  `POC_SLOT=true`.
- Public/archive PoC batch, validation, V2 validation, and V2 commit endpoints
  checked for regular PoC start heights `4105361`, `4120752`, `4136143`, and
  `4151534` returned no raw rows; `all_ml_node_weight_distributions_for_stage`
  returned `Not Implemented`.

## What Was Not Proven

- The chain rows used here do not contain an on-chain hardware inventory field
  proving `4xB200 -> 8xB200`.
- The data proves node IDs and weights, not the physical hardware behind a node
  name.
- The archive rows do not prove that `ml3` was kept out of PoC by
  `POC_SLOT=true` preservation; the visible slot bits show the opposite for
  `ml3` in epochs `263..269`.
- The currently queried LCD routes do not expose the raw PoC submissions,
  validator rows, or weight distributions needed to independently explain why
  `ml3` was measured as `5219` in epochs `267..269`.
- The observed raw `poc_weight` transitions do not by themselves define a
  compensable reward loss.
- No compensable loss formula is established from on-chain data alone; a valid
  formula would need model scale factors and the chain payout denominator for
  each epoch.

## Result

Case `P3-CAND-05` remains a scope/policy decision, not an independently
validated protocol-loss case.

The strongest chain-supported statement is:

> The archive confirms a real `ml3` node/weight transition, but it does not
> confirm the physical hardware change, a `POC_SLOT=true` preservation event for
> `ml3`, or a chain-style compensable loss. PR `#1089` / upgrade `v0.2.12`
> mitigated the broader preserved-node mechanism, but this validation does not
> prove that mechanism caused the reported `ml3` claim.
