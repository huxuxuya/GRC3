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
| [`p4_conceptual_audit_plan.md`](p4_conceptual_audit_plan.md) | Working checklist for auditing claims, evidence, root cause, eligibility, overlap, and policy boundaries without reproducing arithmetic. |
| [`raw_chain_cache_manifest.md`](raw_chain_cache_manifest.md) | Manifest of raw node responses saved during P4 audit passes, with endpoints, hashes, and limitations. |
| [`p4_audit_pass_01.md`](p4_audit_pass_01.md) | First evidence pass: e266 final-set absence, e266 commit endpoint limitation, and e267/e275 Kimi cap-effect evidence. |
| [`p4_e266_commit_final_group_check.csv`](p4_e266_commit_final_group_check.csv) | Derived address-level check for the nine e266 DevOps-listed PoC submitters against final epoch group data. |

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
