# P3-CAND-04 Stage Loss Breakdown

Dropped rows can be tied to an exclusion block and therefore to a concrete
cPoC trigger. Reduced rows do not have exclusion rows; their loss is
therefore attributed conservatively as an h_before to h_after final
snapshot delta.

| Stage | Trigger | Relation | Excluded at stage | Affected attributed | Dropped | Reduced | Lost cw | Compensation, GNK | Attribution |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| `0` | `4264130` | `pre_upgrade` | `6` | `0` | `0` | `0` | `0` | `0.000000000` | no_affected_rows_directly_attributed |
| `1` | `4265965` | `pre_upgrade` | `2` | `0` | `0` | `0` | `0` | `0.000000000` | no_affected_rows_directly_attributed |
| `2` | `4267778` | `post_upgrade` | `5` | `5` | `5` | `0` | `85614` | `20793.397023358` | direct_exclusion_height |
| `3` | `4270605` | `post_upgrade` | `2` | `2` | `2` | `0` | `1480` | `359.453215531` | direct_exclusion_height |
| `final_snapshot_delta` | `` | `post_upgrade_observed_by_h_after` | `` | `12` | `0` | `12` | `46432` | `11277.116015933` | reduced_rows_have_no_exclusion_row; loss observed between h_before and h_after |
