# Реестр компенсационных кейсов Gonka Restitution Committee

Документ предназначен для координации расследований, проверок и подготовки компенсационных предложений. `Proposal #2` уже завершён и принят governance vote; текущая рабочая задача - сформировать состав `Proposal #3`. Подробные основания, выдержки из переписки и ссылки на расчёты находятся в досье каждого кейса.

`@OpenMindedPerson` избран координатором `Proposal #3` в переписке от 26.05.2026. Это назначение не означает автоматическое назначение ответственным за каждый кейс.

## Правила Нумерации

| Формат | Значение |
|---|---|
| `P2-CNN` | Кейс был рассмотрен в завершённом `Proposal #2`. |
| `P3-CAND-NN` | Рабочий кандидат планируемого `Proposal #3`; включение ещё должно быть подтверждено. |
| `P4-CAND-NN` | Кандидат, который обсуждается для будущего `Proposal #4`. |

После утверждения scope `Proposal #3` идентификаторы `P3-CAND-NN` должны быть заменены на финальные `P3-CNN` с одновременным переименованием досье и обновлением ссылок в этой таблице.

## Proposal #2: Завершённые Кейсы

| ID | Кейс | Статус | Эпохи | От кого поступила информация | Пострадавшие / контакт для деталей | Компенсация | Решение | Досье |
|---|---|---|---|---|---|---:|---|---|
| `P2-C01` | Inactive status mid-epoch | Отклонён | 247 | Proposal #2 report; обсуждение Votkon | 9 заявленных; contact не сопоставлен | 0 GNK | Отклонён в Proposal #2 | [досье](cases/P2-C01-inactive-status-epoch-247.md) |
| `P2-C02` | Preserver weight double-scaling / stuck 0.35x | Компенсирован | 249-253 | Proposal #2 report; Mike/Fedor в обсуждении calculation | 34 participant/node pairs; расчётный источник `GRC-e247-preserver-audit` | 30,318.50 GNK | Proposal #2 принят | [досье](cases/P2-C02-preserver-weight-double-scaling.md) |
| `P2-C03` | Epoch loss restitution | Компенсирован | 248-250 | Votkon, Mike, Fedor Tmkhv; Proposal #2 report | По подпакетам; Fedor Tmkhv по remaining-delta расчёту | 217,612.83 GNK | Proposal #2 принят | [досье](cases/P2-C03-epoch-loss-restitution.md) |
| `P2-C04` | API startup blocking issue | Компенсирован | 254 | Proposal #2 report | 14 addresses; contact не сопоставлен | 58,375.96 GNK | Proposal #2 принят | [досье](cases/P2-C04-api-startup-blocking-epoch-254.md) |

Итог по принятым компенсационным кейсам `Proposal #2`: **306,307.29 GNK**.

## Proposal #3: Рабочие Кандидаты

