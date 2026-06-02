# P3-CAND-03 Validation: Failed cPoC / Preserved Kimi Shortfall

This folder contains an independent validation package for Case 3, epoch `267`.

The validation does not execute, import, or copy the published
`gonkalabs/GRC-e267-kimi_shortfall` audit script. The published report is used
only as a final comparison target after the local chain reconstruction is
complete.

## What Is Checked

- Epoch `267` root cohort and total reward denominator.
- Confirmation PoC events at heights `4122271`, `4130085`, `4133665`, and
  `4134529`.
- Qwen and Kimi submissions, validation weights, guardian tie-break outcomes,
  and zero-reward participants.
- The claimant
  `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6`.
- Whether the observable chain data fits a local hardware/config failure better
  than a network validation/preserved-node failure.
- Restitution amount from integer chain inputs.

## Plain-English Explanation

In epoch `267`, the claimant was active and did submit cPoC work. During the
first confirmation PoC, the chain tried to confirm that enough of the claimant's
expected model capacity was actually observed.

That check is summarized by `ConfirmationPoCRatio`:

```text
ConfirmationPoCRatio = confirmed_capacity / expected_capacity
```

`AlphaThreshold` is the minimum allowed ratio. In this epoch it was `0.5`,
meaning the participant had to keep at least 50% of expected confirmation
capacity. If the ratio drops below that value, the chain marks the participant
as failed confirmation PoC.

For this claimant, the archive state shows:

```text
ConfirmationPoCRatio = 0.0057419461588255
AlphaThreshold       = 0.5
```

So the chain saw only about `0.57%` of the expected confirmed capacity, while
the minimum was `50%`. At block `4122552`, the claimant moved from `ACTIVE` to
`INACTIVE` with reason `failed_confirmation_poc`.

The important part is why the confirmed capacity became so small. The cPoC
snapshot shows a high Kimi voting-power participant,
`gonka17gpuntq09zsaqtmpe544gc32tk4424dwv5t34f`, was preserved for that cPoC
episode on Kimi nodes `B9` and `U11`. Because preserved nodes stay on inference
instead of validating cPoC work, that large Kimi voting power did not help
validate the claimant's Kimi row. The claimant therefore lost confirmation
weight, failed the ratio threshold, and received zero reward for the epoch.

In short:

```text
high Kimi voting power preserved
-> not enough Kimi confirmation support
-> claimant confirmation weight collapsed
-> ConfirmationPoCRatio fell below AlphaThreshold
-> failed_confirmation_poc
-> reward = 0
```

This does not look like the simple case "the claimant did not submit anything."
The claimant did submit. The disputed part that remains is policy/eligibility:
whether any proxy configuration responsibility should affect compensation.

Formula check: `case3_chain_formula_reconciliation.md` maps these tables back
to the historical chain code. The raw `>2/3` checks use
`sum(model voting power) > poc_validation_snapshot.TotalNetworkWeight * 2 / 3`;
the final failure ratio uses the pre-fix `foldEventReadings` formula
`(preserved + measured) / (preserved + notPreserved) / 0.909`. The stored epoch
`265` and `267` ratios both reconcile with that formula.

Fixed in: `v0.2.13` microrelease / PR `#1143` / commit `17808620`. The update
stores one epoch snapshot of confirmable models and weight-scale factors for
confirmation and reward calculations, and disables confirmation PoC for the
rest of the upgrade epoch so the new snapshot logic starts cleanly.

## How To Run

The script reads `.env` locally. `GONKA_RPC_URL` or `GONKA_RPC_LCD_URL` must be
set. `GONKA_RPC_API_KEY` is optional. Neither value is written to artifacts.

```bash
python3 validations/P3-CAND-03-failed-cpoc-epoch-267/verify_archive.py
```

Raw node responses are cached under `/tmp/grc3-case3-audit` by default. The
tracked artifacts are normalized CSV/JSON summaries only.

To check the nearest five epochs before epoch `267` and all epochs through the
`v0.2.13` upgrade epoch for the same failed-cPoC signature:

```bash
python3 validations/P3-CAND-03-failed-cpoc-epoch-267/scan_neighbor_epochs.py --center-epoch 267 --epochs-before 5 --epochs-after 9
```

That scan checks epochs `262..276`, caches raw node responses under
`/tmp/grc3-case3-neighbor-scan`, and writes normalized summary artifacts in this
folder.

## Current Result

The independent run confirms one Case 3 candidate:

`gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6`

Confirmed chain facts:

- epoch `267` root cohort has `51` participants and root total weight `541,415`;
- claimant root weight is `19,518`;
- claimant reward for epoch `267` is `0`;
- claimant is in `excluded_participants/267` with reason
  `failed_confirmation_poc` at block `4122552`, inside the first cPoC window;
- claimant status changes from `ACTIVE` at block `4122551` to `INACTIVE` at
  block `4122552`;
