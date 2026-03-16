## ADDED Requirements

### Requirement: Reason plugin exists as ADI-cycle reasoning engine
The system SHALL provide a `reason` plugin (v0.1.0) that implements hypothesis-driven reasoning through the ADI cycle (Abduction → Deduction → Induction). The plugin MUST produce a Design Rationale Record (DRR) as its output artifact.

#### Scenario: User invokes /reason with a decision question
- **WHEN** user runs `/reason "which database for the new service"`
- **THEN** the system launches the ADI cycle with 4 phases (Framing → Abduction → Deduction → Induction → Decision) and saves a DRR to `docs/decisions/YYYY-MM-DD-[topic]-drr.md`

#### Scenario: Reason skill distinguishes from arena and think
- **WHEN** user needs expert debates without hypothesis verification
- **THEN** the system recommends `/arena` instead of `/reason`

### Requirement: Phase 0 frames the decision question
The Reasoning Lead MUST determine bounded context, decision type, constraints, and stakes before generating hypotheses.

#### Scenario: Question framing produces structured context
- **WHEN** a decision question is submitted
- **THEN** the system presents a framing table with: Bounded Context, Decision Type, Key Constraints, Stakes

### Requirement: Phase 1 generates competing hypotheses via abduction
The system SHALL launch 3-5 `reason:hypothesizer` agents IN PARALLEL, each generating ONE hypothesis from a different angle. All hypotheses start at Assurance Level L0 (Observation).

#### Scenario: Hypothesizer agents produce diverse hypotheses
- **WHEN** a tech-choice question is submitted
- **THEN** hypothesizers are assigned angles from the relevant angle set (e.g., performance, DX, ecosystem, maintenance cost, migration risk for tech choices)

#### Scenario: Minimum hypothesis threshold
- **WHEN** fewer than 3 hypothesizers return results
- **THEN** the system reports failure (minimum 3 hypotheses required)

### Requirement: Phase 2 verifies hypotheses via deduction
The system SHALL launch `reason:verifier` agents IN PARALLEL — one per hypothesis. Verifiers check internal consistency, constraint compatibility, and known failure modes WITHOUT gathering empirical evidence.

#### Scenario: Verification updates assurance levels
- **WHEN** a verifier passes a hypothesis
- **THEN** the hypothesis is promoted to L1 (Reasoned)

#### Scenario: All hypotheses invalid after verification
- **WHEN** all hypotheses fail logical verification
- **THEN** the system retries Phase 1 once with broader angles. If still all invalid, reports deadlock.

### Requirement: Phase 3 gathers empirical evidence via induction
The system SHALL launch `reason:evidence-gatherer` agents IN PARALLEL for surviving hypotheses (L0 or L1). Each evidence piece MUST be rated with R (reliability: 0.0-1.0) and CL (congruence: 0.0-1.0).

#### Scenario: Evidence updates assurance levels
- **WHEN** an L1 hypothesis receives evidence with Trust >= 0.7
- **THEN** the hypothesis is promoted to L2 (Verified)

#### Scenario: Weak evidence downgrades hypothesis
- **WHEN** an L1 hypothesis has Trust < 0.4
- **THEN** it is downgraded to L0

### Requirement: WLNK trust scoring
Trust for a hypothesis SHALL be computed as `min(evidence_scores)` where `evidence_score = R × (1 - max(0, 0.5 - CL))`. The weakest link determines overall trust.

#### Scenario: One bad evidence drags trust score
- **WHEN** a hypothesis has 3 evidence pieces with scores [0.9, 0.85, 0.3]
- **THEN** the hypothesis trust is 0.3 (weakest link)

### Requirement: Assurance levels classify hypothesis confidence
The system SHALL use three assurance levels: L0 (Observation — unverified), L1 (Reasoned — passed logical check), L2 (Verified — supported by evidence with Trust >= 0.7).

#### Scenario: Assurance level progression
- **WHEN** a hypothesis passes verification (Phase 2) and has strong evidence (Phase 3)
- **THEN** it progresses L0 → L1 → L2

### Requirement: DRR artifact captures the full reasoning trail
The Design Rationale Record MUST include: decision question, constraints, all hypotheses (including invalid ones), evidence catalog with R/CL ratings, trust summary, winner with comparative reasoning, and trade-offs accepted.

#### Scenario: Invalid hypotheses are preserved
- **WHEN** a hypothesis is marked Invalid during verification
- **THEN** it is kept in the DRR with the reason for rejection

#### Scenario: DRR saved to standard location
- **WHEN** reasoning completes
- **THEN** the DRR is saved to `docs/decisions/YYYY-MM-DD-[topic-slug]-drr.md`

### Requirement: Three specialized agents
The reason plugin SHALL provide 3 agents: `hypothesizer` (generates one grounded hypothesis), `verifier` (logically verifies hypothesis without empirical data), `evidence-gatherer` (gathers empirical evidence with R/CL ratings). All agents use Opus model.

#### Scenario: Agents are one-shot and parallel
- **WHEN** Phase 1 launches
- **THEN** 3-5 hypothesizer agents run in parallel, each returning a single hypothesis

### Requirement: References include DRR template and FPF distillate
The plugin SHALL include `references/drr-template.md` (template for Design Rationale Records) and `references/fpf-distillate.md` (First Principles Framework reference).

#### Scenario: DRR template is used in Phase 4
- **WHEN** the Reasoning Lead compiles the final DRR
- **THEN** it reads `references/drr-template.md` and fills in the template

### Requirement: Evidence without sources is flagged
Evidence without an explicit source MUST be marked as `[INFERRED]` and automatically receives R=0.3.

#### Scenario: Inferred evidence penalty
- **WHEN** an evidence-gatherer provides a claim without a source URL or reference
- **THEN** the evidence is marked [INFERRED] with R=0.3
