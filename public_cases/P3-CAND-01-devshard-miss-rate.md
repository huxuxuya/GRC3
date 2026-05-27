# P3-CAND-01: High Miss Rate / Devshard Issue

| Field | Value |
|---|---|
| Proposal | Proposal #3 candidate |
| Epochs | 269-272; main reported incident: 272 |
| Status | Investigation |
| Reported by | Votkon; technical reports by Nik |
| Affected / detail contact | Not finalized; Nik for monitored nodes |
| Investigated by | Fedor Tmkhv; shard-proof audit outputs |
| Result so far | On-chain reward outcomes identified; protocol bug not established |
| Further analysis | Required: retained devshard proof/stat data and root-cause determination |
| Compensation | Not approved; preliminary estimates only |

## Message Log

| Date | Author | Fact / short quote | Meaning |
|---|---|---|---|
| 2026-05-23 13:12 UTC+03 | Votkon | "another potential case... add it to proposal #3" | Case proposed for Proposal #3 review. |
| 2026-05-24 00:12 UTC+03 | Fedor Tmkhv | Estimated losses across epochs 269-272 by failure category. | Preliminary magnitude only; not an approved calculation. |
| 2026-05-24 00:14 UTC+03 | Fedor Tmkhv | "I don't know the true cause" | Root cause was unresolved. |
| 2026-05-24 07:10 UTC+03 | Nik | Reported abnormal miss rate and a long-input validation error example. | Operator-level evidence and investigation hypothesis. |

## Findings

- An audit of epochs 269-272 found several epoch 272 participants with work/signatures but zero rewards through the downtime/binomial-test outcome.
- The audit does not establish incorrect protocol behaviour.
- Devshard-level retained data is required before compensation eligibility can be determined.

## Sources

- [Audit/calculation repository](https://github.com/huxuxuya/gonka_248_and_250_-epoch_loss/)
