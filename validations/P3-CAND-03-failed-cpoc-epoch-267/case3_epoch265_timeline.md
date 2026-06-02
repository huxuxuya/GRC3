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
| Epoch reward/root `totalFullWeight` | `904,177` |
| cPoC #2 validation snapshot `TotalNetworkWeight` | `732,828` |
| cPoC #2 `2/3` exact line | `488,552` |
| cPoC #2 minimum integer weight for strict `>2/3` | `488,553` |
| Claimant root weight | `66,311` |
| Claimant Qwen voting power | `66,311` |
| Claimant Kimi voting power | `66,311` |
| Alpha threshold | `0.5` / `50%` |

## Which Weight Is The Denominator?

There are three different weight fields in the archive data, and they must not
be mixed:

| Field | Meaning | Used as the `>2/3` denominator? |
|---|---|---|
| cPoC snapshot `TotalNetworkWeight` | Network weight stored in `poc_validation_snapshot/{stage}` for the specific cPoC stage. | yes |
| Epoch reward/root `totalFullWeight` | Reward denominator for the epoch payout formula. For epoch `265` this is `904,177`. | no |
| Model `total_weight` | Model-group capacity/weight total from `epoch_group_data/{epoch}?model_id=...`. | no |
| Model `voting_power` | Per-participant model voting power. Validator, preserved, and non-preserved model weights below are sums of this field. | no |

For cPoC #2 at trigger height `4,102,890`, the archive validation snapshot
sets the `>2/3` line from its own `TotalNetworkWeight`:

```text
cPoC #2 snapshot total = 732,828
strict >2/3 line       = 488,553
```

The epoch reward/root total `904,177` is still used later for the reward payout
formula, but it is not the cPoC #2 majority denominator.

The model totals are shown for context, but they are not the denominator used
in the `>2/3` checks:

| Model | Model `total_weight` | Sum of model `voting_power` | Sum of model `voting_power` as share of epoch reward/root total | `>2/3` denominator used below |
|---|---:|---:|---:|---:|
| Qwen | `1,227,899` | `891,766` | `98.6274%` of epoch reward/root total | cPoC snapshot total |
| Kimi | `377,276` | `842,654` | `93.1957%` of epoch reward/root total | cPoC snapshot total |

## Claimant Model Weights

| Model | Model `weight` field | Model `voting_power` | Confirmation weight | Nodes |
|---|---:|---:|---:|---|
| Qwen | `923` | `66,311` | `66,311` | `node1` |
| Kimi | `52,279` | `66,311` | `66,311` | `kimi30; kimi31; kimi32; kimi33` |

Important scale note: the per-model `weight` field above is raw model
`PocWeight`, not the final consensus/reward weight. The chain scales raw model
weights when it combines models:

```text
scaled consensus weight = sum(raw model weight * model weight_scale_factor)
```

The root `confirmation_weight`/reward weight is already in that combined
consensus scale. The raw model `weight` fields are useful for explaining which
model was lost, but they must be scaled before being used as a reward numerator.

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

The table uses model `voting_power`, not model `total_weight`.
These preserved/non-preserved values are a model voting-power availability
diagnostic for the raw `>2/3` validation context. The final chain
`ConfirmationPoCRatio` uses coefficient-adjusted PoC node readings; see
`case3_chain_formula_reconciliation.md`.

| Model | Sum model voting power | Preserved voting power | Non-preserved voting power | Non-preserved share of epoch reward/root total | Epoch-level diagnostic enough for `>2/3`? | Diagnostic shortfall vs `602,785` |
|---|---:|---:|---:|---:|---|---:|
| Qwen | `891,766` | `309,671` | `582,095` | `64.3784%` | no | `20,690` |
| Kimi | `842,654` | `380,371` | `462,283` | `51.1275%` | no | `140,502` |

Key point for this epoch-level availability diagnostic: unlike epoch `267`, in
epoch `265` both Qwen and Kimi non-preserved model voting power are below the
diagnostic `>2/3` line. The final cPoC #2 majority verdict is shown separately
below from the archive `poc_validation_snapshot`.

