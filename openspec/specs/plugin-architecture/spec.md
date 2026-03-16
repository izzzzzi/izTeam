# Plugin Architecture

Стандартная структура и контракты для всех плагинов izTeam.

## Структура плагина

```
plugins/<name>/
├── .claude-plugin/
│   └── plugin.json           # Метаданные (name, version, description, author, keywords)
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md           # Определение скилла (YAML frontmatter + протокол)
│       ├── scripts/           # Вспомогательные скрипты (bash, python)
│       └── references/        # Справочные файлы для контекста скилла
├── agents/
│   └── <agent-name>.md        # Определения агентов (YAML frontmatter + роль)
├── README.md                  # Документация (EN)
└── README.ru.md               # Документация (RU)
```

## Формат plugin.json

```json
{
  "name": "<lowercase>",
  "version": "<semver>",
  "description": "<одно предложение>",
  "author": { "name": "<имя>", "url": "<github>" },
  "repository": "<github-url>",
  "license": "MIT",
  "keywords": ["<тег1>", "<тег2>"]
}
```

## Формат SKILL.md

```markdown
---
name: <kebab-case>
description: >-
  <что делает, когда использовать, когда НЕ использовать>
argument-hint: "<пример аргументов>"
model: opus
allowed-tools:
  - <Tool1>
  - <Tool2>
---

# <Название>

<Протокол работы с фазами/шагами>
```

Ключевые поля frontmatter:
- `name` — уникальное имя скилла (kebab-case)
- `description` — включает use/don't-use критерии
- `allowed-tools` — whitelist инструментов
- `model` — модель для выполнения (обычно opus)
- `argument-hint` — подсказка по аргументам

## Формат агента (agent.md)

```markdown
---
name: <lowercase-kebab-case>
description: |
  <описание с примерами>
  <example>позитивный пример</example>
  <example type="negative">негативный пример</example>
model: opus
color: <уникальный цвет>
tools:           # ИЛИ allowlist
  - Tool1
disallowedTools: # ИЛИ blocklist (никогда оба)
  - BlockedTool
---

<role>
Идентичность агента (3-5 строк, третье лицо)
</role>

## Key Responsibilities
## Methodology
## Communication Protocol
## Output Rules (P0/P1/P2)
```

## Контракты

### Агент

- Уникальное `name` в kebab-case внутри плагина
- Либо `tools`, либо `disallowedTools` — никогда оба
- Описание с positive и negative примерами
- Секция `<role>` обязательна

### Скилл

- `description` содержит "Use when" и "Don't use for"
- `allowed-tools` — явный whitelist
- Протокол описывает фазы, error handling, output format

### Документация

- README.md (EN) и README.ru.md (RU) обязательны
- Оба документа синхронизированы по содержанию
