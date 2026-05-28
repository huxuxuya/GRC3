# GRC Case Header Template

This README contains the standard header for GRC case investigations.

Use it at the top of any case investigation document or repository. The header should give reviewers the minimum information needed to understand the case before reading details.

## Copy-Paste Header

```md
# CASE-ID: Case Name, Epoch(s)

| Field | Value |
|---|---|
| **Case** | `CASE-ID` - Short case name |
| Proposal | Proposal #N candidate |
| Epochs affected | Exact epoch, range, or `TBD` |
| Affected participants | Confirmed count and unit, or `TBD` |
| Estimated compensation | Amount and denom, or `TBD` |
| **Cause and evidence** | Short cause summary. Evidence: links to calculation, data, chat log, on-chain proof, or `Evidence needed`. |
| **Can it happen again?** | Short recurrence-risk statement: `No known repeat path`, `Reduced risk`, `Still possible`, or `Unknown`. |
| **Mitigation / fix** | PR, release, operational change, or `No confirmed mitigation`. |
| **Compensation overlap** | Other GRC cases or calculations touching the same epochs / losses, or `No known overlap`. |
| **Current decision** | What GRC must decide next: eligibility, inclusion, amount validation, duplicate-risk review, or rejection. |
| **Review focus** | Who should validate and what they must check first. |
```

## Field Rules

Keep every row in the header. If a value is not known yet, use `TBD`, `Unknown`, `Evidence needed`, `No confirmed mitigation`, or `No known overlap`.

| Field | How to fill |
|---|---|
| **Case** | Combine case ID and short readable name in one row. Example: `` `P4-CAND-01` - Kimi Restitution ``. |
| Proposal | Use current proposal classification, not historical planning context. Example: `Proposal #4 candidate`. |
| Epochs affected | Use the exact epoch range where the loss happened. If uncertain, write `TBD` and explain below in Findings. |
| Affected participants | Use confirmed count and unit. Examples: `52 unique addresses`, `19 miners`, `1 claimant`. |
| Estimated compensation | Use the calculated amount and denom. If not calculated, write `TBD`; do not remove the row. |
| **Cause and evidence** | One compact sentence for cause, then direct links to primary proof. Keep detailed chronology below. |
| **Can it happen again?** | State practical recurrence risk after known fixes. Avoid overclaiming if the fix is partial. |
| **Mitigation / fix** | Name the PR/version/process change. If no fix is confirmed, say that explicitly. |
| **Compensation overlap** | List any GRC compensation cases, proposals, or active calculations that touch the same epochs or economic loss. If none are known, write `No known overlap`. |
| **Current decision** | State the next governance or committee decision, not the whole history. |
| **Review focus** | Name validators if assigned and mention the highest-risk checks. |
