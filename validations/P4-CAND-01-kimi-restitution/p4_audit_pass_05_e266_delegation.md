# P4 Conceptual Audit Pass 05: Epoch 266 Delegation Evidence

This pass checks the chain facts behind the epoch `266` delegation
compensation track. It does not approve indirect-loss eligibility.

## Raw Inputs

- `archive_lcd_height_4104861_poc_delegation_<address>.json` for the 9 source delegators
- `archive_lcd_height_4105361_params.json`
- `archive_lcd_epoch_group_data_266.json`
- `archive_lcd_epoch_performance_summary_266.json`

## Summary

- Delegators checked: `9`
- Snapshot height: `4104861`
- Deploy window from chain params: `500`
- Chain `no_participation_penalty`: `0.15`
- Chain `delegation_share`: `0.05`
- Net extra penalty used by source: `0.10`
- Every raw Kimi delegation points to source operator: `True`
- Source operator absent from final epoch group for every row: `True`
- Source chain weights match final group weights: `True`
- Source actual rewards match performance summary: `True`

## Rows

| Delegator | Raw Kimi target | Final weight | Actual rewards (GONKA) | Extra weight | Source comp |
|---|---|---:|---:|---:|---:|
| `gonka1tja3g2da45efhe2p83gk3whtussmgmtsdlgprt` | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `18057` | `15325.866743189` | `2124.35` | `1805.1425` |
| `gonka1hwvel7n3zuk6wruefuzc356l9myske9stckwnz` | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `15760` | `13391.864042618` | `1854.11` | `1575.5134` |
| `gonka12pcu9mcrpa4w4sjd9y3dsksnvu495ss6f9r4ra` | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `11668` | `7997.729972660` | `1372.70` | `1166.4398` |
| `gonka1tlvg4kjx7ljd5thgd5fkgh39q6lu8cmxupktgg` | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `1763` | `1498.087329133` | `207.41` | `176.2456` |
| `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `1139` | `878.628643405` | `134.00` | `113.8648` |
| `gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww` | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `1084` | `863.333367214` | `127.52` | `108.3665` |
| `gonka1tmk2tzdneht6smu34pkmqdvu7p34qavvmwtwq2` | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `1006` | `843.789403192` | `118.35` | `100.5689` |
| `gonka1gyk0aahvr3qeju4zx0nplfreej6cy4jjk8svc5` | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `310` | `256.620744979` | `36.47` | `30.9904` |
| `gonka14ef2pxjge75gflqftn7m2wy0xv59gq9uc7qnct` | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `156` | `0.000000000` | `18.35` | `15.5952` |

## Interpretation

- Chain data confirms the factual delegation setup: all 9 source rows had
  Kimi delegation to `gonka1q5xt54...` at snapshot height `4104861`.
- Chain final group data confirms `gonka1q5xt54...` was absent from the
  epoch `266` final group, while the 9 delegators were present.
- Chain params confirm the source's mechanical delta: `0.15 - 0.05 = 0.10`.
- The remaining question is policy, not raw-data truth: whether indirect
  delegator losses caused by an excluded operator should be compensated
  under this case.
