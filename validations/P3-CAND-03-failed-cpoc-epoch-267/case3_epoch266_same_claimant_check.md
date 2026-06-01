# Epoch 266 Same-Claimant Check

Checked participant:

`gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6`

Question: could the same participant have failed in epoch `266` because ordinary
PoC, rather than confirmation PoC, did not have enough validation weight?

## Short Answer

No durable reward-loss evidence was found for this participant in epoch `266`.

The participant:

- was present in epoch `266`;
- was not present in `excluded_participants/266`;
- received and claimed non-zero reward;
- has `rewarded_coins = 239,625,993,655 ngonka`;
- has `claimed = true`.

The ordinary epoch PoC start height was `4,105,361`. At that height the archive
node returned:

| Endpoint | Count |
|---|---:|
| `count_po_c_batches_at_height/4105361` | `0` |
| `count_po_c_validations_at_height/4105361` | `0` |

So there is no ordinary-PoC validation-weight record at the epoch PoC start
height that supports a claim "ordinary PoC lacked enough validation weight for
this participant".

## Epoch 266 Cohort / Reward State

| Metric | Value |
|---|---:|
| Epoch root total weight | `335,159` |
| `>2/3` threshold | `223,440` |
| Claimant root weight | `282` |
| Claimant root confirmation weight | `331` |
| Claimant Qwen voting power | `282` |
| Claimant Qwen PoC weight | `923` |
| Claimant Kimi model-group row | none |
| Rewarded coins | `239,625,993,655 ngonka` |
| Claimed | `true` |
| Excluded in epoch 266 | no |

## Confirmation PoC Rows In Epoch 266

Epoch `266` had three confirmation PoC events:

| Event | Trigger height |
|---:|---:|
| `0` | `4,115,094` |
| `1` | `4,116,984` |
| `2` | `4,118,103` |

These are confirmation PoC events, not ordinary epoch PoC.

For the same participant, the raw cPoC rows show:

| Event | Model | Submitted count | Actual validating voting power | Share of root total | Meets `>2/3`? | Shortfall/surplus vs `223,440` |
|---:|---|---:|---:|---:|---|---:|
| `0` | Qwen | `992` | `248,450` | `74.1290%` | yes | `+25,010` |
| `0` | Kimi | `43,296` | `108,719` | `32.4380%` | no | `-114,721` |
| `1` | Qwen | `11,424` | `244,178` | `72.8544%` | yes | `+20,738` |
| `1` | Kimi | `48,480` | `108,719` | `32.4380%` | no | `-114,721` |
| `2` | Qwen | `11,776` | `232,101` | `69.2510%` | yes | `+8,661` |
| `2` | Kimi | `49,888` | `99,972` | `29.8282%` | no | `-123,468` |

Interpretation:

- Qwen cPoC rows had enough validation voting power in all three events.
- Kimi cPoC rows did not reach `>2/3`.
- However, the participant had no Kimi model-group row in epoch `266`, was not
  excluded, and received a non-zero claimed reward. Therefore these Kimi rows
  do not prove a compensable ordinary-PoC failure for this participant in epoch
  `266`.

## Boundary For Case 3

Epoch `266` is different from the validated epoch `267` failure:

| Epoch | Exclusion? | Reward | Confirmation failure evidence | Case-3-like compensation evidence |
|---:|---|---:|---|---|
| `266` | no | `239,625,993,655 ngonka` | Kimi cPoC rows below `>2/3`, but no exclusion and no zero reward | no |
| `267` | yes, `failed_confirmation_poc` at `4,122,552` | `0` | `ConfirmationPoCRatio = 0.0057419461588255 < 0.5` | yes |

Conclusion: based on current archive evidence, epoch `266` should not be treated
as another loss for the same claimant unless a separate mechanism is proven.

