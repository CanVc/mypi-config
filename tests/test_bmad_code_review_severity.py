import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE_REVIEW_ROOTS = [
    ROOT / ".agents" / "skills" / "bmad-code-review" / "steps",
    ROOT / ".claude" / "skills" / "bmad-code-review" / "steps",
    ROOT / ".pi" / "skills" / "bmad-code-review" / "steps",
]
ORCHESTRATOR = ROOT / ".pi" / "skills" / "bmad-orchestrator" / "SKILL.md"


class BmadCodeReviewSeverityTests(unittest.TestCase):
    def test_reviewer_prompts_require_finding_severity_in_all_skill_copies(self):
        for steps_dir in CODE_REVIEW_ROOTS:
            with self.subTest(steps_dir=steps_dir):
                text = (steps_dir / "step-02-review.md").read_text(encoding="utf-8")
                self.assertIn("Every review subagent MUST attach a severity", text)
                self.assertIn("Severity: High|Medium|Low", text)
                self.assertIn("`severity` field", text)

    def test_triage_normalizes_and_classifies_by_severity_in_all_skill_copies(self):
        for steps_dir in CODE_REVIEW_ROOTS:
            with self.subTest(steps_dir=steps_dir):
                text = (steps_dir / "step-03-triage.md").read_text(encoding="utf-8")
                self.assertIn("`severity` -- exactly one of `High`, `Medium`, or `Low`", text)
                self.assertIn("Severity-aware classification rules", text)
                self.assertIn("`High` findings are blocking", text)
                self.assertIn("`Low` findings are non-blocking by default", text)
                self.assertIn("If only `Low` findings remain", text)

    def test_present_step_persists_severity_and_uses_non_blocking_low_policy(self):
        for steps_dir in CODE_REVIEW_ROOTS:
            with self.subTest(steps_dir=steps_dir):
                text = (steps_dir / "step-04-present.md").read_text(encoding="utf-8")
                self.assertIn("Every persisted or presented finding MUST include severity", text)
                self.assertIn("[Review][Patch][<Severity>]", text)
                self.assertIn("[Review][Defer][<Severity>]", text)
                self.assertIn("Never keep a story blocked only because `Low` findings exist", text)
                self.assertIn("recommended when no blocking High/Medium findings remain", text)

    def test_orchestrator_selects_next_action_from_review_severity(self):
        text = ORCHESTRATOR.read_text(encoding="utf-8")
        self.assertIn("## Review Severity and Next Action Policy", text)
        self.assertIn("every finding must carry exactly one severity", text)
        self.assertIn("If any unresolved `High`, blocking `Medium`, or `decision_needed` finding remains", text)
        self.assertIn("If only `Low` findings remain", text)
        self.assertIn("If a third review pass still has unresolved blocking `High`/`Medium`", text)
        self.assertIn("If a third review pass has only `Low` findings", text)


if __name__ == "__main__":
    unittest.main()
