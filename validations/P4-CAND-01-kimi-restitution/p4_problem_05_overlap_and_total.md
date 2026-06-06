# P4 Problem 05: Overlap and Aggregate Total

## Question

Can the full source total `946,509.925002 GONKA` be approved as one P4 payout?

## Source Total Split

| Track | Source amount, GONKA | Local status |
|---|---:|---|
| e265 cPoC / attack-attributed rows | `30,592.104861828` | Mixed scope; one row belongs with Case 3, two rows are not strict direct cPoC victims. |
| e266 nonce + delegation | `188,698.468968749` | Chain facts partly confirmed, but scope includes narrow exclusion, top-up rows, zero-reward rows, and indirect delegator loss. |
| e267-e276 GroupCap top-up | `727,219.351170981` | Source model reproducible, but compensability and denominator are policy choices. |
| Full P4 source total | `946,509.925002` | Not validated as one aggregate GRC payout. |

## Known Overlap Risk

| Area | Risk |
|---|---|
| Case 3 | e265 `gonka1j7x6...` is the same class and amount as the Case 3 extension. |
| Case 4 / Case 6 | Public P4 notes warn about epoch overlap, especially epoch `276`; final duplicate matrix is still required. |
| Vote history | Public case notes say GRC previously voted against including P4; any later approval should explicitly state what changed. |

## What Is Proven

- The source total is internally consistent at pinned commit
  `5462c55a6b95d50dfb53bdc4211cdcd31369c2ea`.
- The package contains real chain-state anomalies.
- The package combines several different problem classes.

## What Is Not Proven

- That the aggregate total is a validated payout amount.
- That there is no duplicate compensation across other cases.
- That every row has the same eligibility rationale.

## Recommended Handling

Reject "approve P4 as one number" as the decision shape. Use separate
track-level decisions and build a final overlap matrix before any payout
recommendation.
