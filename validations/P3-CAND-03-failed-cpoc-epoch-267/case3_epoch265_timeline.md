# Epoch 265 cPoC Timeline

This is the same-address neighbor finding discovered by the epoch `262..272`
scan.

Checked participant:

`gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6`

This epoch is not part of the currently validated epoch `267` compensation
amount, but it has the same durable exclusion signature and therefore needs a
separate scope/eligibility decision.

## Constants

| Metric | Value |
|---|---:|
| Epoch | `265` |
| Total network/root weight | `904,177` |
| `2/3` exact line | `602,784.666667` |
| Minimum integer weight for `>2/3` | `602,785` |
| Claimant root weight | `66,311` |
| Claimant Qwen voting power | `66,311` |
| Claimant Kimi voting power | `66,311` |
| Alpha threshold | `0.5` / `50%` |

## Height Timeline

| Height | Event | Claimant status | Claimant confirmation weight | Confirmation ratio | What changed |
|---:|---|---|---:|---:|---|
| `4,095,682` | cPoC #0 trigger | `ACTIVE` | not failed yet | not finalized | Claimant submits both Qwen and Kimi. Kimi reaches `>2/3` by raw validating weight, Qwen does not. |
| `4,098,879` | cPoC #1 trigger | `ACTIVE` | not failed yet | not finalized | Claimant submits both Qwen and Kimi. Neither model reaches `>2/3` by raw validating weight. |
| `4,102,890` | cPoC #2 trigger / failure window | `ACTIVE` before exclusion | not failed yet | not finalized | Claimant submits both Qwen and Kimi. Both models are far below `>2/3`; chain later applies failure. |
| `4,103,170` | Last checked block before exclusion | `ACTIVE` | `66,311` | not failed yet | Claimant is still active immediately before exclusion. |
| `4,103,171` | Exclusion block | `INACTIVE` | `323` | `0.0053586212476565` / `0.5359%` | Chain records `failed_confirmation_poc`; confirmation weight drops by `65,988`; ratio is below alpha `0.5`. |

## Preserved vs Available Weight At Exclusion

Snapshot height context: exclusion block `4,103,171`.

| Model | Preserved weight | Preserved share | Available after preserved | Available share | Is available weight enough for `>2/3`? | Shortfall vs `602,785` |
|---|---:|---:|---:|---:|---|---:|
| Qwen | `309,671` | `34.2489%` | `594,506` | `65.7511%` | no | `8,279` |
| Kimi | `380,371` | `42.0682%` | `523,806` | `57.9318%` | no | `78,979` |

Key point: unlike epoch `267`, in epoch `265` both Qwen and Kimi theoretical
available weight after preserved are below the strict `>2/3` line.

## Preserved Qwen Weight

| Participant | Qwen voting power | Share of total network | Nodes |
|---|---:|---:|---|
| `gonka1tja3g2da45efhe2p83gk3whtussmgmtsdlgprt` | `115,425` | `12.7658%` | `at003;at009` |
| `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e` | `74,862` | `8.2796%` | `node207` |
| `gonka15munkmx6x7k6rqqeexjet4556p7at39ks9qgr5` | `33,800` | `3.7382%` | `ml3` |
| `gonka1hwvel7n3zuk6wruefuzc356l9myske9stckwnz` | `18,392` | `2.0341%` | `fp002` |
| Other preserved Qwen participants | `67,192` | `7.4312%` | mixed |
| **Total** | **`309,671`** | **`34.2489%`** |  |

## Preserved Kimi Weight

| Participant | Kimi voting power | Share of total network | Nodes |
|---|---:|---:|---|
| `gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu` | `189,884` | `21.0008%` | `4B200-spt-kimi-1` |
| `gonka1famtxh54kad6ylwtm60j6d7h6unpc08d4vdqnk` | `96,900` | `10.7169%` | `U11` |
| `gonka17gpuntq09zsaqtmpe544gc32tk4424dwv5t34f` | `46,242` | `5.1143%` | `B9` |
| `gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2` | `13,883` | `1.5354%` | `mlnode-201` |
| Other preserved Kimi participants | `33,462` | `3.7008%` | mixed |
| **Total** | **`380,371`** | **`42.0682%`** |  |

## Claimant Raw cPoC Rows

The `>2/3` threshold is `602,785`.

| cPoC | Trigger height | Model | Submitted count | Actual validating weight | Actual validating share | Meets `>2/3` by weight? | Shortfall/surplus vs `602,785` |
|---:|---:|---|---:|---:|---:|---|---:|
| `0` | `4,095,682` | Qwen | `960` | `509,938` | `56.3980%` | no | `92,847` |
| `0` | `4,095,682` | Kimi | `43,360` | `677,518` | `74.9320%` | yes | `+74,733` |
| `1` | `4,098,879` | Qwen | `960` | `406,730` | `44.9834%` | no | `196,055` |
| `1` | `4,098,879` | Kimi | `43,328` | `535,847` | `59.2635%` | no | `66,938` |
| `2` | `4,102,890` | Qwen | `960` | `35,370` | `3.9118%` | no | `567,415` |
| `2` | `4,102,890` | Kimi | `52,028` | `256,727` | `28.3934%` | no | `346,058` |

## What Actually Failed

At the final cPoC before exclusion:

- claimant submitted Qwen count `960`;
- claimant submitted Kimi count `52,028`;
- Qwen actual validating weight was only `35,370` (`3.9118%`);
- Kimi actual validating weight was only `256,727` (`28.3934%`);
- preserved Qwen weight was `309,671` (`34.2489%`);
- preserved Kimi weight was `380,371` (`42.0682%`);
- both models had theoretical available weight below the `>2/3` line;
- chain reduced claimant confirmation weight from `66,311` to `323`;
- `ConfirmationPoCRatio` became `0.0053586212476565`, below alpha `0.5`;
- at block `4,103,171`, claimant became `INACTIVE` with reason
  `failed_confirmation_poc`;
- actual epoch reward was `0`.

Estimated zero-reward loss from the neighbor scan:

```text
20,896.527179100 GNK
```

This amount is not included in the current epoch `267` case estimate until
governance or validators decide that epoch `265` belongs in scope.

