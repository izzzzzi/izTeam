# Arena Plugin

Дебаты экспертов с конвергенцией на решении. Версия: 1.1.7.

## Скилл: /arena

**Аргумент:** `<вопрос для дебатов>`

Работает для любого домена: разработка, продукт, стратегия, бизнес, наука, философия.

### Фазы

#### Phase 0: Question Analysis & Expert Selection

1. Определить домен(ы), тип решения, ставки
2. Выбрать 3-5 экспертов (стремиться к 5)
3. Назначить Devil's Advocate (право VETO)
4. Презентовать арену пользователю

**Критерии выбора:** разнообразие углов зрения, реальные персоны, anti-groupthink.

#### Phase 1: Research (one-shot agents)

2-4 `arena:researcher` агента параллельно:
- Код: архитектура + best practices + constraints
- Non-tech: данные/тренды + позиции экспертов + кейсы
- Mixed: комбинация

#### Phase 2: Launching the Arena

1. Компиляция briefing из findings
2. TeamCreate("arena-<topic-slug>")
3. Запуск ВСЕХ экспертов параллельно одним сообщением

**Ключевой принцип:** эксперты общаются напрямую через SendMessage. Модератор НЕ ретранслирует сообщения.

**Evidence Rules** (включаются в init prompt каждого эксперта):
- Каждый аргумент MUST cite evidence с R (reliability) и CL (congruence) рейтингами
- Эксперт может challenge R/CL рейтинги другого эксперта с justification
- Финальная позиция MUST include evidence summary table с WLNK trust score

#### Phase 3: Observing the Debates

Эксперты автономно:
1. Broadcast initial positions **с evidence (R/CL рейтинги)**
2. Challenge — аргументы **и evidence ratings** других экспертов
3. Respond — защита или корректировка evidence scores
4. Shift positions при убедительном evidence
5. Signal convergence (финальная позиция + evidence summary table → team-lead)

**Интервенции модератора:**
- Эксперт молчит → nudge
- Уход от темы → redirect broadcast
- Два эксперта в loop → привлечь третьего
- Нет прогресса → запрос interim summary
- >15 минут → timeout, запрос финальных позиций

**Live Commentary** — реалтайм комментарии для пользователя при значимых событиях.

#### Phase 4: Convergence

- 3+ из N экспертов подали финальные позиции → проверка VETO → synthesis
- VETO активен → broadcast VETO, ждать ответы
- >20 минут → timeout broadcast → synthesis

#### Phase 5: Synthesis

1. **Consolidate Evidence** (новый обязательный шаг перед документом):
   - Собрать все evidence tables из финальных позиций экспертов
   - De-duplicate evidence, процитированное несколькими экспертами
   - Resolve contested R/CL рейтинги (использовать лучше обоснованный)
   - Вычислить WLNK trust per position: `Trust = min(evidence_scores)`
   - Назначить assurance levels: L2 (Trust >= 0.7), L1 (0.4-0.7), L0 (< 0.4)
2. Создать документ по шаблону `references/synthesis-template.md`
3. Сохранение в `docs/arena/YYYY-MM-DD-[topic].md`
4. Shutdown команды (SendMessage shutdown → TeamDelete)

### Evidence-Driven Debate Protocol

#### Evidence Rating Scales

**Reliability (R: 0.0-1.0):**

| Source Type | Base R |
|------------|--------|
| Official docs / benchmarks | 0.9 |
| Peer-reviewed / reputable blog | 0.8 |
| Production case study | 0.8 |
| Community benchmark | 0.7 |
| SO / forum consensus | 0.5 |
| Single blog post | 0.4 |
| Own experience / inferred | 0.3 |

**Congruence (CL: 0.0-1.0):**

| Context Match | CL |
|--------------|-----|
| Exact context | 1.0 |
| Similar context | 0.7 |
| Related context | 0.5 |
| Loosely related | 0.3 |

**Trust formula (WLNK):**
```
evidence_score = R × (1 - max(0, 0.5 - CL))
Trust(position) = min(evidence_scores)
```

#### Evidence Challenge Mechanism

Эксперт может оспорить R/CL рейтинг другого эксперта:
- Указать конкретный evidence и спорный рейтинг
- Предоставить justification для альтернативного рейтинга
- Оспоренный эксперт должен защитить или скорректировать

#### Assurance Levels

| Level | Название | Критерий |
|-------|----------|----------|
| L0 | Observation | Trust < 0.4 или opinions без strong evidence |
| L1 | Reasoned | Логически consistent, Trust 0.4-0.7 |
| L2 | Verified | Trust >= 0.7, подтверждено strong evidence |

### Synthesis Document Structure

Шаблон `references/synthesis-template.md` включает:
- **Trust Summary** — таблица: позиция, чемпион, assurance level, WLNK trust, кол-во evidence
- **Evidence Catalog** — все процитированные evidence consolidated и de-duplicated
- **Contested Evidence Resolution** — таблица спорных R/CL рейтингов и их разрешение
- **Debate Progression** — с direct challenges и position shifts
- **Trade-offs Accepted** — принятые компромиссы
- Arena Question, Expert Panel, Key Positions, Convergence Points, Open Disagreements, Recommendation

## Агенты

### arena:expert

Реальная экспертная персона:
- Документированные viewpoints
- Прямые дебаты через SendMessage
- Право VETO (Devil's Advocate)
- **Evidence citation обязательна** — каждый аргумент с R/CL рейтингами
- **Challenge mechanism** — право оспорить R/CL рейтинги других
- **Финальная позиция** включает evidence summary table с WLNK trust
- Имена: kebab-case (`martin-fowler`, `dhh`)

### arena:researcher

One-shot сбор контекста:
- 2-4 агента параллельно
- Code/non-tech/mixed фокус
- WebSearch для внешних данных

## References

- `expert-selection-guide.md` — критерии и шаблон панели
- `live-commentary-rules.md` — протокол комментариев
- `synthesis-template.md` — шаблон итогового документа (с Trust Summary, Evidence Catalog, Contested Evidence Resolution)
- `evidence-scoring.md` — протокол evidence rating (R/CL scales, WLNK formula)
