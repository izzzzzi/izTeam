<p align="right"><a href="./README.md">English</a> | <strong>Русский</strong></p>

# Audit

Находите мёртвый и устаревший код через интерактивный аудит.

## Problem

В проектах с быстрой итерацией экспериментальный код накапливается:
- Фичу попробовали и забросили
- После рефакторинга остались старые пути
- Временные варианты остались в production-коде

Статический анализ часто это пропускает: код может быть формально использован, но уже не нужен продукту.

## Solution

**Interactive audit:**
1. Агент находит подозрительные участки
2. Уточняет, нужен ли каждый участок
3. Безопасно удаляет подтверждённый dead code с git backup

## Installation

```bash
/plugin marketplace add izzzzzi/izTeam
/plugin install audit@izteam
```

## Usage

```
/audit              # Full codebase scan (feature-scanner)
/audit features     # src/features/ deep audit (features-auditor)
/audit server       # src/server/ routers & services (server-auditor)
/audit ui           # src/design-system/ components (ui-auditor)
/audit stores       # src/stores/ Zustand state (stores-auditor)
```

## Workflow

```mermaid
flowchart TD
    D["1. Discovery<br/>feature-scanner находит подозрительные участки"]
    I{"2. Interview<br/>&quot;Это ещё используется?&quot;"}
    DEL["Delete"]
    DEP["Deprecated"]
    KEEP["Keep"]
    NS["Not sure<br/>usage-analyzer"]
    C["3. Cleanup<br/>git branch + commit + TypeScript check"]

    D --> I
    I --> DEL --> C
    I --> DEP
    I --> KEEP
    I --> NS -->|deep analysis| I
```

## Agents

### Core Agents

| Agent | Purpose |
|-------|---------|
| `feature-scanner` | Полный скан: features, routers, pages |
| `usage-analyzer` | Глубокий анализ конкретной фичи |
| `cleanup-executor` | Безопасное удаление с git backup |

### Specialized Auditors

| Agent | Target | What it finds |
|-------|--------|---------------|
| `ui-auditor` | `src/design-system/` | Неиспользуемые компоненты, style inconsistencies |
| `stores-auditor` | `src/stores/` | Мёртвые Zustand slices, неиспользуемые selectors |
| `features-auditor` | `src/features/` | Неиспользуемые exports, внутренний dead code |
| `server-auditor` | `src/server/` | Неиспользуемые tRPC procedures, мёртвые services |

## Safety

- Никогда не удаляет без подтверждения
- Создаёт git branch перед удалением
- Проверяет TypeScript после удаления
- Логирует все изменения

## License

MIT
