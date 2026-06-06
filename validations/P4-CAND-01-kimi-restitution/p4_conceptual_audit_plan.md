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
| 4 | The other two epoch `265` rows are direct cPoC restitution victims. | Per-address chain trace showing the same direct cPoC failure signature, not only confirmation-weight drop. | Audit pass 03 shows `gonka1830...` had Kimi model voting power but zero raw commit rows and zero validation records for both Kimi and Qwen at final cPoC stage `4102890`; `gonka17...` is a rewarded confirmation-weight-drop row, not a direct zero-reward cPoC victim. | `Not confirmed` | Treat both rows as outside strict Case-3-like direct Kimi cPoC shortfall unless committee creates a broader policy track. |
| 5 | Epoch `265` losses were caused by external attack. | Production logs, timestamps, incident correlation, affected Kimi nodes, and chain state transition. | Source repo asserts attack attribution; DevOps evidence supports Kimi operational disruption generally, but current local chain review only proves state changes. | `Partially confirmed` | Require incident evidence and map it to exact block/time and affected rows. |
| 6 | External attack losses in e265 are eligible for GRC restitution. | Committee policy that external actor / operator-disruption losses are in scope. | Existing public case says GRC voted against including P4; eligibility remains policy-based. | `Policy required` | Decide whether external attack losses can be compensated by GRC at all. |
| 7 | Epoch `266` has nine PoC submitters that did not enter the final epoch group. | PoC commit list, final epoch group, excluded/missing participant comparison. | Audit pass 04 confirms all nine source-listed excluded operators have raw PoC commit rows, raw validation records, no final epoch-group row, and no performance row. The independent raw commit and validation outputs still do not include `model_id`; Votkon's source commit artifact labels exactly matching raw rows as Kimi. | `Confirmed` for submission + final-set absence; `Source-backed only` for Kimi-specific attribution | Treat Kimi label as source-backed unless a richer chain endpoint with `model_id` is found. |
| 8 | Epoch `266` reconstructed nonce weights should be used as the reward basis. | On-chain commit counts, historical model scale factors, and an accepted reconstruction rule. | Pass 04 shows the source nonce table has `18` rows: `9` excluded operators, `4` in-final-group rewarded top-up rows, and `5` in-final-group zero-reward rows. This is broader than final-set exclusion. | `Policy required` | Decide whether reconstructed PoC work can compensate top-up rows that were in the final epoch group. |
| 9 | Epoch `266` zero-reward submitters are victims, not ordinary failed participants. | Causal proof that exclusion came from the claimed incident, not local failure, invalid work, or protocol-valid exclusion. | Pass 04 identifies `5` source nonce-compensation rows that were in the final group but had zero rewards and `failed_confirmation_poc` exclusion entries. These need row-level cause review before being treated as attack victims. | `Partially confirmed` | Review each in-final-group zero-reward row separately from the nine absent operators. |
| 10 | Epoch `266` delegators lost an extra `10%` due to ModeNone instead of ModeDelegate. | Delegation snapshot, operator exclusion proof, chain delegation penalty parameters. | Audit pass 05 confirms all `9` source rows had raw Kimi delegation to excluded operator `gonka1q5xt54...` at snapshot height `4104861`; the operator was absent from final epoch group; and chain params confirm `0.15` ModeNone penalty minus `0.05` delegation share. | `Confirmed` for chain mechanics; `Policy required` for compensation eligibility | Keep the raw delegation cache and decide whether indirect delegator losses belong in P4 scope. |
| 11 | e266 delegation compensation is eligible even if the operator's loss came from external attack. | Committee policy on indirect losses and attack scope. | No local policy proof. | `Policy required` | Create an explicit committee decision for indirect/delegator eligibility. |
| 12 | `ComputeGroupCap` existed and reduced Kimi weight in e267-e276. | Chain code/params, DevOps evidence, epoch group weight vs confirmation-weight patterns. | Pass 06 checks raw root and Kimi model group data for every epoch `267..276`; the cap/weight-pressure pattern is real chain state. | `Confirmed` | Treat cap effect as real protocol behavior. |
| 13 | `ComputeGroupCap` was a protocol bug rather than intended balancing behavior. | Code intent, parameter history, reviewer statements, and mitigation rationale. | Public case notes that `ComputeGroupCap` is an intended rule and that GRC reviewers questioned compensating it. | `Policy required` | Committee must decide whether intended cap behavior can become compensable due to context. |
| 14 | e267-e276 Kimi operators were underpaid relative to actual confirmed work. | Accepted counterfactual reward model and chain proof of confirmed work. | Pass 06 confirms source affected rows match raw root `weight`, raw root `confirmation_weight`, and raw performance rewards, and that the source top-up formula is reproducible. Whether this is underpayment depends on the accepted denominator model. | `Partially confirmed` | Resolve denominator/counterfactual model before calling the difference underpayment. |
| 15 | The source e267-e276 formula is chain-correct. | Full reward replay or protocol-level proof that capped `root_total_weight` should remain the denominator. | Pass 06 shows material denominator sensitivity across epochs `267..276`: source capped-root top-up totals `727,219.351170981` GONKA, all-root-confirmation denominator totals `503,653.983658046` GONKA, and replace-affected denominator totals `360,858.547914700` GONKA. | `Policy required` | Choose one model: top-up against paid settlement, all-confirmation denominator, or another full replay rule. |
| 16 | Qwen rewards already paid means Kimi should be topped up without recalculating the full denominator. | Committee policy on non-clawback top-ups and restitution source of funds. | Source makes this argument explicitly, but it is a policy choice. | `Policy required` | Committee must approve or reject top-up accounting. |
| 17 | e276 should be compensated as a full affected epoch. | Upgrade block, stage timing, reward settlement timing, and proration policy. | Pass 06 confirms upgrade block `4,267,300` is inside raw epoch `276` window (`effective_block_height=4,259,671`, `last_block_height=4,275,061`); about `0.4957` of the effective epoch block span is before the upgrade. | `Policy required` | Decide full-epoch vs prorated e276 treatment and document why. |
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
