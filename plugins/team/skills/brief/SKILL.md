---
name: brief
description: >-
  Conducts a short adaptive interview (2-6 questions) to understand the user's
  intent before implementation, then compiles a brief and hands off to /build.
  Use when the user asks to discuss a feature before building, wants to be
  interviewed first, or says 'ask me questions'. Don't use when the user
  already has a detailed spec, wants to jump straight into coding, or invokes
  /build directly.
allowed-tools:
  - Task
  - Read
  - Grep
  - Glob
  - AskUserQuestion
  - Skill
model: opus
---

# Brief — Adaptive Interview Before Implementation

Conducts a short adaptive interview to understand the user's intent, then compiles a brief and hands off to `/build`.

## Core Principle

`/build` is fully autonomous — it infers tech stack, patterns, risks, complexity. The interview captures only **intent and business context** that code scanning cannot reveal.

**DO NOT ASK:** tech stack, affected files, architecture, risks, implementation approach.
**ASK:** what to build, why, who it's for, what success looks like, what's out of scope.

## Protocol

- **ONE AskUserQuestion per message, then STOP.** Never call AskUserQuestion more than once in a single response. Never make parallel AskUserQuestion calls. After calling AskUserQuestion — do NOT call any other tool. Wait for the user's response.
- Skip questions already answered in initial message
- 2-6 questions, under 5 minutes
- **HARD GATE:** No implementation until brief is compiled and user confirms via AskUserQuestion.
- **NEVER invoke /build without explicit user approval** in Phase 3 confirmation.

---

## Phase 0: Project Study (parallel, while greeting user)

Launch researchers to understand the project and generate smart button options:

```
Task(subagent_type="team:codebase-researcher",
  prompt="Quick scan: tech stack, project structure, existing features, conventions,
  user-facing features/roles/flows, architecture layers, data sources, main modules.")
```

While waiting, greet: "I'll ask a few quick questions to make sure I build exactly what you need. Takes 2-3 minutes."

Use findings to populate button options in subsequent questions.

---

## Phase 1: Core Questions (2-4 questions, adaptive)

### Q1 — Intent (always ask unless initial message is detailed)

**"What will change when this works — and for whom?"**

```
AskUserQuestion(
  questions=[{
    "question": "What should change when this feature works? Who will notice the difference?",
    "header": "Feature",
    "options": [
      // Generate 2-3 from researcher findings:
      {"label": "Improve [existing feature]", "description": "Make [X] work better for [users]"},
      {"label": "Add new [capability]", "description": "Users will be able to [Y]"}
    ],
    "multiSelect": false
  }]
)

# STOP HERE. Do not call any other tool. Wait for user response.
# After user responds → proceed to next question or Phase 2.
```

If answer is vague (< 15 words): propose 2-3 hypothesis buttons (Branch B: "Which of these is closest?").

### Q2 — Audience (only if Q1 didn't reveal who)

**"Who will use this most?"** — build options from researcher findings (existing roles). Use `multiSelect: true`.

### Q3 — Success criteria (only if Q1 was abstract)

**"How will you know it's working?"** — skip if Q1 was already concrete ("clients can export invoices as PDF").

### Q4 — Exclusions (optional, when scope seems broad)

**"Anything that must NOT be included?"** — without this, `/build` builds maximum scope. Use `multiSelect: true`.

---

## Phase 2: AI-Generated Follow-ups (0-2 questions)

Ask a follow-up ONLY when:
- Ambiguity: answer could mean two different implementations
- Contradiction: user said X but project context suggests Y
- Critical unknown specific to THIS feature
- User hints at deeper context not yet shared

Frame as button choices (2-4 options), not open questions. Examples of good follow-ups:
- "You mentioned 'admin panel' — should admins see all users' data, or only their team's?"
- "Your project has email notifications for orders. Should this feature also send notifications?"
- "This would change how [existing feature] works. Is that intentional?"

**DO NOT ask** about tech stack, architecture, testing, timeline, or effort — agents handle these.

**Max 2 follow-ups.** If still unclear after 6 total → compile what is known, note uncertainties.

---

## Error Handling

| Situation | Action |
|-----------|--------|
| Researcher fails in Phase 0 | Proceed without project context, ask more questions |
| User abandons interview | Save partial brief, do not invoke /build |
| /build handoff fails | Save brief to `.briefs/`, inform user |
| All researchers fail | Proceed interview-only, mark "NO PROJECT CONTEXT" |

---

## Phase 3: Brief Compilation, Approval & Handoff

See `references/brief-template.md` for the full compilation template.

1. Compile brief from interview answers + researcher findings
2. Show the brief as text output
3. **MANDATORY confirmation** — call AskUserQuestion:

```
AskUserQuestion(
  questions=[{
    "question": "Here's the plan I'll send to the build team. All correct?",
    "header": "Launch?",
    "options": [
      {"label": "Looks good, launch!", "description": "Save the plan and start building"},
      {"label": "I want to adjust", "description": "Let me change something first"}
    ],
    "multiSelect": false
  }]
)

# STOP HERE. Wait for user response.
# "Looks good" → save and hand off to /build
# "I want to adjust" → ask what to change, update brief, show again, re-confirm
```

4. **ONLY after user confirms** → save to `.briefs/[feature-name-kebab-case].md`
5. Hand off: `Skill("build", args=".briefs/[feature-name].md --no-research")`

**NEVER skip this confirmation.** Even if the user seems eager, always show the compiled brief and wait for approval before invoking /build.

---

## Adaptive Behavior Summary

| User's initial message | Interview path | Questions |
|------------------------|---------------|-----------|
| Detailed with audience + success criteria | Confirm → Q4 → Launch | 1-2 |
| Clear feature, missing context | Q1 (refine) → Q3 → Launch | 2-3 |
| Vague idea ("improve the dashboard") | Q1 → Branch B → Q2 → Q3 → Q4 → Launch | 4-5 |
| Very vague ("make it better") | Q1 → Branch B → follow-ups → Q3 → Q4 → Launch | 5-6 |

The interview should feel like a **2-minute conversation**, not a form.

When adapting to edge cases, read `references/interview-principles.md` for expert rationale.
