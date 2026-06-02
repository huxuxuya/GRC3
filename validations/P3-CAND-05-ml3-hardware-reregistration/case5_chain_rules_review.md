# P3-CAND-05 Chain Rules Review

This review checks the preserved-node mechanics relevant to the `ml3`
hardware re-registration claim. It reads upstream Gonka source code but does
not execute any prior case solution code.

## Pre-Fix Mechanics: v0.2.11

Source tag: `gonka-ai/gonka@release/v0.2.11`, commit
`54c09b35bdceb4dd91c6d578635e63b8e41797e2`.

Relevant code paths:

- `decentralized-api/broker/broker.go`
- `decentralized-api/broker/state_commands.go`
- `decentralized-api/poc/validator.go`
- `inference-chain/x/inference/keeper/bitcoin_rewards.go`
- `inference-chain/x/inference/epochgroup/epoch_group.go`

Observed mechanics:

- `NodeState.ShouldContinueInference()` checked each node's
  `EpochMLNodes[*].TimeslotAllocation[1]`.
- Index `1` is `POC_SLOT`.
- If `POC_SLOT=true`, DAPI kept that node in inference service instead of PoC.
- PoC validation filtering excluded nodes that should continue inference.
- Reward/confirmation-weight tests and code treated `POC_SLOT=true` nodes as
  preserved.

This means pre-fix preservation was tied to the epoch-group node row and was
visible as static `timeslot_allocation` state for the epoch.

## Post-Fix Mechanics: v0.2.12

Source tag: `gonka-ai/gonka@release/v0.2.12`, commit
`1a122bcb9c296e6a91c1eb4769edc53e2c88a1e5`.

Relevant code paths:

- `inference-chain/x/inference/module/module.go`
- `inference-chain/x/inference/keeper/preserved_nodes_snapshot.go`
- `inference-chain/x/inference/keeper/query_preserved_nodes_snapshot.go`
- `decentralized-api/broker/broker.go`
- `decentralized-api/poc/validator.go`

Observed mechanics:

- The chain samples `PreservedNodesSnapshot` at the PoC episode anchor.
- The snapshot is stored with `SetPreservedNodesSnapshot`.
- DAPI queries `preserved_nodes_snapshot` and fills
  `node.State.PreservedModels`.
- `NodeState.ShouldContinueInference()` now returns true when
  `PreservedModels` is non-empty.
- The same PoC validator filter excludes preserved nodes, but the source of
  truth is now the episode snapshot rather than static epoch-level
  `timeslot_allocation`.

## PR / Release Linkage

Official `v0.2.12` release notes describe "Random selection of preserved
MLNodes (#1089)": old preserved nodes were selected once per epoch through
static `MLNodeInfo.timeslot_allocation[POC_SLOT]`; v0.2.12 replaces this with
episode-scoped preserved snapshots at regular PoC and confirmation PoC anchors.

Related links:

- PR `#1089`: <https://github.com/gonka-ai/gonka/pull/1089>
- Upgrade PR `#948`: <https://github.com/gonka-ai/gonka/pull/948>
- Release notes: <https://github.com/gonka-ai/gonka/releases/tag/release/v0.2.12>

## Relevance To Case 5

The code supports Arturs' statement that this area was known
`timeslot_allocation` / preserved-node behavior.

However, the strict slot interpretation matters. In the pre-fix code,
`PRE_POC_SLOT` is index `0` and `POC_SLOT` is index `1`; only
`POC_SLOT=true` is treated as preserved for PoC/inference service. The claimant
trace shows `ml3` with `timeslot_allocation = 10` in epochs `263..269`, which
means `PRE_POC_SLOT=true` and `POC_SLOT=false`. Those rows are not evidence
that `ml3` itself was preserved by `POC_SLOT`.

It does not prove the reported hardware replacement. The chain evidence for the
claimant contains:

- participant address;
- model rows;
- node IDs;
- `poc_weight`;
- `throughput`;
- `timeslot_allocation`.

It does not contain a direct on-chain field saying that `ml3` changed from
`4xB200` to `8xB200`.

## Fix Assessment

PR `#1089` is a general mitigation for predictable epoch-long preservation.
It makes preserved selection late-bound and episode-scoped.

It is not a case-specific compensation proof. It does not by itself prove:

- that this operator replaced hardware exactly as claimed;
- that `ml3` was affected by `POC_SLOT=true` preservation in the checked rows;
- that the old chain state caused a compensable loss;
- what amount should be paid.
