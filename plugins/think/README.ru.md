<p align="right"><a href="./README.md">English</a> | <strong>Русский</strong></p>

# Think

Планируйте сложные задачи до кодинга через структурированный экспертный анализ.

## Installation

```bash
/plugin marketplace add izzzzzi/izTeam
/plugin install think@izteam
```

## Usage

```
/think <task or idea>
```

**Example:**
```
/think Implement a feedback collection system with cashback rewards
```

## How It Works

```mermaid
flowchart TD
    S1["Stage 1: Breakdown<br/>Уточнение задачи, выбор главного эксперта,<br/>principles от 3 экспертов"]
    S1 --> AT["Таблица аспектов<br/>5-15 аспектов с назначенными экспертами"]
    AT --> S2["Stage 2: Parallel Expert Analysis<br/>Один агент на аспект, запуск параллельно"]
    S2 --> A1["Изучение проекта<br/>структура, паттерны, код"]
    S2 --> A2["Экспертное мышление<br/>main expert + principles"]
    S2 --> A3["2-4 варианта<br/>с плюсами и минусами"]
    A1 & A2 & A3 --> S3["Stage 3: Summary Document"]
    S3 --> DOC["docs/plans/YYYY-MM-DD-topic-design.md"]
```

Итоговый документ включает: table of contents, overview с ключевыми решениями, детали по каждому аспекту с comparison tables, поэтапный implementation plan и success metrics.

## Structure

```
think/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── think/SKILL.md
├── agents/
│   └── expert.md
├── README.md
└── README.ru.md
```

## Result

Планирующий документ, который включает:
- Список экспертов по разделам
- Decision tables
- Code examples
- Поэтапный implementation plan
- Success metrics

## When to Use

- Новые фичи с неочевидными решениями
- Рефакторинг, где есть несколько подходов
- Архитектурные изменения
- Любые задачи, где важно продумать решение до кодинга

## License

MIT
