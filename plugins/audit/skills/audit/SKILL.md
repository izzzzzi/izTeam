---
name: audit
description: >-
  Conducts an interactive feature audit to find dead code, abandoned
  experiments, and unused features, then asks the user about each one. Use when
  the user wants to clean up the codebase, find unused code, or review
  experimental features. Don't use for security audits, performance profiling,
  dependency scanning, or code quality reviews.
allowed-tools:
  - Task
  - Read
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
argument-hint: "[scope: features | server | ui | stores | all]"
model: opus
---

# Vibe Audit — Interactive Feature Cleanup

The audit skill finds potentially dead or experimental code and **asks the user** whether it's still needed.

## Philosophy

In vibe-coding, lots of experimental code gets created. Some becomes core features, some gets abandoned. This skill identifies what's what through **conversation**, not assumptions.

## Workflow

### Step 1: Discovery

Run the appropriate agent based on scope (see "Scope Options" below):

```
# Default or "all"
Task(audit:feature-scanner) - "Scan codebase for potentially unused features"

# Specific scopes
Task(audit:features-auditor) - "Audit src/features/ for unused exports"
Task(audit:server-auditor) - "Audit src/server/ for unused procedures"
Task(audit:ui-auditor) - "Audit src/design-system/ for orphan components"
Task(audit:stores-auditor) - "Audit src/stores/ for dead Zustand slices"
```

### Step 2: Interactive Review

Loop through findings ONE BY ONE. Each iteration of the loop is:
1. Show context for the current item (text output)
2. Call AskUserQuestion ONCE with exactly 1 question about this item
3. STOP. Wait for the user's response. Do NOT call any other tool in this message.
4. After the user responds, proceed to the next item

**NEVER call AskUserQuestion more than once per message.** Do not make parallel AskUserQuestion calls. Do not ask about item 2 until the user has answered about item 1.

```
# For item N of M:

# First, output context as text:
"📦 **{feature_name}** ({N}/{M})
Files: {file_list}
Usage: {usage_description}
Last commit: {date}"

# Then make exactly ONE tool call:
AskUserQuestion(questions=[{
  question: "What should we do with {feature_name}?",
  header: "{feature_name}",
  options: [
    {label: "Delete", description: "This is dead code — remove it"},
    {label: "Deprecated", description: "Remove soon — mark as deprecated"},
    {label: "Keep", description: "This is an active feature — keep it"},
    {label: "Not sure", description: "Needs deeper investigation before deciding"}
  ],
  multiSelect: false
}])

# STOP HERE. Do not call any other tool. Wait for user response.
# After user responds → repeat for item N+1.
```

If the user answers "Not sure", spawn `audit:usage-analyzer` for that item and return to ask again after analysis.

### Step 3: Generate Report

After all questions answered, create action plan:

```markdown
# 🧹 Vibe Audit Report

## Decisions

### 🗑️ To Delete
- [feature] — reason: [user's answer]

### ⚠️ Deprecated
- [feature] — remove by: [date]

### ✅ Keep
- [feature] — document: [what it does]

## Next Steps
1. [ ] Delete [X] files
2. [ ] Add @deprecated to [Y]
3. [ ] Update documentation for [Z]
```

## Question Templates

When asking about a feature, provide context:

```
📦 **{feature_name}**

What was found:
- Files: {file_count} ({file_list})
- Usage: {usage_description}
- Last commit: {last_commit_date}
- Dependencies: {dependencies}

Is this needed?
```

## Scope Options

| Scope | Agent | Target |
|-------|-------|--------|
| **features** | `features-auditor` | `src/features/` — unused exports, dead code |
| **server** | `server-auditor` | `src/server/` — unused tRPC procedures, services |
| **ui** | `ui-auditor` | `src/design-system/` — orphan components |
| **stores** | `stores-auditor` | `src/stores/` — dead Zustand slices |
| **all** | `feature-scanner` | Full codebase scan |

### Agent Selection

```mermaid
flowchart TD
    S{"Scope argument?"}
    S -->|empty / all| FS["feature-scanner<br/>full codebase scan"]
    S -->|features| FA["features-auditor<br/>src/features/ analysis"]
    S -->|server| SA["server-auditor<br/>src/server/ analysis"]
    S -->|ui| UA["ui-auditor<br/>src/design-system/ analysis"]
    S -->|stores| STA["stores-auditor<br/>src/stores/ analysis"]
    S -->|all explicit| ALL["Run ALL in parallel"]
    ALL --> FS2["feature-scanner"]
    ALL --> FA2["features-auditor"]
    ALL --> SA2["server-auditor"]
    ALL --> UA2["ui-auditor"]
    ALL --> STA2["stores-auditor"]
```

## Error Handling

| Situation | Action |
|-----------|--------|
| Scanner agent fails or returns empty | Inform user: "Scan returned no results. Try narrowing scope." Suggest specific directories. |
| Partial scan results | Report what was found. Note which areas were not scanned. |
| Git operations fail in cleanup | Stop cleanup immediately. Report error. Do not proceed with further deletions. |
| TypeScript check fails after deletion | Report which deletion caused the failure. Suggest rollback via git. |
| Project does not use expected stack (no tRPC, no Zustand, etc.) | Adapt scanning patterns to the actual stack. Skip inapplicable auditors. |

## Important Rules

1. **Never delete without confirmation** — the cleanup-executor agent enforces this with git backup
2. **ONE AskUserQuestion per message** — never call AskUserQuestion more than once in a single response. Never make parallel AskUserQuestion calls. Each response must contain at most one AskUserQuestion call, then STOP and wait. This is the most important rule.
3. **Provide context** — show findings before asking
4. **Accept "not sure"** — some things need more investigation, spawn usage-analyzer
5. **Track decisions** — remember what user said for the report
