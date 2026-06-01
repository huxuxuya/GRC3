# Case 3 Chain Formula Reconciliation

This note maps the Case 3 validation tables back to the chain formulas used at
the historical epoch `265` and `267` heights.

## Code Version Checked

The current `gonka` `main` branch is post-fix and includes
`confirmation_weight_scales`. Historical state for epochs `265` and `267` has
empty `confirmation_weight_scales`, so the matching formula is the pre-fix
parent of the `v0.2.13` microrelease:

```text
gonka commit checked: d8b8e907
later fixed main:      17808620
```

## Fixed In

This failure class is addressed by the `v0.2.13` microrelease:

```text
upgrade / release: v0.2.13
fix PR:            #1143
fix commit:        17808620
proposal path:     proposals/governance-artifacts/update-v0.2.13/README.md
```

The upgrade proposal describes the issue as confirmation PoC using different
model sets for measured weight, preserved weight, and reward rescaling. During
new-model bootstrap this could reduce confirmation weight for honest miners
serving both an eligible model and a not-yet-eligible model.

The fix stores one epoch snapshot of confirmable models and weight-scale
factors, then uses that snapshot for confirmation and reward calculations. The
upgrade also disables confirmation PoC triggers for the rest of the upgrade
epoch so the new snapshot logic starts from the next epoch.

The relevant pre-fix chain paths are:

- `inference-chain/x/inference/module/chainvalidation.go`
- `inference-chain/x/inference/module/confirmation_poc.go`
- `inference-chain/x/inference/module/aggregation.go`

## Raw cPoC Validation Weight

For epochs `265` and `267`, chain params have:

```text
poc_params.validation_slots = 0
```

That means the non-slot branch in `pocValidated` is used. The chain computes:

```text
validWeight = sum(model voting power for validators with ValidatedWeight > 0)
twoThirds   = TotalNetworkWeight * 2 / 3
pass        = validWeight > twoThirds
```

Important consequences for the validation tables:

- the denominator is root/snapshot `TotalNetworkWeight`;
- model `total_weight` is not the `>2/3` denominator;
- model `voting_power` is what gets summed for the validator side;
- the check is strict `>2/3`, so the minimum integer pass line is
  `floor(TotalNetworkWeight * 2 / 3) + 1`.

This matches the corrected epoch timeline tables:

| Epoch | `TotalNetworkWeight` | Exact `2/3` | Minimum integer pass line |
|---:|---:|---:|---:|
| `265` | `904,177` | `602,784.666667` | `602,785` |
| `267` | `541,415` | `360,943.333333` | `360,944` |

## Final Confirmation Ratio

The final exclusion is not decided only by the raw cPoC row. The chain then
updates confirmation weight in `evaluateConfirmation` and `foldEventReadings`.

Pre-fix formula:

```text
reading       = preserved[participant] + measured[participant]
totalExpected = preserved[participant] + notPreserved[participant]

if reading < ConfirmationWeight:
    ConfirmationWeight = reading

ConfirmationPoCRatio = min((reading / totalExpected) / 0.909, 1)
```

Then status logic compares the ratio with:

```text
AlphaThreshold = 0.5
```

The `0.909` value is `pocDeviationCoeff`.

The `preserved` and `notPreserved` maps used here are coefficient-adjusted PoC
node weights from `partitionWeightByPreservation`, not the same thing as the
model voting-power availability diagnostics in the timeline tables.

The coefficient aggregation is:

```text
consensusWeight(participant) =
    sum(model_weight_raw_i * model.WeightScaleFactor_i)
```

Models without an explicit coefficient use `1.0`; the product is truncated to
integer per model.

## Numeric Reconciliation

The chain-state ratio can be reconstructed from the historical formula.

### Epoch 265

Chain state:

```text
ConfirmationWeight before exclusion = 66,311
ConfirmationWeight at exclusion     = 323
ConfirmationPoCRatio                = 0.0053586212476565
```

Formula replay:

```text
323 / 66,311 / 0.909 = 0.0053586212476565778759716088633188091471299714007232
```

The stored ratio differs only by decimal serialization/truncation:

```text
stored ratio = 0.0053586212476565
diff         = 0.0000000000000000778759716088633188091471299714007232
```

### Epoch 267

Chain state:

```text
ConfirmationWeight before exclusion = 65,716
ConfirmationWeight at exclusion     = 343
ConfirmationPoCRatio                = 0.0057419461588255
```

Formula replay:

```text
343 / 65,716 / 0.909 = 0.0057419461588255118652044156269056816205693854430182
```

The stored ratio differs only by decimal serialization/truncation:

```text
stored ratio = 0.0057419461588255
diff         = 0.0000000000000000118652044156269056816205693854430182
```

## Conclusion

The validation package now separates two calculations:

1. Raw cPoC majority diagnostics, which match `pocValidated`:
   `sum(model voting power) > TotalNetworkWeight * 2 / 3`.
2. Final exclusion ratio, which matches `foldEventReadings`:
   `(preserved + measured) / (preserved + notPreserved) / 0.909`.

For epochs `265` and `267`, both the `>2/3` denominators and the final
`ConfirmationPoCRatio` values reconcile with the historical chain formulas.
