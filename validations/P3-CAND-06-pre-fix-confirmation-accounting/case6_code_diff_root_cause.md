# P3-CAND-06 Code-Diff Root-Cause Proof

This note records the independent code review of the fix that matches
`P3-CAND-06`.

Reviewed source:

| Item | Value |
|---|---|
| Repository | `github.com/gonka-ai/gonka` |
| Local checkout | `/tmp/gonka` |
| Fix commit | `17808620293b57112896bcbb7f99c4c2f554d6c8` |
| Release / PR | `v0.2.13` / PR `#1143` |
| Parent comparison | `git diff HEAD^ HEAD -- inference-chain/x/inference` |

The checkout was unshallowed before review, so the file-level findings below
come from the real parent-to-fix diff, not only from final source inspection.

## What The Fix Says It Fixes

The `v0.2.13` commit message describes a confirmation-PoC failure during
new-model bootstrap: measured weight, preserved weight, and reward rescaling
used different model sets. That could slash honest miners that served both an
eligible model and a not-yet-eligible model.

The stated fix is to store one epoch snapshot of confirmable models and
weight-scale factors, then use that snapshot for confirmation and reward-weight
calculations.

That matches the `P3-CAND-06` observed shape:

- at least one submitted model reaches strict `pass_weight`;
- durable state still records `failed_confirmation_poc`;
- the participant receives zero reward;
- the cPoC ratio is below alpha;
- raw stage data confirms validator weight existed for the passing model.

## Code Path Added By The Fix

### 1. One epoch snapshot of confirmable models is built

New file:

```text
inference-chain/x/inference/module/confirmation_weight_scales.go
```

Key behavior in `buildConfirmationWeightScales`:

- takes the epoch's eligible model list;
- scans active participants' model voting powers;
- keeps only models with positive voting power and eligible status;
- stores each kept model with its `WeightScaleFactor`.

Source lines in the reviewed checkout:

```text
confirmation_weight_scales.go:5-35
```

This is important because models outside that snapshot are not supposed to be
counted in cPoC confirmation accounting for that epoch.

### 2. The snapshot is stored in epoch group state

Changed file:

```text
inference-chain/x/inference/module/module.go
```

Relevant diff:

```text
module.go:739-743   buildConfirmationWeightScales(...)
module.go:783-784   upcomingEg.GroupData.ConfirmationWeightScales = confirmationWeightScales
```

The fix also adds a durable field:

```text
inference-chain/proto/inference/inference/epoch_group_data.proto
epoch_group_data.proto:39   repeated ConfirmationWeightScale confirmation_weight_scales = 19;
```

This means the model-set/scale-factor snapshot is part of epoch group data, not
a transient local calculation.

### 3. Initial confirmation weight uses the same snapshot

Changed file:

```text
inference-chain/x/inference/module/module.go
```

Relevant lines:

```text
module.go:1127-1128   coefficients := ConfirmationWeightCoefficients(scales)
module.go:1142-1144   initialConfirmationWeight := ConfirmationWeightOfParticipantWithCoefficients(...)
```

Changed file:

```text
inference-chain/x/inference/epochgroup/epoch_group.go
```

The old helper `CalculateMLNodesTotalWeight` was removed. That old helper used
`1.0` for a model without a coefficient. The new helper only counts models
present in `ConfirmationWeightScales`.

This matters for `P3-CAND-06`: serving a not-yet-confirmable model should not
inflate the denominator or create a mismatched comparison against the submitted
model that actually passed.

### 4. cPoC event evaluation uses the same snapshot

Changed file:

```text
inference-chain/x/inference/module/confirmation_poc.go
```

Relevant lines:

```text
confirmation_poc.go:391-397   load ConfirmationWeightScales and skip if absent
confirmation_poc.go:640-645   filter scales to models present in the validation snapshot
confirmation_poc.go:648-657   measured weight uses ConfirmationWeightCoefficients(scales)
confirmation_poc.go:662-680   preserved weight uses the same coefficients/scales
```

The pre-fix path took model coefficients from current PoC params and partitioned
preserved/not-preserved weight separately. The fix makes the event-local
reading:

