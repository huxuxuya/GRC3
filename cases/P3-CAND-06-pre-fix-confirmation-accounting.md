# P3-CAND-06: Pre-Fix Confirmation Accounting / Pass-Weight But Failed Ratio

[Назад к реестру](../compensation_cases_registry.md)

## Карточка

| Поле | Значение |
|---|---|
| Proposal | Кандидат Proposal #3 |
| Статус | Root-cause, raw stage replay, and code-diff proof added; требуется eligibility и overlap review |
| Эпохи | 263-276 |
| От кого поступила информация | Выявлено при независимой validation `P3-CAND-03` |
| Пострадавший / контакт для деталей | 19 unique participants из archive scan; contacts не сопоставлены |
| Кто уже исследовал / результат | @mikenosov; расширенный scan epochs `262..276`, выделено `24` candidate rows; GRC validation replay подтвердил raw submissions/validator weight, выделил классы риска, and matched the code fix in `v0.2.13` |
| Нужен дополнительный анализ | Да: coefficient-adjusted replay для mismatch rows и overlap checks |
| Investigator | Назначить |
| Validators | Назначить |
| Срок | Назначить |
| Пострадавшие | 19 unique participants / 24 epoch rows |
| Оценка компенсации | `120,822.324371792 GNK` preliminary zero-reward estimate |
| Решение / голосование | Отсутствует |

## Краткое Описание

При расширенной проверке `P3-CAND-03` до всего pre-fix окна перед чистым
стартом `v0.2.13` были найдены `119` zero-reward `failed_confirmation_poc`
строк. Большая часть не похожа на Case 3: у многих не было Qwen/Kimi submission
на выбранном cPoC event.

Отдельно выделены `24` строки, где хотя бы одна модель участника достигла
`pass_weight`, но итоговый `ConfirmationPoCRatio` всё равно оказался ниже
`AlphaThreshold`, participant был исключён с `failed_confirmation_poc` и получил
нулевую награду. Это не strict Case 3 Kimi shortfall, но такие строки прямо
относятся к broader confirmation-accounting risk, который исправлялся в
`v0.2.13`.

## Почему Это Отдельный Кейс

Этот набор нельзя автоматически включить в `P3-CAND-03`, потому что strict Case
3 требует Kimi submission + Kimi validating weight below `>2/3` + preserved
Kimi voting power. Здесь условие другое: одна из моделей уже имела
`pass_weight`, но final confirmation ratio всё равно провалился.

Также нельзя автоматически смешивать этот набор с `P3-CAND-04` или
`P4-CAND-01`, потому что:

- `P3-CAND-04` покрывает epoch `276` upgrade-protection/cPoC misfire;
- `P4-CAND-01` покрывает опубликованный Kimi restitution package `265..276`;
- в этом candidate есть строки из epoch `276` и Kimi-related rows, поэтому
  overlap должен быть проверен до любого payout decision.

## Хронология

| Дата и время | Автор | Событие | Что подтверждает |
|---|---|---|---|
| 17.05.2026-27.05.2026 | Chain state | Candidate rows occur across epochs `263..276` | Pre-fix occurrence window |
| 26.05.2026 17:39:41 MSK | Chain upgrade | `v0.2.13` applied at block `4,267,300`, epoch `276` | Fix installed on-chain |
| 27.05.2026 05:12:33 MSK | Chain epoch boundary | Epoch `277` starts at block `4,275,062` | Clean start after confirmation PoC disabled for upgrade epoch |
| 02.06.2026 | GRC validation work | Extended scan `262..276` identifies `24` broader suspicious rows | Candidate set extracted |

## Подтверждённые Факты

- Scan range: epochs `262..276`.
- `119` zero-reward `failed_confirmation_poc` rows exist in the broad pre-fix
  window.
- Strict Case-3-like Kimi-shortfall rows: `2`, both for
  `gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6`.
- This candidate's broader pass-weight-but-failed-ratio rows: `24`.
- Unique participants in this candidate: `19`.
- Preliminary estimated zero-reward loss: `120,822.324371792 GNK`.
- Epoch `276` subset: `4` rows, `42,799.389553703 GNK`.
- Root-cause replay confirms the anomaly shape: all `24` rows have durable
  `failed_confirmation_poc`, zero reward, `ConfirmationPoCRatio < 0.5`, and at
  least one Qwen/Kimi model that satisfies strict chain `pass_weight`
  (`validWeight > TotalNetworkWeight * 2 / 3`).
- Replay classification: `18` rows are
  `single_model_pass_expected_capacity_failed`; `5` rows are
  `single_model_pass_coefficient_replayed`; `1` row is
  `strong_signal_but_epoch276_overlap`.
- The strongest current contradiction is epoch `276`
  `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09`: Qwen `86.9859%`
  pass-weight and Kimi `78.7207%` pass-weight, but stored confirmation ratio
  `35.2638%`, zero reward, and `17,356.095656742 GNK` estimated loss. This row
  overlaps the `P3-CAND-04` review window and must not be approved twice.
