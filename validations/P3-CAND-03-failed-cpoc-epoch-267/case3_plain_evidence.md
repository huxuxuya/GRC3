# Case 3 Plain Evidence

This note explains the failure in simple terms, using only the independently
collected archive-chain artifacts in this folder.

## One-Sentence Summary

The claimant submitted Kimi work, but not enough Kimi validation power confirmed
it during the first confirmation PoC. A very large Kimi voting-power participant
was preserved for that same cPoC episode, so its Kimi nodes did not validate the
claimant's Kimi row. The claimant's confirmed capacity ratio fell below the
required threshold and the chain excluded the participant.

## Key Addresses

| Role | Address | Evidence |
|---|---:|---|
| Claimant | `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6` | Excluded at block `4122552` with `failed_confirmation_poc` |
| High Kimi voting-power participant | `gonka17gpuntq09zsaqtmpe544gc32tk4424dwv5t34f` | Kimi voting power `159,432`; preserved on Kimi nodes `B9` and `U11` |

## What the Chain Required

After confirmation PoC, the chain compares:

```text
ConfirmationPoCRatio = confirmed_capacity / expected_capacity
```

The minimum allowed ratio was:

```text
AlphaThreshold = 0.5
```

Plainly: the participant needed at least `50%` of expected confirmation capacity
to remain active.

## What Actually Happened

| Check | Value |
|---|---:|
| Status before exclusion, block `4122551` | `ACTIVE` |
| Status at exclusion, block `4122552` | `INACTIVE` |
| Exclusion reason | `failed_confirmation_poc` |
| Expected/root confirmation weight before exclusion | `65,716` |
| Confirmation weight at exclusion | `343` |
| Confirmation weight lost | `65,373` |
| ConfirmationPoCRatio | `0.0057419461588255` |
| AlphaThreshold | `0.5` |

So the chain saw about `0.57%` confirmed capacity, while the minimum was `50%`.

## cPoC #1 Model-Level Evidence

| Model | Claimant submitted count | Validation weight observed | Network total weight | Share of total | Result from raw rows |
|---|---:|---:|---:|---:|---|
| Qwen | `1,024` | `129,251` | `541,415` | `23.8728%` | Guardian-assisted pass |
| Kimi | `57,664` | `171,571` | `541,415` | `31.6894%` | Guardian-assisted in raw rows, but chain exclusion state records failed confirmation PoC |

The important point is that Kimi did not reach the `>2/3` validation-weight
threshold by ordinary voting weight. It depended on guardian/preserved behavior,
and the chain's final durable state still recorded `failed_confirmation_poc`.

## The Missing Kimi Validation Power

The high-power participant had:

```text
Kimi voting power = 159,432
```

This is huge relative to the network total used by the cPoC check:

```text
159,432 / 541,415 = 29.45%
```

That participant appears in the preserved snapshot for the same cPoC anchor:

| Anchor | Model | Preserved participant | Preserved nodes |
|---:|---|---|---|
| `4122271` | Kimi | `gonka17gpuntq09zsaqtmpe544gc32tk4424dwv5t34f` | `B9`, `U11` |
| `4122271` | Qwen | `gonka17gpuntq09zsaqtmpe544gc32tk4424dwv5t34f` | `U2a`, `U2b` |

Preserved nodes stay on inference instead of validating the cPoC episode. The
same high-power participant did not validate the claimant's Kimi cPoC #1 row.

## Why This Proves the Mechanism

1. The claimant did submit Kimi work: `57,664` submitted count.
2. The chain later excluded the claimant with `failed_confirmation_poc`.
3. The exact status transition happened at block `4122552`.
4. At that block, `ConfirmationPoCRatio = 0.0057419461588255`, below the `0.5`
   alpha threshold.
5. The claimant's confirmation weight collapsed from `65,716` to `343`.
6. A high Kimi voting-power participant worth `159,432` Kimi voting power was
   preserved for this cPoC and did not validate the claimant's Kimi row.

Therefore the failure was not that the claimant simply failed to submit. The
failure was that the submitted Kimi capacity was not confirmed by enough
effective validation power during the first confirmation PoC.

## Short Version for Non-Technical Readers

The claimant showed up and sent Kimi proof. The network then needed enough Kimi
validators to confirm that proof. One of the largest Kimi validation-power
holders was preserved and therefore did not validate this cPoC. Because that
large weight was missing, the claimant's confirmed capacity fell to about
`0.57%` of expected capacity, far below the required `50%`. The chain marked the
claimant as failed confirmation PoC and paid zero reward for the epoch.

