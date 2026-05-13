"""Story 1.4 regression checks for BMAD orchestrator task routing state.

These provider-free tests validate the durable Markdown task-state contract and
parent-owned routing lifecycle documented for formal BMAD orchestration.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCHESTRATOR = ROOT / ".pi" / "skills" / "bmad-orchestrator" / "SKILL.md"
CODE_REVIEW_GATHER_STEP = ROOT / ".pi" / "skills" / "bmad-code-review" / "steps" / "step-01-gather-context.md"
CODE_REVIEW_REVIEW_STEP = ROOT / ".pi" / "skills" / "bmad-code-review" / "steps" / "step-02-review.md"
QUICK_DEV_CLARIFY_STEP = ROOT / ".pi" / "skills" / "bmad-quick-dev" / "step-01-clarify-and-route.md"
QUICK_DEV_PLAN_STEP = ROOT / ".pi" / "skills" / "bmad-quick-dev" / "step-02-plan.md"
QUICK_DEV_IMPLEMENT_STEP = ROOT / ".pi" / "skills" / "bmad-quick-dev" / "step-03-implement.md"
QUICK_DEV_REVIEW_STEP = ROOT / ".pi" / "skills" / "bmad-quick-dev" / "step-04-review.md"
QUICK_DEV_ONESHOT_STEP = ROOT / ".pi" / "skills" / "bmad-quick-dev" / "step-oneshot.md"
AGENTS_DIR = ROOT / ".pi" / "agents"

ACTIVE_DISPATCH_STEPS = [
    CODE_REVIEW_REVIEW_STEP,
    QUICK_DEV_CLARIFY_STEP,
    QUICK_DEV_PLAN_STEP,
    QUICK_DEV_IMPLEMENT_STEP,
    QUICK_DEV_REVIEW_STEP,
    QUICK_DEV_ONESHOT_STEP,
]


STATUS_VOCABULARY = ["pending", "in-progress", "completed", "blocked", "failed"]
REQUIRED_FIELDS = ["taskId", "title", "targetAgent", "status", "contextSource"]
OPTIONAL_FIELDS = [
    "dependsOn",
    "activeAgentId",
    "outputArtifact",
    "cause",
    "recommendedNextAction",
    "routingDecision",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def task_state_section() -> str:
    text = read(ORCHESTRATOR)
    match = re.search(
        r"## Task Routing and Task List State\n(?P<section>.*?)(?=\n## |\Z)",
        text,
        flags=re.DOTALL,
    )
    if not match:
        raise AssertionError("Missing Task Routing and Task List State section")
    return match.group("section")


def subagent_blocks(markdown: str) -> list[str]:
    return re.findall(r"subagent\(\{.*?\}\)", markdown, flags=re.DOTALL)


class OrchestratorTaskRoutingStateGuidanceTests(unittest.TestCase):
    def test_task_state_contract_documents_fixed_vocabulary_and_fields(self):
        section = task_state_section()
        self.assertIn("builder-facing status vocabulary", section)
        for status in STATUS_VOCABULARY:
            with self.subTest(status=status):
                self.assertIn(f"`{status}`", section)
        for field in REQUIRED_FIELDS:
            with self.subTest(field=field):
                self.assertRegex(section, rf"required.*`{field}`|`{field}`.*required")
        for field in OPTIONAL_FIELDS:
            with self.subTest(field=field):
                self.assertRegex(section, rf"optional.*`{field}`|`{field}`.*optional")

    def test_task_list_persistence_and_runtime_status_mapping_are_documented(self):
        section = task_state_section()
        self.assertIn("relevant BMAD story/spec/run artifact", section)
        self.assertIn("named Markdown artifact", section)
        for runtime_status in ["running", "complete", "paused", "detached"]:
            with self.subTest(runtime_status=runtime_status):
                self.assertIn(f"`{runtime_status}`", section)
        self.assertIn("mapped into the builder-facing vocabulary", section)
        self.assertIn("before durable Markdown state is written", section)

    def test_pending_in_progress_completed_transition_rules_are_documented(self):
        section = task_state_section()
        self.assertRegex(section, r"validate.*`pending`")
        self.assertRegex(section, r"dependencies.*`completed`")
        self.assertRegex(section, r"Immediately before dispatch.*`in-progress`")
        self.assertIn("`activeAgentId`", section)
        self.assertRegex(section, r"After successful child completion.*`completed`")
        self.assertIn("parent validation", section)
        self.assertIn("output artifact path", section)

    def test_blocked_failed_handling_requires_cause_and_recommended_next_action(self):
        section = task_state_section()
        for condition in [
            "fails",
            "times out",
            "empty/ambiguous output",
            "violates session policy",
            "unclassifiable state",
        ]:
            with self.subTest(condition=condition):
                self.assertIn(condition, section)
        self.assertRegex(section, r"`blocked` or `failed`.*`cause`.*`recommendedNextAction`")
        self.assertIn("do not dispatch later dependent tasks", section)

    def test_sequenced_handoffs_require_declared_context_and_routing_decision(self):
        section = task_state_section()
        for phrase in [
            "direct task text",
            "output artifact path",
            "named `pi-subagents` output file reference",
            "artifact paths/read directives",
            "rather than parent-side summaries",
            "`routingDecision`",
            "why the next task became eligible",
            "which prior output/context source it consumed",
            "control-plane",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, section)

    def test_task_routing_examples_preserve_explicit_fresh_context(self):
        text = read(ORCHESTRATOR)
        blocks = subagent_blocks(text)
        self.assertGreaterEqual(len(blocks), 3, "Expected documented subagent examples")
        for block in blocks:
            with self.subTest(block=block):
                if "task:" in block or "tasks:" in block or "chain:" in block:
                    self.assertIn('context: "fresh"', block)
                    self.assertNotIn('context: "fork"', block)
                    self.assertNotIn('action: "resume"', block)

    def test_policy_rejections_happen_before_task_status_changes(self):
        section = task_state_section()
        self.assertIn("Policy rejection happens before any task status change", section)
        self.assertIn("must not become `in-progress`", section)
        self.assertIn("optional debug note", section)

    def test_active_dispatch_workflows_reference_task_state_contract(self):
        required_phrases = [
            "Task Routing and Task List State",
            "orchestrator-managed task list",
            "before dispatch",
            "`in-progress`",
            "`completed`",
            "`blocked` or `failed`",
            "`cause` and `recommendedNextAction`",
            "do not dispatch dependent tasks",
        ]
        for path in ACTIVE_DISPATCH_STEPS:
            text = read(path)
            with self.subTest(path=path.relative_to(ROOT)):
                for phrase in required_phrases:
                    self.assertIn(phrase, text)

    def test_code_review_diff_includes_untracked_files_for_review_delta(self):
        text = read(CODE_REVIEW_GATHER_STEP)
        self.assertIn("untracked", text)
        self.assertIn("git ls-files --others --exclude-standard", text)
        self.assertIn("git diff --no-index /dev/null <path>", text)
        self.assertIn("tracked and untracked", text)

    def test_quick_dev_context_discovery_spawn_failure_requires_durable_state_before_inline_recovery(self):
        text = read(QUICK_DEV_CLARIFY_STEP)
        self.assertIn("If the spawn fails or times out", text)
        self.assertRegex(text, r"first write .*`blocked` or `failed`")
        self.assertIn("`cause` and `recommendedNextAction`", text)
        self.assertIn("Continuing inline is an explicit recovery", text)
        self.assertIn("separate recovery task", text)
        self.assertIn("`routingDecision`", text)
        self.assertIn("Do not treat failed or timed-out spawn fallback as the same task continuing normally", text)
        self.assertIn('context: "fresh"', text)

    def test_result_handling_reconciles_fail_closed_with_durable_blocked_failed_state(self):
        text = read(ORCHESTRATOR)
        result_section = re.search(
            r"## Result Handling\n(?P<section>.*?)(?=\n## |\Z)",
            text,
            flags=re.DOTALL,
        ).group("section")
        self.assertIn("For orchestrator-managed tasks", result_section)
        self.assertIn("write the durable task state as `blocked` or `failed`", result_section)
        self.assertIn("`cause` and `recommendedNextAction`", result_section)
        self.assertIn("Do not mark the task `completed`", result_section)
        self.assertIn("do not dispatch dependent tasks", result_section)
        self.assertIn("Policy rejection remains pre-dispatch", result_section)

    def test_no_dispatchable_orchestrator_or_child_subagent_tool_grants(self):
        for filename in ["orchestrator.md", "bmad-orchestrator.md"]:
            with self.subTest(filename=filename):
                self.assertFalse((AGENTS_DIR / filename).exists())
        for filename in ["implementer.md", "reviewer-a.md", "reviewer-b.md", "findings-triager.md"]:
            frontmatter = read(AGENTS_DIR / filename).split("---", 2)[1]
            with self.subTest(filename=filename):
                self.assertNotRegex(frontmatter, r"tools:.*\bsubagent\b")


if __name__ == "__main__":
    unittest.main()
