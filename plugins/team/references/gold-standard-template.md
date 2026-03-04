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

### Briefing file template:

```markdown
# Briefing: feature-<name>

## Team Roster
- Lead, Supervisor, Tech Lead, Reviewers, Coders

## Git Mode
git_mode: standard | checkpoint

## Repo Map
<!-- Top 50 lines from .repo-map (if available) -->
<!-- This gives coders instant structural context without exploration -->

## Gold Standards
GOLD STANDARD BLOCK (compiled by Lead):
--- GOLD STANDARD: [layer] — [file path] ---
...
```

**Repo Map section:** If `.repo-map` was generated in Step 1, include the top 50 lines. This gives coders an instant mental model of the codebase without needing to explore. If `.repo-map` doesn't exist, omit this section.

**Git Mode section:** Write `git_mode: standard` (default) or `git_mode: checkpoint` (if `--git-checkpoints` was passed). Coders read this to determine their commit strategy.

### Coder spawn prompt template:
```
prompt="You are Coder #{N}. Team: feature-<name>.
YOUR TASK CONTEXT: {Brief summary of what this coder will work on}
Read .claude/teams/{team-name}/briefing.md for gold standard examples and team roster.
Claim your first task from the task list and start working."
```

Task context FIRST, then briefing reference — coder reads WHAT before HOW.
