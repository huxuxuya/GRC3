# P4-CAND-01 Conceptual Audit Plan

This document is the working audit plan for the community Kimi restitution
case. It intentionally reviews claims, evidence, root-cause statements,
eligibility, and policy boundaries. It does not attempt to reproduce the
investigator's arithmetic.

## Status Labels

| Status | Meaning |
|---|---|
| `Confirmed` | Current evidence is sufficient for the statement. |
| `Partially confirmed` | Some facts are proven, but the complete claim is not. |
| `Not confirmed` | Current evidence does not support the statement. |
| `Policy required` | The committee must define scope before the claim can be accepted or rejected. |
| `Blocked` | The required evidence is not available from current sources. |
| `Out of scope for conceptual audit` | This belongs to arithmetic replay, not claim/evidence audit. |

## Audit Scope

| Field | Value |
|---|---|
| Case | `P4-CAND-01` |
| Source repository | `https://github.com/votkon/gonka-kimi-restitution` |
| Source commit pinned | `5462c55a6b95d50dfb53bdc4211cdcd31369c2ea` |
| Epochs covered by source | `265..276` |
| Source total at pinned commit | `946,509.925002 GONKA` |
| Source affected set at pinned commit | `53` unique addresses |
| Audit purpose | Determine which statements are proven, which are inferred, and which require policy decisions. |
| Explicitly out of scope | Re-running upstream scripts or approving a compensation amount. |

## Evidence Classes

| Evidence class | Examples | How to use |
|---|---|---|
| Chain data | epoch group data, confirmation weights, performance summaries, PoC commits, excluded participants | Can prove state, weights, inclusion/exclusion, rewards, and timing. |
| DevOps evidence | chat logs, incident notes, operator observations, production logs | Can support operational cause, but should be separated from chain proof. |
| Repository claims | README narratives, scripts, JSON outputs, methodology notes | Can define the investigator's claim, but is not independent proof by itself. |
| Code/protocol evidence | chain code, PRs, upgrade heights, params | Can prove protocol behavior and mitigations. |
| Committee policy | scope decisions, prior votes, eligibility rules | Required when the issue is real but restitution eligibility is not technical. |

## Claim Checklist

