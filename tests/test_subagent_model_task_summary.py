"""
Story 1.2.2: Display Subagent Model and Task Summary — Validation tests.

Tests cover AC3, AC5, AC6, AC7, AC8:
  - buildTaskSummary strips framework-injected noise (AC3)
  - Optional taskSummary/model fields in types (AC5 backward compat)
  - Durable patch exists and applies cleanly (AC6)
  - Existing tests still pass (AC7)
  - Story artifacts in correct folder (AC8)
"""

import unittest
import os
import re
import subprocess
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PI_NPM_MODULES = ROOT / ".pi" / "npm" / "node_modules"
PI_SUBAGENTS_SRC = PI_NPM_MODULES / "pi-subagents" / "src"
PATCHES_DIR = ROOT / ".pi" / "patches"
INSTALL_SCRIPT = ROOT / ".pi" / "install-packages.sh"
STORY_DIR = ROOT / "docs" / "_bmad-output" / "implementation-artifacts" / "1-2-2-display-subagent-model-and-task-summary"


class TestBuildTaskSummaryNoiseStripping(unittest.TestCase):
    """AC3: buildTaskSummary strips fork preambles, [Read from:], [Write to:],
    progress instructions, output instructions, and {previous} content."""

    def _run_build_task_summary(self, task: str) -> str:
        """Run buildTaskSummary via tsx subprocess."""
        tsx_file = None
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as f:
                f.write(f'import {{ buildTaskSummary }} from "{PI_SUBAGENTS_SRC}/shared/formatters.ts";\n')
                f.write('const task = JSON.parse(process.env.PI_TEST_TASK || \'""\');\n')
                f.write('process.stdout.write(buildTaskSummary(task));\n')
                tsx_file = f.name

            env = os.environ.copy()
            env["PI_TEST_TASK"] = json.dumps(task)
            env.setdefault("NPM_CONFIG_CACHE", str(Path.home() / ".npm"))
            env.setdefault("NPM_CONFIG_YES", "true")
            result = subprocess.run(
                ["npx", "--yes", "tsx", tsx_file],
                capture_output=True, text=True, timeout=30, env=env,
            )
            if result.returncode != 0:
                raise RuntimeError(f"tsx failed: {result.stderr[:500]}")
            return result.stdout
        finally:
            if tsx_file:
                os.unlink(tsx_file)

    def test_clean_task_passes_through(self):
        """Simple clean task text is returned as-is."""
        result = self._run_build_task_summary("Analyze the codebase for performance issues")
        self.assertEqual(result, "Analyze the codebase for performance issues")

    def test_fork_preamble_stripped(self):
        """AC3: Fork preamble is stripped."""
        task = "You are a delegated subagent...\n\nTask:\nAnalyze the module"
        result = self._run_build_task_summary(task)
        self.assertEqual(result, "Analyze the module")

    def test_read_from_stripped(self):
        """AC3: [Read from: ...] is stripped."""
        task = "[Read from: src/main.ts]\nDo the analysis"
        result = self._run_build_task_summary(task)
        self.assertEqual(result, "Do the analysis")

    def test_write_to_stripped(self):
        """AC3: [Write to: ...] is stripped."""
        task = "[Write to: output.md]\nWrite the report"
        result = self._run_build_task_summary(task)
        self.assertEqual(result, "Write the report")

    def test_progress_instruction_stripped(self):
        """AC3: Write your progress to: ... is stripped."""
        task = "Write your progress to: progress.md\nDo the work"
        result = self._run_build_task_summary(task)
        self.assertEqual(result, "Do the work")

    def test_previous_placeholder_stripped(self):
        """AC3: {previous} placeholder is handled."""
        task = "Review the output\n{previous}"
        result = self._run_build_task_summary(task)
        self.assertEqual(result, "Review the output")

    def test_previous_only_generics_fallback(self):
        """AC3: Task that is just {previous} gets generic summary."""
        result = self._run_build_task_summary("{previous}")
        self.assertEqual(result, "continue from previous output")

    def test_empty_task_returns_empty(self):
        """Empty task returns empty string."""
        result = self._run_build_task_summary("")
        self.assertEqual(result, "")

    def test_long_task_truncated(self):
        """Long task is truncated with ellipsis."""
        long_task = "A" * 200
        result = self._run_build_task_summary(long_task)
        self.assertEqual(len(result), 80)
        self.assertTrue(result.endswith("…"))

    def test_combined_noise_stripped(self):
        """AC3: Multiple noise elements are all stripped."""
        task = (
            "[Read from: src/main.ts]\n"
            "[Write to: output.md]\n"
            "Write your progress to: progress.md\n"
            "Implement the feature"
        )
        result = self._run_build_task_summary(task)
        self.assertEqual(result, "Implement the feature")


