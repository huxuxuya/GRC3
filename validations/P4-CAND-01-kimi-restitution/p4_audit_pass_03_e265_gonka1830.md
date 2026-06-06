# P4 Conceptual Audit Pass 03: Epoch 265 `gonka1830...` cPoC Evidence

This pass checks whether the disputed epoch `265` row
`gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` has the same direct
Kimi cPoC shortfall signature as the confirmed Case 3 overlap row.

The parser reads only saved raw chain cache files and does not query a node.

Raw inputs copied into `raw_chain_cache/`:

- `case6_raw_stage_4102890_all_poc_v2_store_commits.json`
- `case6_raw_stage_4102890_poc_v2_validations_for_stage.json`
- `case6_raw_height_4103171_stage_4102890_poc_validation_snapshot.json`
- `case6_raw_epoch265_model_qwen_epoch_group_data.json`

Derived outputs:

- `p4_e265_gonka1830_cpoc_evidence.csv`
- `p4_e265_gonka1830_cpoc_evidence.json`

## Key Rows

| Address | Model | Model VP | Commit count | Validation rows | Valid validator VP | Classification |
|---|---|---:|---:|---:|---:|---|
| `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6` | `Qwen/Qwen3-235B-A22B-Instruct-2507-FP8` | `66311` | `960` | `10` | `35370` | `submitted_but_below_two_thirds_validation_power` |
| `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6` | `moonshotai/Kimi-K2.6` | `66311` | `52028` | `8` | `256727` | `submitted_but_below_two_thirds_validation_power` |
| `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` | `Qwen/Qwen3-235B-A22B-Instruct-2507-FP8` | `None` | `0` | `0` | `0` | `no_submission_or_validation_record_at_stage` |
| `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` | `moonshotai/Kimi-K2.6` | `13490` | `0` | `0` | `0` | `no_submission_or_validation_record_at_stage` |

## Interpretation

- The confirmed Case 3 overlap address `gonka1j7...` has raw cPoC
  commit rows on the same stage for both Qwen and Kimi. Its Kimi commit
  count is `52028`, and its valid Kimi validator voting power is `256727`,
  below the `>2/3` model-voting-power rule.
- The disputed `gonka1830...` row has Kimi model voting power `13490`
  in the snapshot and appears in the Kimi model group, but it has zero
  commit rows and zero validation records on stage `4102890` for both
  Kimi and Qwen.
- Therefore this row is not proven to be the same direct Kimi cPoC
  shortfall class as the Case 3 overlap. The chain evidence supports a
  different classification: zero-reward `failed_confirmation_poc` with
  no cPoC submission/validation record at the final checked stage.
