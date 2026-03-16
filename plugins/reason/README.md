# Reason Plugin

Hypothesis-driven reasoning with auditable evidence trails, based on the [First Principles Framework (FPF)](https://github.com/ailev/FPF).

## Command

### `/reason` — ADI Reasoning Cycle

Guides a decision through the full Abduction-Deduction-Induction cycle:

1. **Abduction** — generates 3-5 competing hypotheses from different angles
2. **Deduction** — logically verifies each hypothesis against constraints
3. **Induction** — gathers empirical evidence with reliability and congruence ratings
4. **Decision** — ranks hypotheses by trust score and produces a Design Rationale Record

### When to use

- Architectural decisions: "monolith or microservices?"
- Technology choices: "which database for the new service?"
- Trade-off analysis: "speed vs. correctness in this pipeline?"
- Any question where "why this and not that" matters

### When NOT to use

- Quick questions — just ask directly
- Implementation — use `/build`
- Expert analysis without evidence requirements — use `/think`
- Expert debates — use `/arena`

## Agents

| Agent | Role | Lifecycle |
|-------|------|-----------|
| `hypothesizer` | Generates one grounded hypothesis from a specific angle | one-shot |
| `verifier` | Logically verifies a hypothesis (consistency, constraints, failure modes) | one-shot |
| `evidence-gatherer` | Gathers empirical evidence and rates by R (reliability) and CL (congruence) | one-shot |

## Key Concepts

- **WLNK (Weakest Link)** — trust = min(evidence scores), not average
- **Assurance Levels** — L0 (observation) → L1 (reasoned) → L2 (verified)
- **DRR (Design Rationale Record)** — auditable artifact saved to `docs/decisions/`
- **Transformer Mandate** — AI recommends, human decides

## Output

Design Rationale Record saved to `docs/decisions/YYYY-MM-DD-[topic]-drr.md`

## Requirements

- Claude Code with Agent Teams enabled (experimental feature)
- Opus model recommended
