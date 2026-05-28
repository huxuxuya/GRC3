# Public Compensation Case Template

Use this template for public case investigation pages in `public_cases/`.

The first table is the case header. It should be short, clear, and enough for a reader to understand the case without reading the full investigation.

## Header Structure

```md
# CASE-ID: Case Name, Epoch(s)

| Field | Value |
|---|---|
| **Case** | `CASE-ID` - Short case name |
| Proposal | Proposal #N candidate |
| Epochs affected | Exact epoch, range, or `TBD` |
| Affected participants | Number of affected addresses / miners / claimants, or `TBD` |
| Estimated compensation | Amount in GNK, or `TBD` |
| **Cause and evidence** | Short root cause summary. Evidence: calculation repo, chat log, on-chain proof, or `Evidence needed`. |
| **Can it happen again?** | Short recurrence-risk statement: `No known repeat path`, `Reduced risk`, `Still possible`, or `Unknown`. |
| **Mitigation / fix** | PR, release, operational change, or `No confirmed mitigation`. |
| **Compensation overlap** | Other GRC cases or calculations touching the same epochs / losses, or `No known overlap`. |
| **Current decision** | What GRC must decide next: eligibility, inclusion, amount validation, duplicate-risk review, or rejection. |
| **Review focus** | Who should validate and what they must check first. |
```

## How To Fill It

| Field | How to fill |
|---|---|
| **Case** | Combine case ID and short readable name in one row. Example: `` `P4-CAND-01` - Kimi Restitution ``. |
| Proposal | Use current proposal classification, not historical planning context. Example: `Proposal #4 candidate`. |
| Epochs affected | Use the exact epoch range where the loss happened. If uncertain, write `TBD` and explain below in Findings. |
| Affected participants | Use confirmed count and unit. Examples: `52 unique addresses`, `19 miners`, `1 claimant`. |
| Estimated compensation | Use the calculated amount and denom. If not calculated, write `TBD`; do not remove the row. |
| **Cause and evidence** | One compact sentence for cause, then direct links to proof. Keep detailed chronology below. |
| **Can it happen again?** | State practical recurrence risk after known fixes. Avoid overclaiming if the fix is partial. |
| **Mitigation / fix** | Name the PR/version/process change. If no fix is confirmed, say that explicitly. |
| **Compensation overlap** | List any GRC compensation cases, proposals, or active calculations that touch the same epochs or economic loss. If none are known, write `No known overlap`. |
| **Current decision** | State the next governance or committee decision, not the whole history. |
| **Review focus** | Name validators if assigned and mention the highest-risk checks. |

## Recommended Page Sections

After the header, keep details in this order:

```md
## Message Log

## Findings

## Mitigation / Fix Status

## Reward Flow

## Sources
```

## Writing Rules

- Keep the header compact: usually 9-10 rows.
- Use simple public English.
- Put the most important facts first: epochs, affected participants, compensation.
- Keep links in the header only when they are primary evidence.
- Do not duplicate long explanations from later sections.
- Use `TBD`, `Unknown`, or `No confirmed mitigation` instead of hiding missing information.
- Always fill `Compensation overlap`; this prevents double compensation when multiple GRC cases touch the same epochs.
- Use `Review focus` for assigned validators and the most important checks, not as the only place for overlap risk.
