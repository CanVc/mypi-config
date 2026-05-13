#!/usr/bin/env bash
# apply-patches.sh — Apply committed patches to pi-subagents after package restore.
# Called by .pi/npm/postinstall or manually after `pi install`.
#
# Patches are stored in .pi/patches/ and are keyed by package name and version.
# Each patch file is a unified diff relative to .pi/npm/node_modules/<package>/.
#
# Usage:
#   bash .pi/patches/apply-patches.sh

set -euo pipefail

PATCHES_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$PATCHES_DIR/../.." && pwd)"
NODE_MODULES="$PROJECT_ROOT/.pi/npm/node_modules"

fail() {
  echo "apply-patches: ERROR: $*" >&2
  exit 1
}

if [ ! -d "$NODE_MODULES" ]; then
  fail "No node_modules found at $NODE_MODULES. Run: bash .pi/install-packages.sh"
fi

applied=0
already_applied=0

shopt -s nullglob
patch_files=("$PATCHES_DIR"/*.patch)
shopt -u nullglob

if [ "${#patch_files[@]}" -eq 0 ]; then
  fail "No patch files found in $PATCHES_DIR"
fi

for patch_file in "${patch_files[@]}"; do
  basename="$(basename "$patch_file")"

  if [[ ! "$basename" =~ ^(.+)-([0-9]+\.[0-9]+\.[0-9]+)-.+\.patch$ ]]; then
    fail "Patch filename must be '<package>-<exact-semver>-<description>.patch': $basename"
  fi

  package_name="${BASH_REMATCH[1]}"
  expected_version="${BASH_REMATCH[2]}"
  target="$NODE_MODULES/$package_name"

  if [ ! -d "$target" ]; then
    fail "$basename requires package '$package_name', but $target is not installed"
  fi

  installed_version="$(node -p "require('$target/package.json').version" 2>/dev/null || true)"
  if [ "$installed_version" != "$expected_version" ]; then
    fail "$basename requires $package_name@$expected_version, installed '${installed_version:-missing}'"
  fi

  if patch --dry-run -p1 -d "$target" < "$patch_file" >/dev/null 2>&1; then
    patch -p1 -d "$target" < "$patch_file"
    echo "apply-patches: APPLIED $basename"
    applied=$((applied + 1))
  elif patch --reverse --dry-run -p1 -d "$target" < "$patch_file" >/dev/null 2>&1; then
    echo "apply-patches: ALREADY_APPLIED $basename"
    already_applied=$((already_applied + 1))
  else
    # Later project patches can intentionally edit lines introduced by an
    # earlier patch. In that already-patched working tree, the earlier patch may
    # no longer reverse cleanly even though its behavior is present. Detect the
    # Story 1.5 pi-subagents UI patch as the superseding patch for Story 1.2.2's
    # display patch so --patch remains idempotent without hiding clean-install
    # failures (fresh installs still apply the display patch before Story 1.5).
    superseding_patch="$PATCHES_DIR/pi-subagents-0.24.2-ui-visibility-agent-activity.patch"
    if [ "$basename" = "pi-subagents-0.24.2-display-model-task-summary.patch" ] \
      && [ -f "$superseding_patch" ] \
      && patch --reverse --dry-run -p1 -d "$target" < "$superseding_patch" >/dev/null 2>&1; then
      echo "apply-patches: ALREADY_APPLIED $basename (superseded by $(basename "$superseding_patch"))"
      already_applied=$((already_applied + 1))
    else
      fail "$basename cannot be applied and is not already present; package version/content mismatch"
    fi
  fi
done

echo "apply-patches: $applied applied, $already_applied already applied"

# Inject postinstall hook into .pi/npm/package.json for convenience.
# This ensures future npm operations auto-apply patches.
# The durable source is the committed .pi/patches/ directory.
PKG_JSON="$NODE_MODULES/../package.json"
if [ -f "$PKG_JSON" ]; then
  python3 -c "
import json, sys
with open('$PKG_JSON') as f:
    pkg = json.load(f)
scripts = pkg.setdefault('scripts', {})
hook = 'bash ../patches/apply-patches.sh'
if scripts.get('postinstall') != hook:
    scripts['postinstall'] = hook
    with open('$PKG_JSON', 'w') as f:
        json.dump(pkg, f, indent=2)
        f.write('\\n')
    print('apply-patches: Injected postinstall hook into .pi/npm/package.json')
else:
    print('apply-patches: Postinstall hook already present in .pi/npm/package.json')
"
fi
