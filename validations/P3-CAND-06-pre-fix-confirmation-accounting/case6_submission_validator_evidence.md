# P3-CAND-06 Submission And Validator Evidence

This artifact fetches the raw cPoC stage commit and validation rows for
the `24` candidate loss events, then reconstructs submitted counts,
validator counts, valid validator weight, and strict `>2/3` pass/fail
results. It does not execute any external compensation repository.

## Result

| Metric | Value |
|---|---:|
| Candidate rows | `24` |
| Unique participants | `19` |
| Unique cPoC trigger heights fetched | `16` |
| Model rows checked | `48` |
| Model rows matching the previous aggregate CSV | `48` |
| Model rows with a stage commit/submission | `25` |
| Model rows with `pass_weight` | `25` |
| Candidate keys reconstructed | `24` |
| Source mismatches | `0` |

## What This Proves

- The previous aggregate `submitted_count`, `valid_weight`, and model result
  columns are reproducible from raw stage commit and validation rows.
- Every candidate has at least one model with a cPoC store commit and enough
  validator weight to satisfy strict `validWeight > TotalNetworkWeight * 2 / 3`.
- The loss is therefore not explained by a simple lack of validators for the
  passing model.

## What This Does Not Prove

- The chain endpoints expose cPoC store commit counts/root hashes and
  validation rows here, not every individual off-chain nonce/payload body.
- For rows with one passing model and one no-submission model, eligibility is
  still a policy/protocol question: the raw data proves one model passed, but
  not that the missing model should have been ignored for compensation.
- Coefficient replay is now recorded separately: `5/6` prior simple-ratio
  mismatch rows reconcile, and the remaining non-match is in epoch `276`
  overlap review.

## Both-Model Pass Rows

| Epoch | Participant | Trigger | Qwen commit/validators/weight | Kimi commit/validators/weight |
|---:|---|---:|---|---|
| `276` | `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | `4267778` | `11552` / `22` / `86.9859%` | `12160` / `15` / `78.7207%` |

## Stage Fetch Summary

| Trigger height | Commit rows | Validation outer rows | Validation inner rows |
|---:|---:|---:|---:|
| `4073650` | `42` | `42` | `968` |
| `4075202` | `44` | `44` | `1035` |
| `4102890` | `36` | `36` | `610` |
| `4144898` | `35` | `35` | `639` |
| `4153434` | `41` | `41` | `845` |
| `4164861` | `40` | `40` | `793` |
| `4184386` | `40` | `40` | `769` |
| `4202293` | `46` | `46` | `969` |
| `4209686` | `43` | `43` | `900` |
| `4215427` | `41` | `41` | `953` |
| `4231815` | `42` | `42` | `934` |
| `4232787` | `28` | `28` | `407` |
| `4258197` | `41` | `41` | `844` |
| `4264130` | `38` | `38` | `776` |
| `4265965` | `37` | `37` | `793` |
| `4267778` | `39` | `39` | `767` |

Machine-readable details:

- `case6_submission_validator_evidence.csv`
- `case6_submission_validator_evidence.json`
- raw endpoint cache: `raw_stage_cache/`
