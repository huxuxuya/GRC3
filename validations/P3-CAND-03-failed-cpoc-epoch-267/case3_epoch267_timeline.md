# Epoch 267 cPoC Timeline

This table explains what changed during epoch `267` for the Case 3 claimant:

`gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6`

The important distinction is:

- `available after preserved` means theoretical model voting power not locked in
  preserved nodes at that snapshot;
- `actual validating weight` means the model voting power that actually
  validated the claimant's cPoC row;
- chain status is decided later from the participant's confirmation ratio, not
  only from the raw guardian-assisted cPoC row.

## Constants

| Metric | Value |
|---|---:|
| Epoch | `267` |
| Total network/root weight | `541,415` |
| `2/3` exact line | `360,943.333333` |
| Minimum integer weight for `>2/3` | `360,944` |
| Claimant root weight | `19,518` |
| Claimant Qwen voting power | `19,518` |
| Claimant Kimi voting power | `19,518` |
| Alpha threshold | `0.5` / `50%` |

## Height Timeline

| Height | Event | Claimant status | Claimant confirmation weight | Confirmation ratio | What changed |
|---:|---|---|---:|---:|---|
| `4,122,271` | cPoC #1 trigger / episode anchor | `ACTIVE` | not changed yet | not finalized yet | First confirmation PoC starts. Claimant submits both Qwen and Kimi. |
| `4,122,312` | cPoC #1 validation snapshot | `ACTIVE` | not changed yet | not finalized yet | Snapshot records total network weight `541,415`, claimant Qwen/Kimi voting power `19,518`, high-power Kimi participant voting power `159,432`. |
| `4,122,552 - 1` | Last checked block before exclusion | `ACTIVE` | `65,716` | not failed yet | Claimant is still active before chain applies the failure transition. |
| `4,122,552` | Exclusion block | `INACTIVE` | `343` | `0.0057419461588255` / `0.5742%` | Chain records `failed_confirmation_poc`; confirmation weight drops by `65,373`; ratio is below alpha `0.5`. |
| `4,130,085` | cPoC #2 trigger | already `INACTIVE` | already reduced | already failed | Later raw Kimi rows exist, but they do not undo the exclusion from block `4,122,552`. |
| `4,133,665` | cPoC #3 trigger | already `INACTIVE` | already reduced | already failed | Later diagnostic row only. |
| `4,134,529` | cPoC #4 trigger | already `INACTIVE` | already reduced | already failed | Later diagnostic row only. |

## Preserved vs Available Weight at cPoC #1

Snapshot: episode anchor `4,122,271`; validation snapshot height `4,122,312`.

| Model | Preserved weight | Preserved share | Available after preserved | Available share | Is available weight enough for `>2/3`? | Shortfall/surplus vs `360,944` |
|---|---:|---:|---:|---:|---|---:|
| Qwen | `139,925` | `25.8443%` | `401,490` | `74.1557%` | yes | `+40,546` |
| Kimi | `188,581` | `34.8311%` | `352,834` | `65.1689%` | no | `-8,110` |

This is the key model-level fact: after preserved nodes are removed from normal
validation capacity, Kimi's theoretical available weight is already below the
strict `>2/3` line. Qwen still has enough theoretical available weight.

## Preserved Kimi Weight

| Participant | Kimi voting power | Share of total network | Nodes |
|---|---:|---:|---|
| `gonka17gpuntq09zsaqtmpe544gc32tk4424dwv5t34f` | `159,432` | `29.4473%` | `B9;U11` |
| `gonka15munkmx6x7k6rqqeexjet4556p7at39ks9qgr5` | `9,647` | `1.7820%` | `ml3;ml8` |
| `gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2` | `7,068` | `1.3055%` | `mlnode-201` |
| `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` | `4,050` | `0.7480%` | `node802;node812` |
| `gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5` | `3,083` | `0.5695%` | `node2-4xB200` |
| `gonka1mmlyd5xxu5l68yx8wzclrkxkxvm88mhq5tp5s0` | `2,153` | `0.3976%` | `node606` |
| `gonka19cjm4c5mt3j3qdr8vhytmm4hef3pnkvkm0x7m2` | `2,061` | `0.3807%` | `node218` |
| `gonka15p7s7w2hx0y8095lddd4ummm2y0kwpwljk00aq` | `1,087` | `0.2008%` | `node1` |
| **Total** | **`188,581`** | **`34.8311%`** |  |