## Preserved Qwen Weight

| Participant | Qwen voting power | Share of epoch reward/root total | Nodes |
|---|---:|---:|---|
| `gonka1tja3g2da45efhe2p83gk3whtussmgmtsdlgprt` | `115,425` | `12.7658%` | `at003;at009` |
| `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e` | `74,862` | `8.2796%` | `node207` |
| `gonka15munkmx6x7k6rqqeexjet4556p7at39ks9qgr5` | `33,800` | `3.7382%` | `ml3` |
| `gonka1hwvel7n3zuk6wruefuzc356l9myske9stckwnz` | `18,392` | `2.0341%` | `fp002` |
| Other preserved Qwen participants | `67,192` | `7.4312%` | mixed |
| **Total** | **`309,671`** | **`34.2489%`** |  |

## Non-Preserved Qwen Weight

Full per-participant rows are in `case3_epoch265_model_weights.csv`.

| Participant | Qwen voting power | Share of epoch reward/root total | Model `weight` field |
|---|---:|---:|---:|
| `gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu` | `189,884` | `21.0008%` | `50,745` |
| `gonka1duuaqdx06sx8v2dzggltwwmqyuw8lvjkjq7xll` | `128,853` | `14.2509%` | `377,497` |
| `gonka1famtxh54kad6ylwtm60j6d7h6unpc08d4vdqnk` | `96,900` | `10.7169%` | `265,943` |
| `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6` | `66,311` | `7.3339%` | `923` |
| `gonka17gpuntq09zsaqtmpe544gc32tk4424dwv5t34f` | `39,448` | `4.3629%` | `105,138` |
| Other non-preserved Qwen participants | `60,699` | `6.7132%` | mixed |
| **Total** | **`582,095`** | **`64.3784%`** |  |

## Preserved Kimi Weight

| Participant | Kimi voting power | Share of epoch reward/root total | Nodes |
|---|---:|---:|---|
| `gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu` | `189,884` | `21.0008%` | `4B200-spt-kimi-1` |
| `gonka1famtxh54kad6ylwtm60j6d7h6unpc08d4vdqnk` | `96,900` | `10.7169%` | `U11` |
| `gonka17gpuntq09zsaqtmpe544gc32tk4424dwv5t34f` | `46,242` | `5.1143%` | `B9` |
| `gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2` | `13,883` | `1.5354%` | `mlnode-201` |
| Other preserved Kimi participants | `33,462` | `3.7008%` | mixed |
| **Total** | **`380,371`** | **`42.0682%`** |  |

## Non-Preserved Kimi Weight

Full per-participant rows are in `case3_epoch265_model_weights.csv`.