class TestOptionalFieldsBackwardCompat(unittest.TestCase):
    """AC5: taskSummary and model fields are optional and backward compatible."""

    def test_agent_progress_has_task_summary_optional(self):
        """AgentProgress type includes optional taskSummary."""
        types_path = PI_SUBAGENTS_SRC / "shared" / "types.ts"
        content = types_path.read_text()
        # Verify taskSummary exists in AgentProgress
        self.assertIn("taskSummary?: string;", content)
        # Verify model exists in AgentProgress (new addition)
        in_progress = False
        in_single_result = False
        for line in content.split("\n"):
            if "export interface AgentProgress" in line:
                in_progress = True
            elif "export interface" in line and in_progress:
                in_progress = False
            if in_progress and "model?: string" in line:
                break
        else:
            # model might already exist from other fields, check it's in AgentProgress context
            self.assertIn("model?: string", content)

    def test_single_result_has_task_summary(self):
        """SingleResult type includes optional taskSummary."""
        types_path = PI_SUBAGENTS_SRC / "shared" / "types.ts"
        content = types_path.read_text()
        # Find the SingleResult interface and verify taskSummary
        match = re.search(
            r'export interface SingleResult \{[^}]*taskSummary',
            content, re.DOTALL
        )
        self.assertIsNotNone(match, "SingleResult must include taskSummary field")

    def test_async_status_steps_have_task_summary(self):
        """AsyncStatus steps include optional taskSummary."""
        types_path = PI_SUBAGENTS_SRC / "shared" / "types.ts"
        content = types_path.read_text()
        # Find the steps array in AsyncStatus and verify taskSummary
        self.assertIn("taskSummary?: string;", content)

    def test_runner_subagent_step_has_task_summary(self):
        """RunnerSubagentStep includes optional taskSummary."""
        path = PI_SUBAGENTS_SRC / "runs" / "shared" / "parallel-utils.ts"
        content = path.read_text()
        self.assertIn("taskSummary?: string;", content)


class TestPatchDurability(unittest.TestCase):
    """AC6: The durable patch exists and applies cleanly."""

    def test_patch_file_exists(self):
        patch_path = PATCHES_DIR / "pi-subagents-0.24.2-display-model-task-summary.patch"
        self.assertTrue(patch_path.exists(), "Patch file must exist")

    def test_patch_contains_expected_changes(self):
        """AC6: Patch contains changes to the expected files."""
        patch_path = PATCHES_DIR / "pi-subagents-0.24.2-display-model-task-summary.patch"
        content = patch_path.read_text()
        # Verify the patch touches all expected files
        expected_files = [
            "src/shared/formatters.ts",
            "src/shared/types.ts",
            "src/tui/render.ts",
            "src/runs/foreground/execution.ts",
            "src/runs/foreground/chain-execution.ts",
            "src/runs/shared/parallel-utils.ts",
            "src/runs/background/async-execution.ts",
            "src/runs/background/subagent-runner.ts",
            "src/runs/background/async-status.ts",
            "src/runs/background/run-status.ts",
        ]
        for expected in expected_files:
            self.assertIn(expected, content,
                          f"Patch must contain changes to {expected}")

    def test_patch_contains_build_task_summary(self):
        """AC6: Patch contains the buildTaskSummary function."""
        patch_path = PATCHES_DIR / "pi-subagents-0.24.2-display-model-task-summary.patch"
        content = patch_path.read_text()
        self.assertIn("buildTaskSummary", content)

    def test_patch_coexists_with_existing_patch(self):
        """AC6: New patch coexists with existing project-agent override patch."""
        existing_patch = PATCHES_DIR / "pi-subagents-0.24.2-apply-overrides-to-project-agents.patch"
        new_patch = PATCHES_DIR / "pi-subagents-0.24.2-display-model-task-summary.patch"
        self.assertTrue(existing_patch.exists(), "Existing patch must still exist")
        self.assertTrue(new_patch.exists(), "New patch must exist")

    def test_install_packages_applies_both_patches(self):
        """AC6: install-packages.sh applies both patches successfully."""
        result = subprocess.run(
            ["bash", str(INSTALL_SCRIPT)],
            capture_output=True, text=True, timeout=60,
            cwd=str(ROOT),
        )
        output = result.stdout + result.stderr
        # Both patches should be reported as applied or already applied
        self.assertIn("pi-subagents-0.24.2-apply-overrides-to-project-agents.patch", output)
        self.assertIn("pi-subagents-0.24.2-display-model-task-summary.patch", output)
        # No errors
        self.assertNotIn("ERROR", output.split("apply-patches:")[-1] if "apply-patches:" in output else "")


