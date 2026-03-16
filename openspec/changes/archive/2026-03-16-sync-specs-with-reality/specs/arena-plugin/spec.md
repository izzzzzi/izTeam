## ADDED Requirements

### Requirement: Evidence-driven debate protocol
All expert arguments in the arena MUST cite evidence with R (reliability: 0.0-1.0) and CL (congruence: 0.0-1.0) ratings. Experts can challenge other experts' R/CL ratings with justification.

#### Scenario: Expert broadcasts position with evidence
- **WHEN** an expert broadcasts their initial position
- **THEN** each argument includes evidence citations with R and CL ratings

#### Scenario: Expert challenges another's evidence rating
- **WHEN** an expert disagrees with another expert's R/CL rating
- **THEN** they can dispute it with a justification, and the challenged expert must defend or adjust

### Requirement: Evidence reliability scale
The system SHALL use a standard reliability scale: Official docs/benchmarks (0.9), Peer-reviewed/reputable blog (0.8), Production case study (0.8), Community benchmark (0.7), SO/forum consensus (0.5), Single blog post (0.4), Own experience/inferred (0.3).

#### Scenario: Source type determines R rating
- **WHEN** an expert cites an official documentation page
- **THEN** the R rating is 0.9

### Requirement: Evidence congruence scale
The system SHALL use a standard congruence scale: Exact context (1.0), Similar context (0.7), Related context (0.5), Loosely related (0.3).

#### Scenario: Context match determines CL rating
- **WHEN** evidence comes from the exact same technology and use case
- **THEN** the CL rating is 1.0

### Requirement: WLNK trust scoring for arena positions
Each expert's final position MUST include an evidence summary table with WLNK trust score. Trust is computed as `min(evidence_scores)` where `evidence_score = R × (1 - max(0, 0.5 - CL))`.

#### Scenario: Final position includes trust score
- **WHEN** an expert signals convergence and submits their final position
- **THEN** the position includes an evidence summary table with per-evidence scores and overall WLNK trust

### Requirement: Assurance levels for arena positions
The system SHALL classify debate positions with assurance levels: L0 (Observation — opinions without strong evidence), L1 (Reasoned — logically consistent with moderate evidence, Trust 0.4-0.7), L2 (Verified — supported by strong evidence, Trust >= 0.7).

#### Scenario: Assurance level assigned based on trust
- **WHEN** synthesis consolidates evidence
- **THEN** each position receives an assurance level based on its WLNK trust score

### Requirement: Evidence consolidation before synthesis
Before creating the synthesis document, the Moderator MUST: (1) collect all evidence tables from experts' final positions, (2) de-duplicate evidence cited by multiple experts, (3) resolve contested R/CL ratings using the better-justified rating, (4) calculate WLNK trust per position, (5) assign assurance levels.

#### Scenario: Contested R/CL rating resolution
- **WHEN** two experts disagree on the R/CL rating for the same evidence
- **THEN** the system uses the rating with the better justification

## MODIFIED Requirements

### Requirement: Synthesis document structure
The synthesis document MUST follow the template from `references/synthesis-template.md`. The template SHALL include: Trust Summary table (position, champion, assurance level, WLNK trust, evidence count), Evidence Catalog (all cited evidence consolidated and de-duplicated), Contested Evidence Resolution table, Debate Progression with direct challenges and position shifts, Trade-offs Accepted section, and the existing sections (Arena Question, Expert Panel, Debate Summary, Key Positions, Convergence Points, Open Disagreements, Recommendation).

#### Scenario: Synthesis includes trust summary
- **WHEN** the Moderator creates the synthesis document
- **THEN** the document includes a Trust Summary table showing each position's champion, assurance level, WLNK trust score, and evidence count

#### Scenario: Synthesis includes evidence catalog
- **WHEN** the Moderator creates the synthesis document
- **THEN** the document includes a de-duplicated Evidence Catalog with all cited evidence, their R/CL ratings, and which experts cited them

#### Scenario: Synthesis saved to standard location
- **WHEN** the arena concludes
- **THEN** the synthesis is saved to `docs/arena/YYYY-MM-DD-[topic-brief].md`

### Requirement: Expert final position format
Each expert's final position sent to team-lead MUST include: (1) their stance on the question, (2) key arguments with evidence citations, (3) an evidence summary table with R, CL, and score per evidence piece, (4) overall WLNK trust score.

#### Scenario: Expert signals convergence with evidence summary
- **WHEN** an expert believes common ground has been reached
- **THEN** they send a final position to team-lead that includes an evidence summary table with WLNK trust score

### Requirement: References include evidence scoring guide
The plugin SHALL include `references/evidence-scoring.md` as a reference for the evidence rating protocol, in addition to existing references (expert-selection-guide.md, live-commentary-rules.md, synthesis-template.md).

#### Scenario: Four reference files exist
- **WHEN** the arena plugin is inspected
- **THEN** it contains 4 reference files: expert-selection-guide.md, live-commentary-rules.md, synthesis-template.md, evidence-scoring.md
