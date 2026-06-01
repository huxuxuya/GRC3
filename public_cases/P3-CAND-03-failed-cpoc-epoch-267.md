# P3-CAND-03: Failed cPoC / Preserved Kimi Shortfall

| Field | Value |
|---|---|
| Proposal | Proposal #3 candidate |
| Epochs | 267; neighbor scan flags a same-address Case-3-like signature in epoch 265, not included in the current estimate |
| Status | Independently validated; eligibility disputed |
| Reported by | Nik; proposed for GRC review by Votkon |
| Affected / detail contact | One known claimant: `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6`; Nik; Evgenii Maksimenkov |
| Case investigator | @mikenosov |
| Case validators | @dem_ww; @votkon |
| Result so far | Investigator report and independent archive validation both identify one restitution candidate and an amount of `10,262.057515369 GNK` |
| Further analysis | Required: validator review and eligibility vote, especially proxy-configuration responsibility; separately review whether the epoch 265 same-address neighbor finding belongs in scope |
| Compensation | `10,262.057515369 GNK`; independently matched to the published amount; not approved |
| Lost reward destination | Under fixed-reward settlement logic, confirmation-PoC reductions / zero reward shares remain undistributed and are transferred to governance rather than redistributed to other participants. |

## Message Log

| Date | Author | Fact / short quote | Meaning |
|---|---|---|---|
| 2026-05-18 11:01 UTC+03 | Nik | Reported an epoch 267 cPoC loss for one address. | Initial claim. |
| 2026-05-19 20:34 UTC+03 | Mike | "does not fit case 2 scope" | Not covered by Proposal #2 preserver scaling case. |
| 2026-05-19 20:34 UTC+03 | Mike | Epoch 267 was outside published case 3 scope. | Separate scope decision required. |
| 2026-05-26 19:25 UTC+03 | Votkon | Identifying all affected parties is difficult due to preserved-node history. | Primary evidence gap. |
| 2026-05-18 05:52-10:42 UTC+03 | Evgenii Maksimenkov; Gleb Morgachev, DevOps chat | Kimi validation lacked sufficient voting power when delegated Kimi nodes were preserved; Gleb noted a fix in `0.2.13`. | Mechanism and remediation evidence, not a completed payout calculation. |
| 2026-05-30 18:40 UTC+03 | Votkon | Confirmed he proposed this case after seeing it during the Kimi investigation. | Reporter/proposer clarification. |
| 2026-05-30 18:57 UTC+03 | Mike | Published the case intake form. | Investigation artefact created. |
| 2026-05-30 20:49 UTC+03 | Mike | Published report v1; "fully 100% valid participant set" is one address with about `10.2k GNK`. | Calculation available for validation. |
| 2026-05-30 20:55-21:14 UTC+03 | Evgenii Maksimenkov; Nik; Gleb Morgachev; Votkon | Discussed whether the cause was an old proxy configuration; Gleb warned against using GRC for node misconfiguration; Votkon suggested a vote. | Eligibility disputed. |

## Findings