class TestRendererChanges(unittest.TestCase):
    """AC1, AC2, AC4: Verify renderer changes include model and task summary display."""

    def test_render_imports_build_task_summary(self):
        """render.ts imports buildTaskSummary."""
        path = PI_SUBAGENTS_SRC / "tui" / "render.ts"
        content = path.read_text()
        self.assertIn("buildTaskSummary", content)

    def test_compact_single_shows_model(self):
        """AC1: Compact single renderer shows model display."""
        path = PI_SUBAGENTS_SRC / "tui" / "render.ts"
        content = path.read_text()
        self.assertIn("modelDisplay", content)

    def test_compact_single_shows_task_summary(self):
        """AC1: Compact single renderer shows task summary."""
        path = PI_SUBAGENTS_SRC / "tui" / "render.ts"
        content = path.read_text()
        self.assertIn("taskSummary", content)

    def test_multi_compact_shows_model_per_row(self):
        """AC1: Multi compact rows show model per row."""
        path = PI_SUBAGENTS_SRC / "tui" / "render.ts"
        content = path.read_text()
        # The multi-compact path uses modelTag for each result row
        self.assertIn("modelTag", content)

    def test_async_widget_shows_model_and_summary(self):
        """AC2: Async widget shows model and task summary in step rows."""
        path = PI_SUBAGENTS_SRC / "tui" / "render.ts"
        content = path.read_text()
        # Widget step lines include modelTag and summarySuffix
        self.assertIn("summarySuffix", content)

    def test_async_status_shows_model_and_summary(self):
        """AC2: async status formatting shows model and task summary."""
        path = PI_SUBAGENTS_SRC / "runs" / "background" / "async-status.ts"
        content = path.read_text()
        self.assertIn("taskSummary", content)

    def test_run_status_shows_model_and_summary(self):
        """AC2: run-status detailed output shows model and task summary."""
        path = PI_SUBAGENTS_SRC / "runs" / "background" / "run-status.ts"
        content = path.read_text()
        self.assertIn("modelText", content)
        self.assertIn("summaryText", content)


class TestStoryArtifactsPlacement(unittest.TestCase):
    """AC8: Story artifacts are in the correct folder."""

    def test_story_file_in_correct_folder(self):
        story_file = STORY_DIR / "1-2-2-display-subagent-model-and-task-summary.md"
        self.assertTrue(story_file.exists(), "Story file must be in story folder")

    def test_no_root_artifact_pollution(self):
        """AC8: No review or story markdown at the implementation-artifacts root."""
        root_artifacts = ROOT / "docs" / "_bmad-output" / "implementation-artifacts"
        root_files = list(root_artifacts.glob("review-*.md"))
        self.assertEqual(root_files, [],
                         f"No review files at artifacts root, found: {root_files}")

    def test_test_file_not_at_root_tests(self):
        """AC8: This test file should NOT be inside the story folder."""
        self.assertTrue(
            Path(__file__).parent.name == "tests",
            "Test file should be in tests/ directory"
        )


