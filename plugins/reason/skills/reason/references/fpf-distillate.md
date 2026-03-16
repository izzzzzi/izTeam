# FPF Distillate — Core Principles for Reasoning

Condensed from the First Principles Framework (ailev/FPF). Only the patterns
directly applicable to the /reason skill are included here.

---

## ADI Cycle (Canonical Reasoning Cycle)

Three modes of inference, applied in sequence:

1. **Abduction** — Generate plausible hypotheses that explain the observed problem.
   Multiple competing hypotheses are required — a single hypothesis is not reasoning,
   it's rationalization.

2. **Deduction** — Verify hypotheses through logical analysis. Check internal
   consistency, constraint compatibility, and known failure modes. No empirical
   data — pure logic.

3. **Induction** — Gather empirical evidence. Benchmarks, case studies, production
   data. Every claim needs a source. Counter-evidence is mandatory.

---

## Trust Calculus (Simplified F-G-R)

Every piece of evidence is rated on two dimensions:

- **Reliability (R):** How trustworthy is the source? (0.0-1.0)
- **Congruence (CL):** How relevant is this to OUR specific context? (0.0-1.0)

**Congruence Penalty:** When CL < 0.5, evidence gets penalized:
```
score = R × (1 - max(0, 0.5 - CL))
```

---

## WLNK (Weakest Link Principle)

The trust of a hypothesis equals its WEAKEST piece of evidence, not the average.

**Why:** A chain of reasoning is only as strong as its weakest link. One piece of
poor evidence invalidates a stack of good evidence. This prevents "trust inflation"
where many weak sources create false confidence.

```
Trust(hypothesis) = min(evidence_scores)
```

---

## Assurance Levels

| Level | Name | Meaning |
|-------|------|---------|
| L0 | Observation | Unverified hypothesis — just proposed |
| L1 | Reasoned | Logically verified — passed deduction |
| L2 | Verified | Empirically confirmed — passed induction |
| Invalid | Disproved | Failed verification — kept for the record |

Promotion path: L0 → (deduction) → L1 → (induction) → L2
Demotion: any level can drop to Invalid if contradicted.

---

## Bounded Context

Meaning is local. A term, pattern, or best practice from one context may not
apply in another. Always state the bounded context explicitly:
- What system/module/domain is this decision about?
- What are the specific constraints HERE?
- Evidence from other contexts gets a Congruence penalty.

---

## Transformer Mandate

"A system cannot transform itself."

AI generates hypotheses, gathers evidence, and computes trust — but the HUMAN
makes the final decision. The DRR always records a Decision Owner (human).

---

## Design Rationale Records (DRR)

Every decision produces a DRR that captures:
1. The question asked
2. All hypotheses considered (including rejected ones)
3. Evidence for and against each
4. Trust scores with WLNK computation
5. The chosen hypothesis and WHY
6. Trade-offs accepted
7. Decision owner (human)

**Why keep rejected hypotheses?** Because knowing what you considered and
rejected is as valuable as knowing what you chose. It prevents re-visiting
dead ends and documents the decision landscape.

---

*Source: ailev/FPF (FPF-Spec.md), distilled for /reason skill.*