```text
reading = preserved_weight_from_snapshot + measured_weight_from_snapshot
total_expected = active_participant_weight_from_same_snapshot
```

The ratio is then computed from `reading / total_expected`, with the existing
PoC deviation coefficient.

### 5. Reward rescaling uses the same snapshot

Changed file:

```text
inference-chain/x/inference/keeper/bitcoin_rewards.go
```

Relevant lines:

```text
bitcoin_rewards.go:574       ConfirmationWeightCoefficients(epochGroupData.ConfirmationWeightScales)
bitcoin_rewards.go:613-625   rawTotal uses ConfirmationWeightOfModelNodesWithCoefficients(...)
```

This closes the third inconsistent surface named in the release text: rewards
now rescale confirmation weight against the same epoch snapshot instead of a
different model/coefficient set.

## Tests Added Or Changed By The Fix

The fix adds direct tests for the new accounting behavior:

| File | Test | What it proves |
|---|---|---|
| `types/weight_test.go` | `TestConfirmationWeightOfModelNodes` | Models not present in `ConfirmationWeightScales` are ignored. |
| `types/weight_test.go` | `TestConfirmationWeightOfParticipantMatchesModelNodes` | Participant and model-node calculations use the same coefficient logic. |
| `module/preserved_nodes_snapshot_test.go` | `TestPreservedWeightByParticipantFiltersToConfirmationScales` | Preserved weight is filtered to the confirmation snapshot, not all served models. |
| `epochgroup/epoch_group_test.go` | `TestNewEpochMemberFromActiveParticipant_UsesProvidedConfirmationWeight` | Epoch member stores the caller-provided precomputed confirmation weight. |

The most direct test is
`TestPreservedWeightByParticipantFiltersToConfirmationScales`: a participant has
`model-a` and `model-b`, the preserved snapshot includes nodes for both, but
`ConfirmationWeightScales` contains only `model-a`. The expected preserved
weight counts only `model-a`.

## Why This Strengthens The Root-Cause Finding

The raw chain replay already ruled out the simple explanation "there were not
enough validators for the submitted passing model":

| Evidence | Result |
|---|---:|
| Candidate rows | `24` |
| Raw model rows reconstructed | `48` |
| Raw model rows matching aggregate scan | `48/48` |
| Model rows with cPoC store commit/submission | `25` |
| Model rows with strict `pass_weight` | `25` |
| Candidate rows covered by at least one passing model | `24/24` |

The code diff explains how those facts can coexist with durable
`failed_confirmation_poc`: before `v0.2.13`, confirmation accounting could
compare measured, preserved, and reward weights across different model sets
during new-model bootstrap. After `v0.2.13`, one stored epoch snapshot is used
throughout.

Therefore the current root-cause confidence for the class is high:

```text
P3-CAND-06 is consistent with pre-v0.2.13 confirmation accounting mismatch,
not with a simple lack of submissions or validator weight for the passing model.
```

## What This Does Not Yet Prove

This code-diff review does not by itself approve all `24` rows for payout.
Open review remains:

- `20` non-epoch-276 single-model rows are formula-reconciled, but still need
  an eligibility decision: protocol-bug loss vs ordinary incomplete multi-model
  service.
- `4` epoch `276` rows remain blocked by P3-CAND-04 overlap risk.
- The bounded v0.2.13-style replay over available Qwen/Kimi data does not make
  any of the `24` rows pass alpha, so single-model payout remains a policy
  question rather than an automatic technical conclusion.
- The raw cPoC endpoints expose store commits/root hashes and validation rows;
  they do not expose every individual off-chain payload body.

## Conclusion

`v0.2.13` / PR `#1143` is the matching fix family for `P3-CAND-06`.

The fix directly changes the confirmation accounting surfaces that can explain
the candidate rows:

1. build and store a per-epoch confirmable-model scale snapshot;
2. initialize epoch-member confirmation weight from that snapshot;
3. evaluate cPoC measured and preserved weight from that snapshot;
4. rescale rewards from that snapshot;
5. test that non-snapshot models are ignored.

This supports treating `P3-CAND-06` as a real pre-fix confirmation-accounting
candidate set, while keeping eligibility and overlap decisions separate.
