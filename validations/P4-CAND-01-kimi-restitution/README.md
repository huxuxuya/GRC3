# P4-CAND-01 Validation: Kimi Restitution Repository Review

This folder tracks the independent review of the community Kimi restitution
repository:

<https://github.com/votkon/gonka-kimi-restitution>

The review focuses on conceptual truthfulness and compensation methodology, not
on rerunning the investigator's scripts.

## Artifacts

| File | Purpose |
|---|---|
| [`votkon_repo_truth_review.md`](votkon_repo_truth_review.md) | Claim-by-claim review of the current upstream repository, including confirmed facts, internal inconsistencies, and open methodology risks. |

## Current Result

The repository contains real on-chain signals for Kimi weight degradation,
epoch-266 nonce exclusion, and later `ComputeGroupCap` effects. However, the
published compensation total is not a pure chain replay. It depends on policy
choices about external attacks, whether an intended cap should be compensated,
and whether Kimi rewards should be topped up using the already-capped
settlement denominator instead of recomputing the full uncapped settlement.

Therefore the package is useful as evidence, but it should not be treated as a
fully validated GRC compensation case without resolving the methodology items
listed in the review note.