| Participant | Kimi voting power | Share of epoch reward/root total | Model `weight` field |
|---|---:|---:|---:|
| `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `147,538` | `16.3174%` | `72,507` |
| `gonka1y2a9p56kv044327uycmqdexl7zs82fs5ryv5le` | `141,664` | `15.6677%` | `865` |
| `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6` | `66,311` | `7.3339%` | `52,279` |
| `gonka15munkmx6x7k6rqqeexjet4556p7at39ks9qgr5` | `33,800` | `3.7382%` | `22,160` |
| `gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d` | `14,284` | `1.5798%` | `11,913` |
| Other non-preserved Kimi participants | `58,686` | `6.4905%` | mixed |
| **Total** | **`462,283`** | **`51.1275%`** |  |

## Claimant Raw cPoC Rows

The table below is the original neighbor-scan diagnostic table. It used the
epoch reward/root total `904,177` as a quick scan denominator, so its percentage
and shortfall columns are not the final chain denominator for cPoC #2. The raw
submitted counts and validating weights are still useful as the event timeline.

| cPoC | Trigger height | Model | Submitted count | Actual validating weight | Diagnostic share vs `904,177` | Diagnostic result vs `602,785` | Diagnostic shortfall/surplus |
|---:|---:|---|---:|---:|---:|---|---:|
| `0` | `4,095,682` | Qwen | `960` | `509,938` | `56.3980%` | no | `92,847` |
| `0` | `4,095,682` | Kimi | `43,360` | `677,518` | `74.9320%` | yes | `+74,733` |
| `1` | `4,098,879` | Qwen | `960` | `406,730` | `44.9834%` | no | `196,055` |
| `1` | `4,098,879` | Kimi | `43,328` | `535,847` | `59.2635%` | no | `66,938` |
| `2` | `4,102,890` | Qwen | `960` | `35,370` | `3.9118%` | no | `567,415` |
| `2` | `4,102,890` | Kimi | `52,028` | `256,727` | `28.3934%` | no | `346,058` |

## Archive-Confirmed cPoC #2 Majority Check

For the final cPoC before exclusion, the archive snapshot at stage
`4,102,890` gives `TotalNetworkWeight = 732,828`, so strict `>2/3` requires at
least `488,553` validating voting power.

| cPoC | Trigger height | Model | Submitted count | Actual validating weight | Share vs cPoC snapshot total | Meets strict `>2/3`? | Shortfall vs `488,553` |
|---:|---:|---|---:|---:|---:|---|---:|
| `2` | `4,102,890` | Qwen | `960` | `35,370` | `4.8265%` | no | `453,183` |
| `2` | `4,102,890` | Kimi | `52,028` | `256,727` | `35.0324%` | no | `231,826` |

## What Actually Failed

At the final cPoC before exclusion:

- claimant submitted Qwen count `960`;
- claimant submitted Kimi count `52,028`;
- Qwen actual validating weight was only `35,370` (`4.8265%` of the cPoC #2
  snapshot total);
- Kimi actual validating weight was only `256,727` (`35.0324%` of the cPoC #2
  snapshot total);
- preserved Qwen weight was `309,671` (`34.2489%`);
- preserved Kimi weight was `380,371` (`42.0682%`);
- non-preserved Qwen voting power was `582,095`, short `20,690` of the
  epoch-level diagnostic `>2/3` line;
- non-preserved Kimi voting power was `462,283`, short `140,502` of the
  epoch-level diagnostic `>2/3` line;
- chain reduced claimant confirmation weight from `66,311` to `323`;
- `ConfirmationPoCRatio` became `0.0053586212476565`, below alpha `0.5`;
- at block `4,103,171`, claimant became `INACTIVE` with reason
  `failed_confirmation_poc`;
- actual epoch reward was `0`.

## Amount Interpretation

The neighbor scan's `20,896.527179100 GNK` value is a full-root-weight upper
bound:

```text
floor(66,311 * fixedEpochReward / 904,177) = 20,896.527179100 GNK
```

That number treats the whole root weight `66,311` as restored. It does not
answer the narrower question "what would the chain-style reward be if only the
lost Kimi contribution from cPoC #2 were restored?"

The narrower counterfactual must scale raw model weights. The externally
proposed decomposition is:

```text
actual cPoC #2 Qwen measured weight = 323
raw Kimi model weight               = 52,279
proposed Kimi scale factor          = 0.780
floor(52,279 * 0.780)               = 40,777
counterfactual confirmation weight  = 323 + 40,777 = 41,100
```

With that participant weight, the chain reward formula gives:

```text
floor(41,100 * 284,932,503,735,690 / 904,177)
= 12,951.806895703 GNK
```

Current validation status for epoch `265`: the chain facts are confirmed
(`66,311 -> 323`, zero reward, Kimi cPoC shortfall, guardian split). The
`20,896.527179100 GNK` amount should be treated only as a full-weight upper
bound. The `12,951.806895703 GNK` amount is the narrower chain-style
counterfactual if the `0.780` Kimi scale factor is accepted; that scale factor
still needs an explicit source decision because the raw archive params at cPoC
height `4,102,890` show a different current Kimi `weight_scale_factor`.
