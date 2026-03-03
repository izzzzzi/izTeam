<p align="right"><a href="./README.md">English</a> | <strong>Русский</strong></p>

# Team

Реализуйте фичи с командой AI-агентов и встроенными review-gates.

## Требования

> **Agent Teams экспериментальны и по умолчанию выключены.** Перед использованием плагина их нужно включить.

Добавьте `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` в `settings.json` или окружение:

```json
// ~/.claude/settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Или задайте переменную окружения:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

После включения перезапустите Claude Code.

## Установка

```bash
/plugin marketplace add izzzzzi/izTeam
/plugin install team@izteam
```

## Использование

```
/build <описание или путь/к/плану.md> [--coders=N]
/brief <описание> — сначала интервью, потом сборка
/conventions [путь/к/проекту]
```

**Примеры:**
```
/build "Добавить страницу настроек пользователя с редактированием профиля"
/build docs/plan.md --coders=2
/brief "Добавить уведомления"
/conventions
```

## Как это работает

### /build

Team Lead оркестрирует полный поток реализации. Пайплайн масштабируется по сложности задачи: простые задачи проходят быстрее, сложные получают больше проверок.

```mermaid
flowchart TD
    subgraph Phase1["Фаза 1: Исследование и планирование"]
        R["Параллельное исследование<br/>Codebase + Reference researchers"]
        CL{"Классификация<br/>сложности"}
        R --> CL
        CL -->|SIMPLE| S5
        CL -->|MEDIUM / COMPLEX| PV
        PV["Валидация плана<br/>Tech Lead проверяет скоуп и архитектуру"]
        RA["Анализ рисков<br/>Tech Lead + Risk Testers"]
        PV --> RA
    end

    subgraph Phase2["Фаза 2: Реализация"]
        S5["Кодинг по gold standards<br/>Параллельные кодеры реализуют"]
        CC["Проверка конвенций<br/>именование, импорты, схема"]
        SR{"Специализированный<br/>review"}
        AA["Архитектурное одобрение<br/>Tech Lead sign-off"]
        S5 --> CC --> SR --> AA
        SR -.- U["SIMPLE: 1 Unified Reviewer"]
        SR -.- SP["MEDIUM/COMPLEX: Security + Logic + Quality"]
    end

    subgraph Phase3["Фаза 3: Завершение"]
        IV["Интеграционная проверка<br/>build + tests"]
        CU["Обновление конвенций<br/>паттерны и review findings"]
        SM["Итоговый отчёт"]
        IV --> CU --> SM
    end

    RA --> S5
    AA --> IV
```

| Уровень | Когда | Что меняется |
|---------|-------|--------------|
| **SIMPLE** | 1 слой, нет изменений поведения, <3 задач | Лёгкая команда, один reviewer |
| **MEDIUM** | 2+ слоя, изменения существующего кода, 3+ задач | Полная команда, специализированные reviewers, анализ рисков |
| **COMPLEX** | 3+ слоя, затрагивает auth/payments, 5+ задач | Полная команда + глубокий анализ и тестирование рисков |

---

### /conventions

Анализирует кодовую базу и создаёт/обновляет `.conventions/`:
- `gold-standards/` — короткие эталонные snippets
- `anti-patterns/` — чего избегать
- `checks/` — правила именования и импортов

`/build` использует эти conventions как reference examples. Также можно запускать `/conventions` отдельно.

## Уровни сложности

| Уровень | Размер команды | Reviewers | Анализ рисков | Валидация Tech Lead |
|---------|---------------|-----------|---------------|---------------------|
| **SIMPLE** | 4 агента | 1 unified | Пропускается | Пропускается |
| **MEDIUM** | 5-7 агентов | 3 специализированных | Да | Да |
| **COMPLEX** | 6-9+ агентов | 3 специализированных + глубокий анализ | Полный + risk testers | Да + пользователь в курсе ключевых решений |

## Роли в команде

| Роль | Время жизни | Назначение |
|------|-------------|------------|
| **Lead** | Вся сессия | Оркестрирует delivery и работу команды |
| **Supervisor** | Постоянный | Мониторит liveness, loops и escalations |
| **Codebase Researcher** | Разовый | Делает выжимку по структуре и конвенциям |
| **Reference Researcher** | Разовый | Даёт качественные reference-файлы |
| **Tech Lead** | Постоянный | Валидирует планы и архитектуру |
| **Coder** | На задачу | Реализует задачу и делает self-checks |
| **Security Reviewer** | Постоянный | Ищет эксплуатируемые уязвимости |
| **Logic Reviewer** | Постоянный | Ищет ошибки корректности и edge-cases |
| **Quality Reviewer** | Постоянный | Улучшает поддерживаемость и консистентность |
| **Unified Reviewer** | Постоянный | Универсальный reviewer для SIMPLE |
| **Risk Tester** | Разовый | Проверяет явные риски целевыми проверками |

## Структура

```
team/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── build/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── complexity-classification.md
│   │       ├── risk-analysis-protocol.md
│   │       ├── state-ownership.md
│   │       ├── state-template.md
│   │       ├── summary-report-template.md
│   │       └── teardown-fsm.md
│   ├── brief/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── brief-template.md
│   │       └── interview-principles.md
│   └── conventions/SKILL.md
├── agents/
│   ├── supervisor.md
│   ├── codebase-researcher.md
│   ├── reference-researcher.md
│   ├── tech-lead.md
│   ├── coder.md
│   ├── security-reviewer.md
│   ├── logic-reviewer.md
│   ├── quality-reviewer.md
│   ├── unified-reviewer.md
│   └── risk-tester.md
├── references/
│   ├── gold-standard-template.md
│   ├── reviewer-protocol.md
│   ├── risk-testing-example.md
│   ├── status-icons.md
│   └── supervisor-playbooks.md
├── README.md
└── README.ru.md
```

## Лицензия

MIT
