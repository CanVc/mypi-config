"""
Story 1.2: Agent Definitions and Model Routing Contract — Regression/validation tests.

Tests cover AC1–AC9:
  - Wrapper agent file presence, naming, frontmatter correctness (AC1, AC4, AC8, AC9)
  - No subagent tool granted to wrapper agents (AC1 safety)
  - Skills and legacy trees are not exposed as dispatchable project agents (AC2, AC3)
  - Model routing from agent file (AC4, AC8)
  - Settings override precedence: project > user > file (AC5, AC6)
  - Missing/invalid model configuration fails closed (AC9)
  - Committed model references are valid Pi model IDs (AC7)
  - Committed override keys resolve to discovered agents (AC5)

Runtime integration tests exercise actual pi-subagents discovery/resolution
via npx tsx subprocess with isolated project/user settings, providing provider-free
validation of precedence, discovery, and override behavior.
"""

import unittest
import json
import os
import re
import shutil
import tempfile
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PI_AGENTS_DIR = ROOT / ".pi" / "agents"
PI_SETTINGS = ROOT / ".pi" / "settings.json"
PI_SKILLS_DIR = ROOT / ".pi" / "skills"
LEGACY_AGENTS_DIR = ROOT / ".agents"
PATCHES_DIR = ROOT / ".pi" / "patches"
APPLY_SCRIPT = PATCHES_DIR / "apply-patches.sh"
INSTALL_SCRIPT = ROOT / ".pi" / "install-packages.sh"
PI_NPM_MODULES = ROOT / ".pi" / "npm" / "node_modules"
PATCHED_AGENTS_TS = PI_NPM_MODULES / "pi-subagents" / "src" / "agents" / "agents.ts"
PI_SUBAGENTS_SRC = PI_NPM_MODULES / "pi-subagents" / "src" / "agents" / "agents.ts"

# Expected wrapper agents and their properties
EXPECTED_AGENTS = {
    "implementer": {
        "file": "implementer.md",
        "roleLabel": "BMAD Implementer",
        "model": "zai/glm-5.1",
        "tools": ["read", "grep", "find", "ls", "bash", "edit", "write"],
        "systemPromptMode": "replace",
        "inheritProjectContext": True,
        "inheritSkills": False,
        "defaultContext": "fresh",
    },
    "reviewer-a": {
        "file": "reviewer-a.md",
        "roleLabel": "BMAD Reviewer A",
        "model": "openai-codex/gpt-5.4",
        "tools": ["read", "grep", "find", "ls", "bash"],
        "systemPromptMode": "replace",
        "inheritProjectContext": True,
        "inheritSkills": False,
        "defaultContext": "fresh",
    },
    "reviewer-b": {
        "file": "reviewer-b.md",
        "roleLabel": "BMAD Reviewer B",
        "model": "openai-codex/gpt-5.5",
        "tools": ["read", "grep", "find", "ls", "bash"],
        "systemPromptMode": "replace",
        "inheritProjectContext": True,
        "inheritSkills": False,
        "defaultContext": "fresh",
    },
    "findings-triager": {
        "file": "findings-triager.md",
        "roleLabel": "BMAD Findings Triager",
        "model": "openai-codex/gpt-5.5",
        "tools": ["read", "grep", "find", "ls", "bash", "edit", "write"],
        "systemPromptMode": "replace",
        "inheritProjectContext": True,
        "inheritSkills": False,
        "defaultContext": "fresh",
    },
}

# Agents that must NOT exist as dispatchable wrappers
FORBIDDEN_AGENTS = ["orchestrator", "bmad-orchestrator"]

# Known Pi model IDs available in the active environment
KNOWN_MODEL_IDS = {
    "zai/glm-4.5-air",
    "zai/glm-4.7",
    "zai/glm-5-turbo",
    "zai/glm-5.1",
    "zai/glm-5v-turbo",
    "openai-codex/gpt-5.1",
    "openai-codex/gpt-5.1-codex-max",
    "openai-codex/gpt-5.1-codex-mini",
    "openai-codex/gpt-5.2",
    "openai-codex/gpt-5.2-codex",
    "openai-codex/gpt-5.3-codex",
    "openai-codex/gpt-5.3-codex-spark",
    "openai-codex/gpt-5.4",
    "openai-codex/gpt-5.4-mini",
    "openai-codex/gpt-5.5",
}

# Known builtin agent names from pi-subagents
KNOWN_BUILTIN_AGENTS = {
    "scout", "researcher", "planner", "worker", "reviewer",
    "context-builder", "oracle", "delegate",
}


def parse_frontmatter(text: str) -> dict:
    """Parse YAML frontmatter from a markdown string."""
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    fm_text = match.group(1)
    result = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            # Handle boolean values
            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            result[key] = value
    return result


def parse_tools_field(tools_str: str) -> list:
    """Parse a comma-separated tools field into a sorted list."""
    if not tools_str:
        return []
    return sorted(t.strip() for t in tools_str.split(",") if t.strip())


def _runtime_available() -> bool:
    """Check whether the patched pi-subagents runtime is available for integration tests."""
    return PI_SUBAGENTS_SRC.exists()


def _run_tsx_discovery(project_dir: str, home_dir: str | None = None) -> dict:
    """
    Run actual pi-subagents discoverAgentsAll via npx tsx subprocess.

    Returns parsed JSON with project agents, builtin agents, etc.
    Uses isolated HOME for user settings isolation.
    Writes TypeScript to a temp file to avoid shell quoting issues.
    """
    tsx_file = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as f:
            f.write(f'import {{ discoverAgentsAll }} from "{PI_SUBAGENTS_SRC}";\n')
            f.write(f'const result = discoverAgentsAll("{project_dir}");\n')
            f.write('const output = {\n')
            f.write('  project: result.project.map(a => ({ name: a.name, model: a.model, source: a.source })),\n')
            f.write('  builtin: result.builtin.map(a => ({ name: a.name, model: a.model })),\n')
            f.write('  userSettingsPath: result.userSettingsPath,\n')
            f.write('  projectSettingsPath: result.projectSettingsPath,\n')
            f.write('};\n')
            f.write('console.log(JSON.stringify(output));\n')
            tsx_file = f.name

        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        # Some tests isolate HOME so pi-subagents reads only temp user settings.
        # Keep npm/npx cache outside that isolated HOME; otherwise `npx tsx` may
        # attempt a fresh package resolution per test and hang or exceed the
        # subprocess timeout on clean machines.
        env.setdefault("NPM_CONFIG_CACHE", str(Path.home() / ".npm"))
        env.setdefault("NPM_CONFIG_YES", "true")
        if home_dir:
            env["HOME"] = home_dir

        result = subprocess.run(
            ["npx", "--yes", "tsx", tsx_file],
            capture_output=True, text=True, timeout=60, env=env,
            cwd=project_dir,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"tsx discovery failed (rc={result.returncode}): {result.stderr[:500]}"
            )
        # Find the JSON line in stdout (skip npm notices)
        for line in result.stdout.strip().split("\n"):
            line = line.strip()
            if line.startswith("{"):
                return json.loads(line)
        raise RuntimeError(f"No JSON output from tsx: {result.stdout[:500]}")
    finally:
        if tsx_file:
            os.unlink(tsx_file)


