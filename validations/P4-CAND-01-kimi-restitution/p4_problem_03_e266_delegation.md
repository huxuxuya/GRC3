# P4 Problem 03: Epoch 266 Delegation

## Question

Should delegators be compensated for the extra penalty caused by delegating Kimi
to an operator that did not enter the final epoch group?

## Current Evidence

Primary local evidence:

- [`p4_audit_pass_05_e266_delegation.md`](p4_audit_pass_05_e266_delegation.md)
- [`p4_e266_delegation_evidence.csv`](p4_e266_delegation_evidence.csv)
- raw `poc_delegation` snapshots at height `4104861`
- raw chain params at height `4105361`

## Findings

| Item | Local result |
|---|---|
| Delegators checked | `9` |
| Snapshot height | `4104861` |
| Kimi delegate target | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` |
| Target operator final epoch-group status | Absent |
| Chain `no_participation_penalty` | `0.15` |
| Chain `delegation_share` | `0.05` |
| Source mechanical delta | `0.10` |

## What Is Proven

- All 9 source delegation rows had raw Kimi delegation to the same excluded
  operator at the source snapshot height.
- The excluded operator was absent from final epoch group `266`.
- Chain params support the source mechanical delta: `0.15 - 0.05 = 0.10`.
- Source chain weights and actual rewards match raw final group and performance
  data.

## What Is Not Proven

- That indirect delegator loss is in GRC scope.
- That delegators should be compensated even if the operator's loss came from an
  external attack.

## Recommended Handling

Treat the chain mechanics as confirmed, but keep compensation eligibility as a
separate committee policy decision. This should not be silently bundled into the
same decision as direct operator exclusion.
