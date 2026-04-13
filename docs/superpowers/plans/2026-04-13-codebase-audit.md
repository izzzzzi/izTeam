# Codebase Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix 10 issues found during codebase audit — CI bugs, evidence rating duplication, and missing reason plugin in README docs.

**Architecture:** Direct edits to CI workflows, shell scripts, agent markdown definitions, and README files. No new features, no code logic — purely correctness and documentation fixes.

**Tech Stack:** Bash (CI workflows, scripts), Markdown (agents, READMEs), YAML (GitHub Actions)

---

## File Map

| File | Action | Task |
|------|--------|------|
| `.github/workflows/auto-version.yml` | Modify | 1 |
| `scripts/bump-version.sh` | Modify | 2 |
| `plugins/reason/skills/reason/references/evidence-scoring.md` | Create (copy) | 3 |
| `plugins/arena/agents/expert.md` | Modify | 3 |
| `plugins/reason/agents/evidence-gatherer.md` | Modify | 3 |
| `README.md` | Modify | 4 |
| `README.ru.md` | Modify | 5 |
| `scripts/sync-mcp.sh` | Modify | 6 |

---

### Task 1: Fix CI — auto-version.yml (Fixes 1 & 2)

**Files:**
- Modify: `.github/workflows/auto-version.yml:31` (PLUGINS array)
- Modify: `.github/workflows/auto-version.yml:110-114` (HEREDOC indentation)

- [ ] **Step 1: Add "reason" to PLUGINS array**

In `.github/workflows/auto-version.yml`, line 31, change:

```bash
# Before
          PLUGINS=("team" "think" "arena" "audit")

# After
          PLUGINS=("team" "think" "arena" "audit" "reason")
```

- [ ] **Step 2: Fix HEREDOC indentation in commit step**

In `.github/workflows/auto-version.yml`, lines 110-114, the commit message HEREDOC is indented inside the YAML step, causing leading whitespace in commit messages. Change:

```yaml
# Before
      - name: Commit and tag
        if: steps.version.outputs.bumped == 'true'
        run: |
          git add .claude-plugin/marketplace.json plugins/*/.claude-plugin/plugin.json
          git commit -m "$(cat <<EOF
          chore: bump to v${{ steps.version.outputs.version }} [auto-version]
          EOF
          )"

          git tag "v${{ steps.version.outputs.version }}"
          git push origin main --tags

# After
      - name: Commit and tag
        if: steps.version.outputs.bumped == 'true'
        run: |
          git add .claude-plugin/marketplace.json plugins/*/.claude-plugin/plugin.json
          git commit -m "$(cat <<'EOF'
chore: bump to v${{ steps.version.outputs.version }} [auto-version]
EOF
)"

          git tag "v${{ steps.version.outputs.version }}"
          git push origin main --tags
```

Note: the HEREDOC body and closing `EOF` must be at column 0 (no indentation) to avoid whitespace in the commit message. The closing `)` and `"` go on the line after EOF.

- [ ] **Step 3: Verify YAML is valid**

Run: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/auto-version.yml'))"`
Expected: no output (valid YAML)

