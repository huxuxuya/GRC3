# P4 Decision Matrix

This file splits P4 into independent committee decisions. It is not a payout
approval.

## Decision Blocks

| Block | File | Technical status | Policy status | Suggested decision shape |
|---|---|---|---|---|
| Epoch 265 scope | [`p4_problem_01_e265_scope.md`](p4_problem_01_e265_scope.md) | One row confirmed as Case 3-like; two rows not confirmed as strict direct cPoC victims. | Broader attack/weight-drop eligibility unresolved. | Move confirmed row to Case 3; do not approve e265 as a P4 bundle. |
| Epoch 266 nonce | [`p4_problem_02_e266_nonce_scope.md`](p4_problem_02_e266_nonce_scope.md) | 9 excluded operators confirmed; remaining 9 rows are broader classes. | External attack and reconstruction eligibility unresolved. | Vote narrow excluded-operator scope separately from top-up/zero-reward rows. |
| Epoch 266 delegation | [`p4_problem_03_e266_delegation.md`](p4_problem_03_e266_delegation.md) | Chain mechanics confirmed for 9 delegators. | Indirect delegator eligibility unresolved. | Separate policy vote for indirect losses. |
| Epochs 267-276 GroupCap | [`p4_problem_04_groupcap_denominator.md`](p4_problem_04_groupcap_denominator.md) | Cap effect and source rows confirmed; source top-up reproducible. | Intended cap compensability, denominator, and e276 proration unresolved. | Decide compensability, denominator, and e276 treatment before amount approval. |
| Aggregate total / overlap | [`p4_problem_05_overlap_and_total.md`](p4_problem_05_overlap_and_total.md) | Source total pinned and internally consistent. | Aggregate eligibility and duplicate-payment checks unresolved. | Do not approve `946,509.925002` GONKA as one package. |

## Recommended Voting Order

1. Confirm Case 3 overlap handling for e265 `gonka1j7...`.
2. Decide whether external-attack-caused operator exclusion is compensable.
3. Decide whether indirect delegator losses are compensable.
4. Decide whether intended `ComputeGroupCap` effects are compensable.
5. If GroupCap is compensable, choose denominator and e276 proration policy.
6. Build final overlap matrix before any aggregate payout instruction.

## Current Working Position

P4 is useful evidence but should remain split. The full source total
`946,509.925002 GONKA` is not ready for approval as a single GRC compensation
amount.
