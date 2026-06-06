# Votkon Kimi Restitution Repo: Truthfulness Review

Source reviewed: <https://github.com/votkon/gonka-kimi-restitution>

Local read-only clone used for this pass:
`/private/tmp/gonka-kimi-restitution`.

## High-Level Verdict

The repository is partly true, but not fully proven as a compensation case.

What is broadly true:

- There are real on-chain Kimi weight/confirmation anomalies in epochs
  `265..276`.
- Epoch `266` really contains Kimi nonce submitters that did not enter the
  epoch group, and the repository reconstructs weights from commit counts using
  historical model scale factors.
- Epochs `267..276` really show a `ComputeGroupCap` effect where Kimi
  `confirmation_weight` is much larger than capped `weight`.
- The current aggregate total in the repository is internally consistent with
  its JSON outputs: `946,509.925002 GONKA`, `53` unique addresses.

What is not fully proven:

- That all listed losses are eligible for GRC restitution.
- That an external attack in epochs `265..266` should be compensated by GRC.
- That the intended `ComputeGroupCap` protocol rule in epochs `267..276` should
  be treated as a compensable bug rather than a balancing mechanism.
- That the compensation formula is the only chain-correct counterfactual.
- That epoch `276` should be compensated without proration even though
  `v0.2.13` activated mid-epoch.

## Current Repo Totals

The current upstream repository reports:

| Scope | Value |
|---|---:|
| Epochs | `265..276` |
| Unique addresses | `53` |
| Grand total | `946,509.925002 GONKA` |

Per-epoch totals from the checked JSON files:

| Epoch | Reported compensation, GONKA | Method class |
|---:|---:|---|
| `265` | `30,592.104861828` | CPoC degradation / attack attribution |
| `266` | `188,698.468968749` | nonce exclusion + delegation |
| `267` | `246,471.823957226` | `ComputeGroupCap` top-up |
| `268` | `42,634.684509205` | `ComputeGroupCap` top-up |
| `269` | `47,504.581758505` | `ComputeGroupCap` top-up |
| `270` | `76,870.083553475` | `ComputeGroupCap` top-up |
| `271` | `28,422.154068920` | `ComputeGroupCap` top-up |
| `272` | `16,988.149548048` | `ComputeGroupCap` top-up |
| `273` | `86,243.303557245` | `ComputeGroupCap` top-up |
| `274` | `41,818.441790908` | `ComputeGroupCap` top-up |
| `275` | `89,984.775198122` | `ComputeGroupCap` top-up |
| `276` | `50,281.353229327` | `ComputeGroupCap` top-up |

Repository-sync note: the public case page has been updated to the current
upstream repository total: `946,509.925002 GONKA` and `53` addresses.

## Claim Review

| Claim | Review result | Notes |
|---|---|---|
| Kimi was affected across epochs `265..276`. | `Partly confirmed` | The chain evidence shows Kimi-specific anomalies and cap effects, but this does not automatically prove compensation eligibility for every epoch. |
| Epoch `265` has direct Kimi CPoC degradation. | `Partly confirmed` | The largest row for `gonka1j7x6...` matches our Case 3 chain-state result: `20,896.527179100 GONKA`. The two extra e265 rows are broader attack/cw-drop rows and require separate policy review. |
| Epoch `266` has nonce exclusion. | `Partially confirmed, policy contested` | Audit pass 04 confirms the narrow raw fact for the nine source-listed excluded operators: they have PoC commits and are absent from the final epoch group/performance rows. The source nonce table has `18` rows, including in-final-group rewarded top-up rows and in-final-group zero-reward rows, so the full e266 nonce payout is broader than final-set exclusion. The source model labels match the same raw commit rows, but our raw CLI output does not include `model_id`. |
| Delegators in e266 lost extra weight because their operator was excluded. | `Chain facts confirmed, policy required` | Audit pass 05 confirms all 9 source rows had raw Kimi delegation to `gonka1q5xt54...` at snapshot height `4104861`; that operator was absent from the final epoch group; and chain params give `0.15 - 0.05 = 0.10`. Eligibility still depends on accepting indirect delegator losses as compensable. |
| `ComputeGroupCap` reduced Kimi weight in e267+. | `Confirmed as protocol behavior` | The cap effect itself is real. DevOps evidence and repo data both describe the `75%` cap and Kimi scaling. |
| `ComputeGroupCap` underpayment should be compensated. | `Not technically settled` | The cap is an intended protocol mechanism. Compensation requires a policy decision that this intended mechanism produced an unfair/restorable loss. |
| e267+ formula is chain-correct. | `Methodology contested` | The scripts use `correct_reward = confirmation_weight / root_total_weight * epoch_reward`, then subtract actual rewards. This is a top-up against the capped settlement denominator, not a full uncapped network settlement replay. |
| e276 should be included at full epoch amount. | `Unresolved` | The repo states `v0.2.13` activated at block `4,267,300` during epoch `276`, but the e276 script calculates against true epoch end without a visible proration rule. |

