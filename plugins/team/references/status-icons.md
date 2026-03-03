# Status Icons — Unified Visual Language for the Team

> All team agents use these emoji constants for status messages, activeForm, and tree output. Uniformity improves readability and enables quick parsing of team state.

## Agent States

| Icon | State | When to Use |
|------|-------|-------------|
| 🔍 | Research | File search, Glob/Grep, reading code |
| 🔨 | Implementation | Writing/editing code |
| 📝 | Review | Reviewing another agent's code |
| ⏳ | Waiting | Waiting for a response from another agent |
| 🚀 | Start | Claiming a task, beginning work |
| ✅ | Done | Task/review completed |
| ❌ | Blocker | STUCK, IMPOSSIBLE_WAIT, error |
| 🔄 | Retry | Retry, re-check, fix after review |
| 💬 | Escalation | Question to Lead/Tech Lead, ESCALATION |
| 😴 | Idle | Agent is sleeping, waiting for a task |
| 👁 | Monitoring | Supervisor is watching the team |

## Roles (prefix in review)

| Icon | Role |
|------|------|
| 🔒 | Security Review |
| 🧠 | Logic Review |
| 📐 | Quality Review |
| 🔍 | Unified Review |

## Usage

**Message format:** `{icon} [{ROLE}] {action} — {context}`

**activeForm:** `TaskUpdate(taskId="3", activeForm="🔨 Implementing settings endpoint")`

**Tree output (Monitor Mode):**
```
📋 TEAM STATUS
├── 🔨 coder-1: task #3 «Add settings endpoint» (IN_PROGRESS)
├── ⏳ coder-2: task #4 «Update user model» (IN_REVIEW)
├── 👁 supervisor: monitoring
└── ✅ tech-lead: plan validated

Progress: ████░░░░░░ 2/5 tasks
```