def _create_isolated_project(
    tmpdir: str,
    agent_files: dict[str, str] | None = None,
    project_settings: dict | None = None,
    user_settings: dict | None = None,
    include_legacy_agents: bool = False,
) -> tuple[str, str | None]:
    """
    Create an isolated temp project with pi-subagents available for discovery testing.

    Returns (project_dir, home_dir_or_None).
    """
    project_dir = Path(tmpdir) / "project"
    project_dir.mkdir()

    # Copy patched pi-subagents to temp project
    npm_dir = project_dir / ".pi" / "npm" / "node_modules"
    npm_dir.mkdir(parents=True)
    if PI_NPM_MODULES.exists():
        shutil.copytree(
            PI_NPM_MODULES / "pi-subagents",
            npm_dir / "pi-subagents",
        )

    # Create .pi/agents/ with specified agent files (or copy from project)
    agents_dir = project_dir / ".pi" / "agents"
    agents_dir.mkdir(parents=True)
    if agent_files:
        for name, content in agent_files.items():
            (agents_dir / name).write_text(content)
    else:
        for agent_file in PI_AGENTS_DIR.iterdir():
            if agent_file.suffix == ".md":
                shutil.copy2(agent_file, agents_dir / agent_file.name)

    # Create project settings
    settings_path = project_dir / ".pi" / "settings.json"
    if project_settings:
        settings_path.write_text(json.dumps(project_settings, indent=2))
    else:
        settings_path.write_text(json.dumps({"packages": ["npm:pi-subagents@0.24.2"]}))

    # Create legacy .agents/ if requested
    if include_legacy_agents:
        legacy_dir = project_dir / ".agents" / "skills" / "fake-skill"
        legacy_dir.mkdir(parents=True)
        (legacy_dir / "SKILL.md").write_text(
            "---\nname: fake-skill-agent\ndescription: Should not be discovered\ntools: read\n---\nBody.\n"
        )

    # Create user settings in isolated HOME if requested
    home_dir = None
    if user_settings:
        home_dir = str(Path(tmpdir) / "home")
        home_agent_dir = Path(home_dir) / ".pi" / "agent"
        home_agent_dir.mkdir(parents=True)
        (home_agent_dir / "settings.json").write_text(json.dumps(user_settings, indent=2))

    return str(project_dir), home_dir


def validate_provider_free_model_contract(
    project_dir: str,
    known_model_ids: set[str] | None = None,
    valid_override_targets: set[str] | None = None,
) -> list[str]:
    """
    Provider-free AC9 validation for required wrapper model configuration.

    Fails closed by returning actionable errors for:
      - missing/empty required wrapper model
      - unknown wrapper model
      - override targeting an unknown agent
      - override with missing/empty/unknown model
    """
    known_model_ids = known_model_ids or KNOWN_MODEL_IDS
    project_path = Path(project_dir)
    agents_dir = project_path / ".pi" / "agents"
    settings_path = project_path / ".pi" / "settings.json"

    settings = {}
    if settings_path.exists():
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    overrides = settings.get("subagents", {}).get("agentOverrides", {})

    agent_files = sorted(agents_dir.glob("*.md")) if agents_dir.exists() else []
    agents: dict[str, tuple[Path, dict]] = {}
    errors: list[str] = []

    for agent_file in agent_files:
        fm = parse_frontmatter(agent_file.read_text(encoding="utf-8"))
        agent_id = fm.get("name") or agent_file.stem
        agents[agent_id] = (agent_file, fm)

    valid_targets = valid_override_targets or (set(agents) | KNOWN_BUILTIN_AGENTS)

    for override_key, cfg in overrides.items():
        override_path = f"subagents.agentOverrides.{override_key}.model"
        model = cfg.get("model") if isinstance(cfg, dict) else None
        if override_key not in valid_targets:
            errors.append(
                f"[AC9] override '{override_path}' targets unknown agent '{override_key}'; "
                "required fix: rename the override to a discovered agent ID or remove it."
            )
        if model is None or str(model).strip() == "":
            errors.append(
                f"[AC9] override '{override_path}' is missing or empty; required fix: "
                "set it to an approved Pi model ID or remove the invalid override."
            )
        elif model not in known_model_ids:
            errors.append(
                f"[AC9] override '{override_path}' uses unknown model '{model}'; "
                "required fix: use an approved Pi model ID from the active registry."
            )

    for agent_id, (agent_file, fm) in agents.items():
        override_cfg = overrides.get(agent_id, {})
        override_model = override_cfg.get("model") if isinstance(override_cfg, dict) else None
        effective_model = override_model if override_model is not None else fm.get("model")
        rel_agent_path = f".pi/agents/{agent_file.name}"

        if effective_model is None or str(effective_model).strip() == "":
            errors.append(
                f"[AC9] agent '{agent_id}' has no required model in {rel_agent_path}; "
                f"required fix: set non-empty valid 'model' in {rel_agent_path} or "
                f"subagents.agentOverrides.{agent_id}.model."
            )
        elif effective_model not in known_model_ids:
            source = (
                f"subagents.agentOverrides.{agent_id}.model"
                if override_model is not None else f"{rel_agent_path} model"
            )
            errors.append(
                f"[AC9] agent '{agent_id}' resolves unknown model '{effective_model}' from {source}; "
                "required fix: use an approved Pi model ID from the active registry."
            )

    return errors


# ---------------------------------------------------------------------------
# AC1: Agent directory structure and frontmatter
# ---------------------------------------------------------------------------