## Main Methodology Problem

For epochs `267..276`, the repository treats Kimi `confirmation_weight` as the
restored reward numerator while keeping the already-capped
`EpochGroupData.total_weight` as the denominator:

```text
correct_reward = confirmation_weight_i / root_total_weight * epoch_reward
compensation   = max(0, correct_reward - actual_rewards)
```

This is not the same as asking, "what would the whole epoch settlement have
looked like if `ComputeGroupCap` had not existed?"

A full uncapped replay would need to:

1. reconstruct uncapped weights for all affected Kimi rows;
2. recompute the total network denominator;
3. replay rewards for all participants under that denominator;
4. compensate only the difference between actual and replayed rewards.

The repository explicitly rejects this stricter approach by arguing that Qwen
rewards were already paid and cannot be clawed back. That is a policy argument,
not a chain-style settlement replay.

## Internal Inconsistencies / Weak Points

| Item | Why it matters |
|---|---|
| Public case metadata changed materially | The current upstream repo says `946,509.925002 GONKA` / `53` addresses. Earlier local metadata used `710,772.72 GNK` / `52` addresses, so downstream references should pin the upstream commit. |
| e265 script docstring and code disagree | The docstring says `confirmation_weight_i / total_confirmation_weight`, but the code uses `weight / total_epoch_weight`. The resulting numbers use weight, not the docstring formula. |
| e267 `GROUP_CAP.md` contains two denominator descriptions | It first describes `confirmation_weight / total_uncapped_confirmation_weight`, then says using `confirmation_weight / EpochGroupData.total_weight` is correct. These are different denominators. |
| e276 no-proration assumption is not justified in the calculation | The upgrade is described as mid-epoch, but the script uses the full epoch end state. |
| e265/e266 are attributed to external attack | That may be factually true, but GRC eligibility is not a technical conclusion. |
| e267+ cap is an intended protocol rule | Treating an intended balancing mechanism as a compensable bug requires committee approval. |

## Case 3 Overlap

The e265 row for
`gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6` matches our Case 3 extended
chain-state amount:

| Epoch | Address | Votkon amount, GONKA | Our Case 3 position |
|---:|---|---:|---|
| `265` | `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6` | `20,896.527179100` | Same Kimi cPoC shortfall class as epoch `267`; reasonable to include in Case 3 if committee accepts the extension. |

The Votkon repo also includes the same address in epoch `266` for
`18,913.149363914 GONKA`. We did not classify that e266 row as Case 3-like:
our prior check found that the claimant was not in `excluded_participants/266`,
received a non-zero reward, and did not have the same zero-reward cPoC-failure
signature as epochs `265` and `267`.

## Bottom Line

The repository is useful evidence, but as a compensation package it is too broad
to approve mechanically.

Recommended committee treatment:

1. Split the package into separate policy questions:
   - direct cPoC shortfall rows, including the Case 3 e265/e267 address;
   - epoch `266` attack/nonce/delegation reconstruction;
   - epochs `267..276` `ComputeGroupCap` top-up.
2. Do not treat the `946,509.925002 GONKA` total as a validated GRC amount.
3. Require a decision on the e267+ denominator model:
   - top-up using capped `root_total_weight`, as the repo does; or
   - full uncapped settlement replay with a recomputed denominator.
4. Require a specific e276 proration or non-proration justification.
5. Pin any public discussion to the upstream commit used for the totals:
   `5462c55a6b95d50dfb53bdc4211cdcd31369c2ea`.
