# Reason Plugin

Hypothesis-driven reasoning через ADI-цикл с evidence gathering и WLNK trust scoring. Версия: 0.1.0.

## Скилл: /reason

**Аргумент:** `<decision question — e.g. 'which database for the new service'>`

Работает для архитектурных решений, выбора технологий, trade-off анализа — любого вопроса, где важно "почему именно это, а не то".

### Философия

- Каждое архитектурное решение заслуживает **why**, а не только **what**
- Конкурирующие гипотезы предотвращают confirmation bias
- Evidence имеет source и expiration — не все доказательства равны
- Trust вычисляется по слабейшему звену (WLNK), а не по среднему
- Человек решает; фреймворк обеспечивает информированность решения

### Фазы

#### Phase 0: Question Framing

1. Определить Bounded Context (часть системы), Decision Type (tech/architecture/trade-off/process), Constraints (время, бюджет, команда, стек), Stakes (последствия неправильного выбора)
2. Представить пользователю структурированную таблицу framing

#### Phase 1: Abduction (Hypothesize)

Запуск 3-5 `reason:hypothesizer` агентов **IN PARALLEL** в одном сообщении. Каждый генерирует ОДНУ гипотезу с определённого угла.

**Стратегия назначения углов по типу решения:**

| Decision Type | Angles |
|--------------|--------|
| Tech choice | performance, DX, ecosystem, maintenance cost, migration risk |
| Architecture | simplicity, scalability, team familiarity, operational cost, flexibility |
| Trade-off | short-term win, long-term win, risk-minimizing, innovation, pragmatic |
| Process | speed, quality, team autonomy, compliance, simplicity |

Все гипотезы начинают на **Assurance Level L0 (Observation)**.

**Error handling:** минимум 3 гипотезы обязательны. Меньше — report failure.

#### Phase 2: Deduction (Verify)

Запуск `reason:verifier` агентов **IN PARALLEL** — один на гипотезу. Проверка внутренней консистентности, совместимости с constraints, известных failure modes. **Без эмпирических данных** — только логика.

**Обновление assurance levels:**
- PASS → **L1 (Reasoned)**
- FAIL → **Invalid** (сохраняется для записи)
- PARTIAL → остаётся **L0** с отмеченными concerns

Если ВСЕ гипотезы Invalid → возврат к Phase 1 с расширенными углами. Максимум 1 retry.

#### Phase 3: Induction (Validate)

Запуск `reason:evidence-gatherer` агентов **IN PARALLEL** — один на выжившую гипотезу (L0 или L1).

Каждый evidence имеет рейтинг:
- **R (Reliability: 0.0-1.0)** — надёжность источника
- **CL (Congruence: 0.0-1.0)** — релевантность контексту

**Trust formula (WLNK):**
```
Trust(hypothesis) = min(evidence_scores)
evidence_score = R × (1 - max(0, 0.5 - CL))
```

**Обновление assurance levels:**
- L1 + Trust >= 0.7 → **L2 (Verified)**
- L1 + 0.4 <= Trust < 0.7 → остаётся **L1**
- L1 + Trust < 0.4 → downgrade до **L0**

#### Phase 4: Decision & DRR

1. Ранжирование гипотез по Trust score
2. Генерация Design Rationale Record по шаблону `references/drr-template.md`
3. Сохранение в `docs/decisions/YYYY-MM-DD-[topic-slug]-drr.md`
4. Отчёт пользователю: победитель, уровень, trust, напоминание что "AI recommends — human decides"

### Assurance Levels

| Level | Название | Значение | Критерий |
|-------|----------|----------|----------|
| L0 | Observation | Непроверенное наблюдение | Начальное состояние |
| L1 | Reasoned | Прошло логическую проверку | PASS в Phase 2 |
| L2 | Verified | Подтверждено evidence | L1 + Trust >= 0.7 |

### Evidence Rating Scales

**Reliability (R):**

| Source Type | Base R |
|------------|--------|
| Official benchmarks / docs | 0.9 |
| Peer-reviewed / reputable tech blog | 0.8 |
| Production case study (named company) | 0.8 |
| Community benchmark (reproducible) | 0.7 |
| Stack Overflow / forum consensus | 0.5 |
| Single blog post / opinion | 0.4 |
| Inferred from general knowledge | 0.3 |

**Congruence (CL):**

| Context Match | CL |
|--------------|-----|
| Exact same context (stack, scale, constraints) | 1.0 |
| Similar context (same domain, comparable scale) | 0.7 |
| Related context (same technology, different domain) | 0.5 |
| Loosely related (general principle, different stack) | 0.3 |
| Tangential (different domain and stack) | 0.1 |

Evidence без источника автоматически маркируется `[INFERRED]` с R=0.3.

### DRR (Design Rationale Record)

Итоговый артефакт, включающий:
- Decision Question + Constraints
- Все гипотезы (включая Invalid — знать что отвергнуто ценно)
- Evidence Catalog с R/CL рейтингами
- Trust Summary (WLNK)
- Решение с comparative reasoning (почему X, а не Y)
- Trade-offs Accepted + Mitigation Plan
- Decision Owner: [human]

Шаблон: `references/drr-template.md`

## Агенты (3)

### reason:hypothesizer

Генерирует одну обоснованную гипотезу с назначенного угла:
- Изучает проект (Glob, Grep, Read) для grounding
- Внешний контекст (WebSearch, Context7, Tavily при наличии)
- Falsifiable core claim обязателен
- One-shot агент, Opus
- **Запрещённые tools:** Edit, Write, Bash (read-only исследование)

### reason:verifier

Логическая верификация гипотезы:
- Consistency check (внутренние противоречия)
- Constraint compatibility (реальное состояние проекта)
- Logic soundness (fallacies, assumptions)
- Known failure modes (domain knowledge)
- Comparison с другими гипотезами
- Verdict: PASS / FAIL / PARTIAL
- One-shot агент, Opus
- **Запрещённые tools:** Edit, Write, Bash

### reason:evidence-gatherer

Сбор эмпирических доказательств:
- Project-internal evidence (код, тесты, конфиги)
- Documentation evidence (Context7, DeepWiki)
- External evidence (Tavily, Exa, WebSearch, WebFetch)
- **Обязательный** поиск counter-evidence (against hypothesis)
- R/CL рейтинг каждого evidence с justification
- WLNK trust computation
- Aim: 3-7 pieces of evidence (quality over quantity)
- One-shot агент, Opus
- **Запрещённые tools:** Edit, Write, Bash

## References

- `drr-template.md` — шаблон Design Rationale Record
- `fpf-distillate.md` — дистиллят First Principles Framework

## Ключевые правила

1. Lead оркестрирует — никогда не генерирует гипотезы или evidence сам
2. Минимум 3 гипотезы, максимум 5
3. Invalid гипотезы СОХРАНЯЮТСЯ в DRR
4. Trust = WLNK (weakest link) — одно плохое evidence тянет вниз весь score
5. DRR всегда завершается "Decision Owner: [human]" — AI рекомендует, человек решает
6. Evidence без sources → [INFERRED], R=0.3
7. Диаграммы: mermaid `flowchart TD`, не ASCII art
