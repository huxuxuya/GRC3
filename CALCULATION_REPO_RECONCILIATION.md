# Calculation Repository Reconciliation

Checked on 2026-06-07.

This note compares the amounts currently fixed in the external calculation
repositories with the amounts tracked in this repository. I inspected published
output files and README totals only; I did not run third-party calculation
scripts.

## Summary

| Case | Calculation repo HEAD | Current repo amount | Our tracked amount before this check | Result |
|---|---|---:|---:|---|
| `P3-CAND-01` Devshard / high miss rate | `huxuxuya/grc-p3-cand01@d2fe976` | `35040.581153560` confirmed-six amount | `30715.490665898` | Mismatch; updated ledger/tracker to current repo amount. |
| `P3-CAND-02` Negative coin balance / settle-drop | `gonkavip/unclaimed@658d62b` | `1075.336150923` | `1075.336150923` | Match. |
| `P3-CAND-03` strict Kimi cPoC shortfall | `gonkalabs/GRC-e267-kimi_shortfall@9e372ae` | `10262.057515369` strict epoch 267 | `10262.057515369` | Match. |
| `P3-CAND-03-EXT` Kimi-only broader total | `gonkalabs/GRC-e267-kimi_shortfall@9e372ae` | `31158.584694469` for epochs 265+267 | `31158.584694469` | Match. |
| `P3-CAND-04` UpgradeProtectionWindow / cPoC misfire | `gonkavip/payout276@b393de8` | `32429.966254822` | `36209.451291351` | Mismatch; source repo changed after local validation. Revalidation required. |
| `P4-CAND-01` source aggregate Kimi restitution | `votkon/gonka-kimi-restitution@5462c55` | `946509.925002` | `946509.925002` in local ledger; public tracker had stale `710772.719154` | Ledger matched; public tracker updated. |

## Details

### P3-CAND-01

Current `README.md` in `huxuxuya/grc-p3-cand01` reports:

| Scope | Amount, GONKA |
|---|---:|
| Confirmed six reported addresses | `35040.581153560` |
| Total including one manual-review row | `35109.923355683` |

Our old tracker amount `30715.490665898` was stale.

### P3-CAND-02

`gonkavip/unclaimed/unclaimed.csv` contains `19` rows. Summing
`total_gnk` gives:

```text
1075.336150923
```

This matches our tracked amount.

### P3-CAND-03

`gonkalabs/GRC-e267-kimi_shortfall` currently reports:

| Scope | Amount, GONKA |
|---|---:|
| Strict epoch 267 Kimi shortfall | `10262.057515369` |
| Epoch 265 Kimi shortfall extension | `20896.527179100` |
| Kimi-only total | `31158.584694469` |
| Broader cPoC-shortfall total including Qwen-only candidate | `35313.247032984` |

Our Case 3 recommendation uses the Kimi-only total and intentionally excludes
the extra Qwen-only candidate from Case 3.

### P3-CAND-04

Current `gonkavip/payout276` reports:

```text
32429.966254822 GONKA
```

The current `payout_276.csv` has `19` rows and sums to the same value. Our
local Case 4 validation still records an exact match to an earlier published
CSV total:

```text
36209.451291351 GONKA
```

Therefore the correct status is not "validated current source amount"; the
source calculation changed and the new amount requires revalidation.

### P4-CAND-01

Current `votkon/gonka-kimi-restitution/aggregate_compensation.json` reports:

| Field | Value |
|---|---:|
| Unique addresses | `53` |
| Grand total | `946509.925002` |

Per-epoch source totals:

| Epoch | Amount, GONKA |
|---:|---:|
| `265` | `30592.104861828` |
| `266` | `188698.468968749` |
| `267` | `246471.823957226` |
| `268` | `42634.684509205` |
| `269` | `47504.581758505` |
| `270` | `76870.083553475` |
| `271` | `28422.154068920` |
| `272` | `16988.149548048` |
| `273` | `86243.303557245` |
| `274` | `41818.441790908` |
| `275` | `89984.775198122` |
| `276` | `50281.353229327` |

The local P4 validation still recommends rejecting this as one aggregate
approval and splitting it into policy tracks.
