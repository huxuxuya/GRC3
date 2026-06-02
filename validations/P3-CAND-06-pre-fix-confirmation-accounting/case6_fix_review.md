# P3-CAND-06 Fix Review

This note records which release/PR evidence currently matches the
`P3-CAND-06` failure shape.

## Matching Fix

The matching fix family is `v0.2.13` / PR
[`#1143`](https://github.com/gonka-ai/gonka/pull/1143).

The relevant release/PR description says confirmation PoC used different model
sets for:

- measured weight;
- preserved weight;
- reward rescaling.

During new-model bootstrap this could slash honest miners serving both an
eligible model and a not-yet-eligible model. The stated fix stores one epoch
snapshot of confirmable models and weight-scale factors, then uses that
snapshot for confirmation and reward-weight calculations.

The same release text also says confirmation PoC triggers are skipped from the
upgrade height through the end of the upgrade epoch, so the new snapshot logic
starts from the next epoch.

The local code-diff review in `case6_code_diff_root_cause.md` confirms this at
source level. The `v0.2.13` diff adds `ConfirmationWeightScales`, stores it in
epoch group data, and applies it consistently to epoch-member confirmation
weight, cPoC measured/preserved weight, and reward rescaling.

## Why This Matches P3-CAND-06

`P3-CAND-06` rows are exactly in the pre-fix multi-model window:

- at least one Qwen/Kimi model has a cPoC store commit and `pass_weight`;
- the durable participant state still records `failed_confirmation_poc`;
- actual reward is zero;
- `ConfirmationPoCRatio` is below alpha;
- confirmation weight is cut during the cPoC event.

The raw stage replay confirms that this is not explained by a simple lack of
validators for the passing model: all `24` candidates have at least one model
where raw stage validations reconstruct strict `>2/3` valid weight.

## Nonce-Limit Fix Is Separate

PR `#1143` also changes devshard settlement nonce limits:
`DevshardEscrowParams.MaxNonce` replaces the old hardcoded `20_000` limit and
the upgrade sets it to `1_000_000`.

That nonce-limit fix is not the same mechanism as the cPoC weight cut analyzed
here. The P3-CAND-06 evidence uses PoC V2 stage commits and validation rows,
where the chain exposes commit counts/root hashes and validation rows, not the
individual off-chain nonce/payload bodies.

## PR #550 / PR #826

Within the current local evidence, PRs `#550` and `#826` are not treated as the
fix for this candidate. They remain outside the current root-cause chain unless
a direct link to confirmation-PoC weight preservation is later found.

## Current Fix Conclusion

- Direct matching fix: `v0.2.13` / PR `#1143`.
- Direct matching failure mode: confirmation-PoC accounting used inconsistent
  model sets during new-model bootstrap.
- Source-level confirmation: `case6_code_diff_root_cause.md`.
- Not currently a match: devshard nonce limit, claim/settlement-only fixes, or
  generic lack of validators.
