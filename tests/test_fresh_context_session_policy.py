"""Story 1.3 regression checks for BMAD fresh-context session policy.

These tests are provider-free and validate the active v1 policy text that the
parent BMAD session must apply before any formal `pi-subagents` dispatch.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCHESTRATOR = ROOT / ".pi" / "skills" / "bmad-orchestrator" / "SKILL.md"
CODE_REVIEW_STEP = ROOT / ".pi" / "skills" / "bmad-code-review" / "steps" / "step-02-review.md"
QUICK_DEV_CLARIFY_STEP = ROOT / ".pi" / "skills" / "bmad-quick-dev" / "step-01-clarify-and-route.md"
QUICK_DEV_PLAN_STEP = ROOT / ".pi" / "skills" / "bmad-quick-dev" / "step-02-plan.md"
QUICK_DEV_IMPLEMENT_STEP = ROOT / ".pi" / "skills" / "bmad-quick-dev" / "step-03-implement.md"
QUICK_DEV_REVIEW_STEP = ROOT / ".pi" / "skills" / "bmad-quick-dev" / "step-04-review.md"
QUICK_DEV_ONESHOT_STEP = ROOT / ".pi" / "skills" / "bmad-quick-dev" / "step-oneshot.md"
AGENTS_DIR = ROOT / ".pi" / "agents"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def subagent_blocks(markdown: str) -> list[str]:
    return re.findall(r"subagent\(\{.*?\}\)", markdown, flags=re.DOTALL)


class FreshContextSessionPolicyGuidanceTests(unittest.TestCase):
    def test_session_policy_declares_v1_fresh_context_default_and_no_active_reuse(self):
        text = read(ORCHESTRATOR)
        self.assertIn("## Session Policy", text)
        self.assertIn('All formal BMAD dispatches MUST pass `context: "fresh"` explicitly', text)
        self.assertIn("omitted context is forbidden", text)
        self.assertIn('`defaultContext: "fork"`', text)
        self.assertIn("Active v1 allowed reuse/resume exception set: none", text)
        self.assertIn("Future TDD red/green repair exceptions are future scope", text)

    def test_all_orchestrator_subagent_examples_use_explicit_fresh_context(self):
        blocks = subagent_blocks(read(ORCHESTRATOR))
        self.assertGreaterEqual(len(blocks), 3, "Expected documented subagent examples")
        for block in blocks:
            with self.subTest(block=block):
                # Discovery/status/policy-shorthand examples are not launch examples;
                # examples containing a task or tasks/chain launch shape are.
                if "task:" in block or "tasks:" in block or "chain:" in block:
                    self.assertIn('context: "fresh"', block)
                    self.assertNotIn('context: "fork"', block)
                    self.assertNotIn('action: "resume"', block)

    def test_policy_covers_all_formal_invocation_shapes_and_fails_closed(self):
        text = read(ORCHESTRATOR)
        for phrase in [
            "single-agent `agent` dispatch",
            "top-level parallel `tasks` dispatch",
            "`chain` dispatch",
            "parallel-chain dispatch",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        self.assertIn('`context: "fork"` is unsafe for BMAD formal dispatches', text)
        self.assertIn('`subagent({ action: "resume", ... })` is session reuse', text)
        self.assertIn("fail closed before any child launch", text)
        self.assertIn("before any Markdown artifact state transition", text)

    def test_reviewer_validator_and_final_review_roles_are_always_fresh(self):
        text = read(ORCHESTRATOR)
        for phrase in [
            "`reviewer-a`",
            "`reviewer-b`",
            "`findings-triager`",
            "Blind Hunter",
            "Edge Case Hunter",
            "Acceptance Auditor",
            "validators",
            "final reviewers",
            "final-review retry loops",
            "no exception",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        self.assertIn("requested `fork` or `resume` for these roles MUST be blocked", text)

    def test_policy_rejection_text_names_agent_mode_and_policy(self):
        text = read(ORCHESTRATOR)
        for phrase in [
            "requestedAgent",
            "requestedMode",
            "violatedPolicy",
            "requested context/resume mode",
            "violated policy",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_fresh_artifact_context_excludes_previous_transcripts(self):
        text = read(ORCHESTRATOR)
        for phrase in [
            "only the task text and explicitly named artifacts",
            "No previous runtime transcript",
            "parent conversation",
            "child output history",
            "reviewer transcript",
            "must not be appended",
            "artifact paths/read directives",
            "not lossy summaries",
            "inheritProjectContext: true",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_code_review_step_routes_layers_through_fresh_policy(self):
        text = read(CODE_REVIEW_STEP)
        self.assertIn('context: "fresh"', text)
        self.assertIn("centralized BMAD Session Policy", text)
        self.assertIn("no fork/resume", text)
        self.assertIn("always fresh", text)
        for role in ["Blind Hunter", "Edge Case Hunter", "Acceptance Auditor"]:
            with self.subTest(role=role):
                self.assertIn(role, text)

    def test_quick_dev_context_compilation_validates_session_policy_before_artifact_write(self):
        text = read(QUICK_DEV_CLARIFY_STEP)
        self.assertIn('context: "fresh"', text)
        self.assertIn("centralized BMAD Session Policy", text)
        self.assertIn("before writing `{implementation_artifacts}/epic-<N>-context.md`", text)
        self.assertIn("omits context, requests `context: \"fork\"`, or requests `action: \"resume\"`", text)
        self.assertIn("HALT before dispatch and before writing or updating any artifact", text)
        self.assertIn("requested agent, requested mode, and violated policy", text)
        self.assertIn("task text and explicitly named artifact paths", text)
        self.assertIn("must not append parent conversation history", text)

    def test_quick_dev_plan_validates_session_policy_before_investigation_and_spec_write(self):
        text = read(QUICK_DEV_PLAN_STEP)
        self.assertIn('context: "fresh"', text)
        self.assertIn("centralized BMAD Session Policy", text)
        self.assertIn("Before launching any investigation sub-agent/task or writing `{spec_file}`", text)
        self.assertIn("HALT before dispatch and before writing `{spec_file}`", text)
        self.assertIn("omits context, requests `context: \"fork\"`, or requests `action: \"resume\"`", text)
        self.assertIn("requested investigation agent/task, requested mode, and violated policy", text)
        self.assertIn("only the task text and explicitly named artifact paths/read directives", text)
        self.assertIn("must not append parent conversation history", text)
        self.assertIn("previous runtime transcript", text)

    def test_quick_dev_implementation_validates_session_policy_before_status_update(self):
        text = read(QUICK_DEV_IMPLEMENT_STEP)
        self.assertIn('context: "fresh"', text)
        self.assertIn("centralized BMAD Session Policy", text)
        self.assertIn("Before changing `{spec_file}` status", text)
        self.assertIn("HALT before editing `{spec_file}`", text)
        self.assertIn("omits context, requests `context: \"fork\"`, or requests `action: \"resume\"`", text)
        self.assertIn("requested implementer agent, requested mode, and violated policy", text)
        self.assertIn("only `{spec_file}` plus explicitly named context artifacts", text)
        self.assertIn("must not append parent conversation history", text)

    def test_quick_dev_review_validates_session_policy_before_state_update(self):
        text = read(QUICK_DEV_REVIEW_STEP)
        self.assertIn('context: "fresh"', text)
        self.assertIn("no fork/resume", text)
        self.assertIn("Before changing `{spec_file}` status", text)
        self.assertIn("HALT before editing `{spec_file}`", text)
        self.assertIn("requested reviewer role, requested mode, and violated policy", text)

    def test_quick_dev_oneshot_review_uses_fresh_policy(self):
        text = read(QUICK_DEV_ONESHOT_STEP)
        self.assertIn('context: "fresh"', text)
        self.assertIn("no fork/resume", text)
        self.assertIn("Fresh review prompts must not append", text)
        self.assertIn("requested reviewer role, requested mode, and violated policy", text)
        self.assertNotIn("NO conversation context", text)


class FreshContextRoleBoundaryTests(unittest.TestCase):
    def test_no_dispatchable_orchestrator_or_v2_tdd_agents_exist(self):
        forbidden = [
            "orchestrator.md",
            "bmad-orchestrator.md",
            "test-architect.md",
            "test-writer.md",
            "red-validator.md",
            "green-validator.md",
        ]
        for filename in forbidden:
            with self.subTest(filename=filename):
                self.assertFalse((AGENTS_DIR / filename).exists())

    def test_role_agents_do_not_receive_subagent_tool(self):
        for filename in ["implementer.md", "reviewer-a.md", "reviewer-b.md", "findings-triager.md"]:
            text = read(AGENTS_DIR / filename)
            frontmatter = text.split("---", 2)[1]
            with self.subTest(filename=filename):
                self.assertIn("tools:", frontmatter)
                self.assertNotRegex(frontmatter, r"tools:.*\bsubagent\b")
                self.assertIn("defaultContext: fresh", frontmatter)


if __name__ == "__main__":
    unittest.main()
