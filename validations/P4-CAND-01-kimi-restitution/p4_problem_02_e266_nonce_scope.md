# P4 Problem 02: Epoch 266 Nonce Scope

## Question

Which epoch `266` nonce rows are narrow final-set exclusion victims, and which
are broader reconstruction/top-up rows?

## Current Evidence

Primary local evidence:

- [`p4_audit_pass_04_e266_nonce_scope.md`](p4_audit_pass_04_e266_nonce_scope.md)
- [`p4_problem_02a_e266_zero_reward_rows.md`](p4_problem_02a_e266_zero_reward_rows.md)
- [`p4_e266_nonce_scope_classifier.csv`](p4_e266_nonce_scope_classifier.csv)
- [`p4_e266_zero_reward_rows.csv`](p4_e266_zero_reward_rows.csv)
- raw commit and validation cache listed in
  [`raw_chain_cache_manifest.md`](raw_chain_cache_manifest.md)
- source labels listed in
  [`source_cache_manifest.md`](source_cache_manifest.md)

## Findings

| Group | Count | Local status | Decision need |
|---|---:|---|---|
| Source-listed excluded operators | `9` | Raw PoC commit rows exist, raw validation records exist, no final epoch-group row, no performance row. | Chain facts confirmed; compensation still depends on external-attack scope. |
| In-final-group rewarded top-up rows | `4` | Participants were in final group and already received rewards. | Policy required; this is not final-set exclusion. |
| In-final-group zero-reward rows | `5` | Pass 02a confirms they were in final group, had raw commits/validations, then ended with `confirmation_weight=0`, `rewarded_coins=0`, and `failed_confirmation_poc`. Three are Qwen-only by source labels, one is Kimi-only, and one is mixed Kimi+Qwen. | Row-level cause and policy required before treating as attack victims. |

## What Is Proven

- The narrow claim is true for the 9 source-listed excluded operators: they
  submitted raw PoC commits and did not enter the final epoch group.
- The raw CLI commit and validation outputs do not include `model_id`; Kimi
  attribution is backed by the pinned Votkon source artifact, not by that raw CLI
  output alone.

## What Is Not Proven

- That all 18 source nonce-compensation rows are the same class of victim.
- That reconstructed nonce weights are automatically eligible for compensation.
- That the 5 zero-reward in-final-group rows failed because of the same incident
  rather than ordinary cPoC failure or local operator issues.

## Recommended Handling

Split e266 nonce into at least two decisions:

1. Narrow excluded-operator decision for the 9 absent final-set operators.
2. Broader reconstruction/top-up decision for the remaining 9 rows.

Do not approve all 18 rows as one technical class.
