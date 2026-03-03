---
name: think
description: >-
  Performs deep structured thinking by breaking a task into aspects, dispatching
  parallel expert analysts, and producing a unified design document with
  recommendations. Use when the user wants to think through a complex problem,
  plan an architecture, or analyze trade-offs before implementing. Don't use
  for implementation, quick questions, expert debates (use /arena), or simple
  tasks that don't need multi-aspect analysis.
argument-hint: "<task or idea to think through>"
model: opus
---

# Structured Thinking

The skill helps think through a task before implementation, working in three stages.

## Stage 1: Task Breakdown

First, identify **aspects to think through** — parts of the task that need decisions.

Choose a **main expert** for analyzing the task as a whole.

**Output format:**

```
## Understanding the Task

[How you understood the task — 1-2 sentences]

---

### Expert Perspective

> "Analyzing as [Main Expert] because [reason]"
>
> **Principles from 3 experts:**
> 1. [Expert A]: "[principle]"
> 2. [Expert B]: "[principle]"
> 3. [Expert C]: "[principle]"

---

## Aspects to Think Through

| # | Aspect | Why Important | Expert |
|---|--------|---------------|--------|
| 1 | [Name] | [Why needs thinking] | [Who will analyze] |
| 2 | ... | ... | ... |
...
```

Usually 5-10 aspects. No more than 15.

### Expert Table

The full expert table with domains, names, and principles is defined in the `think:expert` agent definition. For other areas — find appropriate specialists.

## Stage 2: Project Study

After breakdown, tell the user:

> "Identified N aspects. Now I'll study the project and launch experts for each. 🐙"

Then launch **in parallel** `think:expert` agents — one per aspect:

**Dispatch decision tree:**

```mermaid
flowchart TD
    A{"Aspects identified?"}
    A -->|0| SIMPLE["Report: task is too simple<br/>for multi-aspect analysis"]
    A -->|1-2| FEW["Launch experts + warn:<br/>Few aspects — consider if /think is needed"]
    A -->|3-15| STD["Launch all in parallel<br/>(standard path)"]
    A -->|>15| GROUP["Group related aspects<br/>(max 15 agents), note groupings"]
```

**Partial returns:** If fewer than half the experts return, compile available results with a warning. If none return, report failure.

```
Task(think:expert): "Aspect: [aspect name]. Task context: [brief context]. Study the project and propose solution options."
```

**IMPORTANT:** Launch all agents in ONE message in parallel.

## Error Handling

| Situation | Action |
|-----------|--------|
| Expert agent fails or returns empty | Compile partial results from successful experts. Note which aspects were not analyzed. |
| Fewer than half the experts return | Compile available results with a warning: "Partial analysis — N of M aspects covered." |
| All experts fail | Report failure to user. Suggest retrying with fewer aspects or checking tool availability. |
| `docs/plans/` directory does not exist | Create it before saving. |
| Save fails | Output the document directly to the user instead of saving to file. |

## Stage 3: Summary Document

When all agents return results, create a **unified document** in the format:

```markdown
# [Task Name]

> **Status:** Research complete
> **Date:** [date]
> **Goal:** [brief goal description]

---

## Table of Contents

1. [Overview](#overview)
2. [Aspect 1](#1-name)
3. [Aspect 2](#2-name)
...
N. [Implementation Plan](#implementation-plan)

---

## Overview

### Goals

1. **[Goal 1]** — description
2. **[Goal 2]** — description
...

### Key Decisions

| Aspect | Decision |
|--------|----------|
| [Aspect 1] | [Brief decision] |
| [Aspect 2] | [Brief decision] |
...

---

## 1. [Aspect Name]

> **Experts:** [Expert 1], [Expert 2], [Expert 3]

### [Subsection with solution]

[Detailed description of chosen option]

| Aspect | Details |
|--------|---------|
| ... | ... |

### [Code/examples if needed]

\`\`\`typescript
// Example code
\`\`\`

---

## 2. [Next Aspect]
...

---

## Implementation Plan

### Phase 1: MVP

- [ ] Task 1
- [ ] Task 2
...

### Phase 2: ...

---

## Success Metrics

| Metric | Baseline | Target |
|--------|----------|--------|
| ... | — | ... |
```

### Diagrams

When the document needs flow diagrams, architecture overviews, or process visualizations — use **mermaid `flowchart TD`** code blocks (` ```mermaid `). Never use ASCII box-drawing art for diagrams in `.md` files.

**Save the document** to `docs/plans/YYYY-MM-DD-[topic]-design.md`

At the end, ask:

> "Summary is ready and saved to `docs/plans/...`. Which aspects would you like to discuss further? Or ready to implement?"
