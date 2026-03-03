# Initial State File Template

> Write this to `.claude/teams/{team-name}/state.md` at Step 5 after spawning the team.

```markdown
# Team State — feature-{name}

## Recovery Instructions
If context is compacted, read this file first.

## Phase: EXECUTION
## Complexity: {SIMPLE | MEDIUM | COMPLEX}

## Ownership
- operational_state_owner: supervisor@{epoch}
- architectural_decisions_owner: tech-lead
- lead_role: decisions/staffing only

## Team Roster
- supervisor: ACTIVE
- tech-lead: {ACTIVE | NOT_SPAWNED}
- security-reviewer: {ACTIVE | NOT_SPAWNED}
- logic-reviewer: {ACTIVE | NOT_SPAWNED}
- quality-reviewer: {ACTIVE | NOT_SPAWNED}
- unified-reviewer: {ACTIVE | NOT_SPAWNED}

## Approval Matrix
See complexity-classification.md for the full roster-scoped approval matrix.

## Tasks
- #{id}: {subject} — {STATUS} ({assignment})

## Active Coders: {N} (max: {M})
```
