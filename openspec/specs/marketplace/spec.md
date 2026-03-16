# Marketplace

Центральный реестр плагинов izTeam для Claude Code.

## Структура

- `.claude-plugin/marketplace.json` — манифест маркетплейса
- `plugins/<name>/` — директории плагинов

## Манифест (marketplace.json)

```json
{
  "name": "izteam",
  "version": "<semver>",
  "owner": { "name": "izzzzzi", "url": "https://github.izzzzzi" },
  "plugins": [
    {
      "name": "<plugin-name>",
      "source": "./plugins/<name>",
      "description": "<краткое описание>",
      "version": "<semver>"
    }
  ]
}
```

## Плагины в реестре

| Плагин | Версия | Описание |
|--------|--------|----------|
| team | 0.3.9 | Мульти-агентная реализация фич с ревью-гейтами |
| think | 1.1.7 | Структурированное планирование через параллельных экспертов |
| arena | 1.1.7 | Дебаты экспертов с конвергенцией на решении |
| audit | 0.1.14 | Интерактивный аудит мёртвого кода |
| reason | 0.1.0 | Hypothesis-driven reasoning через ADI-цикл |

## Версионирование

- Semantic Versioning (major.minor.patch)
- Единый скрипт: `./scripts/bump-version.sh [major|minor|patch]`
- Обновляет `marketplace.json` и все `plugin.json`
- Автоматизация: `.github/workflows/auto-version.yml`

## Установка

```bash
/plugin marketplace add izzzzzi/izTeam
/plugin install <plugin-name>@izteam
```

## Команды

| Команда | Плагин | Назначение |
|---------|--------|------------|
| `/build` | team | Запуск мульти-агентной реализации |
| `/brief` | team | Интервью перед сборкой |
| `/conventions` | team | Извлечение конвенций проекта |
| `/think` | think | Структурированный анализ |
| `/arena` | arena | Дебаты экспертов |
| `/audit` | audit | Аудит мёртвого кода |
| `/reason` | reason | Hypothesis-driven reasoning (ADI) |
