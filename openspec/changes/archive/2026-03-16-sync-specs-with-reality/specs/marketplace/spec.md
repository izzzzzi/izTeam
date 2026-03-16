## MODIFIED Requirements

### Requirement: Plugins in the registry
The marketplace SHALL include 5 plugins in the registry:

| Плагин | Версия | Описание |
|--------|--------|----------|
| team | 0.3.9 | Мульти-агентная реализация фич с ревью-гейтами |
| think | 1.1.7 | Структурированное планирование через параллельных экспертов |
| arena | 1.1.7 | Дебаты экспертов с конвергенцией на решении |
| audit | 0.1.14 | Интерактивный аудит мёртвого кода |
| reason | 0.1.0 | Hypothesis-driven reasoning через ADI-цикл |

#### Scenario: All five plugins listed
- **WHEN** marketplace.json is inspected
- **THEN** it contains entries for team, think, arena, audit, and reason plugins

#### Scenario: Reason plugin entry format
- **WHEN** the reason plugin is added to marketplace
- **THEN** its entry includes name "reason", source "./plugins/reason", version "0.1.0"

### Requirement: Available commands
The marketplace SHALL document all available slash commands:

| Команда | Плагин | Назначение |
|---------|--------|------------|
| `/build` | team | Запуск мульти-агентной реализации |
| `/brief` | team | Интервью перед сборкой |
| `/conventions` | team | Извлечение конвенций проекта |
| `/think` | think | Структурированный анализ |
| `/arena` | arena | Дебаты экспертов |
| `/audit` | audit | Аудит мёртвого кода |
| `/reason` | reason | Hypothesis-driven reasoning (ADI) |

#### Scenario: Reason command documented
- **WHEN** the marketplace spec is inspected
- **THEN** `/reason` command is listed with plugin "reason" and description

#### Scenario: Command count matches plugin count
- **WHEN** all plugins have skills
- **THEN** team has 3 commands, think/arena/audit/reason each have 1, total 7 commands
