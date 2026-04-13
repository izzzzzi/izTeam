<p align="right"><a href="./README.md">English</a> | <strong>Русский</strong></p>

<div align="center">

# 🧩 izteam

**Маркетплейс плагинов для Claude Code: команды AI-агентов, экспертные дебаты, глубокое планирование и интерактивный аудит кода**

[![Validate](https://github.com/izzzzzi/izTeam/actions/workflows/validate.yml/badge.svg)](https://github.com/izzzzzi/izTeam/actions/workflows/validate.yml)
[![Auto Version](https://github.com/izzzzzi/izTeam/actions/workflows/auto-version.yml/badge.svg)](https://github.com/izzzzzi/izTeam/actions/workflows/auto-version.yml)
[![Plugins](https://img.shields.io/badge/Plugins-5-blue?style=flat&colorA=18181B&colorB=28CF8D)](https://github.com/izzzzzi/izTeam)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat&colorA=18181B&colorB=28CF8D)](LICENSE)
[![Contributing](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat&colorA=18181B&colorB=28CF8D)](CONTRIBUTING.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Plugin-purple?style=flat&colorA=18181B&colorB=7C3AED)](https://claude.ai/code)

<br />

*Установите прикладные плагины, которые делают работу Claude Code предсказуемее для разработки, принятия решений и очистки кода.*

</div>

---

## 📖 Обзор

**izteam** — независимый маркетплейс плагинов для [Claude Code](https://claude.ai/code).
Каждый плагин добавляет slash-команды, агентов и готовые workflow: от реализации фич командой AI-агентов до аудита устаревшего кода.

---

## 🗺 Как это работает

```mermaid
graph TD
    subgraph Установка
        A["1. Добавить marketplace<br/><code>/plugin marketplace add izzzzzi/izTeam</code>"]
        B["2. Установить плагины<br/><code>/plugin install team@izteam</code>"]
        A --> B
    end

    B --> C{"Выбрать workflow"}

    subgraph "/build &mdash; Team"
        D1["📋 Brief &mdash; интервью для уточнения скоупа"]
        D2["📐 Plan &mdash; архитектор проектирует задачи"]
        D3["👨‍💻 Code &mdash; параллельные кодеры реализуют"]
        D4["🔍 Review &mdash; security + logic + quality"]
        D5["✅ Commit &mdash; одобренные изменения мерджатся"]
        D1 --> D2 --> D3 --> D4 --> D5
    end

    subgraph "/think &mdash; Think"
        E1["🔬 Декомпозиция на аспекты"]
        E2["🧠 Параллельный экспертный анализ"]
        E3["📄 Единый design-документ"]
        E1 --> E2 --> E3
    end

    subgraph "/arena &mdash; Arena"
        F1["📚 Исследование контекста"]
        F2["🎭 Эксперты спорят"]
        F3["🤝 Достигнут консенсус"]
        F1 --> F2 --> F3
    end

    subgraph "/audit &mdash; Audit"
        G1["🔎 Сканирование кодовой базы"]
        G2["💬 Интерактивный обзор с пользователем"]
        G3["🧹 Очистка подтверждённых элементов"]
        G1 --> G2 --> G3
    end

    subgraph "/reason &mdash; Reason"
        R1["🔬 Генерация конкурирующих гипотез"]
        R2["🔍 Логическая верификация"]
        R3["📊 Сбор эмпирических доказательств"]
        R4["📋 Design Rationale Record"]
        R1 --> R2 --> R3 --> R4
    end

    C --> D1
    C --> E1
    C --> F1
    C --> G1
    C --> R1
```

**Примеры использования:**

```bash
# Собрать фичу командой AI-агентов
/build "Добавь страницу настроек пользователя с редактированием профиля"

# Продумать архитектуру до кодинга
/think "Миграция с REST на GraphQL — компромиссы и план"

# Получить мнения экспертов через структурированные дебаты
/arena "Микросервисы или монолит для нашего SaaS?"

# Найти и почистить мёртвый код
/audit
```

---

## ✨ Плагины

| Плагин | Версия | Описание | Команда |
|--------|--------|----------|---------|
| 🤖 **[team](#-team)** | `0.3.7` | Реализуйте фичи с командой AI-агентов и встроенными review-gates. | `/build` |
| 🧠 **[think](#-think)** | `1.1.7` | Планируйте сложные задачи до кодинга через структурированный экспертный анализ. | `/think` |
| 🎭 **[arena](#-arena)** | `1.1.7` | Сравнивайте экспертные точки зрения и приходите к чёткому решению. | `/arena` |
| 🧹 **[audit](#-audit)** | `0.1.10` | Находите мёртвый и устаревший код через интерактивный аудит. | `/audit` |
| 🧪 **[reason](#-reason)** | `0.1.0` | Рассуждения на основе гипотез с аудируемыми цепочками доказательств (FPF/ADI цикл). | `/reason` |

---

## 🚀 Быстрый старт

### 1. Добавьте marketplace

```bash
/plugin marketplace add izzzzzi/izTeam
```

### 2. Установите плагины

```bash
/plugin install team@izteam
/plugin install think@izteam
/plugin install arena@izteam
/plugin install audit@izteam
/plugin install reason@izteam
```

### 3. Перезапустите Claude Code

Плагины загружаются при старте, поэтому после установки нужен перезапуск.

---

## 🤖 team

Реализуйте фичи с командой AI-агентов и встроенными review-gates.

> **Требуется:** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` в `settings.json`

```bash
/plugin install team@izteam
```

**Команды:**

```bash
/build "Add user settings page"
/build docs/plan.md --coders=2
/brief "Notifications system"
/conventions
```

**Естественный язык — тоже работает:**

```
"Собери страницу настроек с редактированием профиля"
"Реализуй нотификации с email и push"
"Поспрашивай меня перед тем как начнём строить"
"Выдели конвенции проекта и задокументируй стандарты"
```

[Подробнее (RU) →](./plugins/team/README.ru.md) · [EN →](./plugins/team/README.md)

---

## 🧠 think

Планируйте сложные задачи до кодинга через структурированный экспертный анализ.

```bash
/plugin install think@izteam
```

**Команды:**

```bash
/think Implement a feedback collection system with cashback rewards
/think Migrate from REST to GraphQL — trade-offs and strategy
/think Refactor authentication from session-based to JWT
```

**Естественный язык — тоже работает:**

```
"Продумай архитектуру платёжной системы"
"Спланируй миграцию с REST на GraphQL"
"Проанализируй компромиссы между SSR и CSR"
"Опиши полный план для микросервиса"
```

[Подробнее (RU) →](./plugins/think/README.ru.md) · [EN →](./plugins/think/README.md)

---

## 🎭 arena

Сравнивайте экспертные точки зрения и приходите к чёткому решению.

> **Требуется:** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` в `settings.json`

```bash
/plugin install arena@izteam
```

**Команды:**

```bash
/arena Should we use microservices or monolith for our SaaS?
/arena Best pricing strategy for a developer tool?
/arena How should we handle state management in our React app?
```

**Естественный язык — тоже работает:**

```
"Дебаты: микросервисы или монолит для нашего кейса"
"Нужны мнения экспертов по управлению стейтом"
"Сравни Redux vs Zustand vs Jotai — плюсы и минусы"
"Какая лучшая стратегия авторизации? Пусть эксперты поспорят"
```

[Подробнее (RU) →](./plugins/arena/README.ru.md) · [EN →](./plugins/arena/README.md)

---

## 🧹 audit

Находите мёртвый и устаревший код через интерактивный аудит.

```bash
/plugin install audit@izteam
```

**Команды:**

```bash
/audit
/audit features
/audit server
/audit ui
/audit stores
```

**Естественный язык — тоже работает:**

```
"Найди мёртвый код и почисти"
"Почисти кодовую базу от legacy и осиротевшего кода"
"Проверь фичи на неиспользуемые экспорты"
"Проведи аудит сервера на мёртвые API эндпоинты"
"Найди неиспользуемые UI компоненты"
"Проверь сторы на избыточный стейт"
```

[Подробнее (RU) →](./plugins/audit/README.ru.md) · [EN →](./plugins/audit/README.md)

---

## 🧪 reason

Рассуждения на основе гипотез с аудируемыми цепочками доказательств, основано на [First Principles Framework](https://github.com/ailev/FPF).

> **Требуется:** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` в `settings.json`

```bash
/plugin install reason@izteam
```

**Команды:**

```bash
/reason Какую базу данных выбрать для нового сервиса?
/reason Монолит или микросервисы для нашего кейса?
/reason Скорость или корректность в data pipeline?
```

**Естественный язык — тоже работает:**

```
"Проанализируй выбор базы данных с доказательствами"
"Сравни варианты стратегии авторизации с trust-скорами"
"Мне нужен decision record по подходу к кешированию"
```

[Подробнее (RU) →](./plugins/reason/README.ru.md) · [EN →](./plugins/reason/README.md)

---

## 📁 Структура проекта

```text
izteam/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── team/
│   ├── think/
│   ├── arena/
│   ├── audit/
│   └── reason/
├── scripts/
│   └── bump-version.sh
├── .github/workflows/
│   ├── validate.yml
│   └── auto-version.yml
├── CODE_OF_CONDUCT.md
└── CONTRIBUTING.md
```

---

## 🔧 Настройка

### Включение Agent Teams

Плагины `team` и `arena` требуют экспериментальную функцию Agent Teams:

```json
// ~/.claude/settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

---

## 🛠 Разработка

### Версионирование

```bash
# Bump единой версии
./scripts/bump-version.sh patch
./scripts/bump-version.sh minor
```

Репозиторий использует единую версию (`v0.0.1`, `v0.1.0` и т.д.). Версии отдельных плагинов обновляются автоматически.

### CI/CD

- `validate.yml` — проверки структуры и консистентности на PR и push
- `auto-version.yml` — автоматический bump единой версии, теги и релиз

---

## 🐛 Troubleshooting

- Плагин не появился после установки → перезапустите Claude Code.
- Новая версия не подтянулась → очистите кеш:

```bash
rm -rf ~/.claude/plugins/cache/izteam/
```

