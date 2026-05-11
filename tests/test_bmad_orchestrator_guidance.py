import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDANCE = ROOT / ".pi" / "skills" / "bmad-orchestrator" / "SKILL.md"
STORY = ROOT / "docs" / "_bmad-output" / "implementation-artifacts" / "1-1-implement-the-generic-sub-agent-dispatch-tool.md"
GITIGNORE = ROOT / ".gitignore"


def guidance_text() -> str:
    return GUIDANCE.read_text(encoding="utf-8")


def story_text() -> str:
    return STORY.read_text(encoding="utf-8")


class BmadOrchestratorGuidanceTests(unittest.TestCase):
    def test_parent_guidance_declares_active_tool_allowlist_and_child_exclusion(self):
        text = guidance_text()
        self.assertIn("## Active Tool Allowlist", text)
        self.assertIn("`subagent`", text)
        self.assertIn("must not receive the `subagent` tool", text)
        self.assertIn("`dispatch_subagent`", text)

    def test_canonical_agent_identifier_is_recorded_as_dispatch_evidence(self):
        text = guidance_text()
        self.assertIn("canonicalAgentId", text)
        self.assertIn("requestedAgent", text)
        self.assertIn("runId", text)
        self.assertIn("Record the canonical agent identifier", text)

    def test_artifact_paths_are_portable_placeholders_and_validated_before_dispatch(self):
        text = guidance_text()
        self.assertIn("<artifact-path>", text)
        self.assertNotIn("1-1-implement-the-generic-sub-agent-dispatch-tool.md", text)
        self.assertIn("Before dispatching formal artifact paths", text)
        self.assertRegex(text, r"(?is)exists.*readable|readable.*exists")
        self.assertIn("HALT", text)

    def test_child_run_errors_and_timeouts_fail_closed_before_state_updates(self):
        text = guidance_text()
        self.assertIn("timeout", text.lower())
        self.assertIn("error", text.lower())
        self.assertIn("fail closed", text.lower())
        self.assertIn("before updating Markdown artifacts", text)

    def test_unknown_agent_recovery_has_reproducible_parent_follow_up_evidence(self):
        text = guidance_text()
        self.assertIn("Unknown-agent recovery evidence", text)
        self.assertIn('subagent({ action: "list", agentScope: "both" })', text)
        self.assertIn("available identifiers", text.lower())

    def test_story_acceptance_criteria_describe_parent_mediated_unknown_agent_recovery(self):
        text = story_text()
        self.assertIn('then the request is refused with an actionable unknown-agent message; the parent then immediately runs `subagent({ action: "list", agentScope: "both" })` and surfaces the returned valid identifiers.', text)
        self.assertNotIn("the request is refused with an actionable unknown-agent message and available agent identifiers", text)
        self.assertIn("AC4 evidence is parent-mediated", text)
        self.assertIn("runtime fail-closed error does not expose available identifiers inline", text)
        self.assertIn('subagent({ action: "list", agentScope: "both" })', text)

    def test_story_acceptance_criteria_allow_canonical_metadata_fallback(self):
        text = story_text()
        self.assertIn("records the canonical agent identifier from returned metadata when available", text)
        self.assertIn("list/get-validated canonical identifier", text)
        self.assertIn("runId: not exposed", text)

    def test_story_records_canonical_identifier_for_launched_child_without_run_metadata(self):
        text = story_text()
        self.assertIn("Live child dispatch identity evidence", text)
        self.assertIn('requestedAgent: "scout"', text)
        self.assertIn('canonicalAgentId: "scout"', text)
        self.assertIn("runId: not exposed", text)
        self.assertIn("list-validated", text)

    def test_python_bytecode_is_ignored(self):
        text = GITIGNORE.read_text(encoding="utf-8")
        self.assertIn("__pycache__/", text)
        self.assertRegex(text, r"(?m)^\*\.py\[cod\]$")

    def test_story_artifacts_limit_review_skill_scope_without_reading_out_of_scope_skill(self):
        text = story_text()
        self.assertIn("Review-skill scope correction", text)
        file_list = text.split("### File List", 1)[1].split("### Change Log", 1)[0]
        self.assertNotIn("bmad-review-adversarial-general", file_list)

    def test_debug_log_does_not_claim_there_is_no_test_suite_after_tests_were_added(self):
        text = story_text()
        self.assertNotIn("or test suite; final static smoke validation", text)
        self.assertIn("no pre-existing project-level unit test suite", text)

    def test_dev_agent_record_file_list_covers_review_patch_files(self):
        text = story_text()
        for expected in [
            ".gitignore",
            ".pi/npm/.gitignore",
            ".pi/skills/bmad-orchestrator/SKILL.md",
            "tests/test_bmad_orchestrator_guidance.py",
            "docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool.md",
        ]:
            self.assertIn(f"- `{expected}`", text)


if __name__ == "__main__":
    unittest.main()
