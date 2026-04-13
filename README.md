<p align="right"><strong>English</strong> | <a href="./README.ru.md">Русский</a></p>

<div align="center">

# 🧩 izteam

**A Claude Code plugin marketplace for AI agent teams, expert debates, deep planning, and interactive code audits**

[![Validate](https://github.com/izzzzzi/izTeam/actions/workflows/validate.yml/badge.svg)](https://github.com/izzzzzi/izTeam/actions/workflows/validate.yml)
[![Auto Version](https://github.com/izzzzzi/izTeam/actions/workflows/auto-version.yml/badge.svg)](https://github.com/izzzzzi/izTeam/actions/workflows/auto-version.yml)
[![Plugins](https://img.shields.io/badge/Plugins-5-blue?style=flat&colorA=18181B&colorB=28CF8D)](https://github.com/izzzzzi/izTeam)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat&colorA=18181B&colorB=28CF8D)](LICENSE)
[![Contributing](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat&colorA=18181B&colorB=28CF8D)](CONTRIBUTING.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Plugin-purple?style=flat&colorA=18181B&colorB=7C3AED)](https://claude.ai/code)

<br />

*Install focused plugins that make Claude Code more predictable for delivery, decisions, and cleanup.*

</div>

---

## 📖 Overview

**izteam** is an independent plugin marketplace for [Claude Code](https://claude.ai/code).
Each plugin adds slash commands, agents, and ready-to-use workflows: from building features with an AI team to auditing outdated code.

---

## 🗺 How It Works

```mermaid
graph TD
    subgraph Install
        A["1. Add marketplace<br/><code>/plugin marketplace add izzzzzi/izTeam</code>"]
        B["2. Install plugins<br/><code>/plugin install team@izteam</code>"]
        A --> B
    end

    B --> C{"Choose a workflow"}

    subgraph "/build &mdash; Team"
        D1["📋 Brief &mdash; interview to clarify scope"]
        D2["📐 Plan &mdash; architect designs tasks"]
        D3["👨‍💻 Code &mdash; parallel coders implement"]
        D4["🔍 Review &mdash; security + logic + quality"]
        D5["✅ Commit &mdash; approved changes merged"]
        D1 --> D2 --> D3 --> D4 --> D5
    end

    subgraph "/think &mdash; Think"
        E1["🔬 Decompose into aspects"]
        E2["🧠 Parallel expert analysis"]
        E3["📄 Unified design document"]
        E1 --> E2 --> E3
    end

    subgraph "/arena &mdash; Arena"
        F1["📚 Research context"]
        F2["🎭 Experts debate"]
        F3["🤝 Consensus reached"]
        F1 --> F2 --> F3
    end

    subgraph "/audit &mdash; Audit"
        G1["🔎 Scan codebase"]
        G2["💬 Interactive review with user"]
        G3["🧹 Cleanup confirmed items"]
        G1 --> G2 --> G3
    end

    subgraph "/reason &mdash; Reason"
        R1["🔬 Hypothesize competing options"]
        R2["🔍 Verify logic &amp; constraints"]
        R3["📊 Gather empirical evidence"]
        R4["📋 Design Rationale Record"]
        R1 --> R2 --> R3 --> R4
    end

    C --> D1
    C --> E1
    C --> F1
    C --> G1
    C --> R1
```

**Example workflows:**

```bash
# Build a feature with an AI team
/build "Add user settings page with profile editing"

# Think through architecture before coding
/think "Migrate from REST to GraphQL — trade-offs and plan"

# Get expert opinions via structured debate
/arena "Microservices vs monolith for our SaaS?"

# Find and clean up dead code
/audit
```

---

## ✨ Plugins

| Plugin | Version | Description | Command |
|--------|---------|-------------|---------|
| 🤖 **[team](#-team)** | `0.3.7` | Build features with an AI agent team and built-in review gates. | `/build` |
| 🧠 **[think](#-think)** | `1.1.7` | Plan complex tasks before coding with structured expert analysis. | `/think` |
| 🎭 **[arena](#-arena)** | `1.1.7` | Compare expert viewpoints and converge on a clear decision. | `/arena` |
| 🧹 **[audit](#-audit)** | `0.1.10` | Find dead and outdated code with an interactive audit. | `/audit` |
| 🧪 **[reason](#-reason)** | `0.1.0` | Hypothesis-driven reasoning with auditable evidence trails (FPF/ADI cycle). | `/reason` |

---

## 🚀 Quick Start

### 1. Add the marketplace

```bash
/plugin marketplace add izzzzzi/izTeam
```

### 2. Install plugins

```bash
/plugin install team@izteam
/plugin install think@izteam
/plugin install arena@izteam
/plugin install audit@izteam
/plugin install reason@izteam
```

### 3. Restart Claude Code

Plugins are loaded on startup, so restart after installation.

---

## 🤖 team

Build features with an AI agent team and built-in review gates.

> **Required:** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `settings.json`

```bash
/plugin install team@izteam
```

**Commands:**

```bash
/build "Add user settings page"
/build docs/plan.md --coders=2
/build "Add notifications" --git-checkpoints
/brief "Notifications system"
/conventions
```

**Natural language — also works:**

```
"Build a settings page with profile editing"
"Implement notifications with email and push"
"Interview me before we start building"
"Extract project conventions and document standards"
```

Repo Map feature inspired by [Aider](https://github.com/Aider-AI/aider) — generates a ranked symbol map to give agents instant codebase context.

[Read more (EN) →](./plugins/team/README.md) · [RU →](./plugins/team/README.ru.md)

---

## 🧠 think

Plan complex tasks before coding with structured expert analysis.

```bash
/plugin install think@izteam
```

**Commands:**

```bash
/think Implement a feedback collection system with cashback rewards
/think Migrate from REST to GraphQL — trade-offs and strategy
/think Refactor authentication from session-based to JWT
```

**Natural language — also works:**

```
"Think through the architecture for a payments system"
"Plan how to migrate from REST to GraphQL"
"Analyze trade-offs between SSR and CSR"
"Describe a full plan for the microservice"
```

[Read more (EN) →](./plugins/think/README.md) · [RU →](./plugins/think/README.ru.md)

---

## 🎭 arena

Compare expert viewpoints and converge on a clear decision.

> **Required:** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `settings.json`

```bash
/plugin install arena@izteam
```

**Commands:**

```bash
/arena Should we use microservices or monolith for our SaaS?
/arena Best pricing strategy for a developer tool?
/arena How should we handle state management in our React app?
```

**Natural language — also works:**

```
"Debate: microservices vs monolith for our case"
"I need expert opinions on state management"
"Compare Redux vs Zustand vs Jotai — pros and cons"
"What's the best auth strategy? Let experts argue"
```

[Read more (EN) →](./plugins/arena/README.md) · [RU →](./plugins/arena/README.ru.md)

---

## 🧹 audit

Find dead and outdated code with an interactive audit.

```bash
/plugin install audit@izteam
```

**Commands:**

```bash
/audit
/audit features
/audit server
/audit ui
/audit stores
```

**Natural language — also works:**

```
"Find dead code and clean up"
"Clean up the codebase from legacy and orphaned code"
"Check features for unused exports"
"Audit the server for dead API endpoints"
"Find unused UI components"
"Check stores for redundant state"
```

[Read more (EN) →](./plugins/audit/README.md) · [RU →](./plugins/audit/README.ru.md)

---

## 🧪 reason

Hypothesis-driven reasoning with auditable evidence trails, based on the [First Principles Framework](https://github.com/ailev/FPF).

> **Required:** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `settings.json`

```bash
/plugin install reason@izteam
```

**Commands:**

```bash
/reason Which database for the new service?
/reason Monolith or microservices for our case?
/reason Speed vs correctness in the data pipeline?
```

**Natural language — also works:**

```
"Reason through the database choice with evidence"
"Compare options for auth strategy with trust scores"
"I need a decision record for the caching approach"
```

[Read more (EN) →](./plugins/reason/README.md) · [RU →](./plugins/reason/README.ru.md)

---

## 📁 Project Structure

```text
izteam/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── team/
│   ├── think/
│   ├── arena/
│   ├── audit/
│   └── reason/
├── scripts/
│   └── bump-version.sh
├── .github/workflows/
│   ├── validate.yml
│   └── auto-version.yml
├── CODE_OF_CONDUCT.md
└── CONTRIBUTING.md
```

---

## 🔧 Configuration

### Enable Agent Teams

Plugins `team` and `arena` require the experimental Agent Teams feature:

```json
// ~/.claude/settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

---

## 🛠 Development

### Versioning

```bash
# Bump unified version
./scripts/bump-version.sh patch
./scripts/bump-version.sh minor
```

The repo uses a single unified version (`v0.0.1`, `v0.1.0`, etc.). Individual plugin versions are bumped automatically.

### CI/CD

- `validate.yml` — structure and consistency checks on PRs and pushes
- `auto-version.yml` — automatic unified version bump, tagging, and release

---

## 🐛 Troubleshooting

- Plugin not visible after install → restart Claude Code.
- New version not picked up → clear cache:

```bash
rm -rf ~/.claude/plugins/cache/izteam/
```