class TestAgentDirectoryStructure(unittest.TestCase):
    """AC1: .pi/agents/ exists with expected wrapper files."""

    def test_pi_agents_directory_exists(self):
        self.assertTrue(PI_AGENTS_DIR.is_dir(), ".pi/agents/ directory must exist")

    def test_expected_wrapper_agents_are_present(self):
        actual_files = {f.name for f in PI_AGENTS_DIR.iterdir() if f.suffix == ".md"}
        for agent_id, props in EXPECTED_AGENTS.items():
            self.assertIn(props["file"], actual_files,
                          f"Expected agent file {props['file']} not found in .pi/agents/")

    def test_no_extra_md_files_beyond_expected(self):
        actual_files = {f.name for f in PI_AGENTS_DIR.iterdir() if f.suffix == ".md"}
        expected_files = {props["file"] for props in EXPECTED_AGENTS.values()}
        extra = actual_files - expected_files
        self.assertEqual(extra, set(),
                         f"Unexpected agent files in .pi/agents/: {extra}. "
                         f"Only the approved v1 roster should be present.")


class TestForbiddenAgents(unittest.TestCase):
    """AC1/Scope: No orchestrator or bmad-orchestrator wrapper agents."""

    def test_no_orchestrator_wrapper(self):
        for forbidden in FORBIDDEN_AGENTS:
            path = PI_AGENTS_DIR / f"{forbidden}.md"
            self.assertFalse(path.exists(),
                             f"Forbidden agent file must not exist: {forbidden}.md")

    def test_no_v2_tdd_agents(self):
        v2_agents = ["test-architect", "test-writer", "red-validator", "green-validator"]
        for agent_name in v2_agents:
            path = PI_AGENTS_DIR / f"{agent_name}.md"
            self.assertFalse(path.exists(),
                             f"v2 TDD agent must not exist in this story: {agent_name}.md")


class TestAgentFrontmatter(unittest.TestCase):
    """AC1, AC4, AC8: Each wrapper has correct, readable frontmatter."""

    def _read_agent(self, agent_id: str) -> tuple[dict, str]:
        props = EXPECTED_AGENTS[agent_id]
        path = PI_AGENTS_DIR / props["file"]
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        return fm, text

    def test_name_matches_filename_stem(self):
        for agent_id in EXPECTED_AGENTS:
            with self.subTest(agent=agent_id):
                fm, _ = self._read_agent(agent_id)
                self.assertEqual(fm.get("name"), agent_id)

    def test_description_exists_and_is_readable(self):
        for agent_id in EXPECTED_AGENTS:
            with self.subTest(agent=agent_id):
                fm, _ = self._read_agent(agent_id)
                self.assertIn("description", fm)
                self.assertGreater(len(fm["description"]), 10)

    def test_role_label_exists(self):
        for agent_id, props in EXPECTED_AGENTS.items():
            with self.subTest(agent=agent_id):
                fm, _ = self._read_agent(agent_id)
                self.assertIn("roleLabel", fm)
                self.assertEqual(fm["roleLabel"], props["roleLabel"])

    def test_model_exists(self):
        for agent_id, props in EXPECTED_AGENTS.items():
            with self.subTest(agent=agent_id):
                fm, _ = self._read_agent(agent_id)
                self.assertIn("model", fm)
                self.assertEqual(fm["model"], props["model"])

    def test_tools_are_explicit(self):
        for agent_id, props in EXPECTED_AGENTS.items():
            with self.subTest(agent=agent_id):
                fm, _ = self._read_agent(agent_id)
                self.assertIn("tools", fm)
                actual_tools = parse_tools_field(fm["tools"])
                expected_tools = sorted(props["tools"])
                self.assertEqual(actual_tools, expected_tools)

    def test_no_subagent_tool(self):
        """AC1 safety: wrapper agents must not receive the subagent tool."""
        for agent_id in EXPECTED_AGENTS:
            with self.subTest(agent=agent_id):
                fm, _ = self._read_agent(agent_id)
                tools = parse_tools_field(fm.get("tools", ""))
                self.assertNotIn("subagent", tools)

    def test_system_prompt_mode_is_replace(self):
        for agent_id in EXPECTED_AGENTS:
            with self.subTest(agent=agent_id):
                fm, _ = self._read_agent(agent_id)
                self.assertEqual(fm.get("systemPromptMode"), "replace")

    def test_inherit_project_context(self):
        for agent_id, props in EXPECTED_AGENTS.items():
            with self.subTest(agent=agent_id):
                fm, _ = self._read_agent(agent_id)
                self.assertEqual(fm.get("inheritProjectContext"), props["inheritProjectContext"])

    def test_inherit_skills_is_false(self):
        for agent_id in EXPECTED_AGENTS:
            with self.subTest(agent=agent_id):
                fm, _ = self._read_agent(agent_id)
                self.assertEqual(fm.get("inheritSkills"), False)

    def test_default_context_is_fresh(self):
        for agent_id in EXPECTED_AGENTS:
            with self.subTest(agent=agent_id):
                fm, _ = self._read_agent(agent_id)
                self.assertEqual(fm.get("defaultContext"), "fresh")

    def test_no_package_field(self):
        for agent_id in EXPECTED_AGENTS:
            with self.subTest(agent=agent_id):
                fm, _ = self._read_agent(agent_id)
                self.assertNotIn("package", fm)

    def test_filenames_are_lowercase_kebab_case(self):
        for agent_id, props in EXPECTED_AGENTS.items():
            with self.subTest(agent=agent_id):
                filename = props["file"]
                self.assertEqual(filename, filename.lower())
                self.assertNotIn("_", filename)
                self.assertTrue(re.match(r"^[a-z0-9-]+\.md$", filename))

    def test_prompt_body_is_nontrivial(self):
        for agent_id in EXPECTED_AGENTS:
            with self.subTest(agent=agent_id):
                _, text = self._read_agent(agent_id)
                body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, flags=re.DOTALL)
                self.assertGreater(len(body.strip()), 100)

    def test_wrapper_prompt_is_thin_not_full_skill_copy(self):
        for agent_id in EXPECTED_AGENTS:
            with self.subTest(agent=agent_id):
                _, text = self._read_agent(agent_id)
                self.assertLess(len(text), 8000)


# ---------------------------------------------------------------------------
# AC4, AC7, AC8: Model routing from agent files
# ---------------------------------------------------------------------------

