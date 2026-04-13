# Detailed Best Practices Audit: izteam vs mgechev/skills-best-practices README

> **Status:** Research complete
> **Date:** 2026-03-01
> **Goal:** Line-by-line verification of every requirement from the [skills-best-practices README](https://github.com/mgechev/skills-best-practices/blob/main/README.md) against our 6 skills and 20 agents

---

## Table of Contents

1. [Overview](#overview)
2. [Directory Structure](#1-directory-structure)
3. [Frontmatter Name](#2-frontmatter-name)
4. [Frontmatter Description](#3-frontmatter-description)
5. [Line Count (<500)](#4-line-count)
6. [Progressive Disclosure & JiT](#5-progressive-disclosure--jit)
7. [Instruction Style](#6-instruction-style)
8. [Terminology Consistency](#7-terminology-consistency)
9. [Deterministic Scripts](#8-deterministic-scripts)
10. [Validation Process](#9-validation-process)
11. [Anti-Patterns](#10-anti-patterns)
12. [Implementation Plan](#implementation-plan)

---

## Overview

### Compliance Scorecard

| # | Best Practice | Compliance | Grade | Priority |
|---|--------------|:----------:|:-----:|:--------:|
| 1 | Directory Structure (SKILL.md + scripts/ + references/ + assets/) | 38% | D | **HIGH** |
| 2 | Frontmatter Name (format, match dir) | 100% | A+ | -- |
| 3 | Frontmatter Description (triggers, voice, length) | 95% | A | LOW |
| 4 | Line Count (<500 lines) | 100% | A+ | -- |
| 5 | Progressive Disclosure & JiT Loading | 90% | A | LOW |
| 6 | Instruction Style (procedural, voice, templates) | 65% | C | **HIGH** |
| 7 | Terminology Consistency | 55% | D | **HIGH** |
| 8 | Deterministic Scripts & Error Handling | 35% | F | **HIGH** |
| 9 | Validation Process (4 LLM-based steps) | 20% | F | MEDIUM |
| 10 | Anti-Patterns (no docs, no redundancy, no library code) | 70% | C+ | MEDIUM |

**Overall: 67% compliance** (up from ~45% before first audit round)

### Key Decisions

| Aspect | Decision |
|--------|----------|
| Directory Structure | Add scripts/ and references/ only where meaningful (Option B: Justified Compliance) |
| Frontmatter Name | No action needed -- 100% compliant |
| Frontmatter Description | Minor: sharpen build description positive trigger |
| Line Count | No action needed -- all under 500 |
| Progressive Disclosure | Minor: strengthen status-icons JiT trigger |
| Instruction Style | Fix build voice (You->third person), add decision trees to think/arena |
| Terminology | Create glossary, fix phantom roles, standardize web researcher naming |
| Scripts | Extract audit plugin inline bash to scripts/, enhance validate-skills.sh errors |
| Validation Process | Create manual playbook first, then workflow_dispatch automation |
| Anti-Patterns | Extract implementation detail from SKILL.md files to references/ |

---

## 1. Directory Structure

> **Experts:** Sam Newman, Martin Fowler, Kent C. Dodds

### Required structure per skill

```
skill-name/
├── SKILL.md       # Required
├── scripts/       # Executable code
├── references/    # Supplementary context, one level deep
└── assets/        # Templates or static files
```

### Audit results

| Skill | SKILL.md | scripts/ | references/ | assets/ | Score |
|-------|:--------:|:--------:|:-----------:|:-------:|:-----:|
| arena | PASS | FAIL | FAIL | FAIL | 1/4 |
| audit | PASS | FAIL | FAIL | FAIL | 1/4 |
| build | PASS | FAIL | PASS (6 files) | FAIL | 2/4 |
| brief | PASS | FAIL | PASS (1 file) | FAIL | 2/4 |
| conventions | PASS | FAIL | FAIL | FAIL | 1/4 |
| think | PASS | FAIL | FAIL | FAIL | 1/4 |

**Compliance: 8/24 = 33%**

### Gaps

- **scripts/**: 0/6 skills have it. Audit plugin has 25+ inline bash blocks that should be extracted. Other skills use Claude tool APIs and don't need scripts.
- **references/**: 4/6 skills lack it. Arena (expert personas, synthesis template), conventions (researcher prompts, output templates), and audit (report/question templates) have extractable content.
- **assets/**: 0/6 skills have it. Build's `state-template.md` and `summary-report-template.md` are arguably templates (assets), not reference material. Arena's synthesis document template, audit's report template, and brief's brief template are output artifacts.

### Action items

- [ ] Create `plugins/audit/skills/audit/scripts/` with 4 extracted scripts
- [ ] Create `plugins/arena/skills/arena/references/` -- extract expert personas, synthesis template
- [ ] Create `plugins/team/skills/conventions/references/` -- extract researcher prompts, output templates
- [ ] Evaluate moving build templates from `references/` to `assets/`

---

## 2. Frontmatter Name

> **Experts:** Troy Hunt, Theo Browne

### Rules

- 1-64 characters, lowercase letters + numbers + hyphens only, no consecutive hyphens, must match parent directory

### Audit results

| Skill | name value | Chars | Valid chars | No `--` | Matches dir | Status |
|-------|-----------|:-----:|:-----------:|:-------:|:-----------:|:------:|
| arena | `arena` | 5 | PASS | PASS | PASS | PASS |
| audit | `audit` | 5 | PASS | PASS | PASS | PASS |
| build | `build` | 5 | PASS | PASS | PASS | PASS |
| brief | `brief` | 5 | PASS | PASS | PASS | PASS |
| conventions | `conventions` | 11 | PASS | PASS | PASS | PASS |
| think | `think` | 5 | PASS | PASS | PASS | PASS |

**Compliance: 30/30 = 100%. No action needed.**

---

## 3. Frontmatter Description

> **Experts:** Nir Eyal, Sam Newman, Troy Hunt

### Rules

- Max 1024 characters, third-person voice, negative triggers, trigger-optimized

### Audit results

| Skill | Chars | Third person | Negative triggers | Trigger quality | Score |
|-------|:-----:|:------------:|:-----------------:|:---------------:|:-----:|
| arena | 354 | YES | YES (4 exclusions) | Excellent | A |
| audit | 336 | YES | YES (4 exclusions) | Excellent | A |
| build | 276 | YES | YES (4 exclusions) | **Partial** | B+ |
| brief | 390 | YES | YES (3 exclusions) | Excellent (literal phrases) | A+ |
| conventions | 386 | YES | YES (4 exclusions) | Excellent | A |
| think | 422 | YES | YES (4 + redirect hint) | Excellent | A+ |

### One improvement opportunity

**build** description: "build a feature or implement functionality" is generic and risks false-positive activation. Suggested improvement: "build a complex feature requiring coordinated multi-file implementation" to distinguish from simple coding requests.

---

## 4. Line Count

> **Experts:** Martin Fowler, Sam Newman

### Audit results

| Skill | Total lines | Body lines | Status | Headroom |
|-------|:-----------:|:----------:|:------:|:--------:|
| arena | 359 | 335 | PASS | 141 lines |
| audit | 143 | 125 | PASS | 357 lines |
| build | 442 | 418 | PASS | **58 lines** |
| brief | 330 | 319 | PASS | 170 lines |
| conventions | 224 | 204 | PASS | 276 lines |
| think | 187 | 175 | PASS | 313 lines |

**Compliance: 6/6 = 100%. No action needed.** Build at 88% capacity -- monitor when adding features.

---

## 5. Progressive Disclosure & JiT

> **Experts:** Dan Abramov, Rich Hickey, Sam Newman

### Audit results

| Check | Result | Details |
|-------|:------:|---------|
| References one level deep | PASS | All flat, no nested directories |
| JiT loading patterns | 8/9 GOOD | 1 weak: status-icons at build:286 lacks conditional trigger |
| Relative paths with `/` | PASS | Zero violations |
| No anti-pattern docs in skills | PASS | No README/CHANGELOG inside skill dirs |
| No library code | PASS | No scripts/ exist |
| `@references/` paths valid | PASS | All 4 resolve to real files |

**Compliance: ~95%. One minor fix.**

### Action item

- [ ] Strengthen build/SKILL.md line 286: change "using emoji from `@references/status-icons.md`" to "When outputting team status trees, read `@references/status-icons.md` for the canonical emoji set"

---

## 6. Instruction Style

> **Experts:** Minko Gechev, Martin Fowler, Kent C. Dodds

### Rules

- Step-by-step numbering, decision trees, third-person imperative voice, concrete templates, consistent terminology

### Audit results

| Skill | Steps | Decision Trees | Voice | Templates | Overall |
|-------|:-----:|:--------------:|:-----:|:---------:|:-------:|
| arena | GOOD | NEEDS_WORK | NEEDS_WORK | EXCELLENT | GOOD |
| audit | GOOD | NEEDS_WORK | GOOD | EXCELLENT | GOOD |
| build | EXCELLENT | EXCELLENT | **POOR** | EXCELLENT | GOOD* |
| brief | EXCELLENT | GOOD | NEEDS_WORK* | EXCELLENT | EXCELLENT |
| conventions | EXCELLENT | GOOD | EXCELLENT | EXCELLENT | EXCELLENT |
| think | GOOD | **POOR** | NEEDS_WORK | GOOD | GOOD |

*build is dragged down by 9+ "You/Your" violations. brief voice issues are in UI template strings (acceptable).

### Critical findings

**build/SKILL.md -- 9+ second-person violations:**
- "**You** make ALL decisions yourself" (Philosophy section)
- "**Your** context is precious"
- "**You** read these yourself"
- "**You** can also dispatch researchers mid-session"
- Entire Philosophy and Key Rules sections in second person

**think/SKILL.md -- zero decision trees:**
- No branching logic for Stage 2 (expert dispatch)
- No handling of partial returns or minimum aspect count
- Stage 2 is only 5 lines of instruction

**arena/SKILL.md -- mixed Russian voice:**
- Some lines use infinitive (correct): "Запустить 2-4 агента"
- Others use 2nd-person imperative (incorrect): "собери находки"

### Action items

- [ ] Rewrite build Philosophy + Key Rules from "You" to third-person imperative
- [ ] Add decision tree to think Stage 2 for expert dispatch/partial returns
- [ ] Add convergence decision tree to arena Phase 4
- [ ] Normalize arena Russian voice to infinitive form
- [ ] Add ASCII decision tree to audit scope routing

---

## 7. Terminology Consistency

> **Experts:** Martin Kleppmann, Martin Fowler, Sam Newman

### Findings (9 total)

**CRITICAL -- Phantom roles (references to things that don't exist):**

| # | Phantom Role | Location | Problem |
|---|-------------|----------|---------|
| 1 | "deep-analysis agents" | team/README.md:102,141 | No agent definition, no spawn pattern |
| 2 | "backup reviewer routing" | supervisor.md:348 | No mechanism defined anywhere |
| 3 | "web researcher" / "web-research agent" | build/SKILL.md:137,161; codebase-researcher.md:110,116 | 3 names for the same concept, no dedicated agent file |

**HIGH -- Synonym drift:**

| # | Concept | Canonical | Drift variants | Where |
|---|---------|-----------|----------------|-------|
| 4 | Exemplary code | "gold standard" | "reference file", "canonical example", "few-shot example" | reference-researcher.md, build/SKILL.md |
| 5 | Team agent | "teammate" | "team member" | supervisor.md uses both; coder.md uses "team member" |
| 6 | State artifact | "state.md" | "state file", "operational state" | build/SKILL.md, state-template.md |
| 7 | Capitalization | varies | "GOLD STANDARD BLOCK" vs "Gold Standard Block" vs "gold standards" | reference-researcher.md:88 vs :95 |

**MEDIUM -- Mixed language / naming:**

| # | Issue | Location |
|---|-------|----------|
| 8 | Arena/audit agents entirely in Russian; team/think in English | plugins/arena/, plugins/audit/ |
| 9 | "Command" in README vs "skill" internally | README.md:33 vs all SKILL.md files |

### Action items

- [ ] Remove "deep-analysis agents" from team/README.md (or define what it means)
- [ ] Remove "backup reviewer routing" from supervisor.md (or define mechanism)
- [ ] Standardize web researcher naming to one term across all files
- [ ] Create `.conventions/glossary.md` with canonical terms
- [ ] Standardize capitalization: "Gold Standard Block" (title case) for the artifact

---

## 8. Deterministic Scripts

> **Experts:** Kelsey Hightower, Troy Hunt, Martin Fowler

### Compliance: 35/100

| Criterion | Score | Notes |
|-----------|:-----:|-------|
| Skills with scripts/ directory | 0/6 | None |
| Repetitive operations scripted | 0/25+ | All inline bash in audit agents |
| Root scripts: descriptive errors | 60% | bump-version.sh good; validate-skills.sh terse |
| Root scripts: stderr/stdout separation | 0% | All to stdout |
| Root scripts: agent self-correction | 30% | No FIX instructions in error messages |

### Key gap: audit plugin

25+ inline bash blocks in 6 audit agent files:
- `cleanup-executor.md` -- 6 bash blocks (git, grep, rm, tsc)
- `feature-scanner.md` -- 3 bash blocks (grep pipelines, git log)
- `usage-analyzer.md` -- 5 bash blocks (grep, git log, find+xargs)
- `stores-auditor.md` -- 3 bash blocks (find, grep, sort+uniq)

### Action items

- [ ] Create `plugins/audit/skills/audit/scripts/` with extracted scripts:
  - `scan-orphan-routes.sh` -- tRPC route usage
  - `analyze-feature-usage.sh` -- import/route/git analysis
  - `safe-cleanup.sh` -- git branch + remove + verify + commit
  - `find-dead-exports.sh` -- export scanning
- [ ] Enhance `scripts/validate-skills.sh`:
  - Route errors to stderr (`>&2`)
  - Add FIX remediation to every `fail()` call
  - Add heuristic checks: description starts with verb, negative trigger presence, error handling section exists
- [ ] Update audit agent `.md` files to reference scripts instead of inline bash

---

## 9. Validation Process

> **Experts:** Kent C. Dodds, Troy Hunt, Kelsey Hightower

### README requires 4 LLM-based validation steps

| Step | Status | What exists |
|------|:------:|-------------|
| 1. Discovery Validation | NOT IMPLEMENTED | No trigger testing |
| 2. Logic Validation | NOT IMPLEMENTED | No execution simulation |
| 3. Edge Case Testing | NOT IMPLEMENTED | No QA testing |
| 4. Architecture Refinement | NOT IMPLEMENTED | No automated restructuring |
| SkillsBench reference | NOT IMPLEMENTED | No evals framework |

### What we DO have

- `scripts/validate-skills.sh` -- schema/structural validation (147 checks)
- `.github/workflows/validate.yml` -- CI integration
- `.conventions/checks/skill-validation.md` -- documented rules (some unenforced)

### Action items (two phases)

**Phase A: Manual playbook (immediate)**
- [ ] Create `docs/validation-playbook.md` with exact LLM prompts for all 4 steps
- [ ] Include scoring rubric (1-10 per step)
- [ ] Add to release checklist

**Phase B: Automation (after 2-3 manual runs)**
- [ ] Create `.github/workflows/llm-validate.yml` (workflow_dispatch)
- [ ] Uses Claude API with structured prompts from playbook
- [ ] Outputs markdown report as workflow artifact
- [ ] Per-skill targeting to control API cost

---

## 10. Anti-Patterns

> **Experts:** Martin Fowler, Sam Newman, Rich Hickey

### 12 violations found

**HIGH -- SKILL.md too implementation-heavy (4 files):**

| # | File | Problem | Lines affected |
|---|------|---------|:-------------:|
| 1 | arena/SKILL.md | Expert personas, synthesis template, commentary table all inlined; no references/ dir | 36-343 |
| 2 | build/SKILL.md | Monitor mode, stuck protocol, researcher dispatch still inline despite 6 references | 96-173, 300-440 |
| 3 | brief/SKILL.md | Full AskUserQuestion blocks, brief template inlined; only 1 reference | 64-316 |
| 4 | conventions/SKILL.md | Researcher prompts, output templates inlined; no references/ dir | 59-204 |

**MEDIUM -- Nested reference chain:**

| # | File | Problem |
|---|------|---------|
| 5 | build/references/risk-analysis-protocol.md:72,106 | Reference file links to another reference (`@references/risk-testing-example.md`) creating multi-hop chain |

**LOW -- Redundant logic (6 instances):**

| # | File | Line | Redundant instruction |
|---|------|:----:|----------------------|
| 6 | arena/SKILL.md | 51 | "REAL people" instruction (agent would default to real experts) |
| 7 | audit/SKILL.md | 139 | "Never delete without asking" (workflow already enforces) |
| 8 | build/SKILL.md | 426 | "Never implement tasks yourself" (follows from procedure) |
| 9 | build/SKILL.md | 427 | "One file = one coder" (follows from task decomposition) |
| 10 | think/SKILL.md | 57-71 | Expert table duplicated in think:expert agent prompt |
| 11 | brief/SKILL.md | 213-219 | "What NOT to ask" repeats lines 19-25 |

### Action items

- [ ] Extract arena implementation detail to references/ (expert personas, synthesis template, commentary)
- [ ] Extract conventions implementation to references/ (researcher prompts, output templates)
- [ ] Extract brief templates to references/ (AskUserQuestion blocks, brief template)
- [ ] Further extract from build: monitor mode, stuck protocol to references/
- [ ] Fix nested reference: inline `@references/risk-testing-example.md` link into build/SKILL.md directly
- [ ] Remove 6 redundant logic items (or document justification for keeping guardrails)

---

## Implementation Plan

### Phase 1: Critical Structure Fixes (HIGH priority)

- [ ] **Fix build voice**: Rewrite Philosophy + Key Rules from "You/Your" to third-person imperative
- [ ] **Fix phantom roles**: Remove "deep-analysis agents" from README, "backup reviewer routing" from supervisor.md
- [ ] **Standardize web researcher naming**: Pick one term, apply across all files
- [ ] **Create audit scripts/**: Extract 4 scripts from inline bash in agent files
- [ ] **Enhance validate-skills.sh**: stderr routing, FIX messages, heuristic voice/trigger checks
- [ ] **Create glossary**: `.conventions/glossary.md` with canonical terms and forbidden synonyms

### Phase 2: Progressive Disclosure Extraction (MEDIUM priority)

- [ ] **arena/SKILL.md**: Create `references/` dir, extract expert personas + synthesis template + commentary rules
- [ ] **conventions/SKILL.md**: Create `references/` dir, extract researcher prompts + output templates
- [ ] **brief/SKILL.md**: Extract AskUserQuestion blocks + brief template to references/
- [ ] **build/SKILL.md**: Extract monitor mode + stuck protocol to references/ (gains ~80 lines headroom)
- [ ] **Fix nested reference**: Move risk-testing-example link from reference file to SKILL.md
- [ ] **Remove redundant logic**: 6 instances across 5 files

### Phase 3: Decision Trees & Validation (LOW priority)

- [ ] **think/SKILL.md**: Add Stage 2 decision tree (expert dispatch, partial returns, min aspects)
- [ ] **arena/SKILL.md**: Add Phase 4 convergence decision tree, normalize Russian voice
- [ ] **audit/SKILL.md**: Convert scope routing table to ASCII decision tree
- [ ] **Sharpen build description**: "implement functionality" -> "coordinated multi-file implementation"
- [ ] **Strengthen JiT trigger**: status-icons reference at build:286
- [ ] **Create validation playbook**: `docs/validation-playbook.md` with LLM prompts for 4 steps
- [ ] **Create LLM validation workflow**: `.github/workflows/llm-validate.yml` (workflow_dispatch)

---

## Success Metrics

| Metric | Current | Target |
|--------|:-------:|:------:|
| Directory structure compliance | 33% (8/24) | 75%+ (justified omissions documented) |
| Frontmatter name compliance | 100% | 100% |
| Description quality (Excellent) | 5/6 | 6/6 |
| Line count (<500) | 100% | 100% |
| Progressive disclosure compliance | 90% | 95%+ |
| Instruction style (voice compliance) | 3/6 | 6/6 |
| Terminology inconsistencies | 9 | 0 |
| Skills with scripts/ (where needed) | 0/1 | 1/1 (audit) |
| validate-skills.sh agent-friendly errors | 30% | 90% |
| Validation process steps implemented | 1/5 (schema only) | 3/5 (schema + playbook + heuristics) |
| Anti-pattern violations | 12 | 3 or fewer |
| Phantom roles | 3 | 0 |
