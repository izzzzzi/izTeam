#!/bin/bash
# Usage: ./scripts/bump-version.sh <plugin-name> [major|minor|patch]
# Example: ./scripts/bump-version.sh team patch
#          ./scripts/bump-version.sh think minor

set -euo pipefail

PLUGIN="${1:?Usage: bump-version.sh <plugin-name> [major|minor|patch]}"
BUMP="${2:-patch}"

PLUGIN_JSON="plugins/$PLUGIN/.claude-plugin/plugin.json"
MARKETPLACE_JSON=".claude-plugin/marketplace.json"

if [ ! -f "$PLUGIN_JSON" ]; then
  echo "❌ Plugin not found: $PLUGIN"
  echo "Available plugins:"
  ls -1 plugins/
  exit 1
fi

# Get current version
CURRENT=$(jq -r '.version' "$PLUGIN_JSON")
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"

# Bump
case "$BUMP" in
  major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
  minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
  patch) PATCH=$((PATCH + 1)) ;;
  *) echo "❌ Invalid bump type: $BUMP (use major|minor|patch)"; exit 1 ;;
esac

NEW="${MAJOR}.${MINOR}.${PATCH}"

# Update plugin.json
jq --arg v "$NEW" '.version = $v' "$PLUGIN_JSON" > tmp.json && mv tmp.json "$PLUGIN_JSON"

# Update marketplace.json
jq --arg n "$PLUGIN" --arg v "$NEW" '(.plugins[] | select(.name == $n)).version = $v' "$MARKETPLACE_JSON" > tmp.json && mv tmp.json "$MARKETPLACE_JSON"

# Update version in README.md and README.ru.md
sed -i '' "s/\(\[${PLUGIN}\](#[^)]*)\*\* | \)\`[0-9]*\.[0-9]*\.[0-9]*\`/\1\`${NEW}\`/" README.md README.ru.md 2>/dev/null || \
sed -i "s/\(\[${PLUGIN}\](#[^)]*)\*\* | \)\`[0-9]*\.[0-9]*\.[0-9]*\`/\1\`${NEW}\`/" README.md README.ru.md

echo "✅ $PLUGIN: $CURRENT → $NEW"
echo ""
echo "Next steps:"
echo "  git add $PLUGIN_JSON $MARKETPLACE_JSON README.md README.ru.md"
echo "  git commit -m \"release: $PLUGIN v$NEW\""
echo "  git push"