class TestModelRoutingFromAgentFile(unittest.TestCase):
    """AC4, AC8: Agent file model assignment is readable and different agents have different models."""

    def test_each_agent_has_a_model(self):
        for agent_id, props in EXPECTED_AGENTS.items():
            with self.subTest(agent=agent_id):
                path = PI_AGENTS_DIR / props["file"]
                fm = parse_frontmatter(path.read_text(encoding="utf-8"))
                self.assertIn("model", fm)
                self.assertTrue(fm["model"])

    def test_at_least_two_different_models_across_agents(self):
        """AC7: Two sub-agents are assigned different models."""
        models = set()
        for agent_id, props in EXPECTED_AGENTS.items():
            path = PI_AGENTS_DIR / props["file"]
            fm = parse_frontmatter(path.read_text(encoding="utf-8"))
            models.add(fm.get("model"))
        self.assertGreaterEqual(len(models), 2)

    def test_committed_model_references_are_known_pi_ids(self):
        """AC7: Committed model references must be valid Pi model IDs."""
        for agent_id, props in EXPECTED_AGENTS.items():
            with self.subTest(agent=agent_id):
                self.assertIn(props["model"], KNOWN_MODEL_IDS)


# ---------------------------------------------------------------------------
# AC5, AC6: Model precedence via ACTUAL pi-subagents runtime resolution
# ---------------------------------------------------------------------------

