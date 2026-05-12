# Review Round 3 — Reviewer B — Story 1.2

## Verdict

Changes Requested. Runtime behavior in the current working tree is mostly sound, and the real provider-free discovery checks pass in this environment. However, the committed durability path is still not fail-closed: clean restores can drift from the pinned package version and can report success with the required patch missing.

## Severity counts

- High: 0
- Medium: 2
- Low: 0

## Findings

### ID: R3-B-1

Severity: Medium  
Bucket: Durability / Package pinning  
Title: Tracked installer converts the exact `pi-subagents@0.24.2` pin into a floating npm dependency  
Location: `.pi/install-packages.sh:57-66`; `.pi/settings.json:1-4`; local evidence `.pi/npm/package.json:1-6`  
Evidence: `.pi/settings.json` declares the required exact package spec `npm:pi-subagents@0.24.2`, but `.pi/install-packages.sh` parses that spec and writes `deps[name] = '^' + version`. The generated ignored install output confirms the dependency is `pi-subagents` at `^0.24.2` rather than exact `0.24.2`. Because `.pi/npm/package-lock.json` is ignored, a clean restore can resolve a later compatible 0.24.x package while the committed patch remains version-specific to `pi-subagents-0.24.2`.  
AC/Constraint impacted: AC2, AC3, AC5, AC6; story requirement to confirm/pin `npm:pi-subagents@0.24.2` or an approved replacement; durability from tracked sources.  
Recommended action: Preserve exact npm versions when generating `.pi/npm/package.json` (or commit/use an equivalent lock/local fork strategy). Add a clean-restore validation that asserts the installed package version is exactly the settings version before applying the patch.

### ID: R3-B-2

Severity: Medium  
Bucket: Durability / Fail-closed patching  
Title: Patch application can silently skip the required runtime fix and still exit successfully  
Location: `.pi/patches/apply-patches.sh:17-20,57-67`; `.pi/install-packages.sh:92-100`  
Evidence: `apply-patches.sh` exits 0 when `node_modules` is absent, increments `skipped` when a patch has no target or does not apply cleanly, and only prints `applied/skipped` counts. It does not distinguish already-applied patches from version mismatch, and it does not assert that the required markers for project-agent overrides and legacy `.agents` exclusion are present after patching. `install-packages.sh` calls the script and then prints Done without any postcondition. Therefore a clean restore with a mismatched package or failed patch can appear successful while AC2/AC3/AC5/AC6 behavior is absent. Current local evidence shows the patch is applied in this workspace, but the tracked restore mechanism is not fail-closed.  
AC/Constraint impacted: AC2, AC3, AC5, AC6, AC9; safety requirement to block/report invalid required configuration; durability from tracked sources.  
Recommended action: Make patching fail closed: verify the installed package/version, treat an unapplied required patch as an error unless reverse-apply proves it is already applied, and assert expected source markers or runtime discovery/override behavior before `install-packages.sh` exits successfully.

## Validation run

- `git status --short` showed modified `.pi/settings.json`, story artifact, and sprint status; untracked implementation files under `.pi/agents/`, `.pi/install-packages.sh`, `.pi/patches/`, and `tests/test_agent_definitions_model_routing.py`; no deleted tracked files. Existing untracked review artifacts were observed only as process evidence and not used as opinion source.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` — 79 tests ran, OK.
- `PI_TELEMETRY=0 pi list` — project package loaded from `/home/cvc/dev/mypi-config/.pi/npm/node_modules/pi-subagents` as `npm:pi-subagents@0.24.2`.
- `PI_TELEMETRY=0 pi --list-models || true` — active registry includes `zai/glm-5.1`, `openai-codex/gpt-5.1`, and `openai-codex/gpt-5.5`.
- Direct provider-free runtime discovery via `npx tsx` and `discoverAgentsAll(process.cwd())` returned only project agents `implementer`, `reviewer-a`, and `reviewer-b` with models `zai/glm-5.1`, `openai-codex/gpt-5.1`, and `openai-codex/gpt-5.5`; builtin `reviewer` resolved to the project settings override `openai-codex/gpt-5.5`.
- `find . \( -name __pycache__ -o -name *.pyc -o -name *.pyo \) -print` — no bytecode/cache output.
- `git check-ignore -v .pi/npm/package.json .pi/npm/package-lock.json .pi/npm/node_modules/pi-subagents/package.json` confirmed generated install outputs are ignored/local evidence only.
