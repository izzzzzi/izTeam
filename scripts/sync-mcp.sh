#!/usr/bin/env bash
# Usage: ./scripts/sync-mcp.sh [--check] [--verbose] [--help]
# Synchronizes MCP server config from shared/mcp-servers.json to plugin directories.
# Use --check to verify consistency without writing (for CI).

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE="$ROOT/shared/mcp-servers.json"
# Plugins that use MCP tools in their skills/agents.
# reason is intentionally excluded — it does not use MCP tools (no WebSearch/context7 in allowed-tools).
PLUGINS_WITH_MCP=(team arena think)
CHECK_MODE=false
VERBOSE=false

for arg in "$@"; do
  case "$arg" in
    --check) CHECK_MODE=true ;;
    --verbose) VERBOSE=true ;;
    --help|-h)
      echo "Usage: ./scripts/sync-mcp.sh [--check] [--verbose]"
      echo "  Syncs shared/mcp-servers.json to plugins that need MCP."
      echo ""
      echo "Options:"
      echo "  --check    Verify consistency without writing (for CI)"
      echo "  --verbose  Show detailed output"
      echo "  --help     Show this help message"
      exit 0
      ;;
    *) echo "Unknown option: $arg"; exit 1 ;;
  esac
done

if [ ! -f "$SOURCE" ]; then
  echo "ERROR: Source file not found: shared/mcp-servers.json" >&2
  exit 1
fi

# Validate source is valid JSON
if ! jq . "$SOURCE" > /dev/null 2>&1; then
  echo "ERROR: shared/mcp-servers.json is not valid JSON" >&2
  exit 1
fi

ERRORS=0

for plugin in "${PLUGINS_WITH_MCP[@]}"; do
  target="$ROOT/plugins/$plugin/.mcp.json"

  if $CHECK_MODE; then
    if [ ! -f "$target" ]; then
      echo "FAIL: plugins/$plugin/.mcp.json does not exist" >&2
      ERRORS=$((ERRORS + 1))
    elif ! diff -q "$SOURCE" "$target" > /dev/null 2>&1; then
      echo "FAIL: plugins/$plugin/.mcp.json differs from shared/mcp-servers.json" >&2
      if $VERBOSE; then
        diff "$SOURCE" "$target" || true
      fi
      echo "  FIX: Run ./scripts/sync-mcp.sh to update" >&2
      ERRORS=$((ERRORS + 1))
    else
      if $VERBOSE; then
        echo "PASS: plugins/$plugin/.mcp.json is in sync"
      fi
    fi
  else
    cp "$SOURCE" "$target"
    if $VERBOSE; then
      echo "SYNCED: plugins/$plugin/.mcp.json"
    fi
  fi
done

if $CHECK_MODE; then
  if [ "$ERRORS" -gt 0 ]; then
    echo ""
    echo "MCP SYNC CHECK FAILED: $ERRORS plugin(s) out of sync"
    echo "Run: ./scripts/sync-mcp.sh"
    exit 1
  else
    echo "MCP SYNC CHECK PASSED: all plugins in sync"
    exit 0
  fi
else
  echo "MCP config synced to ${#PLUGINS_WITH_MCP[@]} plugins"
fi
