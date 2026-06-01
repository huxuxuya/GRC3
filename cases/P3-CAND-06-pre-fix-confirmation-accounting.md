# P3-CAND-06: Pre-Fix Confirmation Accounting / Pass-Weight But Failed Ratio

[Назад к реестру](../compensation_cases_registry.md)

## Карточка

| Поле | Значение |
|---|---|
| Proposal | Кандидат Proposal #3 |
| Статус | Требуется root-cause и eligibility review |
| Эпохи | 263-276 |
| От кого поступила информация | Выявлено при независимой validation `P3-CAND-03` |
| Пострадавший / контакт для деталей | 19 unique participants из archive scan; contacts не сопоставлены |
| Кто уже исследовал / результат | @mikenosov; расширенный scan epochs `262..276`, выделено `24` candidate rows |
| Нужен дополнительный анализ | Да: row-by-row formula replay и overlap checks |
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
- The fixing upgrade is `v0.2.13` / PR `#1143` / commit `17808620`.

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

- Need to replay each row through the historical `foldEventReadings` formula,
  using coefficient-adjusted PoC node readings, not only model voting power.
- Need to determine whether a single-model `pass_weight` should have prevented
  the final confirmation ratio collapse for each participant.
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
| `v0.2.13` stores one epoch snapshot of confirmable models and weight-scale factors for confirmation/reward calculations | `proposals/governance-artifacts/update-v0.2.13/README.md`; PR `#1143`; commit `17808620` | Fix installed on-chain at block `4,267,300`; clean start epoch `277` |

## Рабочие Действия

| Действие | Ответственный | Проверяющий | Срок | Статус |
|---|---|---|---|---|
| Reconcile all 24 rows against historical chain formulas | Назначить | Назначить | Назначить | Открыто |
| Check overlap with `P3-CAND-04` epoch 276 | Назначить | Назначить | Назначить | Открыто |
| Check overlap with `P4-CAND-01` Kimi restitution package | Назначить | Назначить | Назначить | Открыто |
| Decide whether this is eligible for Proposal #3 or future proposal | Coordinator / committee | Committee vote | Назначить | Открыто |

## Ссылки

- [Validation README](../validations/P3-CAND-06-pre-fix-confirmation-accounting/README.md)
- [Candidate rows CSV](../validations/P3-CAND-06-pre-fix-confirmation-accounting/candidate_rows.csv)
- [Participant epoch timeline](../validations/P3-CAND-06-pre-fix-confirmation-accounting/participant_epoch_timeline.md)
- [Grouped cPoC timeline](../validations/P3-CAND-06-pre-fix-confirmation-accounting/participant_grouped_cpoc_timeline.md)
- [Source scan artifact](../validations/P3-CAND-03-failed-cpoc-epoch-267/case3_neighbor_failed_cpoc_rows.csv)
- [Pre-fix window review](../validations/P3-CAND-03-failed-cpoc-epoch-267/case3_pre_fix_window_review.md)
