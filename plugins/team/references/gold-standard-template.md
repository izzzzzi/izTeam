# Gold Standard Block Template

> Gold standards are the #1 lever for code quality (+15-40% accuracy vs instructions alone).
> Coders MUST receive canonical examples as few-shot context.

## Format

Lead compiles this block from researcher findings + `.conventions/` (if exists):

```
GOLD STANDARD BLOCK (compiled by Lead):

--- GOLD STANDARD: [layer] — [file path] ---
[Full file content or .conventions/ snippet]
[Note: pay attention to X, Y naming]

--- GOLD STANDARD: [layer] — [file path] ---
[Full file content]

--- CONVENTIONS ---
[Key rules from .conventions/checks/ or CLAUDE.md — naming patterns, import rules, etc.]
```

## Rules

- 3-5 examples, ~100-150 lines total
- Prioritize by relevance to the feature
- Include FULL file content (not summaries) — coders need to see the actual pattern
- Add notes pointing to specific patterns to match (naming, error handling, imports)

## Briefing File Pattern (write once, read many)

Lead writes the block to `.claude/teams/{team-name}/briefing.md` (team roster + gold standards). Coder spawn prompts reference it — saves ~3000 tokens per additional coder.

Coder spawn prompt template:
```
prompt="You are Coder #{N}. Team: feature-<name>.
YOUR TASK CONTEXT: {Brief summary of what this coder will work on}
Read .claude/teams/{team-name}/briefing.md for gold standard examples and team roster.
Claim your first task from the task list and start working."
```

Task context FIRST, then briefing reference — coder reads WHAT before HOW.
