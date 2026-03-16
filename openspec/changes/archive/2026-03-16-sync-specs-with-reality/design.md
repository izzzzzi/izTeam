## Context

OpenSpec спеки — источник истины для архитектуры плагинов izTeam. Сейчас 5 плагинов реализованы (team v0.3.9, think v1.1.7, arena v1.1.7, audit v0.1.14, reason v0.1.0), но спеки описывают только 4. Arena спек не включает evidence-driven систему, добавленную в последних изменениях. Team спек неполон.

Все изменения — **документационные**: код уже реализован, спеки нужно привести в соответствие.

## Goals / Non-Goals

**Goals:**
- Создать спек `reason-plugin` — полное описание ADI-цикла, 3 агентов, DRR-артефакта, WLNK trust
- Обновить спек `arena-plugin` — evidence-driven дебаты, R/CL рейтинги, assurance levels, обновлённый synthesis
- Обновить спек `team-plugin` — git checkpoint mode, project profile, недостающие references
- Обновить спек `marketplace` — 5 плагинов, команда `/reason`
- Обновить `config.yaml` — актуальное описание проекта

**Non-Goals:**
- Изменение кода плагинов
- Shared спека для evidence scoring (arena и reason используют по-разному)
- Обновление CI/CD (auto-version.yml для reason — отдельный change)
- Обновление спеков think и audit (нет расхождений)

## Decisions

### 1. Reason спек создаётся по образцу think/arena спеков

**Rationale:** Единообразие структуры (скиллы → фазы, агенты → таблицы, references → список). Think и arena уже задают этот паттерн.

**Alternative:** Создать более формальную спеку с отдельными секциями для trust model — отвергнуто, т.к. trust model неразрывно связана с фазами ADI.

### 2. Evidence scoring описывается в спеках arena и reason по отдельности

**Rationale:** Хотя формулы похожи (WLNK, R/CL), контексты использования разные: arena — дебаты между экспертами с challenge mechanism, reason — верификация гипотез. Shared спек создал бы связанность без реальной пользы.

### 3. Обновление спеков идёт через delta specs в change

**Rationale:** OpenSpec архитектура: delta specs (ADDED/MODIFIED) в change, при archive мержатся в основные спеки. Это даёт ревью до применения.

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| Спеки могут устареть снова при следующих изменениях кода | Добавить в conventions напоминание обновлять спеки при изменении плагинов |
| Delta specs могут быть неполными | Каждый MODIFIED requirement включает полный обновлённый текст |
| config.yaml context описывает 4 плагина — другие инструменты могут использовать этот контекст | Обновить сразу при apply |

## Совместимость версий

Изменение **не влияет** на код плагинов. Все плагины сохраняют текущие версии:
- team v0.3.9, think v1.1.7, arena v1.1.7, audit v0.1.14, reason v0.1.0
