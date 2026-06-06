# P4 Conceptual Audit Pass 06: Epochs 267-276 GroupCap Denominator

This pass checks the later `ComputeGroupCap` track using saved raw chain
data and copied source artifacts. It does not approve a compensation
model.

## Summary

- Raw root group fields match the source compensation JSON fields for all
  checked epochs.
- Source affected rows match raw root `weight`, raw root
  `confirmation_weight`, and raw performance `rewarded_coins`.
- The source formula is reproducible as a top-up using
  `confirmation_weight / root_total_weight * epoch_reward - actual`.
- That is not the only possible counterfactual denominator. Using all-root
  `confirmation_weight` or replacing only affected capped weight with
  affected confirmation weight gives materially different totals.
- Epoch `276` contains upgrade block `4,267,300` inside the epoch window, so
  full-epoch treatment needs an explicit policy/proration decision.

## Epoch Totals

| Epoch | Rows | Root total | Root conf | Source top-up | All-conf denom comp | Replace-affected comp | e276 pre-upgrade share |
|---:|---:|---:|---:|---:|---:|---:|---:|
| `267` | `25` | `541415` | `948169` | `246471.823957226` | `88917.163952910` | `84012.068346910` | `` |
| `268` | `11` | `698639` | `597867` | `42634.684509205` | `65241.369805967` | `33986.241974065` | `` |
| `269` | `19` | `679397` | `677463` | `47504.581758505` | `48012.518031473` | `33029.811095976` | `` |
| `270` | `19` | `717467` | `879344` | `76870.083553475` | `30965.834115886` | `28960.024942392` | `` |
| `271` | `17` | `796030` | `754946` | `28422.154068920` | `38178.788159498` | `27440.162768503` | `` |
| `272` | `11` | `823183` | `726349` | `16988.149548048` | `32434.442996421` | `20949.301243654` | `` |
| `273` | `20` | `758715` | `893211` | `86243.303557245` | `50077.516007804` | `36695.231629458` | `` |
| `274` | `9` | `766804` | `741816` | `41818.441790908` | `47718.948917680` | `23463.501085505` | `` |
| `275` | `18` | `736925` | `945908` | `89984.775198122` | `33938.754950874` | `34759.729245852` | `` |
| `276` | `11` | `798029` | `714732` | `50281.353229327` | `68168.646719533` | `37562.475582385` | `0.4957` |

## Totals Across 267-276

| Model | Total GONKA | Interpretation |
|---|---:|---|
| Source top-up / capped root denominator | `727219.351170981` | Uses the already-capped settlement denominator. |
| All root confirmation denominator | `503653.983658046` | Uses `confirmation_weight` as both numerator and denominator. |
| Replace affected weight denominator | `360858.547914700` | Replaces affected capped weight with affected confirmation weight, leaving other root weights unchanged. |

## Interpretation

- The cap/weight-pressure pattern is real chain state.
- The source amount is a reproducible top-up model, not proof that the
  same amount follows from a unique chain-style replay.
- The committee must choose the denominator model before accepting any
  e267-e276 `ComputeGroupCap` compensation amount.