- `18` rows reconcile with a simple
  `confirmation_weight_at_exclusion / confirmation_weight_before / 0.909`
  diagnostic ratio. Of the `6` simple-ratio mismatch rows, `5` reconcile with
  full coefficient replay using historical coefficients, time normalization,
  preserved snapshots, and MLNode distributions. The remaining non-match is the
  epoch `276` overlap row.
- Full old-formula replay across all `24` rows matches stored ratios for `22`.
  The two non-matches are both in epoch `276`, so they remain in the overlap /
  upgrade-review bucket.
- Bounded v0.2.13-style replay over the available Qwen/Kimi data does not make
  any of the `24` rows pass alpha. This supports keeping single-model row
  payout as a policy decision, not an automatic technical conclusion.
- Eligibility matrix: `20` non-epoch-276 rows are
  `formula_reconciled_policy_required`; `4` epoch-276 rows are
  `blocked_epoch276_overlap`.
- Row-by-row evidence ledger now combines trigger/exclusion heights, Qwen/Kimi
  commit and validator evidence, strict `2/3` threshold comparison, old-formula
  replay, bounded v0.2.13-style replay, loss amount, technical status, overlap
  status, and decision boundary for all `24` rows.
- Action split from the ledger: `6` rows are locally `clear`
  (`14,729.197017136 GNK`), `14` rows need P4-CAND-01 overlap review
  (`63,293.737800953 GNK`), and `4` rows are blocked by P3-CAND-04 overlap
  (`42,799.389553703 GNK`).
- Raw cPoC stage replay fetched `16` unique loss trigger heights and `54` raw
  endpoint cache files. It reconstructed `48` model rows from store commits,
  validation rows, and model voting power; all `48/48` rows match the previous
  aggregate CSV.
- After full formula/new-algorithm replay, the validation raw cache contains
  `140` files (`7.2 MB`) with a manifest and SHA256 hashes.
- The replay confirms `25` model rows with cPoC store commit/submission and
  strict `pass_weight`, covering all `24` candidate rows with at least one
  passing model. Therefore the current evidence does not support "lack of
  validators for the passing model" as the explanation.
- The chain endpoints used here expose cPoC store commit counts/root hashes and
  validation rows. They do not expose every individual off-chain nonce/payload
  body, so the proof is at commit/validation-row level rather than raw payload
  body level.
- The fixing upgrade is `v0.2.13` / PR `#1143` / commit `17808620`.
- Code-diff review confirms the fix added `ConfirmationWeightScales`, stored it
  in epoch group data, and reused the same snapshot for initial confirmation
  weight, cPoC measured/preserved weight, and Bitcoin reward rescaling. This
  matches the root-cause class: pre-fix confirmation accounting used
  inconsistent model sets during new-model bootstrap.

## Candidate Rows

| Epoch | Rows | Estimated loss, GONKA |
|---:|---:|---:|
| `263` | `3` | `8,719.070532944` |
| `264` | `3` | `6,010.126484192` |
| `265` | `1` | `335.927643572` |
| `268` | `1` | `25,309.087745610` |
| `269` | `2` | `2,764.396118755` |
| `271` | `1` | `139.200061369` |
| `272` | `4` | `31,070.826328522` |
| `273` | `2` | `3,237.649981278` |
| `274` | `2` | `310.429493665` |
| `275` | `1` | `126.220428182` |
| `276` | `4` | `42,799.389553703` |
| **Total** | **`24`** | **`120,822.324371792`** |

Top affected participants by preliminary amount:

| Participant | Estimated loss, GONKA |
|---|---:|
| `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `47,830.124048154` |
| `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | `17,356.095656742` |
| `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | `14,970.660343414` |
| `gonka14tqh62mangwzrma2lgg2dm375rcjzn2ydy8ttm` | `11,765.489995489` |
| `gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p` | `8,037.485696859` |

The full row list is in
`validations/P3-CAND-06-pre-fix-confirmation-accounting/candidate_rows.csv`.
The participant/epoch timeline with PoC start, cPoC trigger, exclusion height,
blocks remaining to next epoch, root weight, confirmed weight, and lost
confirmation weight is in
`validations/P3-CAND-06-pre-fix-confirmation-accounting/participant_epoch_timeline.md`.
For the more readable participant -> epoch -> cPoC breakdown, use
`validations/P3-CAND-06-pre-fix-confirmation-accounting/participant_grouped_cpoc_timeline.md`.

## Гипотезы И Пробелы В Данных

- Need to reconcile all `4` epoch `276` rows against `P3-CAND-04` /
  upgrade-protection evidence.
- Need to determine whether the `20` non-epoch-276 single-model rows that
  formula-reconcile are protocol-bug compensation rows or ordinary incomplete
  multi-model service rows.
- Need to separate protocol/accounting failure from ordinary incomplete
  multi-model service.
- Need to check overlap with `P3-CAND-04` and `P4-CAND-01`.

## Расчёт Компенсации

| Элемент | Значение / источник |
|---|---|
| Методика | Preliminary zero-reward estimate: expected epoch reward from root weight minus actual reward |
| Источник данных | Archive LCD scan from `P3-CAND-03` validation artifacts |
| Число строк | `24` |
| Число unique participants | `19` |
| Сумма | `120,822.324371792 GNK` |
| Статус суммы | Preliminary candidate amount; not approved |

## Исправление

| Исправление | Источник | Подтверждённость |
|---|---|---|
| `v0.2.13` stores one epoch snapshot of confirmable models and weight-scale factors for confirmation/reward calculations | `proposals/governance-artifacts/update-v0.2.13/README.md`; PR `#1143`; release announcement; commit `17808620` | Fix installed on-chain at block `4,267,300`; clean start epoch `277` |

