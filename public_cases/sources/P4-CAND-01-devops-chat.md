# P4-CAND-01: DevOps Chat Evidence

Source: `Gonka DevOps only` chat messages. This log records contemporaneous evidence for Kimi nonce exclusion and ComputeGroupCap effects during epochs 266-276.

| Message ID | Date (UTC+03) | Author | Relevance | Addresses / Figures |
|---|---|---|---|---|
| `15343` | 2026-05-17 00:56:31 | Evgenii Maksimenkov | Identifies PoC submitters excluded from the epoch 266 final set. | `41` nonce submitters; `9` excluded PoC submitters; `14` preserved-only final members |
| `15357`-`15360` | 2026-05-17 01:06:54-01:16:40 | Tania Charchian; David Liberman; SegovChik | Records investigation request, chain query methods and published epoch data extracts. | Epoch `266` |
| `15515`-`15524` | 2026-05-17 22:15:49-22:30:25 | Votkon; Danya Yan; David Liberman | Discusses restitution and identifies the `ComputeGroupCap` rule. | `75%` cap |
| `16008`-`16021` | 2026-05-25 10:11:18-15:42:42 | Vas Ily; Nik; Evgenii Maksimenkov; A K | Quantifies later Kimi reduction and discusses confirmed-weight treatment. | Epoch `275` scale approximately `0.659`; one participant link |

## Epoch 266 Excluded PoC Submitters

Message `15343` lists these nine addresses as having submitted PoC nonces but not entered the final epoch 266 set:

- `gonka125n6kr5gvdup0lndfkps7t6rd6592panhrg3np`
- `gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d`
- `gonka1c6fwzedfsmpu4jnjekv4cn7mvr7x7fuqd6uqt9`
- `gonka1jrgm47v5eg876udmzg6j6glqcsd5x0vk6crpax`
- `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg`
- `gonka1qa90tgczc0k5dvk4l5nvlf5y6phgm6mg22sfjv`
- `gonka1wkgawwdzj623ss8eywayzdj6qcgr2llygactje`
- `gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds`
- `gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw`

## Key Excerpts

**Message `15343`, Evgenii Maksimenkov - original Russian**

> Всего отпраляло nonces 41 участник. 9 PoC submitters НЕ попали в финальный set эпохи 266 (отвалились/исключены после PoC).

**English translation**

> A total of 41 participants submitted nonces. Nine PoC submitters did not enter the final set for epoch 266; they dropped out or were excluded after PoC.

**Message `15523`, David Liberman - original Russian**

> ComputeGroupCap - причина срезанного веса, по протоколу модель группа не может получить вес больший, чем 75% от всего веса прошлой эпохи.

**English translation**

> `ComputeGroupCap` is the cause of the reduced weight: under the protocol, a model group cannot receive weight exceeding 75% of the total weight in the previous epoch.

**Message `16012`, Evgenii Maksimenkov - original Russian**

> Для Kimi сейчас действует CapFactor равный 75% ... Для 275 эпохи = 75% * 654,598 = 490,949 ... Чейн делает scale ко всем нодам с кими: 490,949 / 744,509 = 0.659.

**English translation**

> Kimi currently has a `CapFactor` of 75%. For epoch 275 this is `75% * 654,598 = 490,949`. The chain applies a scale to all Kimi nodes: `490,949 / 744,509 = 0.659`.

**Message `16016`, Evgenii Maksimenkov - original Russian**

> Дело в этом участнике: `gonka14ljarev2nlzu4ej50vx7ylj2rvg4n20fnq2ysc`. Он подтвердил вес на 89.86% и оставшиеся `11,578 * 10.14% = 1,174`. Чейн почему-то не вычитает неподтвержденный вес.

**English translation**

> The discrepancy comes from participant `gonka14ljarev2nlzu4ej50vx7ylj2rvg4n20fnq2ysc`. It confirmed weight at `89.86%`, leaving `11,578 * 10.14% = 1,174`. The chain does not subtract the unconfirmed weight.

## Assessment

- The messages provide contemporaneous lists and figures relevant to the published restitution calculation.
- They support separate components of the case: epoch 266 nonce exclusion and subsequent Kimi cap effects.
- The restitution repository remains the authoritative published payout calculation and must be independently validated before approval.

## Public References

- [Epoch 266 group data extract cited in message `15360`](https://gist.github.com/SegovChik/fdb3e0d14d14a29b2aef14667add4f55)
- [Epoch 266 PoC commits extract cited in message `15360`](https://gist.github.com/SegovChik/4a0d12eb05b76d384a18715562525853)
- [Participant tracker link cited in message `16016`](https://tracker.gonka.vip/?epoch=274&participant=gonka14ljarev2nlzu4ej50vx7ylj2rvg4n20fnq2ysc)
- [PR #1143: `v0.2.13` confirmation PoC and Kimi weight mitigation](https://github.com/gonka-ai/gonka/pull/1143)
