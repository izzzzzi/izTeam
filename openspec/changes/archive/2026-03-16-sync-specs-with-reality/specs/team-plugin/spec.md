## ADDED Requirements

### Requirement: Git checkpoint mode
The `/build` skill SHALL support a `--git-checkpoints` flag that enables WIP commits during the build process: pre-review commit, review fixes commit, and final commit. Default mode (without flag) creates a single commit after all approvals.

#### Scenario: Standard mode creates single commit
- **WHEN** `/build` runs without `--git-checkpoints`
- **THEN** a single commit is created after all review approvals

#### Scenario: Checkpoint mode creates WIP commits
- **WHEN** `/build` runs with `--git-checkpoints`
- **THEN** WIP commits are created at each stage: pre-review, review fixes, final

### Requirement: Project profile generation
The `/build` and `/conventions` skills SHALL support `.project-profile.yml` — a machine-readable project profile that caches orientation data for cold-start optimization. The profile is generated during conventions extraction and used by the build pipeline to skip redundant orientation steps.

#### Scenario: Conventions skill generates project profile
- **WHEN** `/conventions` analyzes the codebase
- **THEN** it generates `.project-profile.yml` alongside `.conventions/` directory

#### Scenario: Build skill uses project profile for cold-start
- **WHEN** `/build` starts Phase 1 and `.project-profile.yml` exists
- **THEN** it reads the profile to skip redundant orientation, improving cold-start speed

### Requirement: Repo map generation and caching
The `/build` skill SHALL generate `.repo-map` — a ranked symbol map of the codebase — using `skills/build/scripts/repo-map.py`. The map is cached for 24 hours and regenerated when new commits appear or when the `--fresh` flag is used.

#### Scenario: Repo map is cached for 24h
- **WHEN** `.repo-map` exists and is less than 24 hours old with no new commits
- **THEN** the build pipeline reuses the existing map

#### Scenario: Fresh flag forces regeneration
- **WHEN** `/build --fresh` is run
- **THEN** `.repo-map` is regenerated regardless of cache age

## MODIFIED Requirements

### Requirement: Team plugin references
The team plugin SHALL include the following references at `plugins/team/references/`: `gold-standard-template.md` (шаблон gold-standard примеров), `reviewer-protocol.md` (стандарты ревью), `risk-testing-example.md` (пример тестирования рисков), `status-icons.md` (иконки статуса для state reporting), `supervisor-playbooks.md` (операционные плейбуки supervisor).

#### Scenario: All five reference files exist
- **WHEN** the team plugin is inspected
- **THEN** `plugins/team/references/` contains exactly 5 files: gold-standard-template.md, reviewer-protocol.md, risk-testing-example.md, status-icons.md, supervisor-playbooks.md

### Requirement: Build skill references
The build skill SHALL include the following references at `plugins/team/skills/build/references/`: `complexity-classification.md`, `risk-analysis-protocol.md`, `state-ownership.md`, `state-template.md`, `summary-report-template.md`, `teardown-fsm.md`.

#### Scenario: All six build reference files exist
- **WHEN** the build skill is inspected
- **THEN** `plugins/team/skills/build/references/` contains exactly 6 files

### Requirement: Brief skill references
The brief skill SHALL include references at `plugins/team/skills/brief/references/`: `brief-template.md` (шаблон брифа) and `interview-principles.md` (принципы интервью).

#### Scenario: Brief references exist
- **WHEN** the brief skill is inspected
- **THEN** `plugins/team/skills/brief/references/` contains brief-template.md and interview-principles.md
