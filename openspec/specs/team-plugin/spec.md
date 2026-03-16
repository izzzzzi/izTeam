# Team Plugin

Мульти-агентная реализация фич с ревью-гейтами. Версия: 0.3.9.

## Скиллы

### /build — основной пайплайн

**Аргументы:** `<description | path/to/plan.md> [--coders=N] [--no-research] [--fresh] [--git-checkpoints]`

#### Фазы

**Phase 1: Discovery, Planning & Setup**

1. Quick orientation — CLAUDE.md, Glob, .conventions/, .project-profile.yml, .repo-map
2. Dispatch researchers (conditional) — адаптивный: пропускает известное, исследует неизвестное
3. Classify complexity (SIMPLE / MEDIUM / COMPLEX) + synthesize plan
4. Tech Lead validation (MEDIUM/COMPLEX only)
5. Spawn team + state handoff

**Phase 2: Monitor Mode**

- Lead принимает решения, Supervisor оркестрирует
- Escalation contract через Supervisor → Lead
- Coder-ы отправляют на ревью напрямую (Lead не в цикле ревью)

**Phase 3: Completion & Verification**

1. Integration verification (build + tests)
2. Conventions update (обязательная задача)
3. Tech Lead consistency check (MEDIUM/COMPLEX)
4. Teardown FSM
5. Summary report

#### Классификация сложности

| Уровень | Критерии | Команда |
|---------|----------|---------|
| SIMPLE | 1-3 файла, один слой, знакомый паттерн | unified-reviewer |
| MEDIUM | 4-10 файлов, 2+ слоя, новые паттерны | security + logic + quality reviewers |
| COMPLEX | 10+ файлов, архитектурные решения, незнакомый домен | то же + staged research, risk analysis |

#### Git Mode

| Mode | Поведение |
|------|-----------|
| standard (default) | Один коммит после всех апрувов |
| checkpoint (`--git-checkpoints`) | WIP коммиты: pre-review → review fixes → final |

В checkpoint mode коммиты создаются на трёх этапах:
1. **pre-review** — после завершения реализации, до ревью
2. **review fixes** — после применения замечаний ревьюеров
3. **final** — финальный коммит после всех апрувов

#### Repo Map

- Скрипт: `skills/build/scripts/repo-map.py` (Python 3)
- Генерирует `.repo-map` — ранжированную карту символов кодовой базы
- Кэшируется 24h, обновляется при новых коммитах или `--fresh`
- Используется в Phase 1 для ориентации Lead без чтения каждого файла

#### Project Profile

- Файл: `.project-profile.yml` — machine-readable профиль проекта
- Генерируется через `/conventions` при анализе кодовой базы
- Используется `/build` в Phase 1 для cold-start оптимизации (пропуск redundant orientation)
- Содержит: стек, структуру, ключевые паттерны, зависимости

### /brief — интервью перед сборкой

Структурированный диалог для уточнения скоупа перед `/build`.

### /conventions — извлечение конвенций

Создаёт `.conventions/` с gold-standards, anti-patterns, checks из анализа кодовой базы.
Также генерирует `.project-profile.yml` для cold-start оптимизации.
Адаптивный dispatch researchers — пропускает известное, исследует неизвестное.

## Агенты (10)

### Постоянные (lifetime = session)

| Агент | Роль |
|-------|------|
| supervisor | Операционный мониторинг, liveness, loop detection, state.md, teardown |
| tech-lead | Валидация плана, архитектурное ревью, DECISIONS.md |

### Ревьюеры

| Агент | Когда | Фокус |
|-------|-------|-------|
| unified-reviewer | SIMPLE | Единое ревью |
| security-reviewer | MEDIUM/COMPLEX | Безопасность |
| logic-reviewer | MEDIUM/COMPLEX | Корректность логики |
| quality-reviewer | MEDIUM/COMPLEX | Качество кода |

### One-shot / Temporary

| Агент | Роль |
|-------|------|
| codebase-researcher | Изучение структуры проекта |
| reference-researcher | Поиск лучших практик и примеров |
| coder | Реализация задач (per-task, self-check → review → fix → commit) |
| risk-tester | Верификация архитектурных рисков |

## Ключевые принципы

- **Полная автономия** — Lead никогда не спрашивает пользователя
- **Защита контекста Lead** — dispatch researchers, не читать файлы напрямую
- **Gold standards в каждом промпте coder-а** — главный рычаг качества
- **Coders drive review** — прямой SendMessage к ревьюерам
- **State file для resilience** — Supervisor обновляет state.md после каждого события

## References

### Plugin-level (`plugins/team/references/`)

- `gold-standard-template.md` — шаблон gold-standard примеров
- `reviewer-protocol.md` — стандарты ревью
- `risk-testing-example.md` — пример тестирования рисков
- `status-icons.md` — иконки статуса для state reporting
- `supervisor-playbooks.md` — операционные плейбуки

### Build skill (`plugins/team/skills/build/references/`)

- `complexity-classification.md` — дерево решений для сложности
- `risk-analysis-protocol.md` — протокол анализа рисков
- `state-ownership.md` — контракт владения состоянием
- `state-template.md` — шаблон файла состояния
- `summary-report-template.md` — шаблон итогового отчёта
- `teardown-fsm.md` — детерминистический shutdown

### Brief skill (`plugins/team/skills/brief/references/`)

- `brief-template.md` — шаблон брифа
- `interview-principles.md` — принципы интервью
