# P3-CAND-06 Overlap Review

This note separates proven address overlap from epoch-level review signals.

## P3-CAND-04

| Check | Result |
|---|---:|
| Epoch `276` candidate rows | `4` |
| Known same-address overlap in local evidence | `1` |

Known same-address overlap:

| Epoch | Participant | Loss, GONKA | Note |
|---:|---|---:|---|
| `276` | `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | `17356.095656742` | Also named in P3-CAND-04 public evidence. |

The other epoch `276` rows are epoch-level overlaps with P3-CAND-04, but
the local repository does not contain the full `payout276` address list.
They should remain blocked from payout until checked against that list.

## P4-CAND-01

| Check | Result |
|---|---:|
| Candidate rows in P4-CAND-01 epoch range `265..276` | `18` |

This is an epoch-level overlap only. The current repository does not include
a normalized P4-CAND-01 address-by-epoch table, so same-address duplicate
risk is unresolved here.

## Decision Rule

- Do not approve any P3-CAND-06 row that overlaps an already-approved row by
  address and epoch.
- Treat epoch-level overlap as a mandatory review signal, not as proof of
  duplicate compensation.
