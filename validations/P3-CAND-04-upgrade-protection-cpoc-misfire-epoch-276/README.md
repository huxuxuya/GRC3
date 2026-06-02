# P3-CAND-04 Validation

Independent archive-chain validation for the epoch 276
UpgradeProtectionWindow / cPoC misfire candidate.

## Result

- Affected set: `19` participants (`7` dropped, `12` reduced).
- Independent total: `36,209.451291351 GONKA`.
- Published CSV total: `36,209.451291351 GONKA`.
- Published CSV comparison exact match: `True`.
- Root-cause support: `LastUpgradeHeight` latest null proof = `True`.
- Scope scan case4-like post-upgrade cPoC rows: `2`.
- Code fix identified: PR #1268 `https://github.com/gonka-ai/gonka/pull/1268` on branch `upgrade-v0.2.14`; deployment requires separate chain confirmation.

## What Was Checked

- Historical `epoch_group_data/276` at `4267299` and `4274661`.
- Historical participant status at the same two heights.
- Final `epoch_performance_summary/276` rewards.
- Epoch `270..283` control cPoC timeline around the upgrade epoch.
- Post-upgrade cPoC stages inside epoch 276.
- Direct `LastUpgradeHeight` `abci_query` evidence.
- Full member completeness matrix for epoch 276.
- Local overlap matrix with P4-CAND-01 and P3-CAND-06 references.

## Files

- `case4_epoch276_timeline.md/csv/json`
- `case4_upgrade_protection_evidence.md/json`
- `case4_root_cause_deep_dive.md/json`
- `case4_scope_control_scan.md/csv/json`
- `case4_stage_loss_breakdown.md/csv/json`
- `case4_completeness_matrix.md/csv/json`
- `case4_overlap_matrix.md/csv/json`
- `case4_affected_participants.md/csv/json`
- `case4_compensation_replay.md/csv/json`
- `case4_published_compare.md/json`
- `raw_cache/` sanitized archive responses and published CSV text