| ID | Кейс | Статус | Эпохи | От кого поступила информация | Пострадавшие / контакт для деталей | Investigator / результат | Validator(s) / доп. анализ | Источник расчёта | Оценка | Следующий шаг | Досье |
|---|---|---|---|---|---|---|---|---|---:|---|---|
| `P3-CAND-01` | High miss rate / devshard issue | На расследовании | 269-272, основной эпизод 272 | Votkon; технические детали от Nik | Не установлено; Nik по monitored nodes | @OpenMindedPerson; prior evidence: Fedor preliminary losses, audit confirmed chain outcome but not protocol bug | @maksimenkoff; нужны devshard data и root cause | On-chain audit; нужны devshard data | Предварительно, не утверждено | Собрать devshard proof data и определить причину | [досье](cases/P3-CAND-01-devshard-miss-rate-epochs-269-272.md) |
| `P3-CAND-02` | Negative coin balance / settle-drop | Рассчитан, требуется решение | 1-274 по расчёту | Evgenii Maksimenkov | 19 miners; Evgenii Maksimenkov | @maksimenkoff; deterministic script/result, 19 affected | @dem_ww; independent validation и scope decision | [gonkavip/unclaimed](https://github.com/gonkavip/unclaimed) | 1,075.336 GNK | Провести validation и решить включение | [досье](cases/P3-CAND-02-negative-coin-balance-settle-drop.md) |
| `P3-CAND-03` | Failed cPoC / preserved Kimi validation shortfall | Требуется решение о scope | 267 | Nik; дополнительный контекст от Votkon | `gonka1j7x...`; Nik | @mikenosov; full victim set не найден | @dem_ww; @votkon; evidence и calculation methodology | On-chain facts; нужны historical preserved-node data | Не рассчитано | Определить eligibility и данные для расчёта | [досье](cases/P3-CAND-03-failed-cpoc-preserved-kimi-epoch-267.md) |
| `P3-CAND-04` | UpgradeProtectionWindow / CPoC misfire | Рассчитан, требуется решение | 276 | Votkon; расчёт от Evgenii Maksimenkov | 19 miners; Evgenii Maksimenkov | @maksimenkoff; calculation published, Nik prior script result confirmed | @votkon; @OpenMindedPerson; independent validation и inclusion decision | [gonkavip/payout276](https://github.com/gonkavip/payout276) | 36,209.451 GNK | Провести финальную validation | [досье](cases/P3-CAND-04-upgrade-protection-cpoc-misfire-epoch-276.md) |
| `P4-CAND-01` | Kimi restitution / CPoC, nonce exclusion, ComputeGroupCap | Рассчитан; обсуждается eligibility в GRC | 265-276 | Votkon | 52 unique addresses; Votkon | @votkon; calculation completed, 710,772.72 GNK | @maksimenkoff; @mikenosov; validation и eligibility decision | [votkon/gonka-kimi-restitution](https://github.com/votkon/gonka-kimi-restitution) | 710,772.72 GNK | Выполнить validations и решить eligibility в GRC | [досье](cases/P4-CAND-01-kimi-restitution-epochs-265-276.md) |

## Other Candidates

| ID | Кейс | Статус | Эпохи | От кого поступила информация | Пострадавшие / контакт для деталей | Кто уже исследовал / результат | Нужен доп. анализ | Оценка | Следующий шаг | Досье |
|---|---|---|---|---|---|---|---|---:|---|---|
| `P3-CAND-05` | `ml3` hardware re-registration | Требуется решение о scope; не входит в текущие пять назначенных кейсов Proposal #3 | Около 269 | SegovChik от `@gonkstein` и его technical contact | `gonka15munk...`; `@gonkstein` через SegovChik | Arturs: on-chain HW proof отсутствует, noted preserved-node behavior | Да: сначала scope/policy decision | Не рассчитано | Решить, является ли это protocol issue | [досье](cases/P3-CAND-05-ml3-hardware-reregistration.md) |
| `P3-CAND-06` | Pre-fix confirmation accounting / pass-weight but failed ratio | Требуется root-cause и eligibility review; не включать автоматически в Case 3 | 263-276 | Выявлено при validation `P3-CAND-03` | 19 unique participants / 24 epoch rows; contacts не сопоставлены | @mikenosov: archive scan `262..276`, выделен отдельный candidate set | Да: formula replay, overlap checks with `P3-CAND-04` and `P4-CAND-01` | 120,822.324 GNK preliminary | Провести отдельный root-cause review и решить scope | [досье](cases/P3-CAND-06-pre-fix-confirmation-accounting.md) |

## Легенда Статусов

| Статус | Значение |
|---|---|
| `Отклонён` | Исследование завершено, выплаты по кейсу не приняты. |
| `Компенсирован` | Кейс включён в принятое governance proposal. |
| `Рассчитан, требуется решение` | Сумма рассчитана, но committee scope и/или validation ещё не завершены. |
| `На расследовании` | Причина и eligibility ещё устанавливаются. |
| `Требуется решение о scope` | Факты заявки известны, но не решено, относится ли случай к компенсационному процессу GRC. |

## Открытые Назначения Proposal #3

| Кейс | Требуется |
|---|---|
| `P3-CAND-01` | @OpenMindedPerson investigates; @maksimenkoff validates; нужны devshard proof data и root cause. |
| `P3-CAND-02` | @maksimenkoff investigates; @dem_ww validates; нужно решение о включении. |
| `P3-CAND-03` | @mikenosov investigates; @dem_ww и @votkon validate; нужны victim set и methodology. |
| `P3-CAND-04` | @maksimenkoff investigates; @votkon и @OpenMindedPerson validate; нужна финальная validation. |
| `P4-CAND-01` | @votkon investigates; @maksimenkoff и @mikenosov validate; нужны validation и eligibility decision. |
| `P3-CAND-06` | Назначить investigator/validators; нужны row-by-row formula replay и overlap checks. |

## Правила Обновления

1. Любое новое утверждение о причине, количестве пострадавших, сумме, исправлении или решении сначала фиксируется в соответствующем досье вместе с источником.
2. В реестр переносится только краткий итог из досье.
3. Сумма из расчётного репозитория считается `рассчитанной`, но не `принятой`, пока нет итогового governance decision.
4. Для отсутствующих назначений, сроков и доказательств используется явная отметка `Назначить`, `Не рассчитано`, `Не установлено` или `Требует подтверждения`.
