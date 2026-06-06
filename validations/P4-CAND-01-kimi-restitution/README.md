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
| [`p4_decision_matrix.md`](p4_decision_matrix.md) | Split P4 decision matrix with the recommended voting order and per-track policy gates. |
| [`p4_problem_01_e265_scope.md`](p4_problem_01_e265_scope.md) | Epoch 265 scope note: separates Case 3 overlap from non-strict direct cPoC rows. |
| [`p4_problem_02_e266_nonce_scope.md`](p4_problem_02_e266_nonce_scope.md) | Epoch 266 nonce note: separates 9 excluded operators from broader reconstruction/top-up rows. |
| [`p4_problem_02a_e266_zero_reward_rows.md`](p4_problem_02a_e266_zero_reward_rows.md) | Epoch 266 zero-reward note: row-level evidence for the 5 in-final-group failed-confirmation nonce candidates. |
| [`p4_problem_02b_e266_rewarded_topup_rows.md`](p4_problem_02b_e266_rewarded_topup_rows.md) | Epoch 266 rewarded top-up note: row-level evidence for the 4 already-rewarded reconstruction rows. |
| [`p4_problem_03_e266_delegation.md`](p4_problem_03_e266_delegation.md) | Epoch 266 delegation note: confirmed chain mechanics and unresolved indirect-loss policy. |
| [`p4_problem_04_groupcap_denominator.md`](p4_problem_04_groupcap_denominator.md) | Epochs 267-276 GroupCap note: denominator alternatives and e276 proration issue. |
| [`p4_problem_05_overlap_and_total.md`](p4_problem_05_overlap_and_total.md) | Aggregate total and overlap note: explains why `946,509.925002` GONKA should not be approved as one package. |
| [`raw_chain_cache_manifest.md`](raw_chain_cache_manifest.md) | Manifest of raw node responses saved during P4 audit passes, with endpoints, hashes, and limitations. |
| [`p4_audit_pass_01.md`](p4_audit_pass_01.md) | First evidence pass: e266 final-set absence, e266 commit endpoint limitation, and e267/e275 Kimi cap-effect evidence. |
| [`p4_e266_commit_final_group_check.csv`](p4_e266_commit_final_group_check.csv) | Derived address-level check for the nine e266 DevOps-listed PoC submitters against final epoch group data. |
| [`p4_audit_pass_02_e265.md`](p4_audit_pass_02_e265.md) | Epoch 265 row classifier separating strict Case-3-like cPoC shortfall, broader failed-confirmation candidate, and rewarded confirmation-weight drop. |
| [`p4_e265_row_classifier.csv`](p4_e265_row_classifier.csv) | Machine-readable classifier for the three epoch 265 rows in the P4 source package. |
| [`p4_audit_pass_03_e265_gonka1830.md`](p4_audit_pass_03_e265_gonka1830.md) | Row-level cPoC evidence for `gonka1830...`, showing no raw Kimi/Qwen submission or validation record at final cPoC stage `4102890`. |
| [`p4_e265_gonka1830_cpoc_evidence.csv`](p4_e265_gonka1830_cpoc_evidence.csv) | Machine-readable commit/validation/voting-power evidence for the epoch 265 disputed rows. |
| [`p4_audit_pass_04_e266_nonce_scope.md`](p4_audit_pass_04_e266_nonce_scope.md) | Epoch 266 nonce scope classifier: separates nine absent operators from in-final-group reconstruction/top-up rows. |
| [`p4_e266_nonce_scope_classifier.csv`](p4_e266_nonce_scope_classifier.csv) | Machine-readable e266 nonce scope classification for the 18 source nonce-compensation rows. |
| [`p4_e266_zero_reward_rows.csv`](p4_e266_zero_reward_rows.csv) | Machine-readable e266 zero-reward evidence for the 5 in-final-group failed-confirmation rows. |
| [`p4_e266_rewarded_topup_rows.csv`](p4_e266_rewarded_topup_rows.csv) | Machine-readable e266 rewarded top-up evidence for the 4 in-final-group rewarded rows. |
| [`p4_audit_pass_05_e266_delegation.md`](p4_audit_pass_05_e266_delegation.md) | Epoch 266 delegation evidence: verifies raw Kimi delegations, operator absence, and chain penalty parameters while leaving eligibility as policy. |
| [`p4_e266_delegation_evidence.csv`](p4_e266_delegation_evidence.csv) | Machine-readable e266 delegation evidence for the 9 source delegation-compensation rows. |
| [`p4_audit_pass_06_e267_e276_groupcap.md`](p4_audit_pass_06_e267_e276_groupcap.md) | Epochs 267-276 GroupCap denominator check: verifies source rows against raw chain data and compares three counterfactual denominator models. |
| [`p4_e267_e276_groupcap_denominator_check.csv`](p4_e267_e276_groupcap_denominator_check.csv) | Machine-readable e267-e276 denominator comparison and e276 upgrade-in-epoch flag. |
| [`source_cache_manifest.md`](source_cache_manifest.md) | Manifest of copied source artifacts from the pinned Votkon repository used as claim labels. |

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
