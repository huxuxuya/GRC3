# P3-CAND-03: Failed cPoC / Preserved Kimi Shortfall

| Field | Value |
|---|---|
| Proposal | Proposal #3 candidate |
| Epochs | 267 |
| Status | Scope decision required |
| Reported by | Nik; follow-up context by Votkon |
| Affected / detail contact | One known claimant: `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6`; Nik; Evgenii Maksimenkov |
| Investigated by | Mike; Evgenii Maksimenkov; Gleb Morgachev |
| Result so far | Known claimant is outside Proposal #2 scopes; DevOps evidence describes the Kimi validation shortfall mechanism |
| Further analysis | Required: affected set, historical preserved-node evidence and methodology |
| Compensation | Not calculated |
| Lost reward destination | Under fixed-reward settlement logic, confirmation-PoC reductions / zero reward shares remain undistributed and are transferred to governance rather than redistributed to other participants. |

## Message Log

| Date | Author | Fact / short quote | Meaning |
|---|---|---|---|
| 2026-05-18 11:01 UTC+03 | Nik | Reported an epoch 267 cPoC loss for one address. | Initial claim. |
| 2026-05-19 20:34 UTC+03 | Mike | "does not fit case 2 scope" | Not covered by Proposal #2 preserver scaling case. |
| 2026-05-19 20:34 UTC+03 | Mike | Epoch 267 was outside published case 3 scope. | Separate scope decision required. |
| 2026-05-26 19:25 UTC+03 | Votkon | Identifying all affected parties is difficult due to preserved-node history. | Primary evidence gap. |
| 2026-05-18 05:52-10:42 UTC+03 | Evgenii Maksimenkov; Gleb Morgachev, DevOps chat | Kimi validation lacked sufficient voting power when delegated Kimi nodes were preserved; Gleb noted a fix in `0.2.13`. | Mechanism and remediation evidence, not a completed payout calculation. |

## Findings

- For the known address, the discussion cites `failed_confirmation_poc` and zero reward in epoch 267.
- No complete victim set or payout method is available.
- The case cannot reuse Proposal #2 scope without a new committee decision.
- A cited technical fix reduces recurrence risk but does not by itself determine compensation eligibility.

## Mitigation / Fix Status

| Item | Status |
|---|---|
| Fix reference | PR [`#1143`](https://github.com/gonka-ai/gonka/pull/1143) states that `v0.2.13` fixes confirmation PoC weight loss during new-model bootstrap by using a consistent epoch snapshot for confirmation and reward-weight calculations. |
| DevOps confirmation | Gleb Morgachev stated in message `15567` that a fix was added in `0.2.13` to prevent the relevant nodes from remaining preserved in this condition. |
| Timing | DevOps announcement reports `v0.2.13` executed on mainnet at block `4267300` on 2026-05-26. Historical losses remain a compensation decision. |

## Reward Flow

The identified claimant is described as having a Kimi confirmation-PoC shortfall and zero reward in epoch 267. In fixed-reward settlement, confirmation-weight reductions are included in the governance remainder and are not renormalized onto successful participants.

## Sources

- No standalone public calculation repository identified for this candidate.
- [DevOps chat evidence log](sources/P3-CAND-03-devops-chat.md)
- [PR #1143: v0.2.13 microrelease](https://github.com/gonka-ai/gonka/pull/1143)
- [Settlement logic: `accountsettle.go`](https://github.com/gonka-ai/gonka/blob/17808620293b57112896bcbb7f99c4c2f554d6c8/inference-chain/x/inference/keeper/accountsettle.go)
- [Reward remainder logic: `bitcoin_rewards.go`](https://github.com/gonka-ai/gonka/blob/17808620293b57112896bcbb7f99c4c2f554d6c8/inference-chain/x/inference/keeper/bitcoin_rewards.go)
