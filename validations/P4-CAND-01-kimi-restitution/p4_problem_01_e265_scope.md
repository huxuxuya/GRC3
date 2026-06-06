# P4 Problem 01: Epoch 265 Scope

## Question

Which epoch `265` rows belong in P4, and which should be handled by Case 3 or
rejected from strict direct-cPoC scope?

## Current Evidence

Primary local evidence:

- [`p4_audit_pass_02_e265.md`](p4_audit_pass_02_e265.md)
- [`p4_audit_pass_03_e265_gonka1830.md`](p4_audit_pass_03_e265_gonka1830.md)
- [`p4_e265_row_classifier.csv`](p4_e265_row_classifier.csv)
- [`p4_e265_gonka1830_cpoc_evidence.csv`](p4_e265_gonka1830_cpoc_evidence.csv)

## Findings

| Row / address | Source amount, GONKA | Local classification | Decision need |
|---|---:|---|---|
| `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6` | `20,896.527179100` | Confirmed as the same direct Kimi cPoC shortfall class as Case 3 epoch `267`. | Keep in Case 3 extension, not as an independent P4 row. |
| `gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu` | Source e265 row | Rewarded confirmation-weight drop, not a direct zero-reward cPoC victim. | Policy required if committee wants broader attack/weight-drop scope. |
| `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` | Source e265 row | No raw Kimi/Qwen commit rows and no validation records at final cPoC stage `4102890`. | Not confirmed as direct Kimi cPoC shortfall. |

## What Is Proven

- The `gonka1j7...` e265 row overlaps with the Case 3 pattern and amount.
- The other two e265 rows do not currently satisfy strict direct Kimi cPoC
  restitution criteria.

## What Is Not Proven

- That all e265 P4 rows are direct restitution victims.
- That external attack attribution alone is enough for GRC compensation.

## Recommended Handling

Do not approve e265 as a P4 bundle. Treat `gonka1j7...` as Case 3 scope and
put the other two rows into a separate broader-policy question only if the
committee wants to compensate attack-attributed weight degradation beyond direct
cPoC failure.
