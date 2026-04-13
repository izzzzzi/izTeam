# MCP Server Deduplication

> **Status:** Research complete
> **Date:** 2026-03-01
> **Goal:** Eliminate MCP config duplication across plugins, reduce tool namespace bloat

---

## Table of Contents

1. [Overview](#overview)
2. [Current Duplication Scope](#1-current-duplication-scope)
3. [Claude Code MCP Architecture](#2-claude-code-mcp-architecture)
4. [Plugin-level vs Global MCP](#3-plugin-level-vs-global-mcp)
5. [Agent Tool Filtering](#4-agent-tool-filtering)
6. [Performance Impact](#5-performance-impact)
7. [Recommended Architecture](#6-recommended-architecture)
8. [Implementation Plan](#implementation-plan)

---

## Overview

### Goals

1. **Eliminate 3x duplication** — identical `.mcp.json` across team/arena/think plugins
2. **Reduce tool namespace bloat** — 90+ deferred MCP tools (same 6 servers x 3 plugins + user-level)
3. **Single source of truth** — one place to add/remove/update MCP servers

### Key Decisions

| Aspect | Decision |
|--------|----------|
| Config location | Single source at `shared/mcp-servers.json`, generated into each plugin |
| Generation mechanism | `scripts/sync-mcp.sh` + CI validation check |
| Agent access control | Keep current pattern — `tools:` allowlist / `disallowedTools:` denylist |
| Performance optimization | Not urgent — MCP servers are session-wide, not per-agent |
| Plugin distribution | Generated `.mcp.json` files committed to git for marketplace compatibility |

---

## 1. Current Duplication Scope

> **Expert:** Sam Newman (Architecture)

### Inventory

| File | Servers | Status |
|------|---------|--------|
| `plugins/team/.mcp.json` | 6 servers (context7, deepwiki, exa, ddg-search, codewiki, tavily) | Identical |
| `plugins/arena/.mcp.json` | Same 6 servers | Identical |
| `plugins/think/.mcp.json` | Same 6 servers | Identical |
| `plugins/audit/` | No `.mcp.json` | Intentional |

**All three files are byte-for-byte identical.** 18 total MCP definitions, 12 are pure duplication.

### Tool Namespace Explosion

Each plugin's MCP servers get namespaced separately:
```
mcp__plugin_team_context7__resolve-library-id
mcp__plugin_arena_context7__resolve-library-id
mcp__plugin_think_context7__resolve-library-id
mcp__context7__resolve-library-id              (user-level)
mcp__plugin_context7_context7__resolve-library-id  (official plugin)
```

Result: **5 instances of context7** in a single session. ~90+ deferred MCP tools total.

---

## 2. Claude Code MCP Architecture

> **Expert:** Kelsey Hightower (DevOps)

### Key Findings

| Property | Behavior |
|----------|----------|
| MCP scope hierarchy | local > project > user > plugin (no inheritance between levels) |
| Plugin MCP isolation | Each plugin's `.mcp.json` creates independently namespaced tools |
| Cross-plugin sharing | **Not supported** — no inheritance, no shared config mechanism |
| Subagent MCP access | Session-wide — subagents inherit MCP tools from main session |
| Plugin sandboxing | Plugins cannot reference files outside their directory after installation |
| Symlinks | Resolved at cache copy time — works but fragile |

### Platform Constraints

- **No plugin dependency mechanism** — cannot declare "plugin A requires plugin B"
- **No shared `.mcp.json`** — official docs state "each plugin independently configures and manages its MCP servers"
- **Open bugs** (#13605, #21560, #15810) — custom subagents may not reliably access plugin MCP tools

---

## 3. Plugin-level vs Global MCP

> **Expert:** Theo Browne (API Design)

### Options Evaluated

| Option | Viable? | Why |
|--------|---------|-----|
| A: Project-root `.mcp.json` | No | Does not work for marketplace-installed plugins |
| B: Symlinks to shared file | Partial | Works on macOS/Linux, fragile on Windows, subtle mechanism |
| C: MCP proxy/gateway | No | Over-engineered, no mature implementation exists |
| **D: Generated from single source** | **Yes** | Fits existing patterns, works with marketplace, CI-enforced |

### Why Option D Wins

1. Plugins are distributed via marketplace — each must contain a real `.mcp.json`
2. Project already uses generation scripts (`bump-version.sh`, `validate-skills.sh`)
3. CI already validates cross-plugin consistency
4. Supports per-plugin overrides if needs diverge in future

---

## 4. Agent Tool Filtering

> **Expert:** Dan Abramov (Component Architecture)

### Current Patterns (Working Correctly)

| Pattern | Agents | MCP Access |
|---------|--------|------------|
| `tools:` allowlist (strict) | auditors, coder, supervisor, reviewers | Blocked — MCP not in allowlist |
| `disallowedTools:` denylist | arena researcher, arena expert, think expert | Inherited — MCP available |
| No `.mcp.json` at plugin level | all audit agents | Blocked — no MCP servers configured |

**No changes needed.** The `tools:` allowlist implicitly blocks MCP tools for agents that don't need them. Research agents use `disallowedTools:` and get MCP by inheritance. Agent prompts already handle MCP absence gracefully: "Check availability before use. If MCP is unavailable — WebSearch and WebFetch always work."

---

## 5. Performance Impact

> **Expert:** Martin Kleppmann (Distributed Systems)

### Critical Finding: MCP is Session-Wide, Not Per-Agent

MCP servers are started **once per session**, not per agent. A build session with 10+ agents still runs only:
- 4 Node.js child processes (stdio servers) — ~440 MB total
- 2 HTTP connections (deepwiki, exa) — stateless, zero local cost

### Cost Model

| Cost Category | Value | Impact |
|---------------|-------|--------|
| Memory (4 stdio processes) | ~440 MB | Fixed per session |
| Cold start (npx) | 8-20 seconds | One-time |
| Warm start (cached) | < 4 seconds | Subsequent sessions |
| Tool definitions (with Tool Search) | ~8.5K tokens | Deferred, low impact |
| Tool definitions (without Tool Search) | ~85-95K tokens | Would be severe |
| Per-call latency (stdio) | < 5 ms | Negligible |
| Per-call latency (HTTP) | 100-500 ms | Network-bound |

### Conclusion

Performance is **not the primary concern**. The real problem is:
1. **Maintenance burden** — updating 3 identical files
2. **Tool namespace bloat** — 90+ deferred tools instead of ~30
3. **Drift risk** — files can accidentally diverge

---

## 6. Recommended Architecture

> **Expert:** Sam Newman (Architecture)

### Solution: Generated `.mcp.json` from Single Source

```
shared/
  mcp-servers.json              # Single source of truth

scripts/
  sync-mcp.sh                   # Generates plugins/*/.mcp.json

.github/workflows/validate.yml  # CI check: generated files match source
```

### How It Works

1. `shared/mcp-servers.json` defines the canonical 6 MCP servers
2. `scripts/sync-mcp.sh` copies it to `plugins/{team,arena,think}/.mcp.json`
3. Generated files include a header comment: `// AUTO-GENERATED — do not edit`
4. CI validates consistency on every push
5. `audit` plugin intentionally excluded (no MCP needed)

### Per-Plugin Overrides (Future)

If a plugin ever needs different MCP servers:
- Create `plugins/<name>/.mcp-override.json`
- Script merges shared config + overrides
- Not needed today — all 3 plugins use identical config

---

## Implementation Plan

### Phase 1: Single Source + Generation Script

- [ ] Create `shared/mcp-servers.json` with canonical MCP config
- [ ] Create `scripts/sync-mcp.sh` that generates `plugins/*/.mcp.json`
- [ ] Add auto-generated header to output files
- [ ] Run script to verify output matches current files
- [ ] Add MCP consistency check to `validate-skills.sh` or `validate.yml`

### Phase 2: CI Enforcement

- [ ] Add CI step that runs `sync-mcp.sh --check` (verify, don't write)
- [ ] Document in CLAUDE.md: "After MCP changes, run `./scripts/sync-mcp.sh`"

### Phase 3: Cleanup (Optional)

- [ ] Pin `@latest` versions in MCP config for stable cold starts
- [ ] Evaluate removing `codewiki-mcp` from `~/.claude/mcp.json` (provided by plugin)
- [ ] Monitor Claude Code for native plugin MCP sharing support

---

## Success Metrics

| Metric | Baseline | Target |
|--------|----------|--------|
| MCP config files to edit | 3 | 1 (shared source) |
| Deferred MCP tools | ~90+ | ~90 (unchanged, but single source of truth) |
| Risk of config drift | High | Zero (CI-enforced) |
| Maintenance burden | Edit 3 files | Edit 1 file + run script |

---

## Sources

- [Claude Code MCP Docs](https://code.claude.com/docs/en/mcp)
- [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference)
- [GitHub #13605](https://github.com/anthropics/claude-code/issues/13605) — subagent MCP access bug
- [GitHub #6915](https://github.com/anthropics/claude-code/issues/6915) — session-wide MCP sharing
- [GitHub #16143](https://github.com/anthropics/claude-code/issues/16143) — inline mcpServers broken
- [TM Dev Lab Benchmark](https://www.tmdevlab.com/mcp-server-performance-benchmark.html) — Node.js MCP: 110 MB, 10.66 ms
- [Joe Njenga](https://medium.com/@joe.njenga/claude-code-just-cut-mcp-context-bloat-by-46-9-51k-tokens-down-to-8-5k-with-new-tool-search-ddf9e905f734) — Tool Search 46.9% reduction
