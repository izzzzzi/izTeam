# Best Practices Audit: izteam vs mgechev/skills-best-practices

> **Status:** Research complete
> **Date:** 2026-03-01
> **Goal:** Deep audit of izteam plugin marketplace against published skill authoring best practices

---

## Table of Contents

1. [Overview](#overview)
2. [Directory Structure Compliance](#1-directory-structure-compliance)
3. [Frontmatter & Discoverability](#2-frontmatter--discoverability)
4. [SKILL.md Leanness (<500 lines)](#3-skillmd-leanness)
5. [Progressive Disclosure & JiT Loading](#4-progressive-disclosure--jit-loading)
6. [Instruction Style (Procedural vs Prose)](#5-instruction-style)
7. [Terminology Consistency](#6-terminology-consistency)
8. [Deterministic Scripts](#7-deterministic-scripts)
9. [Error Handling & Edge Cases](#8-error-handling--edge-cases)
10. [Validation Process](#9-validation-process)
11. [Template & Asset Usage](#10-template--asset-usage)
12. [Implementation Plan](#implementation-plan)

---

## Overview

### Goals

1. **Compliance Audit** -- systematically check all 6 skills and 20+ agents against each best practice from mgechev/skills-best-practices
2. **Gap Analysis** -- identify what's missing and prioritize by impact
3. **Action Plan** -- concrete steps to achieve full compliance

### Scorecard

| # | Best Practice | Compliance | Priority |
|---|--------------|:----------:|:--------:|
| 1 | Directory Structure | 5/6 skills PASS | MEDIUM |
| 2 | Frontmatter & Discoverability | 0/6 fully compliant | **HIGH** |
| 3 | SKILL.md Leanness (<500 lines) | 5/6 PASS | **HIGH** |
| 4 | Progressive Disclosure & JiT Loading | Mostly compliant | LOW |
| 5 | Instruction Style (Procedural) | Mixed (strong procedures, weak voice) | MEDIUM |
| 6 | Terminology Consistency | 8 inconsistencies found | **HIGH** |
| 7 | Deterministic Scripts | 0 skill-level scripts exist | **HIGH** |
| 8 | Error Handling & Edge Cases | 2 EXCELLENT, 2 POOR | MEDIUM |
| 9 | Validation Process | Zero skill-level validation | **HIGH** |
| 10 | Template & Asset Usage | Fully compliant (intent met) | LOW |

### Key Decisions

| Aspect | Decision |
|--------|----------|
| Directory Structure | Extract `build/SKILL.md` sections into colocated `references/` |
| Frontmatter | Full rewrite of all 6 descriptions with negative triggers |
| SKILL.md Leanness | Surgical extraction of ~437 lines from `build/SKILL.md` |
| Progressive Disclosure | Fix JiT loading in `brief/SKILL.md` only |
| Instruction Style | Tiered: full conversion for SKILL.md files, voice-only for agents |
| Terminology | Comprehensive audit + glossary creation |
| Scripts | Create scripts for audit, build, conventions plugins + root validation |
| Error Handling | Add structured error sections to 4 skills lacking them |
| Validation | Schema-based CI validation, then LLM-based discovery validation |
| Templates | Status quo -- inline templates already meet the intent |

---

## 1. Directory Structure Compliance

> **Experts:** Martin Fowler, Sam Newman, Kelsey Hightower

### Results

| Skill | Plugin | Lines | Structure | References | Overall |
|-------|--------|-------|-----------|------------|---------|
| `arena` | arena | 342 | PASS | N/A | **COMPLIANT** |
| `audit` | audit | 128 | PASS | N/A | **COMPLIANT** |
| `brief` | team | 314 | PASS | PASS | **COMPLIANT** |
| `build` | team | 1004 | PASS | **FAIL** | **NON-COMPLIANT** |
| `conventions` | team | 208 | PASS | N/A | **COMPLIANT** |
| `think` | think | 171 | PASS | N/A | **COMPLIANT** |

### Violations in `build`

1. **SKILL.md is 1004 lines** (limit: 500) -- over 2x the allowed size
2. **References not colocated** -- 4 reference files live at plugin level (`plugins/team/references/`) instead of inside `plugins/team/skills/build/references/`
3. **3 dead references** -- SKILL.md points to `references/gold-standard-template.md`, `references/risk-testing-example.md`, `@references/status-icons.md` that don't exist in the skill directory

### Recommended Fix

Move plugin-level references into `plugins/team/skills/build/references/` and extract ~437 lines of inline content into new reference files:

| Extract to | ~Lines | Content |
|-----------|--------|---------|
| `references/complexity-classification.md` | 100 | Trigger tables, team roster matrix |
| `references/risk-analysis-protocol.md` | 100 | Risk templates, tester spawn, comparison table |
| `references/state-ownership.md` | 80 | Ownership routing contract, handoff protocol |
| `references/teardown-fsm.md` | 65 | State machine, retry constants |
| `references/state-template.md` | 35 | The `state.md` file template |
| `references/summary-report-template.md` | 37 | Summary report format |
| `references/gold-standard-template.md` | 20 | Gold standard compilation rules (fixes dead ref) |
| `references/status-icons.md` | -- | Status emoji reference (fixes dead ref) |

**Target:** SKILL.md reduced to ~490-500 lines.

---

## 2. Frontmatter & Discoverability

> **Experts:** Theo Browne, Sam Newman, Troy Hunt

### Results

| Skill | Name OK | Third-person | Trigger-optimized | Negative triggers | Routing clarity |
|-------|:-------:|:------------:|:-----------------:|:-----------------:|:---------------:|
| arena | PASS | FAIL | FAIL | FAIL | FAIL |
| audit | PASS | PARTIAL | PARTIAL | FAIL | PARTIAL |
| brief | PASS | PARTIAL | PASS | FAIL | PASS |
| build | PASS | FAIL | PARTIAL | FAIL | PARTIAL |
| conventions | PASS | FAIL | PARTIAL | FAIL | PASS |
| think | PASS | FAIL | PARTIAL | FAIL | PARTIAL |

### Critical Findings

- **0/6 skills have negative triggers** -- universal gap
- **5/6 fail third-person voice** -- only `brief` partially passes
- **`arena` description is in Russian** -- critical routing risk for English-speaking agent router
- **`arena` vs `think` confusion** -- both mention "expert analysis"

### Recommended Rewrites

```
arena: "Orchestrates multi-expert debates with real-world personas who argue
directly with each other until convergence. Use when the user wants multiple
opposing viewpoints, expert panel discussion, or structured debate. Don't use
for quick questions, single-expert analysis, or implementation planning."

audit: "Conducts an interactive feature audit to find dead code, abandoned
experiments, and unused features, then asks the user about each one. Use when
the user wants to clean up the codebase or find unused code. Don't use for
security audits, performance profiling, or dependency scanning."

brief: "Conducts a short adaptive interview (2-6 questions) to understand
the user's intent before implementation, then compiles a brief and hands off
to /build. Use when the user asks to discuss a feature before building or
says 'ask me questions'. Don't use when the user already has a detailed spec
or invokes /build directly."

build: "Launches an autonomous agent team to implement a feature end-to-end
with researchers, coders, reviewers, and a tech lead. Use when the user wants
to build a feature or implement functionality. Don't use for bug fixes, small
edits, refactoring, or code review of existing code."

conventions: "Analyzes the codebase and creates or updates a .conventions/
directory with gold standards, anti-patterns, and checks. Use when the user
wants to extract project conventions or document coding standards. Don't use
for linting files, fixing code style, or generating documentation."

think: "Performs deep structured thinking by breaking a task into aspects,
dispatching parallel expert analysts, and producing a unified design document.
Use when the user wants to think through a complex problem or plan an
architecture. Don't use for implementation, quick questions, or expert
debates (use /arena)."
```

---

## 3. SKILL.md Leanness

> **Experts:** Martin Fowler, Sam Newman, Kelsey Hightower

### Line Counts

| Skill | Lines | Limit | Status |
|-------|:-----:|:-----:|:------:|
| arena | 342 | 500 | PASS |
| audit | 128 | 500 | PASS |
| brief | 314 | 500 | PASS |
| **build** | **1004** | **500** | **FAIL (2x over)** |
| conventions | 208 | 500 | PASS |
| think | 171 | 500 | PASS |

### `build/SKILL.md` Content Analysis

The file is information-dense, not verbose. Compression won't work -- surgical extraction is needed.

**Candidates for extraction** (see Section 1 for details): ~437 lines can be moved to `references/`, bringing SKILL.md to ~490-500 lines.

**Additional finding:** 3 dead references point to files that don't exist in any `references/` directory.

---

## 4. Progressive Disclosure & JiT Loading

> **Experts:** Minko Gechev, Rich Hickey, Sam Newman

### Results

| Check | Status |
|-------|--------|
| JiT Loading | `build` -- EXCELLENT, `brief` -- PARTIAL, others N/A |
| Explicit Pathing (relative, forward slashes) | **FULLY COMPLIANT** across all plugins |
| Flat Subdirectories (one level deep) | **FULLY COMPLIANT** |
| No Unnecessary Files in skill dirs | **FULLY COMPLIANT** |

### Single Fix Needed

In `plugins/team/skills/brief/SKILL.md`, the reference to `references/interview-principles.md` is listed passively under "Additional Resources" without an explicit trigger. Convert to:

```
When adapting questions to edge cases or unusual situations, read
`references/interview-principles.md` for expert rationale behind
question design (Cagan, Portigal, Torres, Krug, Hickey).
```

### Note on `@references/` Pattern

Agent files use `@references/` for eager loading at spawn time. This is NOT JiT but is architecturally correct for agents that need shared protocol from lifecycle start. Leave as-is.

---

## 5. Instruction Style

> **Experts:** Martin Fowler, Kent C. Dodds, Theo Browne

### Consolidated Scores (out of 10)

| File | Step-by-Step | Voice (3rd-person) | Decision Trees | Templates |
|------|:---:|:---:|:---:|:---:|
| build/SKILL.md | 9 | 5 | **10** | 9 |
| arena/SKILL.md | 7 | 3 | 5 | 7 |
| brief/SKILL.md | 7 | 5 | 6 | 9 |
| conventions/SKILL.md | 8 | 7 | 6 | 8 |
| think/SKILL.md | 7 | 5 | 3 | 9 |
| audit/SKILL.md | 7 | 3 | 5 | 7 |
| Agent definitions (avg) | 7 | 4 | 4 | 7 |

### Top Violations

1. **Voice: Second-person ("You"/"Ты") is universal** -- not a single file uses third-person imperative consistently. Every `<role>` block opens with "You are a...". Every Philosophy section uses "you/your".

2. **Decision Trees missing in 10 of 19 agent files** -- only `build/SKILL.md` and `supervisor.md` have formal ASCII decision trees.

3. **Prose sections where procedures should be** -- arena "Live Commentary", build "Philosophy", audit introductions.

### Recommended Tiered Approach

- **SKILL.md files (6 files):** Full conversion -- fix voice, add decision trees where branching logic hides in prose, extract large inline templates to references
- **Agent definitions (13+ files):** Voice-only fix -- convert "You are a **Coder**" to bare imperative/third-person, leave structure unchanged

---

## 6. Terminology Consistency

> **Experts:** Martin Fowler, Sam Newman, Troy Hunt

### 8 Inconsistencies Found

| # | Issue | Severity | Files Affected |
|---|-------|:--------:|:--------------:|
| 1 | "Lead" vs "Moderator" vs `team-lead` slug in arena | **MAJOR** | arena SKILL + expert agent |
| 2 | Reviewer examples show "Lead sends" but protocol says "coders send" | **MAJOR** | 3 reviewer agents |
| 3 | "Supervisor" vs "TaskOrchestrator" dual naming | MINOR | supervisor.md |
| 4 | "web researcher" -- phantom role with no agent definition | MODERATE | build/SKILL.md |
| 5 | `subagent_type=Explore` in conventions vs `team:codebase-researcher` elsewhere | MODERATE | conventions/SKILL.md |
| 6 | Coder lifecycle: "temporary" vs "per task" vs "killed after completion" | MINOR | coder.md, build/SKILL.md |
| 7 | "enabling agents" mentioned but undefined/unimplemented | MINOR | build/SKILL.md |
| 8 | Bilingual terminology mixing within single files | MINOR | status-icons.md, audit agents |

### Recommended Fixes (Priority Order)

1. **Fix reviewer examples (#2)** -- update `<example>` blocks in `security-reviewer.md`, `logic-reviewer.md`, `quality-reviewer.md` to show coder as sender
2. **Fix arena naming (#1)** -- use "Arena Moderator" consistently, consider renaming slug from `team-lead` to `moderator`
3. **Fix web researcher (#4)** -- either create `web-researcher.md` agent or replace all mentions with "general-purpose researcher"
4. **Fix Explore vs codebase-researcher (#5)** -- align `conventions/SKILL.md` to use `team:codebase-researcher`
5. **Remove phantom references (#7)** -- delete "enabling agents" from build/SKILL.md
6. **Remove dual naming (#3)** -- drop "(TaskOrchestrator)" from supervisor.md
7. **Create terminology glossary** -- `references/glossary.md` as single source of truth

---

## 7. Deterministic Scripts

> **Experts:** Kelsey Hightower, Martin Fowler, Troy Hunt

### Current State

| Location | Scripts | Status |
|----------|---------|--------|
| `scripts/bump-version.sh` | 1 | Well-written (set -euo pipefail, validation, clear errors) |
| Plugin skill `scripts/` directories | 0 | **None exist** |
| CI inline shell | ~130 lines | Duplicates logic from bump-version.sh |

### 20+ Shell Recipes Embedded in Agent Prose

The audit plugin agents (`feature-scanner.md`, `features-auditor.md`, `usage-analyzer.md`) contain 20+ raw grep/find/git recipes that the LLM must reconstruct every invocation.

### Recommended Scripts

| Script | Location | Replaces |
|--------|----------|----------|
| `scan-unused-exports.sh` | `audit/skills/audit/scripts/` | feature-scanner grep recipes |
| `trace-dependencies.sh` | `audit/skills/audit/scripts/` | usage-analyzer dependency trace |
| `find-dead-code.sh` | `audit/skills/audit/scripts/` | features-auditor analysis |
| `git-activity-report.sh` | `audit/skills/audit/scripts/` | feature-scanner stale detection |
| `detect-naming-conventions.sh` | `team/skills/conventions/scripts/` | conventions pattern discovery |
| `run-all-checks.sh` | `team/skills/build/scripts/` | build Phase 3 integration check |
| `validate-plugins.sh` | `scripts/` | validate.yml inline shell |

Each script must: use `set -euo pipefail`, include `--help`, return descriptive error messages, exit non-zero on failure.

---

## 8. Error Handling & Edge Cases

> **Experts:** Troy Hunt, Martin Kleppmann, Theo Browne

### Assessment Matrix

| Skill/Agent | Stuck Protocol | Failure Fallbacks | Edge Cases | Tool Availability | Overall |
|-------------|:-:|:-:|:-:|:-:|:-:|
| `/build` | 10 scenarios | Researcher fallback tree | Documented | TOOL_UNAVAILABLE event | **EXCELLENT** |
| supervisor | 6 playbooks | Staged intervention | Documented | TOOL_UNAVAILABLE event | **EXCELLENT** |
| coder | Decision policy | Partial | Partial | No | GOOD |
| `/arena` | Intervention table | No | Partial | No | MODERATE |
| `/brief` | No | No | Adaptive behavior | No | MODERATE |
| `/audit` | No | No | Safety rules | No | MODERATE |
| `/conventions` | No | No | No | No | **POOR** |
| `/think` | No | No | No | No | **POOR** |

### Required Additions

**`/think`:** Fallback for partial expert results, directory creation check, timeout handling

**`/conventions`:** Researcher failure fallback tree, command verification failure handling, write error handling

**`/arena`:** Researcher/expert spawn failure handling, explicit timeout mechanism

**`/brief`:** Phase 0 researcher failure fallback, `/build` handoff failure handling

**`/audit`:** Scanner agent failure handling, stack-agnostic language

---

## 9. Validation Process

> **Experts:** Kent C. Dodds, Troy Hunt, Kelsey Hightower

### Current State

| What's Validated | How | Gap |
|------------------|-----|-----|
| JSON syntax (marketplace.json, plugin.json) | CI (`jq`) | None |
| Version consistency | CI (bash) | None |
| Description consistency | CI (bash) | None |
| **SKILL.md frontmatter** | **Nothing** | **HIGH** |
| **SKILL.md line count** | **Nothing** | **HIGH** |
| **Skill discoverability** | **Nothing** | **HIGH** |
| **Logic simulation** | **Nothing** | **MEDIUM** |
| **Edge case testing** | **Nothing** | **MEDIUM** |

### Recommended Two-Phase Approach

**Phase 1: Schema-Based CI Validation** (add to `validate.yml`)
- SKILL.md frontmatter: name matches directory, description <1024 chars, required fields present
- SKILL.md body: line count <500
- Agent definitions: required YAML frontmatter fields, tool lists valid
- Implement as `scripts/validate-skills.sh`

**Phase 2: LLM-Based Discovery Validation** (manual workflow)
- For each skill, feed frontmatter to LLM
- Generate 3 positive + 3 negative trigger prompts
- Score routing accuracy
- Run as `workflow_dispatch` (not on every push due to API cost)

---

## 10. Template & Asset Usage

> **Experts:** Sam Newman, Martin Fowler, Theo Browne

### Assessment

| Metric | Value |
|--------|-------|
| Plugins with `assets/` directories | 0 of 4 |
| Plugins with `references/` directories | 1 of 4 (team) |
| Agents with concrete inline templates | **20 of 20 (100%)** |
| Skills with concrete inline templates | **6 of 6 (100%)** |
| Prose-only output descriptions (the anti-pattern) | **0 found** |

### Verdict: COMPLIANT (Intent Met)

The project achieves the intent of "Provide Concrete Templates" through inline code block templates and the `references/` directory. Every agent and skill has concrete, copy-pasteable output format blocks. The `references/` directory serves the same purpose as `assets/`. The naming convention differs but the substance is fully present.

**No action needed.**

---

## Implementation Plan

### Phase 1: Critical (HIGH priority)

- [ ] **Rewrite all 6 skill descriptions** with third-person voice, trigger optimization, and negative triggers
- [ ] **Extract `build/SKILL.md`** -- move ~437 lines to `references/`, fix 3 dead references, target <500 lines
- [ ] **Fix reviewer example inconsistency** -- update 3 reviewer agents to show coder as sender (not Lead)
- [ ] **Add `scripts/validate-skills.sh`** to CI -- frontmatter validation, line count check
- [ ] **Remove "enabling agents" phantom references** from build/SKILL.md

### Phase 2: Important (MEDIUM priority)

- [ ] **Add error handling sections** to `/think`, `/conventions`, `/arena`, `/brief`, `/audit`
- [ ] **Fix arena terminology** -- "Arena Moderator" consistently, consider slug rename
- [ ] **Fix voice** in all 6 SKILL.md files -- convert to third-person imperative
- [ ] **Create audit plugin scripts** -- `scan-unused-exports.sh`, `trace-dependencies.sh`, `find-dead-code.sh`, `git-activity-report.sh`
- [ ] **Fix web researcher phantom** -- create agent definition or rename to "general-purpose researcher"
- [ ] **Align conventions SKILL** to use `team:codebase-researcher` instead of `Explore`

### Phase 3: Polish (LOW priority)

- [ ] **Fix voice** in all 13+ agent definitions -- convert "You are a..." to third-person/bare imperative
- [ ] **Add JiT loading trigger** in `brief/SKILL.md` for `interview-principles.md`
- [ ] **Create `scripts/validate-plugins.sh`** -- extract CI inline shell to reusable script
- [ ] **Create `run-all-checks.sh`** and `detect-naming-conventions.sh` scripts for team plugin
- [ ] **Create terminology glossary** at `references/glossary.md`
- [ ] **Remove "TaskOrchestrator" dual naming** from supervisor.md
- [ ] **Add LLM-based discovery validation** as manual CI workflow

---

## Success Metrics

| Metric | Baseline (Current) | Target |
|--------|:------------------:|:------:|
| Skills with compliant directory structure | 5/6 (83%) | 6/6 (100%) |
| Skills with negative triggers in description | 0/6 (0%) | 6/6 (100%) |
| Skills under 500-line limit | 5/6 (83%) | 6/6 (100%) |
| Terminology inconsistencies | 8 | 0 |
| Skills with error handling sections | 2/6 (33%) | 6/6 (100%) |
| Skill-level validation checks in CI | 0 | 5+ checks |
| Deterministic scripts for repetitive ops | 0 | 7 scripts |
| Skills with third-person imperative voice | 0/6 (0%) | 6/6 (100%) |
