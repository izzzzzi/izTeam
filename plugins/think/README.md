<p align="right"><strong>English</strong> | <a href="./README.ru.md">Русский</a></p>

# Think

Plan complex tasks before coding with structured expert analysis.

## Installation

```bash
/plugin marketplace add izzzzzi/izTeam
/plugin install think@izteam
```

## Usage

```
/think <task or idea>
```

**Example:**
```
/think Implement a feedback collection system with cashback rewards
```

## How It Works

```mermaid
flowchart TD
    S1["Stage 1: Breakdown<br/>Clarify task, select main expert,<br/>pull principles from 3 experts"]
    S1 --> AT["Aspects table<br/>5-15 aspects with assigned experts"]
    AT --> S2["Stage 2: Parallel Expert Analysis<br/>One agent per aspect launched in parallel"]
    S2 --> A1["Study project<br/>structure, patterns, code"]
    S2 --> A2["Apply expert thinking<br/>main expert + principles"]
    S2 --> A3["Propose 2-4 options<br/>with pros & cons"]
    A1 & A2 & A3 --> S3["Stage 3: Summary Document"]
    S3 --> DOC["docs/plans/YYYY-MM-DD-topic-design.md"]
```

The summary document includes: table of contents, overview with key decisions, details for each aspect with comparison tables, phased implementation plan, and success metrics.

## Structure

```
think/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── think/SKILL.md
├── agents/
│   └── expert.md
├── README.md
└── README.ru.md
```

## Result

A planning document that includes:
- Experts used per section
- Decision tables
- Code examples
- Phased implementation plan
- Success metrics

## When to Use

- New features with many non-obvious decisions
- Refactoring where multiple approaches are possible
- Architectural changes
- Any task that needs careful planning before coding

## License

MIT
