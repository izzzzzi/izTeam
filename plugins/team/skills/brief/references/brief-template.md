# Brief Compilation Template

> Compile interview answers and researcher findings into this format.

```markdown
# Feature Brief: [descriptive name]

## Intent
[What should change, for whom, why — from Q1 and clarifications]

## Audience
[Who will use this — from Q2 or inferred from Q1]

## Success Criteria
[Concrete, observable criteria — verifiable: "User can do X", "Y is visible", "Z happens when..."]

## Exclusions
[What NOT to build — from Q4, or "None specified"]

## Additional Context
[Anything from AI-generated follow-ups]

## Project Context
[Condensed summary from researchers: stack, relevant features, key patterns]

---

## Review Checklist (for code reviewers)

- [ ] [Success criterion 1 — restated as checkable item]
- [ ] [Success criterion 2]
- [ ] Exclusions respected: [list what must NOT be present]
```

## Confirmation Flow

Present brief, then:
```
AskUserQuestion(
  questions=[{
    "question": "Here's the plan I'll send to the build team. All correct?",
    "header": "Launch?",
    "options": [
      {"label": "Looks good, launch!", "description": "Save the plan and start building"},
      {"label": "I want to adjust", "description": "Let me change something first"}
    ],
    "multiSelect": false
  }]
)
```

## Save & Handoff

Save to `.briefs/[feature-name-kebab-case].md`, then:
```
Skill("build", args=".briefs/[feature-name].md --no-research")
```
