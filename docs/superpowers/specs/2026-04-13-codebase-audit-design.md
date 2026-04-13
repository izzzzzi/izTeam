# Codebase Audit: izteam plugin marketplace

> **Status:** Approved
> **Date:** 2026-04-13
> **Scope:** CI/infrastructure, all 5 plugins, README documentation

---

## Context

izteam is a Claude Code plugin marketplace with 5 plugins: team, think, arena, audit, reason. The `reason` plugin was added recently (v0.3.0) but several integration points were missed — CI, docs, and README were not updated to include it. Additionally, the evidence rating system is duplicated across arena and reason plugins.

## Approach

Hybrid: fix CI/infrastructure first (blocks all plugins), then per-plugin fixes, then documentation.

---

## Phase 1: CI & Infrastructure

### Fix 1: Add "reason" to auto-version workflow

**File:** `.github/workflows/auto-version.yml`
**Line:** 31
**Change:** Add `"reason"` to the PLUGINS array.

```bash
# Before
PLUGINS=("team" "think" "arena" "audit")

# After
PLUGINS=("team" "think" "arena" "audit" "reason")
```

**Why:** Without this, the reason plugin never gets automatic version bumps when its files change.

### Fix 2: Fix HEREDOC indentation in commit message

**File:** `.github/workflows/auto-version.yml`
**Lines:** 111-114
**Change:** Remove leading whitespace from the HEREDOC body so commit messages don't start with spaces.

```yaml
# Before (indented inside YAML step)
      git commit -m "$(cat <<EOF
          chore: bump to v${{ steps.version.outputs.version }} [auto-version]
          EOF
          )"

# After
      git commit -m "$(cat <<'EOF'
chore: bump to v${{ steps.version.outputs.version }} [auto-version]
EOF
)"
```

### Fix 3: Add plugin.json bumping to manual bump-version.sh

**File:** `scripts/bump-version.sh`
**Change:** After bumping the unified version in marketplace.json, also iterate over all plugin.json files and bump their patch versions. This keeps manual releases in sync with what auto-version does.

Currently the script only bumps `.claude-plugin/marketplace.json`. Add a loop that:
1. Reads each `plugins/*/.claude-plugin/plugin.json`
2. Bumps the patch version
3. Updates the corresponding entry in marketplace.json

---

## Phase 2: Plugins

### Fix 4: Extract shared evidence rating reference

**Problem:** The R/CL evidence rating table is defined identically in 3 places:
- `plugins/arena/agents/expert.md` (lines 154-171)
- `plugins/arena/skills/arena/references/evidence-scoring.md` (full file)
- `plugins/reason/agents/evidence-gatherer.md` (lines 64-81)

**Change:** 
1. Keep `plugins/arena/skills/arena/references/evidence-scoring.md` as the canonical source (it's already the most complete version).
2. Copy it to `plugins/reason/skills/reason/references/evidence-scoring.md` (reason needs its own copy since plugins are independently installable).
3. In `plugins/arena/agents/expert.md`: replace the inline R/CL tables with a brief summary + reference to `evidence-scoring.md` via `@references/evidence-scoring.md` pattern.
4. In `plugins/reason/agents/evidence-gatherer.md`: replace the inline R/CL tables with a brief summary + reference to `references/evidence-scoring.md`.

**Trade-off:** Plugins must be self-contained (independently installable), so we can't share a single file across plugins. Two copies (one per plugin) is the minimum. The reduction is from 3 copies to 2, and agents reference instead of inlining.

---

## Phase 3: README Documentation

### Fix 5: Update badge count

**File:** `README.md` (line ~12)
**Change:** `Plugins-4-blue` → `Plugins-5-blue`

### Fix 6: Add reason to mermaid graph

**File:** `README.md` (lines ~33-77)
**Change:** Add a `/reason` subgraph block:

```mermaid
subgraph "/reason — Reason"
    R1["🔬 Hypothesize competing options"]
    R2["🔍 Verify logic & constraints"]
    R3["📊 Gather empirical evidence"]
    R4["📋 Design Rationale Record"]
    R1 --> R2 --> R3 --> R4
end
```

And connect: `C --> R1`

### Fix 7: Add reason to plugins table

**File:** `README.md` (lines ~99-104)
**Change:** Add row:

```
| 🧪 **[reason](#-reason)** | `0.1.0` | Hypothesis-driven reasoning with auditable evidence trails (FPF/ADI cycle). | `/reason` |
```

### Fix 8: Add full reason section

**File:** `README.md` (after arena section)
**Change:** Add a full section following the same pattern as other plugins:

```markdown
## 🧪 reason

Hypothesis-driven reasoning with auditable evidence trails, based on the First Principles Framework.

> **Required:** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `settings.json`

**Commands:**

/reason Which database for the new service?
/reason Monolith or microservices for our case?
/reason Speed vs correctness in the data pipeline?

**Natural language — also works:**

"Reason through the database choice with evidence"
"Compare options for auth strategy with trust scores"
"I need a decision record for the caching approach"

[Read more (EN) →](./plugins/reason/README.md) · [RU →](./plugins/reason/README.ru.md)
```

### Fix 9: Add reason to project structure

**File:** `README.md` (lines ~262-277)
**Change:** Add `├── reason/` line under plugins.

### Fix 10: Mirror fixes 5-9 in README.ru.md

**File:** `README.ru.md`
**Change:** Apply the same 5 documentation changes, translated to Russian.

---

## Out of Scope

The following were noted during audit but intentionally excluded from this spec:

- **Hardcoded SLA thresholds in supervisor.md** — acceptable for v0.x, revisit when configurable profiles are added
- **Hardcoded paths in audit agents (src/features/, etc.)** — documented behavior, not a bug
- **build SKILL.md at 311 lines** — within the 500-line limit, no action needed
- **sync-mcp.sh not including reason** — reason doesn't use MCP tools, so this is correct behavior. Add a comment in sync-mcp.sh explaining why reason is excluded.

## Success Criteria

1. `./scripts/validate-skills.sh` passes (currently 197 checks)
2. `./scripts/sync-mcp.sh --check` passes
3. All 5 plugins listed in README.md with correct versions
4. Mermaid graph includes all 5 workflows
5. auto-version.yml includes reason in PLUGINS array
6. No duplicate evidence rating tables in agent files (replaced with references)
