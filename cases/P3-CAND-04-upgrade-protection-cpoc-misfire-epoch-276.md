# P3-CAND-04: UpgradeProtectionWindow / CPoC Misfire

[Назад к реестру](../compensation_cases_registry.md)

## Карточка

| Поле | Значение |
|---|---|
| Proposal | Кандидат Proposal #3 |
| Статус | Независимо провалидирован, root cause подтверждён, требуется решение |
| Эпохи | 276 |
| От кого поступила информация | Votkon; расчёт подготовил Evgenii Maksimenkov |
| Пострадавший / контакт для деталей | 19 miners из payout list; Evgenii Maksimenkov |
| Кто уже исследовал / результат | @maksimenkoff; calculation: [gonkavip/payout276](https://github.com/gonkavip/payout276); Nik сообщил о совпавшем script run; GRC independent validation matched published CSV exactly and confirmed historical `LastUpgradeHeight = null` |
| Нужен дополнительный анализ | Да: решение о включении и duplicate-overlap handling |
| Investigator | @maksimenkoff |
| Validators | @votkon; @OpenMindedPerson |
| Срок | Назначить |
| Пострадавшие | 19 miners: 7 dropped, 12 reduced confirmation weight |
| Оценка компенсации | 36,209.451291351 GNK |
| Решение / голосование | Включение не принято |

## Краткое Описание

После апгрейда v0.2.13 в epoch 276 ожидаемое protection window не предотвратило последующие cPoC rounds. Независимая archive-chain validation подтвердила, что post-upgrade cPoC triggers `4267778` и `4270605` произошли внутри epoch `276`; семь active-before participants выпали из выплат, а ещё двенадцать потеряли часть `confirmation_weight`.

Root cause теперь подтверждён не только перепиской: прямой `abci_query` state key `0x1b` / `LastUpgradeHeight` вернул `null` на heights `4267299`, `4267300`, `4267778`, `4270605`, `4274661` и на latest checked height. Это объясняет, почему cPoC skip после upgrade не сработал.

## Почему Кейс Отнесён К Этому Proposal

Кейс появился в период координации Proposal #3 и представляет отдельную проблему от Kimi e265-e276. Votkon прямо указал, что из того же периода существует ещё один case, который GRC должен рассмотреть отдельно.

## Хронология

| Дата и время | Автор | Событие | Что подтверждает |
|---|---|---|---|
| 26.05.2026 21:54:54 UTC+03:00 | Votkon | Описана проблема `LastUpgradeHeight` и stale scales | Root-cause statement для расследования |
| 27.05.2026 06:18:41 UTC+03:00 | Evgenii Maksimenkov | Сообщено о 7 dropped participants и вопросе о reduced weight | Определение scope расчёта |
| 27.05.2026 10:12:47 UTC+03:00 | Evgenii Maksimenkov | Представлен script и total compensation | Рассчитанная сумма |
| 27.05.2026 12:09:27 UTC+03:00 | Nik | Сообщено о запуске script и совпадении результата | Первичный verification run |

## Цитаты Из Переписки И Объяснение

> "после v0.2.13 в state не записался LastUpgradeHeight, поэтому проверка перед запуском cPoC не увидела недавний апгрейд и не пропустила его."

Атрибуция: Votkon, 26.05.2026 21:54:54 UTC+03:00, `message522`.
Значение: формулирует предполагаемую root cause и проверяемое on-chain состояние.

> "As a result of the upgrade bug, 7 participants were affected and dropped out during the following two cPoC rounds."

Атрибуция: Evgenii Maksimenkov, 27.05.2026 06:18:41 UTC+03:00, `message523`.
Значение: фиксирует первоначально выявленную dropped группу и вопрос расширения scope на partial weight losses.

> "The resulting compensation amount comes to 36,209 GNK in total."

Атрибуция: Evgenii Maksimenkov, 27.05.2026 10:12:47 UTC+03:00, `message528`.
Значение: подтверждает публикацию расчёта; точная сумма уточнена README calculation repository.

## Подтверждённые Факты

- Independent validation определяет `19 miners`, включая `7` dropped и `12` с reduced confirmation weight.
- Total compensation: `36,209.451291351 GNK`; generated CSV matches `gonkavip/payout276` exactly.
- Calculation использует standard on-chain endpoints и historical snapshots at block heights `4267299` and `4274661`.
- Replay confirms `54` epoch members, `46` `ACTIVE`-before epoch-group members, `714732` `total_cw_after`, `133526` eligible lost cw, and `193,820.331174280 GNK` total rewarded in epoch `276`.
- Direct state proof confirms `LastUpgradeHeight` key `0x1b` was `null` at upgrade height and both post-upgrade cPoC trigger heights.
- Scope scan `270..283` finds only `2` case4-like cPoC rows: `4267778` and `4270605`, both post-upgrade and still inside the epoch `276` upgrade window.
- The error is limited to epoch `276` because upgrade block `4267300` lands inside epoch `276` (`4259271..4275061`); epochs before are pre-upgrade controls, and epoch `277+` are later clean epochs rather than the same upgrade-epoch misfire.
- Code fix identified in PR [#1268](https://github.com/gonka-ai/gonka/pull/1268), merged to branch `upgrade-v0.2.14`: future full upgrades record `LastUpgradeHeight` from the upgrade handler and tests cover full/partial upgrade tracking. Public release/deployment still needs separate confirmation.
- Published README says `47` `ACTIVE` before upgrade, but the published CSV row set and amounts match the independent replay exactly.
- Logs и third-party indexers для воспроизведения расчёта не требуются.
- Nik сообщил об успешном запуске script с совпадающим результатом.

## Гипотезы И Пробелы В Данных

- Нужно проверить duplicate-payment overlap с P4-CAND-01 перед выплатой.
- Требуется решение, включать ли этот отдельный case в Proposal #3.

## Расчёт Компенсации

| Элемент | Значение / источник |
|---|---|
| Методика | `lost_cw * total_rewarded // total_cw_after` для active-before participants |
| Источник данных | Archive node snapshots `epoch_group_data`, `participant`, `epoch_performance_summary` |
| Расчётный репозиторий | [gonkavip/payout276](https://github.com/gonkavip/payout276) |
| Число пострадавших | 19 miners |
| Сумма | 36,209.451291351 GNK |
| Статус суммы | Независимо пересчитано по archive-chain state; не утверждено governance |

## Independent Validation

| Artifact | Result |
|---|---|
| [Validation README](../validations/P3-CAND-04-upgrade-protection-cpoc-misfire-epoch-276/README.md) | Summary and reproduction notes |
| [Compensation replay](../validations/P3-CAND-04-upgrade-protection-cpoc-misfire-epoch-276/case4_compensation_replay.md) | `19` rows, `36,209.451291351 GNK` |
| [Upgrade/cPoC timeline](../validations/P3-CAND-04-upgrade-protection-cpoc-misfire-epoch-276/case4_epoch276_timeline.md) | post-upgrade cPoCs at `4267778` and `4270605` |
| [Root-cause deep dive](../validations/P3-CAND-04-upgrade-protection-cpoc-misfire-epoch-276/case4_root_cause_deep_dive.md) | historical `LastUpgradeHeight = null` proof and why only epoch `276` |
| [Scope control scan](../validations/P3-CAND-04-upgrade-protection-cpoc-misfire-epoch-276/case4_scope_control_scan.md) | epochs `270..283`; only two case4-like rows, both in epoch `276` |
| [Completeness matrix](../validations/P3-CAND-04-upgrade-protection-cpoc-misfire-epoch-276/case4_completeness_matrix.md) | all `54` members accounted for; exactly `19` eligible affected rows |
| [Overlap matrix](../validations/P3-CAND-04-upgrade-protection-cpoc-misfire-epoch-276/case4_overlap_matrix.md) | flags same-address overlap review with local candidates |
| [Published compare](../validations/P3-CAND-04-upgrade-protection-cpoc-misfire-epoch-276/case4_published_compare.md) | exact match with published CSV |

## Исправление

| Исправление | Источник | Подтверждённость |
|---|---|---|
| Intended `UpgradeProtectionWindow` в v0.2.13 | [payout276 README](https://github.com/gonkavip/payout276) | Подтверждает ожидаемое поведение и misfire |
| Expected skip behavior | [PR #1143](https://github.com/gonka-ai/gonka/pull/1143) and Gonka release announcement | cPoC should be skipped from upgrade height through the upgrade epoch |
| `LastUpgradeHeight` failure | Direct chain state query and DevOps evidence | Confirmed: key `0x1b` was `null`, so skip could not detect the recent upgrade |
| Финальный code fix misfire | [PR #1268](https://github.com/gonka-ai/gonka/pull/1268), branch `upgrade-v0.2.14` | Code fix identified: records `LastUpgradeHeight` from upgrade handler and adds tests; on-chain deployment requires separate confirmation |

## Рабочие Действия

| Действие | Ответственный | Проверяющий | Срок | Статус |
|---|---|---|---|---|
| Воспроизвести CSV на committee archive node | GRC validation | @votkon; @OpenMindedPerson | 02.06.2026 | Done: exact CSV match |
| Validate eligibility для dropped и reduced rows | GRC validation | @votkon; @OpenMindedPerson | 02.06.2026 | Done: `status_before == ACTIVE`, `7` dropped, `12` reduced |
| Проверить duplicate overlap перед выплатой | Назначить | Назначить | Назначить | Открыто |
| Принять решение о включении в Proposal #3 | Координатор Proposal #3 | Committee vote | Назначить | Открыто |

## Ссылки

- [Calculation repository: gonkavip/payout276](https://github.com/gonkavip/payout276)
- [Proposal #54 referenced by calculation report](https://gonka.gg/network/proposals/54)
