"""Story 1.5 provider-free regression tests for Pi UI agent activity visibility."""

import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PI_SUBAGENTS_SRC = ROOT / ".pi" / "npm" / "node_modules" / "pi-subagents" / "src"
PATCHES_DIR = ROOT / ".pi" / "patches"
ORCHESTRATOR = ROOT / ".pi" / "skills" / "bmad-orchestrator" / "SKILL.md"
DEV_CYCLE = ROOT / ".pi" / "skills" / "bmad-dev-cycle" / "workflow.md"
AGENTS_DIR = ROOT / ".pi" / "agents"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def run_tsx(source: str, env_vars: dict | None = None) -> str:
    fd, filename = tempfile.mkstemp(suffix=".ts")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(source)
        env = os.environ.copy()
        env.setdefault("NPM_CONFIG_YES", "true")
        if env_vars:
            env.update(env_vars)
        result = subprocess.run(
            ["npx", "--yes", "tsx", filename],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            timeout=40,
        )
        if result.returncode != 0:
            raise AssertionError(f"tsx failed\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
        return result.stdout
    finally:
        try:
            os.unlink(filename)
        except FileNotFoundError:
            pass


class TestPiUiVisibilityContract(unittest.TestCase):
    def test_orchestrator_documents_v1_pi_ui_contract_and_boundaries(self):
        text = read(ORCHESTRATOR)
        self.assertIn("## Pi UI Visibility Contract", text)
        for phrase in [
            "Pi TUI and `pi-subagents` status/widget rendering",
            "Do not add or require a web dashboard",
            "separate frontend",
            "read-only projection",
            "must never mark workflow success",
            "`pending`, `in-progress`, `completed`, `blocked`, `failed`",
            "roleLabel",
            "taskStatePath",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_parent_workflow_exposes_task_state_path_to_pi_subagents(self):
        text = read(DEV_CYCLE)
        self.assertIn('taskStatePath: "{story_file}"', text)
        self.assertIn('context: "fresh"', text)
        dispatch_blocks = re.findall(r"subagent\(\{.*?\}\)", text, flags=re.DOTALL)
        self.assertGreaterEqual(len(dispatch_blocks), 2)
        for block in dispatch_blocks:
            if "agent:" in block or "tasks:" in block:
                self.assertIn('context: "fresh"', block)
                self.assertNotIn('context: "fork"', block)
        self.assertNotIn('dispatch_subagent', text)

    def test_no_separate_frontend_dashboard_server_is_introduced(self):
        forbidden_dirs = [
            ROOT / ".pi" / "extensions" / "bmad-dashboard",
            ROOT / ".pi" / "extensions" / "bmad-ui-server",
            ROOT / "frontend",
            ROOT / "dashboard",
        ]
        for path in forbidden_dirs:
            with self.subTest(path=path):
                self.assertFalse(path.exists())
        for pattern in ["express", "fastify", "createServer", "WebSocketServer"]:
            hits = list(ROOT.glob(".pi/extensions/**/package.json"))
            for pkg in hits:
                self.assertNotIn(pattern, read(pkg))


class TestRoleLabelsAndActivityTitles(unittest.TestCase):
    def test_project_agent_role_labels_exist_and_child_agents_lack_subagent_tool(self):
        expected = {
            "implementer.md": "BMAD Implementer",
            "reviewer-a.md": "BMAD Reviewer A",
            "reviewer-b.md": "BMAD Reviewer B",
        }
        for filename, role_label in expected.items():
            frontmatter = read(AGENTS_DIR / filename).split("---", 2)[1]
            with self.subTest(filename=filename):
                self.assertIn(f"roleLabel: {role_label}", frontmatter)
                self.assertNotRegex(frontmatter, r"tools:.*\bsubagent\b")
        self.assertFalse((AGENTS_DIR / "orchestrator.md").exists())
        self.assertFalse((AGENTS_DIR / "bmad-orchestrator.md").exists())

    def test_role_label_fallback_title_formatting_and_noise_stripping(self):
        source = f'''
import {{ resolveAgentRoleLabel, formatActivityTitle, sanitizeUiTitle }} from "{PI_SUBAGENTS_SRC}/shared/ui-visibility.ts";
const out = {{
  configured: resolveAgentRoleLabel({{ name: "implementer", localName: "implementer", extraFields: {{ roleLabel: "BMAD Implementer" }} }}),
  fallback: resolveAgentRoleLabel({{ name: "future-agent", localName: "Future Agent" }}),
  title: formatActivityTitle({{ roleLabel: "BMAD Implementer", taskId: "dev-R1", title: "Implement story" }}),
  sanitized: sanitizeUiTitle("bad\\u001b[31m title\\nwith noise", 80),
}};
process.stdout.write(JSON.stringify(out));
'''
        out = json.loads(run_tsx(source))
        self.assertEqual(out["configured"], "BMAD Implementer")
        self.assertEqual(out["fallback"], "Future Agent")
        self.assertEqual(out["title"], "BMAD Implementer · dev-R1 · Implement story")
        self.assertEqual(out["sanitized"], "bad title with noise")

    def test_parallel_same_agent_titles_remain_distinguishable(self):
        source = f'''
import {{ formatActivityTitle }} from "{PI_SUBAGENTS_SRC}/shared/ui-visibility.ts";
process.stdout.write(JSON.stringify([
  formatActivityTitle({{ roleLabel: "BMAD Implementer", taskId: "dev-R1", title: "Implement" }}),
  formatActivityTitle({{ roleLabel: "BMAD Implementer", taskId: "dev-R2", title: "Fix review" }}),
]));
'''
        titles = json.loads(run_tsx(source))
        self.assertNotEqual(titles[0], titles[1])
        self.assertIn("dev-R1", titles[0])
        self.assertIn("dev-R2", titles[1])

    def test_runtime_activity_title_matches_durable_task_id_before_same_agent_fallback(self):
        markdown = '''
### Task State
```yaml
tasks:
  - taskId: "dev-R1"
    title: "Implement first task"
    targetAgent: "implementer"
    status: "in-progress"
    contextSource:
      type: "artifact-path"
      paths:
        - "story.md"
    activeAgentId: "implementer"
  - taskId: "dev-R2"
    title: "Fix review finding"
    targetAgent: "implementer"
    status: "in-progress"
    contextSource:
      type: "artifact-path"
      paths:
        - "story.md"
    activeAgentId: "implementer"
```
'''
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", dir=ROOT, delete=False) as handle:
            handle.write(markdown)
            task_state_path = handle.name
        try:
            source = f'''
import {{ buildRuntimeActivityTitle }} from "{PI_SUBAGENTS_SRC}/shared/ui-visibility.ts";
const taskStatePath = JSON.parse(process.env.PI_TEST_TASK_STATE_PATH!);
const foregroundTitle = buildRuntimeActivityTitle({{
  details: {{
    taskStatePath,
    progress: [{{ index: 1, agent: "implementer", roleLabel: "BMAD Implementer", durableTaskId: "dev-R2", status: "running", task: "Fix", recentTools: [], recentOutput: [], toolCount: 0, tokens: 0, durationMs: 0 }}],
    results: []
  }}
}});
const asyncTitle = buildRuntimeActivityTitle({{
  job: {{ asyncId: "async-1", asyncDir: ".", taskStatePath, durableTaskIds: ["dev-R2"], status: "running", mode: "single", agents: ["implementer"] }}
}});
const fallbackTitle = buildRuntimeActivityTitle({{
  details: {{
    progress: [{{ index: 1, agent: "implementer", roleLabel: "BMAD Implementer", durableTaskId: "dev-R2", status: "running", task: "Fix", taskSummary: "Fix runtime", recentTools: [], recentOutput: [], toolCount: 0, tokens: 0, durationMs: 0 }}],
    results: []
  }}
}});
process.stdout.write(JSON.stringify({{ foregroundTitle, asyncTitle, fallbackTitle }}));
'''
            titles = json.loads(run_tsx(source, {"PI_TEST_TASK_STATE_PATH": json.dumps(task_state_path)}))
        finally:
            Path(task_state_path).unlink(missing_ok=True)
        for key in ["foregroundTitle", "asyncTitle"]:
            self.assertIn("dev-R2", titles[key])
            self.assertIn("Fix review finding", titles[key])
            self.assertNotIn("dev-R1", titles[key])
        self.assertIsNone(titles.get("fallbackTitle"), "durable task ids without taskStatePath must not fall back to a normal runtime title")

    def test_shared_arbitration_blocks_terminal_and_missing_durable_state_titles(self):
        markdown = '''
### Task State
```yaml
tasks:
  - taskId: "done-R1"
    title: "Already complete"
    targetAgent: "implementer"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "story.md"
    activeAgentId: "implementer"
  - taskId: "active-R1"
    title: "Still active"
    targetAgent: "reviewer-a"
    status: "in-progress"
    contextSource:
      type: "artifact-path"
      paths:
        - "story.md"
    activeAgentId: "reviewer-a"
```
'''
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", dir=ROOT, delete=False) as handle:
            handle.write(markdown)
            task_state_path = handle.name
        try:
            source = f'''
import {{ arbitrateRuntimeUiActivity, buildRuntimeActivityTitle }} from "{PI_SUBAGENTS_SRC}/shared/ui-visibility.ts";
const taskStatePath = JSON.parse(process.env.PI_TEST_TASK_STATE_PATH!);
const completedRuntime = {{ agent: "implementer", roleLabel: "BMAD Implementer", durableTaskId: "done-R1", status: "running", task: "stale", taskSummary: "stale", recentTools: [], recentOutput: [], toolCount: 0, tokens: 0, durationMs: 0 }};
const completedRuntimeWithoutId = {{ agent: "implementer", roleLabel: "BMAD Implementer", status: "running", task: "stale", taskSummary: "stale", recentTools: [], recentOutput: [], toolCount: 0, tokens: 0, durationMs: 0 }};
const activeRuntime = {{ agent: "reviewer-a", roleLabel: "BMAD Reviewer A", durableTaskId: "active-R1", status: "running", task: "active", taskSummary: "active", recentTools: [], recentOutput: [], toolCount: 0, tokens: 0, durationMs: 0 }};
const terminal = arbitrateRuntimeUiActivity({{ taskStatePath, runtimeItems: [completedRuntime], runtimeStatus: "running" }});
const terminalWithoutId = arbitrateRuntimeUiActivity({{ taskStatePath, runtimeItems: [completedRuntimeWithoutId], runtimeStatus: "running" }});
const active = arbitrateRuntimeUiActivity({{ taskStatePath, runtimeItems: [activeRuntime], runtimeStatus: "running" }});
const missing = arbitrateRuntimeUiActivity({{ runtimeItems: [activeRuntime], runtimeStatus: "running" }});
process.stdout.write(JSON.stringify({{
  terminalCanShowActive: terminal.canShowActive,
  terminalStatus: terminal.terminalDurableStatus,
  terminalWithoutIdCanShowActive: terminalWithoutId.canShowActive,
  terminalWithoutIdStatus: terminalWithoutId.terminalDurableStatus,
  activeCanShowActive: active.canShowActive,
  activeTitle: active.activityTitle,
  missingDegraded: missing.degradedReason,
  terminalTitle: buildRuntimeActivityTitle({{ details: {{ taskStatePath, progress: [completedRuntime], results: [] }} }}) ?? null,
  terminalWithoutIdTitle: buildRuntimeActivityTitle({{ details: {{ taskStatePath, progress: [completedRuntimeWithoutId], results: [] }} }}) ?? null,
  activeTitleFromHelper: buildRuntimeActivityTitle({{ details: {{ taskStatePath, progress: [activeRuntime], results: [] }} }}) ?? null,
}}));
'''
            out = json.loads(run_tsx(source, {"PI_TEST_TASK_STATE_PATH": json.dumps(task_state_path)}))
        finally:
            Path(task_state_path).unlink(missing_ok=True)
        self.assertFalse(out["terminalCanShowActive"])
        self.assertEqual(out["terminalStatus"], "completed")
        self.assertFalse(out["terminalWithoutIdCanShowActive"])
        self.assertEqual(out["terminalWithoutIdStatus"], "completed")
        self.assertIsNone(out["terminalTitle"])
        self.assertIsNone(out["terminalWithoutIdTitle"])
        self.assertTrue(out["activeCanShowActive"])
        self.assertIn("active-R1", out["activeTitle"])
        self.assertIn("active-R1", out["activeTitleFromHelper"])
        self.assertIn("path was not provided", out["missingDegraded"])


class TestDurableTaskProjection(unittest.TestCase):
    TASK_MARKDOWN = """
## BMAD Dev Cycle (AI)

### Task State
```yaml
tasks:
  - taskId: "dev-R1"
    title: "Implement or resume story via dev-story workflow"
    targetAgent: "implementer"
    status: "in-progress"
    contextSource:
      type: "artifact-path"
      paths:
        - "story.md"
    dependsOn: []
    activeAgentId: "implementer"
  - taskId: "review-a-R1"
    title: "Independent code review pass A"
    targetAgent: "reviewer-a"
    status: "pending"
    contextSource:
      type: "artifact-path"
      paths:
        - "story.md"
    activeAgentId: null
  - taskId: "review-b-R1"
    title: "Independent code review pass B"
    targetAgent: "reviewer-b"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "story.md"
    activeAgentId: null
  - taskId: "blocked-R1"
    title: "Blocked task"
    targetAgent: "reviewer-a"
    status: "blocked"
    contextSource:
      type: "artifact-path"
      paths:
        - "story.md"
    activeAgentId: null
  - taskId: "failed-R1"
    title: "Failed task"
    targetAgent: "reviewer-b"
    status: "failed"
    contextSource:
      type: "artifact-path"
      paths:
        - "story.md"
    activeAgentId: null
```
"""

    def test_projection_handles_all_statuses_runtime_annotations_and_stale_prevention(self):
        source = f'''
import {{ parseDurableTaskState, enrichTaskProjection }} from "{PI_SUBAGENTS_SRC}/shared/ui-visibility.ts";
const markdown = JSON.parse(process.env.PI_TEST_MARKDOWN!);
const projection = enrichTaskProjection(parseDurableTaskState(markdown), [
  {{ agent: "implementer", roleLabel: "BMAD Implementer", durableTaskId: "dev-R1", status: "running", model: "openai-codex/gpt-5.5", taskSummary: "Implement", currentTool: "edit", currentPath: ".pi/x.ts", tokens: 12400, durationMs: 192000 }},
  {{ agent: "reviewer-b", roleLabel: "BMAD Reviewer B", durableTaskId: "review-b-R1", status: "running", model: "openai-codex/gpt-5.5", taskSummary: "stale runtime" }},
]);
process.stdout.write(JSON.stringify(projection));
'''
        projection = json.loads(run_tsx(source, {"PI_TEST_MARKDOWN": json.dumps(self.TASK_MARKDOWN)}))
        self.assertIsNone(projection.get("degradedReason"))
        statuses = {task["taskId"]: task["durableStatus"] for task in projection["tasks"]}
        self.assertEqual(set(statuses.values()), {"pending", "in-progress", "completed", "blocked", "failed"})
        active = next(task for task in projection["tasks"] if task["taskId"] == "dev-R1")
        self.assertEqual(active["roleLabel"], "BMAD Implementer")
        self.assertEqual(active["runtimeStatus"], "running")
        self.assertEqual(active["currentTool"], "edit")
        self.assertEqual(active["tokenCount"], 12400)
        completed = next(task for task in projection["tasks"] if task["taskId"] == "review-b-R1")
        self.assertEqual(completed["durableStatus"], "completed")
        self.assertNotIn("currentTool", completed, "completed durable state must not render as active")

    def test_read_projection_loads_configured_role_labels_for_inactive_durable_tasks(self):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", dir=ROOT, delete=False) as handle:
            handle.write(self.TASK_MARKDOWN)
            task_state_path = handle.name
        try:
            source = f'''
import {{ readDurableTaskProjection }} from "{PI_SUBAGENTS_SRC}/shared/ui-visibility.ts";
const taskStatePath = JSON.parse(process.env.PI_TEST_TASK_STATE_PATH!);
process.stdout.write(JSON.stringify(readDurableTaskProjection(taskStatePath)));
'''
            projection = json.loads(run_tsx(source, {"PI_TEST_TASK_STATE_PATH": json.dumps(task_state_path)}))
        finally:
            Path(task_state_path).unlink(missing_ok=True)
        labels = {task["taskId"]: task.get("roleLabel") for task in projection["tasks"]}
        self.assertEqual(labels["review-a-R1"], "BMAD Reviewer A")
        self.assertEqual(labels["review-b-R1"], "BMAD Reviewer B")
        self.assertEqual(labels["blocked-R1"], "BMAD Reviewer A")
        self.assertEqual(labels["failed-R1"], "BMAD Reviewer B")

    def test_missing_malformed_or_invalid_task_state_degrades_without_success(self):
        missing_context = self.TASK_MARKDOWN.replace('    contextSource:\n      type: "artifact-path"\n      paths:\n        - "story.md"\n', "", 1)
        bad_inputs = ["", "```yaml\ntasks: []\n```", self.TASK_MARKDOWN.replace('status: "failed"', 'status: "running"'), missing_context]
        source = f'''
import {{ parseDurableTaskState }} from "{PI_SUBAGENTS_SRC}/shared/ui-visibility.ts";
const inputs = JSON.parse(process.env.PI_TEST_INPUTS!);
process.stdout.write(JSON.stringify(inputs.map((value: string) => parseDurableTaskState(value))));
'''
        outputs = json.loads(run_tsx(source, {"PI_TEST_INPUTS": json.dumps(bad_inputs)}))
        for output in outputs:
            self.assertIn("degradedReason", output)
            self.assertEqual(output["tasks"], [])
            self.assertNotIn("completed", output.get("degradedReason", "").lower())


class TestRendererAndPatchDurability(unittest.TestCase):
    def test_renderer_preserves_existing_widget_facts_and_adds_visibility_fields(self):
        render = read(PI_SUBAGENTS_SRC / "tui" / "render.ts")
        for phrase in [
            "roleLabel",
            "durableTaskId",
            "bmadTaskProjectionLines",
            "modelTag",
            "taskSummary",
            "formatTokenStat",
            "formatDuration",
            "currentTool",
            "currentPath",
            "setTitle",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, render)

    def test_renderer_degrades_when_bmad_view_expected_without_task_state_path(self):
        render = read(PI_SUBAGENTS_SRC / "tui" / "render.ts")
        self.assertIn("expectsBmadTaskProjection", render)
        self.assertIn("durableTaskIds", render)
        self.assertIn("BMAD task state artifact path was not provided", render)
        self.assertIn("!taskStatePath && !expectsBmadTaskProjection", render)
        self.assertIn("⚠ BMAD task state unavailable", render)
        self.assertIn("runtimeDurableTaskIds(item).length > 0", render)

    def test_renderer_gates_runtime_rows_through_central_arbitration(self):
        render = read(PI_SUBAGENTS_SRC / "tui" / "render.ts")
        shared = read(PI_SUBAGENTS_SRC / "shared" / "ui-visibility.ts")
        for phrase in [
            "arbitrateRuntimeUiActivity",
            "durableStatusForRuntimeItem",
            "durableStatusForRuntimeItems",
            "runtimeIsRunning",
            "widgetStatusGlyph(job, theme, durableStatus)",
            "widgetStepGlyph(step.status, theme, durableStatus)",
            "widgetStepStatus(step.status, theme, durableStatus)",
            "resultGlyph(r, output, theme, isRunning, durableStatus)",
            "step.status === \"running\" && !isTerminalDurableStatus(durableStatus)",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, render)
        for phrase in [
            "TERMINAL_DURABLE_STATUSES",
            "export function isTerminalDurableStatus",
            "export function arbitrateRuntimeUiActivity",
            "export function durableStatusForRuntimeItem",
            "export function durableStatusForRuntimeItems",
            "export function durableStatusesForRuntimeItems",
        ]:
            with self.subTest(shared_phrase=phrase):
                self.assertIn(phrase, shared)

    def test_foreground_single_updates_preserve_task_state_path_before_title_update(self):
        executor = read(PI_SUBAGENTS_SRC / "runs" / "foreground" / "subagent-executor.ts")
        self.assertIn("taskStatePath: update.details.taskStatePath ?? params.taskStatePath", executor)
        self.assertIn("onUpdate(updateWithTaskState)", executor)

    def test_foreground_terminal_title_lifecycle_uses_progress_updates_and_clears(self):
        executor = read(PI_SUBAGENTS_SRC / "runs" / "foreground" / "subagent-executor.ts")
        for phrase in [
            "function setActivityTitle(ctx: ExtensionContext, result: AgentToolResult<Details>): void",
            "buildRuntimeActivityTitle({ details: result.details })",
            "setActivityTitle(ctx, contextual)",
            "function clearActivityTitle(ctx: ExtensionContext): void",
            "ctx.ui.setTitle?.(undefined)",
            "finally",
            "clearActivityTitle(ctx)",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, executor)

    def test_async_terminal_title_selection_uses_central_arbitration(self):
        render = read(PI_SUBAGENTS_SRC / "tui" / "render.ts")
        for phrase in [
            "asyncJobCanOwnActivityTitle",
            "arbitrateRuntimeUiActivity({ taskStatePath: job.taskStatePath, runtimeItems: items, runtimeStatus: job.status })",
            "if (arbitration.hasDurableTaskIds) return arbitration.canShowActive",
            "const runningTitleJob = jobs.find((job) => asyncJobCanOwnActivityTitle(job))",
            "runningTitleJob ? buildRuntimeActivityTitle({ job: runningTitleJob }) : undefined",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, render)

    def test_async_multi_job_header_bucketing_uses_central_arbitration(self):
        render = read(PI_SUBAGENTS_SRC / "tui" / "render.ts")
        shared = read(PI_SUBAGENTS_SRC / "shared" / "ui-visibility.ts")
        for phrase in [
            "asyncJobTerminalDurableStatus",
            "asyncJobEffectiveBucketStatus",
            "arbitration.terminalDurableStatus",
            "const running = jobs.filter((job) => asyncJobEffectiveBucketStatus(job, taskStatePath) === \"running\")",
            "const queued = jobs.filter((job) => asyncJobEffectiveBucketStatus(job, taskStatePath) === \"queued\")",
            "const finished = jobs.filter((job) => asyncJobEffectiveBucketStatus(job, taskStatePath) === \"finished\")",
            "const hasActive = running.length > 0 || queued.length > 0",
            "asyncJobTerminalDurableStatus(job, taskStatePath) ?? durableStatusForRuntimeItem(taskStatePath, job)",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, render)
        self.assertIn("statuses.find((status) => status === \"failed\")", shared)

    def test_async_title_clears_when_durable_task_ids_lack_readable_task_state(self):
        render = read(PI_SUBAGENTS_SRC / "tui" / "render.ts")
        shared = read(PI_SUBAGENTS_SRC / "shared" / "ui-visibility.ts")
        for phrase in [
            "function asyncJobHasReadableDurableProjection(job: AsyncJobState): boolean",
            "runtimeDurableTaskIdsForItems(items).length === 0 || !arbitration.degradedReason",
            "if (arbitration.hasDurableTaskIds) return arbitration.canShowActive",
            "ctx.ui.setTitle?.(runningTitleJob ? buildRuntimeActivityTitle({ job: runningTitleJob }) : undefined)",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, render)
        for phrase in [
            "BMAD task state artifact path was not provided",
            "if (arbitration.degradedReason && durableTaskIds.length > 0) return undefined",
        ]:
            with self.subTest(shared_phrase=phrase):
                self.assertIn(phrase, shared)

    def test_async_status_list_and_detail_apply_central_arbitration_and_degraded_warnings(self):
        task_markdown = '''
### Task State
```yaml
tasks:
  - taskId: "done-R1"
    title: "Already completed"
    targetAgent: "implementer"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "story.md"
    activeAgentId: "implementer"
```
'''
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            tmp_path = Path(tmp)
            async_root = tmp_path / "async"
            results_dir = tmp_path / "results"
            async_root.mkdir()
            results_dir.mkdir()
            story_path = tmp_path / "story.md"
            story_path.write_text(task_markdown, encoding="utf-8")
            terminal_dir = async_root / "terminal-run"
            terminal_dir.mkdir()
            job_terminal_dir = async_root / "job-terminal-run"
            job_terminal_dir.mkdir()
            missing_dir = async_root / "missing-state-run"
            missing_dir.mkdir()
            job_missing_dir = async_root / "job-missing-state-run"
            job_missing_dir.mkdir()
            base_status = {
                "sessionId": "session-1",
                "mode": "single",
                "state": "running",
                "startedAt": 1700000000000,
                "lastUpdate": 1700000000100,
                "currentStep": 0,
                "steps": [{"agent": "implementer", "roleLabel": "BMAD Implementer", "durableTaskId": "done-R1", "status": "running", "taskSummary": "runtime says active"}],
            }
            terminal_status = {**base_status, "runId": "terminal-run", "taskStatePath": str(story_path)}
            job_terminal_status = {k: v for k, v in terminal_status.items() if k not in {"steps", "currentStep"}}
            job_terminal_status["runId"] = "job-terminal-run"
            job_terminal_status["durableTaskIds"] = ["done-R1"]
            missing_status = {**base_status, "runId": "missing-state-run"}
            job_missing_status = {k: v for k, v in missing_status.items() if k not in {"steps", "currentStep"}}
            job_missing_status["runId"] = "job-missing-state-run"
            job_missing_status["durableTaskIds"] = ["done-R1"]
            (terminal_dir / "status.json").write_text(json.dumps(terminal_status), encoding="utf-8")
            (job_terminal_dir / "status.json").write_text(json.dumps(job_terminal_status), encoding="utf-8")
            (missing_dir / "status.json").write_text(json.dumps(missing_status), encoding="utf-8")
            (job_missing_dir / "status.json").write_text(json.dumps(job_missing_status), encoding="utf-8")
            source = f'''
import {{ listAsyncRuns, formatAsyncRunList }} from "{PI_SUBAGENTS_SRC}/runs/background/async-status.ts";
import {{ inspectSubagentStatus }} from "{PI_SUBAGENTS_SRC}/runs/background/run-status.ts";
const asyncRoot = JSON.parse(process.env.PI_TEST_ASYNC_ROOT!);
const resultsDir = JSON.parse(process.env.PI_TEST_RESULTS_DIR!);
const active = listAsyncRuns(asyncRoot, {{ states: ["queued", "running"], resultsDir, reconcile: false }});
const all = listAsyncRuns(asyncRoot, {{ resultsDir, reconcile: false }});
const terminalDetail = inspectSubagentStatus({{ id: "terminal-run" }}, {{ asyncDirRoot: asyncRoot, resultsDir }}).content[0].text;
const jobTerminalDetail = inspectSubagentStatus({{ id: "job-terminal-run" }}, {{ asyncDirRoot: asyncRoot, resultsDir }}).content[0].text;
const missingDetail = inspectSubagentStatus({{ id: "missing-state-run" }}, {{ asyncDirRoot: asyncRoot, resultsDir }}).content[0].text;
const jobMissingDetail = inspectSubagentStatus({{ id: "job-missing-state-run" }}, {{ asyncDirRoot: asyncRoot, resultsDir }}).content[0].text;
process.stdout.write(JSON.stringify({{
  activeIds: active.map((run) => run.id),
  allText: formatAsyncRunList(all, "All async runs"),
  terminalDetail,
  jobTerminalDetail,
  missingDetail,
  jobMissingDetail,
}}));
'''
            out = json.loads(run_tsx(source, {"PI_TEST_ASYNC_ROOT": json.dumps(str(async_root)), "PI_TEST_RESULTS_DIR": json.dumps(str(results_dir))}))
        self.assertNotIn("terminal-run", out["activeIds"], "durable completed work must not be listed as active")
        self.assertNotIn("job-terminal-run", out["activeIds"], "job-level durable completed work must not be listed as active")
        self.assertIn("missing-state-run", out["activeIds"], "missing task state should stay visible as degraded, not disappear")
        self.assertIn("job-missing-state-run", out["activeIds"], "job-level missing task state should stay visible as degraded")
        self.assertIn("completed", out["terminalDetail"])
        self.assertIn("completed", out["jobTerminalDetail"])
        self.assertNotIn("Intercom target", out["terminalDetail"])
        self.assertIn("⚠ BMAD task state unavailable", out["allText"])
        self.assertIn("path was not provided", out["allText"])
        self.assertIn("running (degraded)", out["missingDetail"])
        self.assertIn("running (degraded)", out["jobMissingDetail"])
        self.assertIn("path was not provided", out["missingDetail"])
        self.assertIn("path was not provided", out["jobMissingDetail"])

    def test_types_and_async_status_carry_role_label_task_identity_and_task_state_path(self):
        types = read(PI_SUBAGENTS_SRC / "shared" / "types.ts")
        for phrase in ["roleLabel?: string", "durableTaskId?: string", "durableTaskIds?: string[]", "taskStatePath?: string", "currentTool?: string", "currentPath?: string"]:
            self.assertIn(phrase, types)
        self.assertIn("durableTaskId", read(PI_SUBAGENTS_SRC / "runs" / "background" / "async-status.ts"))
        self.assertIn("durableTaskId", read(PI_SUBAGENTS_SRC / "runs" / "background" / "subagent-runner.ts"))
        self.assertIn("durableTaskId", read(PI_SUBAGENTS_SRC / "runs" / "foreground" / "execution.ts"))

    def test_patch_file_exists_and_install_script_applies_story15_patch(self):
        patch = PATCHES_DIR / "pi-subagents-0.24.2-ui-visibility-agent-activity.patch"
        self.assertTrue(patch.exists())
        content = read(patch)
        for expected in [
            "src/shared/ui-visibility.ts",
            "src/tui/render.ts",
            "src/runs/foreground/subagent-executor.ts",
            "src/runs/background/async-execution.ts",
            "src/runs/background/subagent-runner.ts",
            "src/extension/schemas.ts",
        ]:
            self.assertIn(expected, content)
        self.assertNotIn("src/agents/agents.ts", content, "Story 1.5 patch must not duplicate prior agent-discovery patch hunks")
        script = read(ROOT / ".pi" / "install-packages.sh") + read(PATCHES_DIR / "apply-patches.sh")
        self.assertIn("*.patch", script)

    def test_no_dispatch_subagent_or_dispatchable_orchestrator_child_agent(self):
        all_text = "\n".join(read(path) for path in [ORCHESTRATOR, DEV_CYCLE])
        self.assertNotIn("dispatch_subagent(", all_text)
        self.assertFalse((AGENTS_DIR / "orchestrator.md").exists())
        self.assertFalse((AGENTS_DIR / "bmad-orchestrator.md").exists())


if __name__ == "__main__":
    unittest.main()
