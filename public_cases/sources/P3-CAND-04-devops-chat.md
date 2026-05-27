# P3-CAND-04: DevOps Chat Evidence

Source: `Gonka DevOps only` chat messages. This log records contemporaneous evidence for the unintended epoch 276 cPoC after the `v0.2.13` upgrade.

| Message ID | Date (UTC+03) | Author | Relevance | Addresses / Figures |
|---|---|---|---|---|
| `16053`-`16059` | 2026-05-26 18:52:09-18:57:41 | Arturs Plisko; Evgenii Maksimenkov; Gleb Morgachev | Confirms cPoC happened unexpectedly and that participants dropped afterward. | `5` participants dropped; one address identified |
| `16063` | 2026-05-26 19:09:52 | Vas Ily | Identifies the participant discussed as affected. | `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` |
| `16065`-`16067` | 2026-05-26 21:49:49-21:52:37 | Egor; Gleb Morgachev | Documents cause and expected next-epoch recovery. | `LastUpgradeHeight` reported null; old scales used |

## Key Excerpts

**Messages `16057` and `16059`, Evgenii Maksimenkov - original Russian**

> Из-за смены коэффициентов у этого участника например confirmation ration 53.21% но он вылетел из эпохи: `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09`.
>
> Точно могу сказать по чейну, что после последнего cpoc выбыло 5 participants.

**English translation**

> Due to the coefficient change, this participant had a `53.21%` confirmation ratio but dropped out of the epoch: `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09`.
>
> I can state from the chain that five participants dropped out after the latest cPoC.

**Message `16065`, Egor - original Russian**

> После v0.2.13 в state не записался LastUpgradeHeight, поэтому проверка перед запуском cPoC не увидела недавний апгрейд и не пропустила его. Коэффициенты в epoch_group_data тоже остались на старом snapshot. Из-за этого после апгрейда cPoC всё-таки сработал, и часть нод была срезана.

**English translation**

> After `v0.2.13`, `LastUpgradeHeight` was not written to state, so the pre-cPoC check did not see the recent upgrade and did not skip cPoC. Coefficients in `epoch_group_data` also remained on the old snapshot. As a result, cPoC ran after the upgrade and some nodes were reduced.

## Assessment

- These messages independently support the unintended-cPoC cause described in the published case.
- They identify one affected address and an initial observed count of five dropped participants; the published compensation calculation has the broader final affected set.
- The calculation repository remains the source for the compensation total.

## Public References

- [Participant tracker link cited in message `16057`](https://tracker.gonka.vip/?participant=gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09)
- Verification endpoints cited in message `16065`:
  - `http://node1.gonka.ai:8000/chain-rpc/abci_query?path=%22%2Fstore%2Finference%2Fkey%22&data=0x1b`
  - `http://node1.gonka.ai:8000/chain-api/productscience/inference/inference/epoch_group_data/276`
  - `http://node1.gonka.ai:8000/chain-api/productscience/inference/inference/params`
- [PR #1143: intended `v0.2.13` upgrade protection behavior](https://github.com/gonka-ai/gonka/pull/1143)