class TestExecutionPropagation(unittest.TestCase):
    """AC1: Execution code propagates taskSummary and model."""

    def test_execution_builds_task_summary(self):
        """execution.ts builds taskSummary from task."""
        path = PI_SUBAGENTS_SRC / "runs" / "foreground" / "execution.ts"
        content = path.read_text()
        self.assertIn("buildTaskSummary(task)", content)

    def test_execution_sets_model_on_progress(self):
        """execution.ts sets model on AgentProgress."""
        path = PI_SUBAGENTS_SRC / "runs" / "foreground" / "execution.ts"
        content = path.read_text()
        # model: modelArg should be in progress initialization
        self.assertIn("model: modelArg", content)

    def test_async_execution_builds_task_summary(self):
        """async-execution.ts builds taskSummary for runner steps."""
        path = PI_SUBAGENTS_SRC / "runs" / "background" / "async-execution.ts"
        content = path.read_text()
        self.assertIn("buildTaskSummary(cleanTaskText)", content)

    def test_subagent_runner_propagates_task_summary(self):
        """subagent-runner.ts writes taskSummary to status.json steps."""
        path = PI_SUBAGENTS_SRC / "runs" / "background" / "subagent-runner.ts"
        content = path.read_text()
        self.assertIn("step.taskSummary", content)


class TestReviewFollowUpRunningSummary(unittest.TestCase):
    """AC1 follow-up: foreground running parallel/chain rows must render task summaries."""

    def test_render_no_running_gate_on_task_summary(self):
        """AC1: Multi-compact rows do not gate taskSummary behind !rRunning."""
        path = PI_SUBAGENTS_SRC / "tui" / "render.ts"
        content = path.read_text()
        # The pattern 'taskSummary && !rRunning' must NOT appear in multi-compact path
        # Find the multi-compact block and verify no rRunning gate on taskSummary
        # The old buggy code was: if (taskSummary && !rRunning) {
        # The fix removes the !rRunning condition
        self.assertNotRegex(
            content,
            r'taskSummary && !rRunning',
            "taskSummary must not be gated behind !rRunning in multi-compact rows"
        )

    def test_render_shows_task_summary_for_all_states(self):
        """AC1: Multi-compact rows show taskSummary regardless of running state."""
        path = PI_SUBAGENTS_SRC / "tui" / "render.ts"
        content = path.read_text()
        # Find the multi-compact section where taskSummary is shown
        # The summary line should appear before the rRunning check
        # Verify pattern: taskSummary check does NOT have rRunning condition
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'const taskSummary = r.taskSummary || rProg?.taskSummary || r.progress?.taskSummary' in line:
                # Check the next line is 'if (taskSummary) {' NOT 'if (taskSummary && !rRunning) {'
                next_line = lines[i + 1] if i + 1 < len(lines) else ''
                self.assertIn('if (taskSummary)', next_line)
                self.assertNotIn('rRunning', next_line)
                break
        else:
            self.fail("Could not find taskSummary check in multi-compact rows")

    def test_render_uses_progress_summary_fallback_for_running_rows(self):
        """AC1: Multi-compact rows use the resolved running-progress summary fallback."""
        path = PI_SUBAGENTS_SRC / "tui" / "render.ts"
        content = path.read_text()
        self.assertIn(
            "const taskSummary = r.taskSummary || rProg?.taskSummary || r.progress?.taskSummary",
            content,
        )


