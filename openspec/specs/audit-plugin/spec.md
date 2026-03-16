# Audit Plugin

Интерактивный аудит мёртвого кода. Версия: 0.1.14.

## Скилл: /audit

**Аргумент:** `[scope: features | server | ui | stores | all]`

### Философия

Vibe-coding создаёт много экспериментального кода. Audit находит потенциально мёртвый код через **диалог**, а не предположения.

### Workflow

#### Step 1: Discovery

Выбор агента по scope:

| Scope | Agent | Target |
|-------|-------|--------|
| features | features-auditor | `src/features/` — unused exports |
| server | server-auditor | `src/server/` — unused tRPC procedures |
| ui | ui-auditor | `src/design-system/` — orphan components |
| stores | stores-auditor | `src/stores/` — dead Zustand slices |
| all (default) | feature-scanner | Full codebase scan |

Если результат пустой или `"verdict": "clean"` → сообщить "кодовая база чистая", **END**.

#### Step 2: Interactive Review

Цикл по findings, ONE BY ONE:
1. Показать контекст (файлы, использование, последний коммит)
2. AskUserQuestion с опциями: Удалить / Deprecated / Оставить / Не уверен
3. **STOP** — ждать ответ

**CRITICAL:** ONE AskUserQuestion per message, затем STOP. Нарушение = auto-approve с пустым ответом.

"Не уверен" → spawn `usage-analyzer` → показать анализ → спросить снова.

#### Step 3: Generate Report

Markdown отчёт с секциями: To Delete, Deprecated, Keep, Next Steps.

#### Step 4: Final Confirmation

AskUserQuestion: Подтвердить удаление / Отменить. **Обязательный шаг** даже если уже ответили "Удалить" по отдельности.

Подтверждение → spawn `cleanup-executor` для каждого элемента (git branch backup + удаление).

#### Step 5: Merge to Main

AskUserQuestion: Влить cleanup-ветки / Оставить для ручной проверки.

#### Step 6: Delete Cleanup Branches

AskUserQuestion: Удалить ветки / Сохранить для истории.

## Агенты

### Сканеры

| Агент | Фокус |
|-------|-------|
| feature-scanner | Полное сканирование кодовой базы |
| features-auditor | `src/features/` unused exports |
| server-auditor | `src/server/` unused tRPC |
| ui-auditor | `src/design-system/` orphan components |
| stores-auditor | `src/stores/` dead Zustand slices |

### Аналитики и исполнители

| Агент | Роль |
|-------|------|
| usage-analyzer | Глубокий анализ зависимостей по запросу |
| cleanup-executor | Безопасное удаление с git backup |

## Скрипты

- `find-dead-exports.sh` — поиск неиспользуемых exports
- `scan-orphan-routes.sh` — поиск orphan API routes
- `analyze-feature-usage.sh` — анализ зависимостей фичи
- `safe-cleanup.sh` — git-backed удаление

## Ключевые правила

1. Скилл **READ-ONLY** — все удаления только через cleanup-executor после Step 4
2. ONE AskUserQuestion per message — **самое важное правило**
3. One item per turn
4. Bash только для git операций (Steps 5-6)
