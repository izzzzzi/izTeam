# Conventions System

Система проектных соглашений — единый источник истины для паттернов кода.

## Структура

```
.conventions/
├── gold-standards/          # Канонические примеры для подражания
│   ├── agent-definition.md  # Структура определения агента
│   └── skill-definition.md  # Структура определения скилла
├── checks/                  # Правила валидации
│   ├── agent-contracts.md   # Контракты агентов
│   └── skill-validation.md  # Валидация скиллов
├── decisions/               # Архитектурные решения (ADR-like)
│   └── *.md
├── tool-chains/             # CI/CD инструменты
│   └── README.md
├── glossary.md              # Каноническая терминология
└── formatting.md            # Правила форматирования
```

## Gold Standards

Эталонные примеры кода, которые агенты используют как few-shot контекст. Главный рычаг качества в `/build`.

- Включаются в briefing.md при создании команды
- 3-5 примеров, ~100-150 строк
- Coders получают их в каждом промпте

## Глоссарий (ключевые термины)

| Термин | Значение |
|--------|----------|
| gold standard | Эталонный пример кода для подражания |
| unified reviewer | Единый ревьюер для SIMPLE задач |
| specialized reviewers | Security + Logic + Quality для MEDIUM/COMPLEX |
| Lead | Оркестратор команды |
| Supervisor | Операционный монитор |
| Coder | Агент реализации |
| Tech Lead | Архитектурный валидатор |

## Создание и обновление

- `/conventions` — извлечение из анализа кодовой базы
- `/build` Phase 3 — обязательная задача обновления conventions (через ревью)
- `.conventions/` MUST exist и быть обновлён в текущей сессии (completion gate)

## CI/CD валидация

- `.github/workflows/validate.yml` — проверка структуры и консистентности
- `.github/workflows/auto-version.yml` — автоматический bump версий