If python3/yaml is unavailable, run: `cat .github/workflows/auto-version.yml | head -5` to sanity-check the file is not corrupted.

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/auto-version.yml
git commit -m "fix: add reason plugin to auto-version and fix HEREDOC indentation"
```

---

### Task 2: Fix bump-version.sh (Fix 3)

**Files:**
- Modify: `scripts/bump-version.sh`

- [ ] **Step 1: Add plugin.json bumping loop**

After the unified version bump (after line 29 `jq --arg v "$NEW" ...`), add the following block that bumps each plugin's patch version and syncs it to marketplace.json:

```bash
# Bump individual plugin versions (patch) and sync to marketplace.json
for plugin_dir in plugins/*/; do
  PLUGIN_JSON="${plugin_dir}.claude-plugin/plugin.json"
  if [ ! -f "$PLUGIN_JSON" ]; then
    continue
  fi

  PLUGIN_NAME=$(jq -r '.name' "$PLUGIN_JSON")
  CURRENT_PV=$(jq -r '.version' "$PLUGIN_JSON")
  IFS='.' read -r PV_MAJOR PV_MINOR PV_PATCH <<< "$CURRENT_PV"
  PV_PATCH=$((PV_PATCH + 1))
  NEW_PV="${PV_MAJOR}.${PV_MINOR}.${PV_PATCH}"

  jq --arg v "$NEW_PV" '.version = $v' "$PLUGIN_JSON" > tmp.json && mv tmp.json "$PLUGIN_JSON"
  jq --arg name "$PLUGIN_NAME" --arg v "$NEW_PV" \
    '(.plugins[] | select(.name == $name)).version = $v' \
    "$MARKETPLACE_JSON" > tmp.json && mv tmp.json "$MARKETPLACE_JSON"

  echo "  $PLUGIN_NAME: $CURRENT_PV -> $NEW_PV"
done
```

The full file after edits should look like:

```bash
#!/bin/bash
# Usage: ./scripts/bump-version.sh [major|minor|patch]
# Bumps the unified repo version and all plugin versions.
# Example: ./scripts/bump-version.sh patch
#          ./scripts/bump-version.sh minor

set -euo pipefail

BUMP="${1:-patch}"
MARKETPLACE_JSON=".claude-plugin/marketplace.json"

if [ ! -f "$MARKETPLACE_JSON" ]; then
  echo "ERROR: $MARKETPLACE_JSON not found"
  exit 1
fi

# Bump unified version
CURRENT=$(jq -r '.version' "$MARKETPLACE_JSON")
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"

case "$BUMP" in
  major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
  minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
  patch) PATCH=$((PATCH + 1)) ;;
  *) echo "ERROR: Invalid bump type: $BUMP (use major|minor|patch)"; exit 1 ;;
esac

NEW="${MAJOR}.${MINOR}.${PATCH}"
jq --arg v "$NEW" '.version = $v' "$MARKETPLACE_JSON" > tmp.json && mv tmp.json "$MARKETPLACE_JSON"

echo "Unified version: $CURRENT -> $NEW"
echo ""

# Bump individual plugin versions (patch) and sync to marketplace.json
echo "Plugin versions:"
for plugin_dir in plugins/*/; do
  PLUGIN_JSON="${plugin_dir}.claude-plugin/plugin.json"
  if [ ! -f "$PLUGIN_JSON" ]; then
    continue
  fi

  PLUGIN_NAME=$(jq -r '.name' "$PLUGIN_JSON")
  CURRENT_PV=$(jq -r '.version' "$PLUGIN_JSON")
  IFS='.' read -r PV_MAJOR PV_MINOR PV_PATCH <<< "$CURRENT_PV"
  PV_PATCH=$((PV_PATCH + 1))
  NEW_PV="${PV_MAJOR}.${PV_MINOR}.${PV_PATCH}"

  jq --arg v "$NEW_PV" '.version = $v' "$PLUGIN_JSON" > tmp.json && mv tmp.json "$PLUGIN_JSON"
  jq --arg name "$PLUGIN_NAME" --arg v "$NEW_PV" \
    '(.plugins[] | select(.name == $name)).version = $v' \
    "$MARKETPLACE_JSON" > tmp.json && mv tmp.json "$MARKETPLACE_JSON"

  echo "  $PLUGIN_NAME: $CURRENT_PV -> $NEW_PV"
done

echo ""
echo "Next steps:"
echo "  git add $MARKETPLACE_JSON plugins/*/.claude-plugin/plugin.json"
echo "  git commit -m \"release: v$NEW\""
echo "  git tag v$NEW"
echo "  git push origin main --tags"
```

- [ ] **Step 2: Test the script in dry mode**

Run: `bash scripts/bump-version.sh patch`
Expected output should show unified version bump AND each plugin version bump:
```
Unified version: 0.3.0 -> 0.3.1

Plugin versions:
  arena: 1.1.7 -> 1.1.8
  audit: 0.1.14 -> 0.1.15
  reason: 0.1.0 -> 0.1.1
  team: 0.3.10 -> 0.3.11
  think: 1.1.7 -> 1.1.8
