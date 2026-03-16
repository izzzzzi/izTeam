# Evidence Scoring Guide (FPF)

> Referenced from expert agent and synthesis phase. Provides the evidence rating
> system based on the First Principles Framework.

## Reliability (R: 0.0-1.0)

How trustworthy is the source?

| Source Type | Base R |
|------------|--------|
| Official benchmarks / documentation | 0.9 |
| Peer-reviewed paper / reputable tech blog | 0.8 |
| Production case study (named company) | 0.8 |
| Community benchmark (reproducible) | 0.7 |
| Stack Overflow / forum consensus | 0.5 |
| Single blog post / personal opinion | 0.4 |
| Own experience / inferred knowledge | 0.3 |

## Congruence (CL: 0.0-1.0)

How relevant is this evidence to OUR specific context?

| Context Match | CL |
|--------------|-----|
| Exact same stack, scale, constraints | 1.0 |
| Similar context (same domain, comparable scale) | 0.7 |
| Related context (same technology, different domain) | 0.5 |
| Loosely related (general principle, different stack) | 0.3 |
| Tangential (different domain and stack) | 0.1 |

## Score Calculation

```
score = R × (1 - max(0, 0.5 - CL))
```

When CL >= 0.5, there is no penalty: `score = R`
When CL < 0.5, a congruence penalty applies.

Examples:
- Official benchmark, exact context: `0.9 × 1.0 = 0.9`
- Blog post, similar context: `0.4 × 1.0 = 0.4`
- Production case study, loosely related: `0.8 × (1 - 0.2) = 0.64`
- Inferred, tangential: `0.3 × (1 - 0.4) = 0.18`

## WLNK (Weakest Link Principle)

```
Trust(position) = min(all evidence scores for that position)
```

One weak piece of evidence drags the whole trust score down.
This prevents "trust inflation" from stacking many mediocre sources.

## Assurance Levels

| Level | Trust Range | Meaning |
|-------|------------|---------|
| L2 (Verified) | >= 0.7 | Strong empirical backing |
| L1 (Reasoned) | 0.4 - 0.7 | Moderate evidence, logically sound |
| L0 (Observation) | < 0.4 | Weak evidence or opinion-based |

## Contesting Evidence

Experts can challenge each other's R or CL ratings:
- "Your CL of 0.7 is inflated because [specific reason this context differs]"
- "That benchmark's R should be 0.5, not 0.8, because [methodology concern]"

The Moderator resolves contested ratings in the synthesis using the
better-justified rating.