- claimant `ConfirmationPoCRatio` at exclusion is `0.0057419461588255`, below
  `AlphaThreshold = 0.5`; in plain terms, about `0.57%` confirmed capacity was
  observed against a `50%` minimum;
- claimant root `confirmation_weight` drops from `65,716` before exclusion to
  `343` at exclusion;
- claimant submitted both Qwen and Kimi at cPoC #1;
- Kimi cPoC #1 validation weight was `171,571 / 541,415`, below the `>2/3`
  weight threshold;
- high Kimi voting-power participant
  `gonka17gpuntq09zsaqtmpe544gc32tk4424dwv5t34f` had Kimi voting power
  `159,432` and did not validate the claimant's Kimi cPoC #1 row;
- the preserved snapshot for cPoC anchor `4122271` shows that same high-power
  participant preserved on Kimi nodes `B9` and `U11`;
- the integer reward reconciliation matches `10,262.057515369 GONKA`.

Extended pre-fix scan through epoch `276`:

- `119` zero-reward `failed_confirmation_poc` rows were found before the clean
  `v0.2.13` start;
- strict Case-3-like Kimi-shortfall signature appears only in epochs `265` and
  `267`, both for the same claimant;
- `24` additional rows had at least one submitted model reach `pass_weight` but
  still failed the confirmation ratio, so they are broader confirmation
  accounting candidates for separate review, not automatic Case 3 inclusions.

Important limitation: the raw REST validation rows alone are not the final
chain verdict, because the chain also applies cPoC snapshot/slot logic and then
records the actual outcome in exclusion state. The inclusion decision therefore
uses `excluded_participants` plus the submission/weight trace, not only the raw
guardian vote count from validation rows.

## Artifacts

- `case3_inputs_manifest.json` - source hashes, event list, aggregate result.
- `case3_epoch_cohort.csv` - root cohort and model voting powers.
- `case3_cpoc_events.csv` - cPoC event and row counts.
- `case3_cpoc_matrix.csv` - per-participant, per-event, per-model result matrix.
- `case3_zero_reward_review.csv` - zero-reward inclusion/exclusion review.
- `case3_claimant_trace.csv` - claimant-only trace.
- `case3_high_power_kimi_validator_trace.csv` - trace for the high-power Kimi
  non-voting participant cited in DevOps discussion.
- `case3_root_cause_trace.json` - status transition, ratio/threshold,
  confirmation-weight drop, validation snapshot, and preserved snapshot focus.
- `case3_preserved_snapshot_focus.csv` - preserved nodes for the high-power
  participant relevant to the Case 3 mechanism.
- `case3_amount_reconciliation.json` - integer reward calculation.
- `case3_published_compare.json` - final comparison against the published
  Case 3 amount.
- `case3_root_cause_review.md` - hardware/config vs chain/protocol assessment.
- `case3_plain_evidence.md` - simple human-readable explanation with the
  exact weights, ratio, threshold, preserved-node evidence, and conclusion.
- `case3_epoch267_timeline.md` - height-by-height timeline for epoch `267`
  with preserved weight, available validation weight, actual claimant
  validation weight, and `>2/3` threshold checks.
- `case3_epoch265_timeline.md` - same-address neighbor timeline for epoch
  `265`, including cPoC heights, preserved weight, available validation
  weight, actual claimant validation weight, and exclusion state.
- `case3_epoch265_model_weights.csv` - full epoch `265` per-model
  participant weights with model `weight`, model `voting_power`, preserved
  flag, and preserved node IDs.
- `case3_chain_formula_reconciliation.md` - mapping from the validation tables
  to the historical chain formulas, including numeric reconciliation of the
  epoch `265` and `267` `ConfirmationPoCRatio` values.
- `case3_time_reference.md` - UTC/MSK timestamps for epoch `265`, epoch `267`,
  the claimant cPoC/exclusion blocks, and the on-chain `v0.2.13` upgrade
  installation.
- `case3_pre_fix_window_review.md` - extended epoch `262..276` scan summary,
  separating strict Case-3-like rows from broader pre-fix confirmation-accounting
  candidates.
- `../P3-CAND-06-pre-fix-confirmation-accounting/` - standalone candidate case
  package for the `24` broader pass-weight-but-failed-ratio rows found during
  the pre-fix scan.
- `case3_epoch266_same_claimant_check.md` - boundary check for the same
  claimant in epoch `266`, separating ordinary PoC from confirmation PoC and
  documenting why epoch `266` does not currently prove a same-claimant reward
  loss.
- `scan_neighbor_epochs.py` - independent scanner for neighbor and pre-fix
  epochs around epoch `267`.
- `case3_neighbor_epoch_summary.csv` - per-epoch counts for the neighbor scan.
- `case3_neighbor_failed_cpoc_rows.csv` - every `failed_confirmation_poc` row
  found in the neighbor scan with model weights, ratio, and loss estimate.
- `case3_neighbor_epoch_scan.json` - machine-readable neighbor-scan result.
- `case3_neighbor_epoch_scan.md` - human-readable neighbor-scan summary.
