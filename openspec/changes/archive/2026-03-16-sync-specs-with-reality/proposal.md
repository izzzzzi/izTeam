## Why

Спеки OpenSpec отстали от кодовой базы. Пятый плагин **reason** (v0.1.0) полностью реализован, но не имеет спеки. Плагин **arena** получил evidence-driven систему (R/CL рейтинги, WLNK trust, assurance levels), которая не отражена в спеке. Конфиг проекта (`config.yaml`) до сих пор описывает "четыре плагина". Без синхронизации спеки становятся ненадёжным источником истины.

## What Changes

- **Новый спек `reason-plugin`** — описание ADI-цикла (Abduction → Deduction → Induction), 3 агентов (hypothesizer, verifier, evidence-gatherer), DRR-артефактов, WLNK trust scoring
- **Обновление спека `arena-plugin`** — evidence-driven debate protocol: R/CL рейтинги на аргументах, assurance levels (L0/L1/L2), обновлённый synthesis template с Trust Summary и Evidence Catalog
- **Обновление спека `team-plugin`** — добавить `--git-checkpoints` mode, `.project-profile.yml`, недостающие references (status-icons, risk-testing-example)
- **Обновление спека `marketplace`** — reason plugin в реестре, 5 плагинов вместо 4, команда `/reason`
- **Обновление `config.yaml`** — пять плагинов, reason в списке

## Non-goals

- Изменение кода плагинов — это чисто документационное обновление
- Создание shared спеки для evidence scoring framework (пока не нужна — arena и reason используют его по-своему)
- Обновление CI/CD workflows (auto-version.yml для reason) — отдельный change

## Capabilities

### New Capabilities

- `reason-plugin`: Hypothesis-driven reasoning через ADI-цикл с evidence gathering и WLNK trust scoring

### Modified Capabilities

- `arena-plugin`: Добавлена evidence-driven система дебатов (R/CL рейтинги, assurance levels, обновлённый synthesis)
- `team-plugin`: Git checkpoint mode, project profile generation, недостающие references
- `marketplace`: Пятый плагин reason в реестре и командах

## Impact

**Затронутые плагины:** reason (новый спек), arena, team, marketplace (обновления)

**Затронутые файлы:**
- `openspec/specs/reason-plugin/spec.md` — новый
- `openspec/specs/arena-plugin/spec.md` — обновление
- `openspec/specs/team-plugin/spec.md` — обновление
- `openspec/specs/marketplace/spec.md` — обновление
- `openspec/config.yaml` — обновление

**Зависимости:** нет — спеки описывают уже реализованный код