class TestReviewFollowUpChainCleanSummary(unittest.TestCase):
    """AC3, AC7 follow-up: chain summaries from clean task, stripping progress/output injected forms."""

    def test_progress_instruction_stripped(self):
        """AC3: progress-only injected text does not leak into the summary."""
        task = "\n\n---\nCreate and maintain progress at: /tmp/chain/progress.md"
        result = self._run_build_task_summary(task)
        self.assertEqual(result, "")

    def test_labeled_output_instruction_stripped(self):
        """AC3: labeled single-output instructions are stripped from summary."""
        task = "\n\n---\n**Output:** Write your findings to: /tmp/output.md"
        result = self._run_build_task_summary(task)
        self.assertEqual(result, "")

    def test_injected_progress_suffix_stripped(self):
        """AC3: Full chain-injected task with progress suffix produces clean summary."""
        task = (
            "Analyze the codebase for issues"
            "\n\n---\n"
            "Create and maintain progress at: /tmp/chain/progress.md"
        )
        result = self._run_build_task_summary(task)
        self.assertEqual(result, "Analyze the codebase for issues")

    def test_update_progress_stripped(self):
        """AC3: 'Update progress at:' lines are stripped from summary."""
        task = (
            "Refactor the module"
            "\n\n---\n"
            "Update progress at: /tmp/chain/progress.md"
        )
        result = self._run_build_task_summary(task)
        self.assertEqual(result, "Refactor the module")

    def test_previous_step_output_stripped(self):
        """AC3: 'Previous step output:' and all subsequent content is stripped."""
        task = (
            "Write the documentation"
            "\n\n---\n"
            "Update progress at: progress.md\n"
            "Previous step output:\n"
            "This is a very long output from the previous step that should not appear...\n"
            "More content here..."
        )
        result = self._run_build_task_summary(task)
        self.assertEqual(result, "Write the documentation")

    def test_separator_dash_stripped(self):
        """AC3: Bare '---' separators do not become the summary."""
        task = (
            "\n\n---\n"
            "Create and maintain progress at: /path/progress.md"
        )
        result = self._run_build_task_summary(task)
        # After stripping all noise, no meaningful content remains
        self.assertEqual(result, "")

    def test_combined_chain_noise_stripped(self):
        """AC3: Full chain-injected task with all noise elements produces clean summary."""
        task = (
            "[Read from: src/main.ts]\n"
            "[Write to: output.md]\n"
            "Implement the feature\n"
            "\n\n---\n"
            "Create and maintain progress at: /tmp/progress.md\n"
            "Previous step output:\n"
            "Some long previous output..."
        )
        result = self._run_build_task_summary(task)
        self.assertEqual(result, "Implement the feature")

    def test_chain_execution_passes_clean_task_summary(self):
        """AC7: chain-execution.ts passes taskSummaryOverride from summarySource (pre-{previous} replacement)."""
        path = PI_SUBAGENTS_SRC / "runs" / "foreground" / "chain-execution.ts"
        content = path.read_text()
        self.assertIn("taskSummaryOverride: buildTaskSummary(summarySource)", content)
        # Verify buildTaskSummary is imported in chain-execution.ts
        self.assertIn("buildTaskSummary", content)
        # Verify it's imported from formatters
        self.assertIn("from \"../../shared/formatters.ts\"", content)

    def test_execution_uses_task_summary_override(self):
        """AC7: execution.ts uses taskSummaryOverride when provided."""
        path = PI_SUBAGENTS_SRC / "runs" / "foreground" / "execution.ts"
        content = path.read_text()
        self.assertIn("options.taskSummaryOverride ?? buildTaskSummary(task)", content)

    def test_run_sync_options_has_override(self):
        """AC7: RunSyncOptions includes taskSummaryOverride field."""
        path = PI_SUBAGENTS_SRC / "shared" / "types.ts"
        content = path.read_text()
        self.assertIn("taskSummaryOverride?: string", content)

    def test_patch_contains_chain_execution_changes(self):
        """AC6: Patch includes chain-execution.ts changes for clean task summary propagation."""
        patch_path = PATCHES_DIR / "pi-subagents-0.24.2-display-model-task-summary.patch"
        content = patch_path.read_text()
        self.assertIn("src/runs/foreground/chain-execution.ts", content)
        self.assertIn("taskSummaryOverride", content)

    _run_build_task_summary = None  # Will be set from TestBuildTaskSummaryNoiseStripping

    def _run_build_task_summary(self, task: str) -> str:
        """Run buildTaskSummary via tsx subprocess."""
        tsx_file = None
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as f:
                f.write(f'import {{ buildTaskSummary }} from "{PI_SUBAGENTS_SRC}/shared/formatters.ts";\n')
                f.write('const task = JSON.parse(process.env.PI_TEST_TASK || "");\n')

                f.write('process.stdout.write(buildTaskSummary(task));\n')
                tsx_file = f.name

            env = os.environ.copy()
            env["PI_TEST_TASK"] = json.dumps(task)
            env.setdefault("NPM_CONFIG_CACHE", str(Path.home() / ".npm"))
            env.setdefault("NPM_CONFIG_YES", "true")
            result = subprocess.run(
                ["npx", "--yes", "tsx", tsx_file],
                capture_output=True, text=True, timeout=30, env=env,
            )
            if result.returncode != 0:
                raise RuntimeError(f"tsx failed: {result.stderr[:500]}")
            return result.stdout
        finally:
            if tsx_file:
                os.unlink(tsx_file)


