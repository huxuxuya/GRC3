# OBS-01: Governance Zero Voting Weight

| Field | Value |
|---|---|
| Classification | Additional observation; not proposed for compensation |
| Date range | Identified 2026-05-15; referenced again 2026-05-25 |
| Reported by | Evgenii Maksimenkov; Gleb Morgachev; Mitch |
| Known affected | `gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu`; `gonka16k03ze5ynkprsd4n6e5uzhthvu9jjk553rauqy` |
| Reported impact | Governance voting weight not counted for some nodes |
| Compensation evidence | None: no reward or coin loss asserted in the reviewed messages |
| Action status | Review only |

## Evidence

| Message ID | Date (UTC+03) | Author | Fact |
|---|---|---|---|
| `15169` | 2026-05-15 15:42:48 | Evgenii Maksimenkov | Identified `gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu` as a participant whose weight was not counted. |
| `15176` | 2026-05-15 16:08:56 | Gleb Morgachev | Described a validator-key propagation issue affecting consensus/governance, not rewards. |
| `15217` | 2026-05-15 18:13:43 | Evgenii Maksimenkov | Stated that `gonka16k03ze5ynkprsd4n6e5uzhthvu9jjk553rauqy` had voted with zero weight since proposal 39. |
| `16023` | 2026-05-25 18:22:49 | Mitch | Stated that votes in a prior NOP proposal were not counted because some nodes had zero voting weight. |

## Key Excerpt

**Message `15176`, Gleb Morgachev - original Russian**

> Это не влияет на ревоорды, но влияет на consensus module, который подписывает блоки и считает governance.

**English translation**

> This does not affect rewards, but it affects the consensus module that signs blocks and counts governance.

## Assessment

This issue is material for governance integrity, but the reviewed evidence explicitly distinguishes it from a reward loss. It is recorded for transparency and is not a compensation candidate.

## Mitigation / Fix Status

| Item | Status |
|---|---|
| Identified code area | Message `15212` points to validator computation flow in `gonka-ai/cosmos-sdk`. |
| Planned target stated in chat | Gleb Morgachev stated in message `15176` that the fix was not included in proposed `0.2.13` and should be prioritised for `0.2.14`. |
| Public delivery evidence | No merged Gonka PR or confirmed deployed fix was identified for this issue as of 2026-05-27. |
| Timing | `0.2.14` is a stated target, not a confirmed release date. |

## Public References

- [Participant tracker link cited in message `15176`](https://tracker.gonka.hyperfusion.io/?participant=gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu)
- [Consensus code reference cited in message `15212`](https://github.com/gonka-ai/cosmos-sdk/blob/7d8a91cc44ab5e4fd09538c848cf8369a058c1a8/x/staking/keeper/compute.go#L306)
