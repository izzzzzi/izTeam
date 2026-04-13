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
