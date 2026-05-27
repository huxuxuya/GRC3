# P3-CAND-03: DevOps Chat Evidence

Source: `Gonka DevOps only` chat messages. This log records evidence about the epoch 267 preserved Kimi validation shortfall.

| Message ID | Date (UTC+03) | Author | Relevance | Addresses / Figures |
|---|---|---|---|---|
| `15548` | 2026-05-18 05:52:05 | Evgenii Maksimenkov | Identifies a participant that submitted enough nonces but lost validation for Qwen and Kimi. | `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6` |
| `15555` | 2026-05-18 08:48:52 | Evgenii Maksimenkov | Explains why Kimi validation failed for that participant while Qwen passed via guardian protection. | Kimi weight reported as `99%` unconfirmed |
| `15565` | 2026-05-18 10:38:06 | Evgenii Maksimenkov | States that Kimi lacked two-thirds validation and a high-voting-power Kimi participant had both ML nodes preserved. | `gonka17gpuntq09zsaqtmpe544gc32tk4424dwv5t34f`; voting power `159432` |
| `15567` | 2026-05-18 10:42:11 | Gleb Morgachev | States that a fix had been added in `0.2.13` to prevent this preserved condition. | Fix reference only |

## Key Excerpts

**Message `15548`, Evgenii Maksimenkov - original Russian**

> Этот участник выбыл, потому что его мало кто провалидировал (хотя он отправил достаточно nonces). Это произошло и для qwen и kimi одновременно: `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6`.

**English translation**

> This participant dropped out because too few validators validated it, although it submitted enough nonces. This happened for both Qwen and Kimi simultaneously: `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6`.

**Message `15565`, Evgenii Maksimenkov - original Russian**

> В этот cpoc у всех не набралось 2/3 валидаций kimi, даже у гардиан. ... у ноды `gonka17gpuntq09zsaqtmpe544gc32tk4424dwv5t34f` скопилось большой voting power `159432` из-за делегаций и ... обе ml ноды, которые обслуживали kimi стали preserved и не валидировали других.

**English translation**

> In this cPoC nobody reached two-thirds Kimi validation, including the guardian. Participant `gonka17gpuntq09zsaqtmpe544gc32tk4424dwv5t34f` accumulated voting power of `159432` through delegations, and both ML nodes serving Kimi became preserved and did not validate others.

**Message `15567`, Gleb Morgachev - original Russian**

> Вот для этого фикс в 0.2.13 после отмены добавили. Чтобы такие ноды в preserved не были.

**English translation**

> A fix was added in `0.2.13` after the rollback for exactly this situation, so that such nodes would not be preserved.

## Assessment

- The DevOps discussion supports the described validation-shortfall mechanism and points to a remediation.
- It identifies one known affected participant and a high-voting-power preserved participant relevant to the mechanism.
- It does not supply a complete victim set or payout methodology for Proposal #3.

## Public References

- [Participant tracker link cited in message `15548`](https://tracker.gonka.vip/?participant=gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6)
- [PR #1143: `v0.2.13` confirmation PoC mitigation](https://github.com/gonka-ai/gonka/pull/1143)