| # | Claim / statement | Evidence required | Current evidence | Status | Next action |
|---:|---|---|---|---|---|
| 1 | Upstream source version and totals are pinned. | GitHub HEAD/commit, `aggregate_compensation.json`, per-epoch JSON outputs. | Source commit pinned as `5462c55a6b95d50dfb53bdc4211cdcd31369c2ea`; current total recorded as `946,509.925002 GONKA` across `53` addresses. | `Confirmed` | Keep this commit hash in all public references. Re-check only if upstream changes are intentionally adopted. |
| 2 | The case should be treated as one continuous Kimi issue covering epochs `265..276`. | Evidence that the same root cause or policy class applies across all epochs. | The repo groups e265 CPoC degradation, e266 nonce/delegation loss, and e267-e276 `ComputeGroupCap` top-up. These are distinct mechanisms. | `Partially confirmed` | Split review into at least three tracks: e265 direct cPoC, e266 nonce/delegation, e267-e276 cap. |
| 3 | Epoch `265` includes a direct Kimi cPoC shortfall for `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6`. | Chain timeline showing active entry, Kimi submitted work, failed confirmation path, zero reward, and chain-style counterfactual. | Our Case 3 review already found the same claimant and amount `20,896.527179100 GONKA` as the same Kimi cPoC shortfall class as epoch `267`. | `Confirmed` | Keep this row in Case 3 scope if committee accepts the epoch `265` extension. |
| 4 | The other two epoch `265` rows are direct cPoC restitution victims. | Per-address chain trace showing the same direct cPoC failure signature, not only confirmation-weight drop. | Source repo identifies cw-drop rows, but current local review has not proven they match the strict Case 3 signature. | `Partially confirmed` | Build separate row-level evidence for each e265 non-Case-3 address before accepting them. |
| 5 | Epoch `265` losses were caused by external attack. | Production logs, timestamps, incident correlation, affected Kimi nodes, and chain state transition. | Source repo asserts attack attribution; DevOps evidence supports Kimi operational disruption generally, but current local chain review only proves state changes. | `Partially confirmed` | Require incident evidence and map it to exact block/time and affected rows. |
| 6 | External attack losses in e265 are eligible for GRC restitution. | Committee policy that external actor / operator-disruption losses are in scope. | Existing public case says GRC voted against including P4; eligibility remains policy-based. | `Policy required` | Decide whether external attack losses can be compensated by GRC at all. |
| 7 | Epoch `266` has nine PoC submitters that did not enter the final epoch group. | PoC commit list, final epoch group, excluded/missing participant comparison. | Audit pass 01 confirms all nine DevOps-listed addresses have PoC v2 store commits at stage `4105361` when queried at height `4120751`, and all nine are absent from final `epoch_group_data_266` and `epoch_performance_summary_266`. The saved CLI commit output does not include `model_id`, so the Kimi-specific label still depends on DevOps/source context or richer commit evidence. | `Confirmed` for PoC submission + final-set absence; `Partially confirmed` for Kimi-specific attribution | Add richer commit evidence with `model_id` if available. |
| 8 | Epoch `266` reconstructed nonce weights should be used as the reward basis. | On-chain commit counts, historical model scale factors, and an accepted reconstruction rule. | Source uses Kimi scale `1.2620856201975851` and Qwen scale `0.3593`. This is a reconstruction, not direct settlement state. | `Policy required` | Decide whether reconstructed PoC work can define compensation when the participant was not in the epoch group. |
| 9 | Epoch `266` zero-reward submitters are victims, not ordinary failed participants. | Causal proof that exclusion came from the claimed incident, not local failure, invalid work, or protocol-valid exclusion. | Source argues zero reward is evidence of attack victimization. That is plausible but not sufficient by itself. | `Partially confirmed` | For each zero-reward row, require commit evidence, exclusion state, and root-cause classification. |
| 10 | Epoch `266` delegators lost an extra `10%` due to ModeNone instead of ModeDelegate. | Delegation snapshot, operator exclusion proof, chain delegation penalty parameters. | Source method is coherent: `15%` ModeNone penalty minus `5%` delegation share. Eligibility still depends on accepting operator exclusion as compensable. | `Partially confirmed` | Verify delegation snapshots and decide whether indirect delegator loss is in scope. |
| 11 | e266 delegation compensation is eligible even if the operator's loss came from external attack. | Committee policy on indirect losses and attack scope. | No local policy proof. | `Policy required` | Create an explicit committee decision for indirect/delegator eligibility. |
| 12 | `ComputeGroupCap` existed and reduced Kimi weight in e267-e276. | Chain code/params, DevOps evidence, epoch group weight vs confirmation-weight patterns. | DevOps source describes the `75%` cap; source repo and local review identify Kimi `confirmation_weight` greater than capped `weight`. | `Confirmed` | Treat cap effect as real protocol behavior. |
| 13 | `ComputeGroupCap` was a protocol bug rather than intended balancing behavior. | Code intent, parameter history, reviewer statements, and mitigation rationale. | Public case notes that `ComputeGroupCap` is an intended rule and that GRC reviewers questioned compensating it. | `Policy required` | Committee must decide whether intended cap behavior can become compensable due to context. |
| 14 | e267-e276 Kimi operators were underpaid relative to actual confirmed work. | Accepted counterfactual reward model and chain proof of confirmed work. | Source uses Kimi `confirmation_weight` as restored numerator. This shows a top-up model, not the only possible settlement replay. | `Partially confirmed` | Resolve denominator/counterfactual model before calling the difference underpayment. |
| 15 | The source e267-e276 formula is chain-correct. | Full reward replay or protocol-level proof that capped `root_total_weight` should remain the denominator. | Source uses `confirmation_weight / root_total_weight * epoch_reward - actual`. Local review flags this as a top-up, not a full uncapped network replay. | `Policy required` | Choose one model: top-up against paid settlement, or full uncapped settlement replay. |
| 16 | Qwen rewards already paid means Kimi should be topped up without recalculating the full denominator. | Committee policy on non-clawback top-ups and restitution source of funds. | Source makes this argument explicitly, but it is a policy choice. | `Policy required` | Committee must approve or reject top-up accounting. |
| 17 | e276 should be compensated as a full affected epoch. | Upgrade block, stage timing, reward settlement timing, and proration policy. | Source states `v0.2.13` activated at block `4,267,300` during epoch `276`; script uses true epoch end and does not show a visible proration rule. | `Policy required` | Decide full-epoch vs prorated e276 treatment and document why. |
| 18 | `v0.2.13` fixed the root problem. | PR/code diff, mainnet activation block, post-upgrade regression scan. | Public case cites PR `#1143` and activation block `4,267,300`; local Case 6 post-upgrade scan is related but not a P4-specific proof. | `Partially confirmed` | Separate mitigation evidence from payout proof; add post-upgrade cap/state check if needed. |
| 19 | "No known repeat path" is proven. | Security review of current gateway and protocol surfaces. | Source repo says risk is reduced/no known repeat path for some components. This is operational/security evidence, not chain proof. | `Partially confirmed` | Treat as operational risk statement, not as restitution eligibility proof. |
| 20 | The published total `946,509.925002 GONKA` is a validated GRC payout. | Completed policy decisions, overlap checks, accepted formula, and row-level evidence. | Current local review says the package is useful evidence but too broad to approve mechanically. | `Not confirmed` | Do not approve the aggregate total as one package without resolving tracks and overlaps. |
| 21 | There is no duplicate compensation with Case 3. | Address/epoch overlap matrix and prior payment records. | Case 3 e265 overlap is known for `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6`; source also includes e266 for same address, which local Case 3 did not classify as Case 3-like. | `Partially confirmed` | Build final overlap table by address, epoch, and payment proposal before approval. |
| 22 | There is no duplicate compensation with Case 4 or Case 6. | Address/epoch overlap matrix against existing validation artifacts and payments. | Public P4 case warns about epoch overlaps, especially epoch `276`; detailed duplicate-payment decision is not recorded here. | `Partially confirmed` | Reuse Case 4/Case 6 overlap artifacts and mark rows as exclude, offset, or independently eligible. |
| 23 | Source repo internal wording is consistent. | README/scripts/docs comparison. | Local review found e265 docstring/code mismatch and inconsistent denominator language in `GROUP_CAP.md`. | `Not confirmed` | Record inconsistencies as review findings; require corrected source wording before relying on methodology text. |
| 24 | Arithmetic reproduction is needed for this conceptual audit. | N/A | The requested audit is conceptual: statements, evidence, and policy boundaries. | `Out of scope for conceptual audit` | Keep arithmetic replay separate if committee later accepts a track for payout calculation. |

## Working Order

1. Pin the source commit and freeze the claim set under review.
2. Split the case into e265, e266, and e267-e276 tracks.
3. For each track, identify whether the root issue is chain/protocol, external attack, operational failure, or policy-only.
4. Convert every major statement in the source repository into a checklist row.
5. Attach an evidence type to each row: chain, DevOps, repository claim, protocol code, or committee policy.
6. Mark rows as `Confirmed` only when the named evidence proves the exact statement.
7. Resolve GRC eligibility before reviewing any final payout amount.
8. Resolve denominator/top-up policy before treating e267-e276 amounts as underpayment.
9. Resolve e276 proration before accepting epoch `276` rows.
10. Build final overlap and prior-payment matrix before any approval recommendation.

## Current Working Conclusion

P4 should not be approved as one aggregate package at the current evidence
level.

The case should be split into separate decisions:

- direct e265 cPoC shortfall rows, including the known Case 3 overlap;
- e266 nonce/delegation reconstruction, subject to external-attack scope
  policy;
- e267-e276 `ComputeGroupCap` top-up, subject to cap-eligibility,
  denominator, and e276-proration policy.

The source total `946,509.925002 GONKA` should remain a proposed investigator
total until these conceptual checks are closed.