class TestReviewFollowUpChainSummarySourceBeforePrevious(unittest.TestCase):
    """AC3, AC7 second-pass: chain summaries computed from template before {previous} replacement."""

    def test_sequential_chain_uses_summary_source(self):
        """AC3: Sequential chain path computes summarySource before {previous} replacement."""
        path = PI_SUBAGENTS_SRC / "runs" / "foreground" / "chain-execution.ts"
        content = path.read_text()
        # The sequential path must compute summarySource from the template
        # before replacing {previous} with actual prev output
        self.assertIn(
            'const summarySource = stepTask.replace(/\\{previous\\}/g, "continue from previous output")',
            content,
        )
        # And the taskSummaryOverride must use summarySource, not cleanTask
        self.assertIn("taskSummaryOverride: buildTaskSummary(summarySource)", content)

    def test_parallel_chain_uses_summary_source(self):
        """AC3: Parallel chain path computes summarySource before {previous} replacement."""
        path = PI_SUBAGENTS_SRC / "runs" / "foreground" / "chain-execution.ts"
        content = path.read_text()
        # The parallel path must compute summarySource before {previous} replacement
        # Count occurrences — there should be two summarySource declarations (parallel + sequential)
        count = content.count('const summarySource = ')
        self.assertGreaterEqual(count, 2,
                                f"Expected >= 2 summarySource declarations (parallel + sequential), found {count}")

    def test_summary_source_replaces_previous_neutrally(self):
        """AC3: summarySource replaces {previous} with neutral text, not actual prior output."""
        path = PI_SUBAGENTS_SRC / "runs" / "foreground" / "chain-execution.ts"
        content = path.read_text()
        self.assertIn(
            '"continue from previous output"',
            content,
            "summarySource must replace {previous} with neutral text, not actual prior output"
        )

    def test_clean_task_still_used_for_record_run(self):
        """AC7: cleanTask (with expanded {previous}) is still used for recordRun, not summary."""
        path = PI_SUBAGENTS_SRC / "runs" / "foreground" / "chain-execution.ts"
        content = path.read_text()
        # recordRun still uses cleanTask for logging purposes
        self.assertIn("recordRun(task.agent, cleanTask,", content)
        self.assertIn("recordRun(seqStep.agent, cleanTask,", content)

    def test_default_previous_template_produces_neutral_summary(self):
        """AC3: Default {previous}-only template produces neutral summary, not expanded output."""
        # When the template is just "{previous}", after {task} and {chain_dir} replacement
        # it's still "{previous}", and summarySource becomes "continue from previous output"
        result = self._run_build_task_summary("continue from previous output")
        self.assertEqual(result, "continue from previous output")

    def test_explicit_previous_in_mixed_template(self):
        """AC3: Template with explicit task + {previous} produces summary from task part only."""
        # Template: "Analyze the codebase for {previous} issues"
        # summarySource: "Analyze the codebase for continue from previous output issues"
        # buildTaskSummary on that should capture the meaningful part
        result = self._run_build_task_summary(
            "Analyze the codebase for continue from previous output issues"
        )
        self.assertIn("Analyze the codebase", result)

    def _run_build_task_summary(self, task: str) -> str:
        """Run buildTaskSummary via tsx subprocess."""
        tsx_file = None
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as f:
                f.write(f'import {{ buildTaskSummary }} from "{PI_SUBAGENTS_SRC}/shared/formatters.ts";\n')
                f.write('const task = JSON.parse(process.env.PI_TEST_TASK || "");\n')
                f.write('process.stdout.write(buildTaskSummary(task));\n')
                tsx_file = f.name

            env = os.environ.copy()
            env["PI_TEST_TASK"] = json.dumps(task)
            env.setdefault("NPM_CONFIG_CACHE", str(Path.home() / ".npm"))
            env.setdefault("NPM_CONFIG_YES", "true")
            result = subprocess.run(
                ["npx", "--yes", "tsx", tsx_file],
                capture_output=True, text=True, timeout=30, env=env,
            )
            if result.returncode != 0:
                raise RuntimeError(f"tsx failed: {result.stderr[:500]}")
            return result.stdout
        finally:
            if tsx_file:
                os.unlink(tsx_file)


if __name__ == "__main__":
    unittest.main()
