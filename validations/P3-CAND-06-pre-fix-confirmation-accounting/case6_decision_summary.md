# P3-CAND-06 Decision Summary

P3-CAND-06 is a candidate set for pre-fix confirmation-accounting losses.
The rows were found independently from archive-chain data. The common
shape is: the participant received zero reward after
`failed_confirmation_poc`, while at least one submitted Qwen/Kimi model
had strict cPoC validator weight above the chain's `2/3` threshold.

## Current Conclusion

The technical evidence supports a pre-`v0.2.13` confirmation-accounting
mismatch as the root-cause family. It does not prove that all rows should
be paid automatically.

| Check | Result |
|---|---:|
| Candidate rows | `24` |
| Unique participants | `19` |
| Estimated zero-reward loss | `120,822.324371792000 GONKA` |
| Old-formula replay matches stored ratio | `22` |
| Bounded v0.2.13-style rows passing alpha | `0` |
| Formula-reconciled rows needing policy decision | `20` |
| Epoch-276 rows blocked by overlap | `4` |

## What Is Proven

- For every row, at least one Qwen/Kimi model had cPoC evidence that reached
  strict `pass_weight`.
- The evidence includes chain cPoC store commits/root hashes, validation
  rows, validator counts, and valid validator voting weight.
- The full pre-fix formula replay matches stored confirmation ratios for
  `22` of `24` rows.
- The two old-formula non-matches are both in epoch `276`, which is already
  blocked for overlap review.
- The fix family is `v0.2.13` / PR `#1143`, where the chain added a stable
  confirmation-weight snapshot and reused it across confirmation and reward
  calculations.

## What Is Not Proven

- The available raw endpoints do not expose every off-chain nonce/payload
  body; the proof is at chain commit and validator-row level.
- The bounded v0.2.13-style replay does not make any of these rows pass
  alpha automatically, so single-model compensation remains a committee
  policy decision.
- Epoch `276` rows cannot be paid from this case until P3-CAND-04 duplicate
  risk is resolved.

## Action Split

| Action | Rows | Loss, GNK | Meaning |
|---|---:|---:|---|
| `clear` | `6` | `14,729.197017136000` | No local overlap signal; still needs single-model policy decision. |
| `review` | `14` | `63,293.737800953000` | Compare against P4-CAND-01 before payout. |
| `blocked` | `4` | `42,799.389553703000` | Resolve P3-CAND-04 duplicate risk first. |

## Overlap Split

| Overlap status | Rows |
|---|---:|
| `known_p3_cand_04_same_address` | `1` |
| `no_known_overlap_in_local_repo` | `6` |
| `p3_cand_04_epoch_overlap_unresolved` | `3` |
| `p4_cand_01_epoch_range_overlap` | `14` |

## Recommended Reading Order

1. `case6_decision_summary.md` for the one-page conclusion.
2. `case6_evidence_ledger.md` for row-by-row evidence.
3. `case6_full_old_formula_replay.md` for formula reconciliation.
4. `case6_new_algorithm_replay.md` for the bounded post-fix counterfactual.
5. `case6_overlap_matrix.md` before any payout decision.