PRs `#550` and `#826` are currently not treated as the fix for this candidate:
within the available local evidence they relate to settlement/claim paths, not
to confirmation-PoC weight preservation. The main fix reference for this case is
PR `#1143` / `v0.2.13`.

The `v0.2.13` devshard `MaxNonce` change is also not treated as the explanation
for this cPoC weight cut. It is a settlement nonce-limit fix; the candidate rows
here are reconstructed from PoC V2 stage commits and validation rows.

## Рабочие Действия

| Действие | Ответственный | Проверяющий | Срок | Статус |
|---|---|---|---|---|
| Build row-by-row root-cause replay from local archive artifacts | GRC validation | Назначить | 02.06.2026 | Done |
| Reconstruct submissions and validator weight from raw cPoC stage endpoints | GRC validation | Назначить | 02.06.2026 | Done |
| Review `v0.2.13` source diff for the matching confirmation-accounting fix | GRC validation | Назначить | 02.06.2026 | Done |
| Reconcile 6 simple-ratio mismatch rows against historical coefficient-adjusted formulas | GRC validation | Назначить | 02.06.2026 | 5/6 done; epoch 276 remains open |
| Replay all 24 rows through full old formula and bounded v0.2.13-style formula | GRC validation | Назначить | 02.06.2026 | Done: old `22/24`, new-style `0/24` pass alpha |
| Decide eligibility for 20 non-epoch-276 formula-reconciled single-model-pass rows | Назначить | Назначить | Назначить | Открыто |
| Check overlap with `P3-CAND-04` epoch 276 | Назначить | Назначить | Назначить | Открыто |
| Check overlap with `P4-CAND-01` Kimi restitution package | Назначить | Назначить | Назначить | Открыто |
| Decide whether this is eligible for Proposal #3 or future proposal | Coordinator / committee | Committee vote | Назначить | Открыто |

## Ссылки

- [Validation README](../validations/P3-CAND-06-pre-fix-confirmation-accounting/README.md)
- [Candidate rows CSV](../validations/P3-CAND-06-pre-fix-confirmation-accounting/candidate_rows.csv)
- [Participant epoch timeline](../validations/P3-CAND-06-pre-fix-confirmation-accounting/participant_epoch_timeline.md)
- [Grouped cPoC timeline](../validations/P3-CAND-06-pre-fix-confirmation-accounting/participant_grouped_cpoc_timeline.md)
- [Root-cause replay](../validations/P3-CAND-06-pre-fix-confirmation-accounting/case6_root_cause_replay.md)
- [Row formula replay CSV](../validations/P3-CAND-06-pre-fix-confirmation-accounting/case6_row_formula_replay.csv)
- [Submission and validator evidence](../validations/P3-CAND-06-pre-fix-confirmation-accounting/case6_submission_validator_evidence.md)
- [Fix review](../validations/P3-CAND-06-pre-fix-confirmation-accounting/case6_fix_review.md)
- [Code-diff root-cause proof](../validations/P3-CAND-06-pre-fix-confirmation-accounting/case6_code_diff_root_cause.md)
- [Coefficient replay](../validations/P3-CAND-06-pre-fix-confirmation-accounting/case6_coefficient_replay.md)
- [Full old formula replay](../validations/P3-CAND-06-pre-fix-confirmation-accounting/case6_full_old_formula_replay.md)
- [Bounded v0.2.13-style replay](../validations/P3-CAND-06-pre-fix-confirmation-accounting/case6_new_algorithm_replay.md)
- [Eligibility matrix](../validations/P3-CAND-06-pre-fix-confirmation-accounting/case6_eligibility_matrix.md)
- [Overlap matrix](../validations/P3-CAND-06-pre-fix-confirmation-accounting/case6_overlap_matrix.md)
- [Epoch 276 overlap deep dive](../validations/P3-CAND-06-pre-fix-confirmation-accounting/case6_epoch276_overlap_deep_dive.md)
- [Raw data manifest](../validations/P3-CAND-06-pre-fix-confirmation-accounting/case6_raw_data_manifest.md)
- [Overlap review](../validations/P3-CAND-06-pre-fix-confirmation-accounting/case6_overlap_review.md)
- [Source scan artifact](../validations/P3-CAND-03-failed-cpoc-epoch-267/case3_neighbor_failed_cpoc_rows.csv)
- [Pre-fix window review](../validations/P3-CAND-03-failed-cpoc-epoch-267/case3_pre_fix_window_review.md)