```

- [ ] **Step 3: Revert the test bump**

The script actually modified files. Revert them:
```bash
git checkout -- .claude-plugin/marketplace.json plugins/*/.claude-plugin/plugin.json
```

- [ ] **Step 4: Commit**

```bash
git add scripts/bump-version.sh
git commit -m "fix: bump-version.sh now syncs individual plugin versions"
```

---

### Task 3: Deduplicate evidence rating tables (Fix 4)

**Files:**
- Create: `plugins/reason/skills/reason/references/evidence-scoring.md`
- Modify: `plugins/arena/agents/expert.md:150-175`
- Modify: `plugins/reason/agents/evidence-gatherer.md:62-83`

- [ ] **Step 1: Copy evidence-scoring.md to reason plugin**

Copy `plugins/arena/skills/arena/references/evidence-scoring.md` to `plugins/reason/skills/reason/references/evidence-scoring.md` (exact copy — plugins must be self-contained).

```bash
cp plugins/arena/skills/arena/references/evidence-scoring.md \
   plugins/reason/skills/reason/references/evidence-scoring.md
```

- [ ] **Step 2: Replace inline tables in arena expert.md**

In `plugins/arena/agents/expert.md`, replace the full "EVIDENCE RATING" section (lines 150-175) with a compact summary that references the canonical file:

```markdown
## EVIDENCE RATING

Every argument MUST be backed by evidence with two ratings:

- **Reliability (R: 0.0-1.0):** Source trustworthiness (0.9 = official docs, 0.3 = inferred)
- **Congruence (CL: 0.0-1.0):** Relevance to THIS specific context (1.0 = exact match, 0.1 = tangential)
- **Score:** `R × (1 - max(0, 0.5 - CL))`

Full rating tables and WLNK calculation: see `@references/evidence-scoring.md` in the arena skill.

When challenging another expert's evidence, you can dispute their R or CL ratings with justification.
```

- [ ] **Step 3: Replace inline tables in reason evidence-gatherer.md**

In `plugins/reason/agents/evidence-gatherer.md`, replace the "Evidence Rating" section (lines 62-83) with a compact summary:

```markdown
## Evidence Rating

For each piece of evidence, rate on two dimensions:

- **Reliability (R: 0.0-1.0):** Source trustworthiness (0.9 = official docs, 0.3 = inferred)
- **Congruence (CL: 0.0-1.0):** Relevance to THIS specific context (1.0 = exact match, 0.1 = tangential)

Full rating tables, score calculation, and WLNK principle: see `references/evidence-scoring.md`.
```

- [ ] **Step 4: Verify validate-skills.sh still passes**

Run: `bash scripts/validate-skills.sh`
Expected: `ALL PASSED` (the new evidence-scoring.md in reason doesn't need to be referenced from SKILL.md — it's referenced from the agent).

- [ ] **Step 5: Commit**

```bash
git add plugins/reason/skills/reason/references/evidence-scoring.md \
       plugins/arena/agents/expert.md \
       plugins/reason/agents/evidence-gatherer.md
git commit -m "refactor: deduplicate evidence rating tables across arena and reason"
```

---

### Task 4: Update README.md (Fixes 5-9)

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Fix badge count (Fix 5)**

Line ~12, change:
```
Plugins-4-blue
```
to:
```
Plugins-5-blue
```

- [ ] **Step 2: Add reason to mermaid graph (Fix 6)**

After the `/audit` subgraph block (after line 71 `G1 --> G2 --> G3`) and before `end`, add the reason subgraph:

```mermaid
    subgraph "/reason &mdash; Reason"
        R1["🔬 Hypothesize competing options"]
        R2["🔍 Verify logic &amp; constraints"]
        R3["📊 Gather empirical evidence"]
        R4["📋 Design Rationale Record"]
        R1 --> R2 --> R3 --> R4
    end
```

And add the connection alongside the other `C -->` lines (after `C --> G1`):

```
    C --> R1
```

- [ ] **Step 3: Add reason to plugins table (Fix 7)**

After the audit row (line ~104), add:

```markdown
| 🧪 **[reason](#-reason)** | `0.1.0` | Hypothesis-driven reasoning with auditable evidence trails (FPF/ADI cycle). | `/reason` |
```

- [ ] **Step 4: Add reason section (Fix 8)**

After the `## 🧹 audit` section (after line ~255, before `## 📁 Project Structure`), add:

```markdown
---

## 🧪 reason

Hypothesis-driven reasoning with auditable evidence trails, based on the [First Principles Framework](https://github.com/ailev/FPF).

> **Required:** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `settings.json`

```bash
/plugin install reason@izteam
```

**Commands:**

```bash
/reason Which database for the new service?
/reason Monolith or microservices for our case?
/reason Speed vs correctness in the data pipeline?
```

**Natural language — also works:**

```
"Reason through the database choice with evidence"
"Compare options for auth strategy with trust scores"
"I need a decision record for the caching approach"
```

[Read more (EN) →](./plugins/reason/README.md) · [RU →](./plugins/reason/README.ru.md)
```

- [ ] **Step 5: Add reason to project structure (Fix 9)**

In the project structure tree (line ~266), change:

```text
├── plugins/
│   ├── team/
│   ├── think/
│   ├── arena/
│   └── audit/
```

to:

```text
├── plugins/
│   ├── team/
│   ├── think/
│   ├── arena/
│   ├── audit/
│   └── reason/
```

- [ ] **Step 6: Add reason to Quick Start install commands**

In the Quick Start section (lines ~117-123), add after `/plugin install audit@izteam`:

```bash
/plugin install reason@izteam
```

- [ ] **Step 7: Commit**

```bash
git add README.md
git commit -m "docs: add reason plugin to README — badge, graph, table, section, structure"
```

---

### Task 5: Update README.ru.md (Fix 10)

**Files:**
- Modify: `README.ru.md`

- [ ] **Step 1: Fix badge count**

Line ~11, change `Plugins-4-blue` to `Plugins-5-blue`.

- [ ] **Step 2: Add reason to mermaid graph**

After the `/audit` subgraph (after line 71 `G1 --> G2 --> G3`), add:

```mermaid
    subgraph "/reason &mdash; Reason"
        R1["🔬 Генерация конкурирующих гипотез"]
        R2["🔍 Логическая верификация"]
        R3["📊 Сбор эмпирических доказательств"]
        R4["📋 Design Rationale Record"]
        R1 --> R2 --> R3 --> R4
    end
```

And add `C --> R1` alongside other connections.

- [ ] **Step 3: Add reason to plugins table**

After the audit row (line ~104), add:

```markdown
| 🧪 **[reason](#-reason)** | `0.1.0` | Рассуждения на основе гипотез с аудируемыми цепочками доказательств (FPF/ADI цикл). | `/reason` |
```

- [ ] **Step 4: Add reason section**

After the `## 🧹 audit` section, before `## 📁 Структура проекта`, add:

```markdown
---

## 🧪 reason

Рассуждения на основе гипотез с аудируемыми цепочками доказательств, основано на [First Principles Framework](https://github.com/ailev/FPF).

> **Требуется:** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` в `settings.json`

```bash
/plugin install reason@izteam
```

**Команды:**

```bash
/reason Какую базу данных выбрать для нового сервиса?
/reason Монолит или микросервисы для нашего кейса?
/reason Скорость или корректность в data pipeline?
```

**Естественный язык — тоже работает:**

```
"Проанализируй выбор базы данных с доказательствами"
"Сравни варианты стратегии авторизации с trust-скорами"
"Мне нужен decision record по подходу к кешированию"
```

[Подробнее (RU) →](./plugins/reason/README.ru.md) · [EN →](./plugins/reason/README.md)
```

- [ ] **Step 5: Add reason to project structure**

Change the plugins tree to include `reason/`:

```text
├── plugins/
│   ├── team/
│   ├── think/
│   ├── arena/
│   ├── audit/
│   └── reason/
```

- [ ] **Step 6: Add reason to Quick Start install commands**

After `/plugin install audit@izteam`, add:

```bash
/plugin install reason@izteam
```

- [ ] **Step 7: Commit**

```bash
git add README.ru.md
git commit -m "docs: добавить reason плагин в README.ru.md"
```

---

### Task 6: Add comment to sync-mcp.sh (Out of Scope note)

**Files:**
- Modify: `scripts/sync-mcp.sh:10`

- [ ] **Step 1: Add explanatory comment**

In `scripts/sync-mcp.sh`, line 10, add a comment explaining why reason is excluded:

```bash
# Plugins that use MCP tools in their skills/agents.
# reason is intentionally excluded — it does not use MCP tools (no WebSearch/context7 in allowed-tools).
PLUGINS_WITH_MCP=(team arena think)
```

- [ ] **Step 2: Verify sync check still passes**

Run: `bash scripts/sync-mcp.sh --check`
Expected: `MCP SYNC CHECK PASSED: all plugins in sync`

- [ ] **Step 3: Commit**

```bash
git add scripts/sync-mcp.sh
git commit -m "docs: explain why reason is excluded from MCP sync"
```

---

## Verification Checklist

After all tasks are complete, verify:

- [ ] `bash scripts/validate-skills.sh` → ALL PASSED
- [ ] `bash scripts/sync-mcp.sh --check` → PASSED
- [ ] `grep -c "reason" README.md` → 5+ matches (badge, graph, table, section, structure)
- [ ] `grep -c "reason" README.ru.md` → 5+ matches
- [ ] `grep "reason" .github/workflows/auto-version.yml` → present in PLUGINS array
- [ ] `wc -l plugins/reason/skills/reason/references/evidence-scoring.md` → 70 lines (copied from arena)