## Claimant Raw cPoC Rows

The `>2/3` threshold is `360,944`.

| cPoC | Trigger height | Model | Submitted count | Actual validating weight | Actual validating share | Meets `>2/3` by weight? | Shortfall vs `360,944` | Raw row result |
|---:|---:|---|---:|---:|---:|---|---:|---|
| `0` | `4,122,271` | Qwen | `1,024` | `129,251` | `23.8728%` | no | `231,693` | `pass_guardian` |
| `0` | `4,122,271` | Kimi | `57,664` | `171,571` | `31.6894%` | no | `189,373` | `pass_guardian` |
| `1` | `4,130,085` | Qwen | `0` | `0` | `0.0000%` | no | `360,944` | `no_submission` |
| `1` | `4,130,085` | Kimi | `57,408` | `239,088` | `44.1598%` | no | `121,856` | `pass_guardian` |
| `2` | `4,133,665` | Qwen | `0` | `0` | `0.0000%` | no | `360,944` | `no_submission` |
| `2` | `4,133,665` | Kimi | `45,376` | `302,807` | `55.9288%` | no | `58,137` | `pass_guardian` |
| `3` | `4,134,529` | Qwen | `0` | `0` | `0.0000%` | no | `360,944` | `no_submission` |
| `3` | `4,134,529` | Kimi | `57,888` | `311,717` | `57.5745%` | no | `49,227` | `pass_guardian` |

No claimant row reaches the `>2/3` weight threshold by raw validation weight.
The rows pass only through guardian-assisted fallback. The durable chain state
still later records `failed_confirmation_poc`.

## High-Power Preserved Participant Trace

High-power participant:

`gonka17gpuntq09zsaqtmpe544gc32tk4424dwv5t34f`

| cPoC | Trigger height | Model | Participant submitted count | Actual validating weight on its own row | Actual validating share | Result |
|---:|---:|---|---:|---:|---:|---|
| `0` | `4,122,271` | Qwen | `102,208` | `482,515` | `89.1211%` | `pass_weight` |
| `0` | `4,122,271` | Kimi | `0` | `0` | `0.0000%` | `no_submission` |
| `1` | `4,130,085` | Qwen | `108,992` | `505,624` | `93.3894%` | `pass_weight` |
| `1` | `4,130,085` | Kimi | `0` | `0` | `0.0000%` | `no_submission` |
| `2` | `4,133,665` | Qwen | `90,560` | `502,310` | `92.7773%` | `pass_weight` |
| `2` | `4,133,665` | Kimi | `0` | `0` | `0.0000%` | `no_submission` |
| `3` | `4,134,529` | Qwen | `88,800` | `424,173` | `78.3453%` | `pass_weight` |
| `3` | `4,134,529` | Kimi | `0` | `0` | `0.0000%` | `no_submission` |

At cPoC #1 this participant had `159,432` Kimi voting power in the preserved
snapshot, but it did not validate the claimant's Kimi row.

## What Actually Failed

The failure point is not "claimant had no weight" and not "claimant submitted
nothing".

At cPoC #1:

- claimant submitted Kimi count `57,664`;
- actual Kimi validating weight for claimant was only `171,571`
  (`31.6894%`);
- Kimi preserved weight was `188,581` (`34.8311%`);
- Kimi theoretical available weight after preserved was `352,834`
  (`65.1689%`), which is below the `>2/3` minimum `360,944`;
- chain then reduced claimant confirmation weight from `65,716` to `343`;
- `ConfirmationPoCRatio` became `0.0057419461588255`, below alpha `0.5`;
- at block `4,122,552`, claimant became `INACTIVE` with reason
  `failed_confirmation_poc`.