- For the known address, the discussion cites `failed_confirmation_poc` and zero reward in epoch 267.
- The investigator report currently treats one address as the fully valid restitution set, with a compensation amount around `10.2k GNK`.
- Independent archive validation in [`validations/P3-CAND-03-failed-cpoc-epoch-267`](../validations/P3-CAND-03-failed-cpoc-epoch-267/) confirms one candidate, exact amount match, and chain exclusion reason `failed_confirmation_poc` at block `4122552`.
- Root-cause trace shows the claimant changed from `ACTIVE` at block `4122551` to `INACTIVE` at block `4122552`; `ConfirmationPoCRatio = 0.0057419461588255` was below `AlphaThreshold = 0.5`.
- The claimant's root confirmation weight dropped from `65,716` before exclusion to `343` at exclusion.
- The confirmed candidate submitted both Qwen and Kimi at cPoC #1; Kimi cPoC #1 raw validation weight was `171,571 / 541,415`, below the `>2/3` weight threshold.
- A high Kimi voting-power participant, `gonka17gpuntq09zsaqtmpe544gc32tk4424dwv5t34f`, had Kimi voting power `159,432`, was preserved for Kimi at cPoC anchor `4122271` on nodes `B9` and `U11`, and did not validate the claimant's Kimi cPoC #1 row.
- A nearest-neighbor scan of epochs `262..272` found `71` `failed_confirmation_poc` rows. Only two rows matched the stricter Case-3-like signature: the validated epoch `267` row and an epoch `265` row for the same claimant. The epoch `265` row has `ConfirmationPoCRatio = 0.0053586212476565`, Kimi submitted count `52,028`, Kimi validation weight `256,727 / 904,177` (`28.3934%`), max single preserved Kimi weight `189,884 / 904,177` (`21.0008%`), and estimated zero-reward loss `20,896.527179100 GNK`.
- Additional cohort sanity checks may affect wording, but the report does not present a larger fully validated participant set.
- The case has an epoch-level overlap with the Kimi restitution package in epoch 267, but no same-address overlap was found in the checked aggregate compensation data.
- Eligibility is disputed because later discussion links the validation failure to an outdated proxy configuration / missing `poc/proofs` exemption, raising the question of operator configuration versus protocol fault.
- A cited technical fix reduces recurrence risk but does not by itself determine compensation eligibility.
- The independent validation does not support a simple claimant-hardware-failure explanation, because cPoC submissions exist and the failure is recorded as a chain `failed_confirmation_poc` exclusion. The old proxy / `poc/proofs` responsibility dispute is still an eligibility question.

## Mitigation / Fix Status

| Item | Status |
|---|---|
| Fix reference | PR [`#1143`](https://github.com/gonka-ai/gonka/pull/1143) states that `v0.2.13` fixes confirmation PoC weight loss during new-model bootstrap by using a consistent epoch snapshot for confirmation and reward-weight calculations. |
| DevOps confirmation | Gleb Morgachev stated in message `15567` that a fix was added in `0.2.13` to prevent the relevant nodes from remaining preserved in this condition. |
| Configuration dispute | Gleb later noted that `poc/proofs` had been in the recommended proxy config since January and warned against creating a precedent for node-misconfiguration compensation. |
| Timing | DevOps announcement reports `v0.2.13` executed on mainnet at block `4267300` on 2026-05-26. Historical losses remain a compensation decision. |

## Reward Flow

The identified claimant is described as having a Kimi confirmation-PoC shortfall and zero reward in epoch 267. In fixed-reward settlement, confirmation-weight reductions are included in the governance remainder and are not renormalized onto successful participants.

Independent amount reconciliation:

- participant root weight: `19,518`
- root total weight: `541,415`
- fixed epoch reward used by the audit: `284,661,946,392,231 ngonka`
- actual reward: `0`
- loss: `10,262,057,515,369 ngonka` = `10,262.057515369 GNK`

## Sources

- [Investigation repository](https://github.com/gonkalabs/GRC-e267-kimi_shortfall)
- [Independent validation package](../validations/P3-CAND-03-failed-cpoc-epoch-267/)
- [Case intake form](https://github.com/gonkalabs/GRC-e267-kimi_shortfall/blob/main/grc-form.md)
- [Restitution report](https://github.com/gonkalabs/GRC-e267-kimi_shortfall/blob/main/RESTITUTION_REPORT.md)
- [GRC chat update export index](sources/GRC-chat-update-2026-06-01.md)
- [DevOps chat evidence log](sources/P3-CAND-03-devops-chat.md)
- [PR #1143: v0.2.13 microrelease](https://github.com/gonka-ai/gonka/pull/1143)
- [Settlement logic: `accountsettle.go`](https://github.com/gonka-ai/gonka/blob/17808620293b57112896bcbb7f99c4c2f554d6c8/inference-chain/x/inference/keeper/accountsettle.go)
- [Reward remainder logic: `bitcoin_rewards.go`](https://github.com/gonka-ai/gonka/blob/17808620293b57112896bcbb7f99c4c2f554d6c8/inference-chain/x/inference/keeper/bitcoin_rewards.go)