class TestRuntimeModelPrecedence(unittest.TestCase):
    """
    AC5, AC6: Validate model precedence by exercising the actual pi-subagents
    discoverAgentsAll runtime with isolated project/user settings.

    These tests run the real TypeScript discovery code via npx tsx in an isolated
    temp project directory, proving the patched runtime resolves models correctly.
    """

    def setUp(self):
        if not _runtime_available():
            self.fail(
                "Patched pi-subagents runtime is required for provider-free integration tests; "
                "run: bash .pi/install-packages.sh"
            )

    def test_file_model_used_when_no_overrides(self):
        """AC4/AC5: When no overrides exist, agent file model is the effective model."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir, _ = _create_isolated_project(tmpdir)
            result = _run_tsx_discovery(project_dir)

            project_agents = {a["name"]: a for a in result["project"]}
            for agent_id, props in EXPECTED_AGENTS.items():
                self.assertIn(agent_id, project_agents,
                              f"Agent {agent_id} must be discovered")
                self.assertEqual(project_agents[agent_id]["model"], props["model"],
                                 f"Agent {agent_id}: file model must be effective when no overrides")

    def test_project_override_replaces_file_model(self):
        """AC6: Project settings override replaces agent file model."""
        override_model = "openai-codex/gpt-5.4"
        self.assertIn(override_model, KNOWN_MODEL_IDS)

        with tempfile.TemporaryDirectory() as tmpdir:
            project_settings = {
                "packages": ["npm:pi-subagents@0.24.2"],
                "subagents": {
                    "agentOverrides": {
                        "implementer": {"model": override_model}
                    }
                }
            }
            project_dir, _ = _create_isolated_project(tmpdir, project_settings=project_settings)
            result = _run_tsx_discovery(project_dir)

            project_agents = {a["name"]: a for a in result["project"]}
            self.assertEqual(project_agents["implementer"]["model"], override_model,
                             "Project override must replace implementer file model")
            # Other agents should keep their file models
            self.assertEqual(project_agents["reviewer-a"]["model"],
                             EXPECTED_AGENTS["reviewer-a"]["model"])

    def test_project_override_beats_user_override(self):
        """AC6: Project settings override takes precedence over user settings override."""
        project_model = "openai-codex/gpt-5.4"
        user_model = "openai-codex/gpt-5.2"
        self.assertIn(project_model, KNOWN_MODEL_IDS)
        self.assertIn(user_model, KNOWN_MODEL_IDS)

        with tempfile.TemporaryDirectory() as tmpdir:
            project_settings = {
                "packages": ["npm:pi-subagents@0.24.2"],
                "subagents": {
                    "agentOverrides": {
                        "implementer": {"model": project_model}
                    }
                }
            }
            user_settings = {
                "subagents": {
                    "agentOverrides": {
                        "implementer": {"model": user_model}
                    }
                }
            }
            project_dir, home_dir = _create_isolated_project(
                tmpdir,
                project_settings=project_settings,
                user_settings=user_settings,
            )
            result = _run_tsx_discovery(project_dir, home_dir=home_dir)

            project_agents = {a["name"]: a for a in result["project"]}
            self.assertEqual(project_agents["implementer"]["model"], project_model,
                             "Project override must beat user override for implementer")

    def test_user_override_beats_file_model(self):
        """AC5: User override takes precedence over agent file model (no project override)."""
        user_model = "openai-codex/gpt-5.2"
        self.assertIn(user_model, KNOWN_MODEL_IDS)

        with tempfile.TemporaryDirectory() as tmpdir:
            user_settings = {
                "subagents": {
                    "agentOverrides": {
                        "reviewer-a": {"model": user_model}
                    }
                }
            }
            project_dir, home_dir = _create_isolated_project(
                tmpdir,
                user_settings=user_settings,
            )
            result = _run_tsx_discovery(project_dir, home_dir=home_dir)

            project_agents = {a["name"]: a for a in result["project"]}
            self.assertEqual(project_agents["reviewer-a"]["model"], user_model,
                             "User override must replace reviewer-a file model")
            # implementer should keep file model (no override)
            self.assertEqual(project_agents["implementer"]["model"],
                             EXPECTED_AGENTS["implementer"]["model"])

    def test_multiple_agents_resolve_independently(self):
        """AC7: Each agent resolves its own model independently."""
        override_model = "openai-codex/gpt-5.4"

        with tempfile.TemporaryDirectory() as tmpdir:
            project_settings = {
                "packages": ["npm:pi-subagents@0.24.2"],
                "subagents": {
                    "agentOverrides": {
                        "implementer": {"model": override_model}
                    }
                }
            }
            project_dir, _ = _create_isolated_project(tmpdir, project_settings=project_settings)
            result = _run_tsx_discovery(project_dir)

            project_agents = {a["name"]: a for a in result["project"]}
            # implementer gets the override
            self.assertEqual(project_agents["implementer"]["model"], override_model)
            # reviewer-a and reviewer-b keep their file models
            self.assertEqual(project_agents["reviewer-a"]["model"],
                             EXPECTED_AGENTS["reviewer-a"]["model"])
            self.assertEqual(project_agents["reviewer-b"]["model"],
                             EXPECTED_AGENTS["reviewer-b"]["model"])

    def test_user_settings_isolation(self):
        """AC5: Isolated user settings don't leak into the real developer's settings."""
        fake_user_model = "zai/glm-4.7"
        self.assertIn(fake_user_model, KNOWN_MODEL_IDS)

        with tempfile.TemporaryDirectory() as tmpdir:
            user_settings = {
                "subagents": {
                    "agentOverrides": {
                        "implementer": {"model": fake_user_model}
                    }
                }
            }
            project_dir, home_dir = _create_isolated_project(
                tmpdir, user_settings=user_settings,
            )

            # Verify the isolated HOME is used
            result = _run_tsx_discovery(project_dir, home_dir=home_dir)
            self.assertTrue(result["userSettingsPath"].startswith(home_dir),
                            f"User settings path must be under isolated HOME: {result['userSettingsPath']}")

            # Verify the override was applied from the isolated user settings
            project_agents = {a["name"]: a for a in result["project"]}
            self.assertEqual(project_agents["implementer"]["model"], fake_user_model)

            # Verify real developer settings are not contaminated
            real_user_settings = Path.home() / ".pi" / "agent" / "settings.json"
            if real_user_settings.exists():
                real_content = json.loads(real_user_settings.read_text())
                real_overrides = real_content.get("subagents", {}).get("agentOverrides", {})
                self.assertNotEqual(
                    real_overrides.get("implementer", {}).get("model"),
                    fake_user_model,
                    "Isolation check: fake user model should not appear in real settings"
                )


# ---------------------------------------------------------------------------
# AC2, AC3: Runtime discovery isolation — only .pi/agents/ wrappers dispatchable
# ---------------------------------------------------------------------------

class TestRuntimeDiscoveryIsolation(unittest.TestCase):
    """
    AC2, AC3: Validate via actual pi-subagents runtime that only approved
    .pi/agents/ wrappers are discovered as project agents, and that legacy
    .agents/skills/** are excluded from agent discovery.
    """

    def setUp(self):
        if not _runtime_available():
            self.fail(
                "Patched pi-subagents runtime is required for provider-free integration tests; "
                "run: bash .pi/install-packages.sh"
            )

    def test_only_approved_wrappers_discovered_as_project_agents(self):
        """AC2: Only the approved v1 roster is discovered as project agents."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir, _ = _create_isolated_project(tmpdir)
            result = _run_tsx_discovery(project_dir)

            discovered_names = {a["name"] for a in result["project"]}
            expected_names = set(EXPECTED_AGENTS.keys())
            self.assertEqual(discovered_names, expected_names,
                             f"Project agents must be exactly the approved wrappers. "
                             f"Got: {discovered_names}, expected: {expected_names}")

    def test_legacy_agents_directory_excluded_from_agent_discovery(self):
        """AC3: Legacy .agents/skills/** files are NOT discovered as project agents."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir, _ = _create_isolated_project(
                tmpdir, include_legacy_agents=True,
            )
            result = _run_tsx_discovery(project_dir)

            discovered_names = {a["name"] for a in result["project"]}
            self.assertNotIn("fake-skill-agent", discovered_names,
                             "Legacy .agents/skills/ files must NOT appear as project agents")
            # Should still only have the approved wrappers
            expected_names = set(EXPECTED_AGENTS.keys())
            self.assertEqual(discovered_names, expected_names)

    def test_all_discovered_agents_are_source_project(self):
        """AC2: All discovered project agents have source='project'."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir, _ = _create_isolated_project(tmpdir)
            result = _run_tsx_discovery(project_dir)

            for agent in result["project"]:
                self.assertEqual(agent["source"], "project",
                                 f"Agent {agent['name']} should have source='project'")

    def test_builtin_agents_are_separate(self):
        """AC2: Builtin agents are discovered separately from project agents."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir, _ = _create_isolated_project(tmpdir)
            result = _run_tsx_discovery(project_dir)

            builtin_names = {a["name"] for a in result["builtin"]}
            project_names = {a["name"] for a in result["project"]}
            # Builtin and project should not overlap in names (except if overridden)
            overlap = builtin_names & project_names
            self.assertEqual(overlap, set(),
                             f"No overlap between builtin and project agent names: {overlap}")


# ---------------------------------------------------------------------------
# AC9: Invalid model detection via runtime
# ---------------------------------------------------------------------------

class TestRuntimeInvalidModel(unittest.TestCase):
    """
    AC9: Validate via actual pi-subagents runtime that agents without valid
    model assignments are handled correctly.
    """

    def setUp(self):
        if not _runtime_available():
            self.fail(
                "Patched pi-subagents runtime is required for provider-free integration tests; "
                "run: bash .pi/install-packages.sh"
            )

    def test_agent_with_missing_model_still_discovered_with_undefined_model(self):
        """AC9: Agent without model field is still discovered (model is undefined/None)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_files = {
                "no-model.md": "---\nname: no-model\ndescription: Test\ntools: read\n---\nBody.\n",
            }
            project_dir, _ = _create_isolated_project(tmpdir, agent_files=agent_files)
            result = _run_tsx_discovery(project_dir)

            project_agents = {a["name"]: a for a in result["project"]}
            self.assertIn("no-model", project_agents,
                          "Agent without model should still be discovered")
            # Model should be absent/undefined — TypeScript omits undefined fields from JSON
            self.assertNotIn("model", project_agents["no-model"],
                             "Agent without model field should have no 'model' key in runtime output")

    def test_runtime_project_override_applies_even_to_agents_without_file_model(self):
        """AC5/AC9: An override can provide a model even when the file lacks one."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_files = {
                "no-model.md": "---\nname: no-model\ndescription: Test\ntools: read\n---\nBody.\n",
            }
            project_settings = {
                "packages": ["npm:pi-subagents@0.24.2"],
                "subagents": {
                    "agentOverrides": {
                        "no-model": {"model": "zai/glm-5.1"}
                    }
                }
            }
            project_dir, _ = _create_isolated_project(
                tmpdir,
                agent_files=agent_files,
                project_settings=project_settings,
            )
            result = _run_tsx_discovery(project_dir)

            project_agents = {a["name"]: a for a in result["project"]}
            self.assertEqual(project_agents["no-model"]["model"], "zai/glm-5.1",
                             "Override must provide model for agent without file model")

    def test_current_project_agents_all_have_valid_models(self):
        """AC9: All current wrapper agents resolve to valid model IDs via runtime."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir, _ = _create_isolated_project(tmpdir)
            result = _run_tsx_discovery(project_dir)

            for agent in result["project"]:
                self.assertIsNotNone(agent["model"],
                                     f"Agent {agent['name']} must have a non-None model from runtime")
                self.assertIn(agent["model"], KNOWN_MODEL_IDS,
                              f"Agent {agent['name']} runtime model '{agent['model']}' "
                              f"not in known Pi model registry")


class TestProviderFreeAC9Validation(unittest.TestCase):
    """AC9: Provider-free validation reports actionable, fail-closed model errors."""

    def test_current_project_model_contract_is_valid(self):
        errors = validate_provider_free_model_contract(str(ROOT))
        self.assertEqual(errors, [], f"Current project model contract must be valid: {errors}")

    def test_missing_required_wrapper_model_reports_agent_and_fix(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_files = {
                "no-model.md": "---\nname: no-model\ndescription: Test agent\ntools: read\n---\nBody.\n",
            }
            project_dir, _ = _create_isolated_project(tmpdir, agent_files=agent_files)
            errors = validate_provider_free_model_contract(project_dir)

            joined = "\n".join(errors)
            self.assertIn("agent 'no-model'", joined)
            self.assertIn(".pi/agents/no-model.md", joined)
            self.assertIn("required fix", joined)
            self.assertIn("subagents.agentOverrides.no-model.model", joined)

    def test_empty_required_wrapper_model_reports_agent_and_fix(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_files = {
                "empty-model.md": "---\nname: empty-model\ndescription: Test agent\nmodel: \ntools: read\n---\nBody.\n",
            }
            project_dir, _ = _create_isolated_project(tmpdir, agent_files=agent_files)
            errors = validate_provider_free_model_contract(project_dir)

            joined = "\n".join(errors)
            self.assertIn("agent 'empty-model'", joined)
            self.assertIn("no required model", joined)
            self.assertIn("required fix", joined)

    def test_unknown_required_wrapper_model_reports_agent_and_fix(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_files = {
                "bad-model.md": "---\nname: bad-model\ndescription: Test agent\nmodel: provider/not-real\ntools: read\n---\nBody.\n",
            }
            project_dir, _ = _create_isolated_project(tmpdir, agent_files=agent_files)
            errors = validate_provider_free_model_contract(project_dir)

            joined = "\n".join(errors)
            self.assertIn("agent 'bad-model'", joined)
            self.assertIn("provider/not-real", joined)
            self.assertIn("approved Pi model ID", joined)

    def test_invalid_override_reports_override_key_and_fix(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_settings = {
                "packages": ["npm:pi-subagents@0.24.2"],
                "subagents": {
                    "agentOverrides": {
                        "ghost-agent": {"model": "provider/not-real"},
                        "implementer": {"model": ""},
                    }
                },
            }
            project_dir, _ = _create_isolated_project(tmpdir, project_settings=project_settings)
            errors = validate_provider_free_model_contract(project_dir)

            joined = "\n".join(errors)
            self.assertIn("subagents.agentOverrides.ghost-agent.model", joined)
            self.assertIn("unknown agent 'ghost-agent'", joined)
            self.assertIn("unknown model 'provider/not-real'", joined)
            self.assertIn("subagents.agentOverrides.implementer.model", joined)
            self.assertIn("missing or empty", joined)
            self.assertIn("required fix", joined)

    def test_runtime_invalid_override_is_caught_after_resolution(self):
        """AC9: Actual runtime can resolve invalid strings, but validation blocks them."""
        if not _runtime_available():
            self.fail(
                "Patched pi-subagents runtime is required for provider-free integration tests; "
                "run: bash .pi/install-packages.sh"
            )
        with tempfile.TemporaryDirectory() as tmpdir:
            project_settings = {
                "packages": ["npm:pi-subagents@0.24.2"],
                "subagents": {
                    "agentOverrides": {
                        "implementer": {"model": "provider/not-real"},
                    }
                },
            }
            project_dir, _ = _create_isolated_project(tmpdir, project_settings=project_settings)
            result = _run_tsx_discovery(project_dir)
            project_agents = {a["name"]: a for a in result["project"]}
            self.assertEqual(project_agents["implementer"]["model"], "provider/not-real")

            errors = validate_provider_free_model_contract(project_dir)
            joined = "\n".join(errors)
            self.assertIn("agent 'implementer'", joined)
            self.assertIn("subagents.agentOverrides.implementer.model", joined)
            self.assertIn("required fix", joined)


# ---------------------------------------------------------------------------
# AC5: Committed override keys validation
# ---------------------------------------------------------------------------

class TestSettingsOverrides(unittest.TestCase):
    """AC5, AC6, AC8: Settings override structure and alignment."""

    def _read_settings(self):
        return json.loads(PI_SETTINGS.read_text(encoding="utf-8"))

    def test_settings_file_exists_and_is_valid_json(self):
        self.assertTrue(PI_SETTINGS.exists())
        settings = self._read_settings()
        self.assertIsInstance(settings, dict)

    def test_packages_pins_pi_subagents(self):
        settings = self._read_settings()
        packages = settings.get("packages", [])
        self.assertIn("npm:pi-subagents@0.24.2", packages)

    def test_no_inert_bmad_dev_story_override(self):
        """AC5: bmad-dev-story override was inert (targeted legacy skill, not .pi/agents/ wrapper)."""
        settings = self._read_settings()
        overrides = settings.get("subagents", {}).get("agentOverrides", {})
        self.assertNotIn("bmad-dev-story", overrides)

    def test_override_keys_align_with_wrapper_ids_or_builtins(self):
        """AC5: Override keys must correspond to known wrapper agent IDs or builtin agent names."""
        settings = self._read_settings()
        overrides = settings.get("subagents", {}).get("agentOverrides", {})
        valid_keys = set(EXPECTED_AGENTS.keys()) | KNOWN_BUILTIN_AGENTS
        for key in overrides:
            self.assertIn(key, valid_keys,
                          f"Override key '{key}' does not match any known wrapper or builtin agent")

    def test_override_model_values_are_known_pi_ids(self):
        """AC7: Override model references must be valid Pi model IDs."""
        settings = self._read_settings()
        overrides = settings.get("subagents", {}).get("agentOverrides", {})
        for key, cfg in overrides.items():
            with self.subTest(override_key=key):
                model = cfg.get("model")
                if model:
                    self.assertIn(model, KNOWN_MODEL_IDS)

    def test_no_secrets_or_api_keys_in_settings(self):
        """Security: No provider API keys or credentials committed."""
        text = PI_SETTINGS.read_text(encoding="utf-8")
        secret_patterns = [
            r'api[_-]?key',
            r'secret',
            r'token',
            r'password',
            r'credential',
            r'sk-[a-zA-Z0-9]',
            r'AIza[a-zA-Z0-9]',
        ]
        for pattern in secret_patterns:
            self.assertNotRegex(text, pattern)


# ---------------------------------------------------------------------------
# AC2, AC3: Static discovery isolation — legacy tree risk validation
# ---------------------------------------------------------------------------

class TestNoUnintendedDispatchableAgents(unittest.TestCase):
    """
    AC2, AC3: Only approved .pi/agents/ wrappers are dispatchable project agents.
    Legacy .agents/skills/** must not be discovered as agents despite having name+description.
    """

    def test_legacy_agents_directory_exists(self):
        """AC3: Legacy .agents/ tree must exist (story premise)."""
        self.assertTrue(LEGACY_AGENTS_DIR.is_dir(),
                        "Legacy .agents/ directory must exist per AC3 premise")

    def test_legacy_skills_have_name_and_description_frontmatter(self):
        """
        AC3: Verify legacy skill files DO have name+description frontmatter
        (confirming they would be discovered as agents without the patch).
        """
        skill_count = 0
        for skill_dir in (LEGACY_AGENTS_DIR / "skills").iterdir():
            skill_file = skill_dir / "SKILL.md" if skill_dir.is_dir() else None
            if skill_file and skill_file.exists():
                fm = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
                if fm.get("name") and fm.get("description"):
                    skill_count += 1
        self.assertGreater(skill_count, 0,
                           "Legacy .agents/skills/ should contain files with name+description "
                           "frontmatter — otherwise there's no discovery risk to validate")

    def test_legacy_skill_names_are_not_wrapper_names(self):
        """
        AC3: Legacy skill names differ from wrapper names,
        proving they are separate entries that need filtering.
        """
        wrapper_names = set(EXPECTED_AGENTS.keys())
        legacy_names = set()
        for skill_dir in (LEGACY_AGENTS_DIR / "skills").iterdir():
            skill_file = skill_dir / "SKILL.md" if skill_dir.is_dir() else None
            if skill_file and skill_file.exists():
                fm = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
                if fm.get("name"):
                    legacy_names.add(fm["name"])
        self.assertTrue(len(legacy_names) > 0)
        self.assertEqual(wrapper_names & legacy_names, set(),
                         f"Wrapper names should not overlap with legacy skills: "
                         f"{wrapper_names & legacy_names}")

    def test_pi_agents_wrappers_are_only_dispatchable_agents(self):
        """AC2: Only the approved v1 roster exists in .pi/agents/."""
        agent_files = [f.name for f in PI_AGENTS_DIR.iterdir() if f.suffix == ".md"]
        expected_files = {props["file"] for props in EXPECTED_AGENTS.values()}
        for af in agent_files:
            self.assertIn(af, expected_files,
                          f"Unexpected agent file in .pi/agents/: {af}")

    def test_pi_skills_are_not_agents(self):
        """AC2: .pi/skills/** SKILL.md files must not appear as agents in .pi/agents/."""
        self.assertTrue(PI_SKILLS_DIR.is_dir())
        agent_names = set()
        for agent_file in PI_AGENTS_DIR.iterdir():
            if agent_file.suffix == ".md":
                fm = parse_frontmatter(agent_file.read_text(encoding="utf-8"))
                if fm.get("name"):
                    agent_names.add(fm["name"])

        skill_names = set()
        for skill_dir in PI_SKILLS_DIR.iterdir():
            skill_file = skill_dir / "SKILL.md" if skill_dir.is_dir() else None
            if skill_file and skill_file.exists():
                fm = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
                if fm.get("name"):
                    skill_names.add(fm["name"])

        overlap = skill_names & agent_names
        self.assertEqual(overlap, set(),
                         f"Skill names should not appear in agent set: {overlap}")


# ---------------------------------------------------------------------------
# AC9: Invalid model configuration fails closed (static validation)
# ---------------------------------------------------------------------------

class TestInvalidModelConfiguration(unittest.TestCase):
    """AC9: Missing or invalid model configuration fails closed."""

    def test_agent_file_with_missing_model_field_is_detected(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_file = Path(tmpdir) / "test-no-model.md"
            agent_file.write_text(
                "---\nname: test-no-model\ndescription: Test agent\ntools: read\n---\nBody.\n"
            )
            fm = parse_frontmatter(agent_file.read_text(encoding="utf-8"))
            self.assertNotIn("model", fm)

    def test_agent_file_with_empty_model_is_detected(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_file = Path(tmpdir) / "test-empty-model.md"
            agent_file.write_text(
                "---\nname: test-empty\ndescription: Test\nmodel: \ntools: read\n---\nBody.\n"
            )
            fm = parse_frontmatter(agent_file.read_text(encoding="utf-8"))
            model = fm.get("model", "").strip()
            self.assertFalse(model)

    def test_current_wrapper_models_are_all_valid(self):
        """AC9: All current wrapper agents have valid, non-empty model assignments."""
        for agent_id, props in EXPECTED_AGENTS.items():
            with self.subTest(agent=agent_id):
                path = PI_AGENTS_DIR / props["file"]
                fm = parse_frontmatter(path.read_text(encoding="utf-8"))
                model = fm.get("model", "").strip()
                self.assertTrue(model)
                self.assertIn(model, KNOWN_MODEL_IDS)

    def test_settings_override_with_missing_model_key_fails_closed(self):
        """AC9: An override entry without 'model' is reported with an actionable fix."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_settings = {
                "packages": ["npm:pi-subagents@0.24.2"],
                "subagents": {
                    "agentOverrides": {
                        "implementer": {"disabled": True}
                    }
                },
            }
            project_dir, _ = _create_isolated_project(tmpdir, project_settings=project_settings)
            errors = validate_provider_free_model_contract(project_dir)

        joined = "\n".join(errors)
        self.assertIn("subagents.agentOverrides.implementer.model", joined)
        self.assertIn("missing or empty", joined)
        self.assertIn("required fix", joined)


# ---------------------------------------------------------------------------
# Patch mechanism durability — tracked sources
# ---------------------------------------------------------------------------

class TestPatchMechanismDurability(unittest.TestCase):
    """
    Verify the committed patch mechanism for pi-subagents is durable from
    tracked (committed) sources, not dependent on gitignored files.
    """

    def test_patches_directory_exists(self):
        self.assertTrue(PATCHES_DIR.is_dir())

    def test_apply_script_exists_and_is_executable(self):
        self.assertTrue(APPLY_SCRIPT.exists())
        self.assertTrue(os.access(APPLY_SCRIPT, os.X_OK))

    def test_install_packages_script_exists_and_is_executable(self):
        """Tracked .pi/install-packages.sh must exist for durable package management."""
        self.assertTrue(INSTALL_SCRIPT.exists())
        self.assertTrue(os.access(INSTALL_SCRIPT, os.X_OK))

    def test_install_packages_script_not_gitignored(self):
        """The install script must be tracked, not ignored."""
        result = subprocess.run(
            ["git", "check-ignore", str(INSTALL_SCRIPT)],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        self.assertNotEqual(result.returncode, 0,
                            f"{INSTALL_SCRIPT} must NOT be gitignored — it is the tracked durability mechanism")

    def test_apply_script_not_gitignored(self):
        """The apply-patches script must be tracked, not ignored."""
        result = subprocess.run(
            ["git", "check-ignore", str(APPLY_SCRIPT)],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        self.assertNotEqual(result.returncode, 0,
                            f"{APPLY_SCRIPT} must NOT be gitignored")

    def test_patch_files_not_gitignored(self):
        """Patch files must be tracked, not ignored."""
        patch_file = PATCHES_DIR / "pi-subagents-0.24.2-apply-overrides-to-project-agents.patch"
        self.assertTrue(patch_file.exists())
        result = subprocess.run(
            ["git", "check-ignore", str(patch_file)],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        self.assertNotEqual(result.returncode, 0,
                            f"{patch_file} must NOT be gitignored")

    def test_project_agent_override_patch_exists(self):
        patch_file = PATCHES_DIR / "pi-subagents-0.24.2-apply-overrides-to-project-agents.patch"
        self.assertTrue(patch_file.exists())

    def test_patch_is_valid_unified_diff(self):
        patch_file = PATCHES_DIR / "pi-subagents-0.24.2-apply-overrides-to-project-agents.patch"
        text = patch_file.read_text(encoding="utf-8")
        self.assertIn("--- a/src/agents/agents.ts", text)
        self.assertIn("+++ b/src/agents/agents.ts", text)
        self.assertIn("@@", text)
        self.assertIn("applyBuiltinOverride", text)
        self.assertNotIn("implementer", text)
        self.assertNotIn("reviewer-a", text)
        self.assertNotIn("zai/glm", text)

    def test_patch_is_applied_to_installed_package(self):
        """Verify the patch has been applied to the installed pi-subagents source."""
        if not PATCHED_AGENTS_TS.exists():
            self.fail(
                "Patched pi-subagents source is required; run: bash .pi/install-packages.sh"
            )
        text = PATCHED_AGENTS_TS.read_text(encoding="utf-8")
        self.assertIn("projectAgentsRaw", text)
        self.assertIn("Apply user and project overrides to project-defined agents", text)

    def test_install_packages_script_references_tracked_mechanisms(self):
        """The install script must reference the tracked patches directory."""
        script_text = INSTALL_SCRIPT.read_text(encoding="utf-8")
        self.assertIn("patches/apply-patches.sh", script_text)
        self.assertIn("pi install", script_text)

    def test_install_packages_script_preserves_exact_pin(self):
        """Package restore must install exact pi-subagents@0.24.2, not a semver range."""
        script_text = INSTALL_SCRIPT.read_text(encoding="utf-8")
        self.assertIn("deps[name] = version", script_text)
        self.assertNotIn("deps[name] = '^' + version", script_text)
        self.assertIn("expected pi-subagents@0.24.2", script_text)

    def test_generated_package_json_uses_exact_pin_when_present(self):
        """Local evidence package.json, when generated, must preserve the exact pin."""
        package_json = ROOT / ".pi" / "npm" / "package.json"
        if package_json.exists():
            pkg = json.loads(package_json.read_text(encoding="utf-8"))
            self.assertEqual(pkg.get("dependencies", {}).get("pi-subagents"), "0.24.2")

    def test_apply_patches_script_fails_without_node_modules(self):
        """Patch application cannot skip silently when ignored install output is absent."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            temp_patches = temp_root / ".pi" / "patches"
            temp_patches.mkdir(parents=True)
            shutil.copy2(APPLY_SCRIPT, temp_patches / "apply-patches.sh")
            shutil.copy2(
                PATCHES_DIR / "pi-subagents-0.24.2-apply-overrides-to-project-agents.patch",
                temp_patches / "pi-subagents-0.24.2-apply-overrides-to-project-agents.patch",
            )
            result = subprocess.run(
                ["bash", str(temp_patches / "apply-patches.sh")],
                capture_output=True, text=True, cwd=str(temp_root),
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("No node_modules found", result.stderr)
        self.assertIn(".pi/install-packages.sh", result.stderr)

    def test_apply_patches_script_checks_already_applied_and_version(self):
        """Patch script must fail closed on version/content mismatch, not generic skip."""
        script_text = APPLY_SCRIPT.read_text(encoding="utf-8")
        self.assertIn("installed_version", script_text)
        self.assertIn("expected_version", script_text)
        self.assertIn("--reverse --dry-run", script_text)
        self.assertIn("cannot be applied and is not already present", script_text)
        self.assertNotIn("patch does not apply cleanly — may already be applied", script_text)

    def test_runtime_integration_tests_do_not_skip_missing_install_output(self):
        """Provider-free runtime validations must fail closed if .pi/npm/node_modules is absent."""
        test_text = Path(__file__).read_text(encoding="utf-8")
        self.assertNotIn("skipTest(\"Patched pi-subagents runtime", test_text)
        self.assertIn("Patched pi-subagents runtime is required", test_text)

    def test_apply_patches_script_injects_postinstall_hook(self):
        """The apply-patches script should inject postinstall hook for convenience."""
        script_text = APPLY_SCRIPT.read_text(encoding="utf-8")
        self.assertIn("postinstall", script_text,
                      "apply-patches.sh should inject postinstall hook into package.json")


# ---------------------------------------------------------------------------
# AC1 safety: Reviewer tool boundaries
# ---------------------------------------------------------------------------

class TestReviewerToolBoundaries(unittest.TestCase):
    """AC1 safety: Reviewer agents have read-only tool boundaries."""

    def test_reviewers_do_not_have_edit_or_write_tools(self):
        for reviewer_id in ["reviewer-a", "reviewer-b"]:
            with self.subTest(reviewer=reviewer_id):
                props = EXPECTED_AGENTS[reviewer_id]
                self.assertNotIn("edit", props["tools"])
                self.assertNotIn("write", props["tools"])

    def test_implementer_has_edit_and_write_tools(self):
        props = EXPECTED_AGENTS["implementer"]
        self.assertIn("edit", props["tools"])
        self.assertIn("write", props["tools"])


if __name__ == "__main__":
    unittest.main()
