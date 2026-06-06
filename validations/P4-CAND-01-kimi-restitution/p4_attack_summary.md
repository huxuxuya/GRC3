# P4 Attack Summary: Epochs 265-266

This note summarizes the P4 attack-attributed part only: epochs `265`
and `266`. It uses saved raw chain cache files and copied source
artifacts; it does not query nodes and does not run source scripts.

Important data-source split: participant counts, final rewarded coins,
burned coins, final group rows, and exclusion rows come from saved raw
chain responses. The theoretical fixed epoch reward pool is taken from
the saved source compensation JSON, because the raw performance summary
endpoint does not expose that pool directly.

## Epoch Summary

| Epoch | Participants union | Final group | Excluded | Zero-reward perf rows | Source affected rows | Source affected unique | Source comp | Gov remainder |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `265` | `53` | `51` | `14` | `16` | `3` | `3` | `30592.104861828` | `99367.459994517` |
| `266` | `48` | `46` | `7` | `10` | `27` | `26` | `188698.468968749` | `23623.554076714` |

## E266 Source Split

| Sub-track | Rows |
|---|---:|
| Absent final-set operators | `9` |
| In-final-group zero-reward rows | `5` |
| In-final-group rewarded top-up rows | `4` |
| Delegation rows | `9` |

## Gov Remainder Interpretation

- Source e265+e266 compensation total: `219290.573830577` GONKA.
- Raw-settlement gov remainder for e265+e266: `122991.014071231` GONKA.
- These numbers are not expected to match. Source compensation is a
  counterfactual reconstruction; gov remainder is the epoch reward pool
  left undistributed after actual rewarded/burned coins.
- Treat the gov remainder as an epoch-level undistributed settlement
  remainder, not as a direct proof of a wallet balance delta.
- For e266 especially, source compensation is much larger than the gov
  remainder, so the source claim cannot be described as simply
  'all lost rewards went to the gov wallet'.

## Main Takeaway

The attack-attributed source package covers a small subset of participant
rows, but its proposed compensation is not equal to the amount that can
be directly identified as epoch-level governance remainder.
