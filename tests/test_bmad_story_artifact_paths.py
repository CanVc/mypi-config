"""Story 1.2.1 regression checks for story-scoped BMAD artifacts.

These tests validate the active .pi skill instructions for the v1 convention:
`{implementation_artifacts}/{story_key}/{story_key}.md`, with legacy flat
story files supported only as a fallback.
"""

import re
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PI_SKILLS = ROOT / ".pi" / "skills"


def read_skill(relative_path: str) -> str:
    return (PI_SKILLS / relative_path).read_text(encoding="utf-8")


def canonical_story_path(implementation_artifacts: Path, story_key: str) -> Path:
    return implementation_artifacts / story_key / f"{story_key}.md"


def legacy_story_path(implementation_artifacts: Path, story_key: str) -> Path:
    return implementation_artifacts / f"{story_key}.md"


def review_artifact_dir(implementation_artifacts: Path, spec_file: Path, story_key: str | None = None) -> Path:
    """Model code-review routing: known BMAD stories always use story folders."""
    if story_key:
        return implementation_artifacts / story_key

    if spec_file.parent == implementation_artifacts and re.match(r"^\d+-\d+-[a-z0-9-]+$", spec_file.stem):
        return implementation_artifacts / spec_file.stem

    if spec_file.parent.parent == implementation_artifacts and spec_file.parent.name == spec_file.stem:
        return spec_file.parent

    return spec_file.parent


def resolve_story_file(implementation_artifacts: Path, story_key: str) -> Path | None:
    """Model the required canonical-first, legacy-fallback lookup."""
    canonical = canonical_story_path(implementation_artifacts, story_key)
    if canonical.exists():
        return canonical
    legacy = legacy_story_path(implementation_artifacts, story_key)
    if legacy.exists():
        return legacy
    return None


def discover_story_files(implementation_artifacts: Path) -> list[Path]:
    """Return story markdown files, excluding story-scoped review artifacts."""
    story_key_pattern = re.compile(r"^\d+-\d+-[a-z0-9-]+$")
    results: list[Path] = []
    for path in implementation_artifacts.rglob("*.md"):
        stem = path.stem
        if not story_key_pattern.match(stem):
            continue
        if path.name.startswith("review-"):
            continue
        # Canonical folder-based file or legacy flat file.
        if path.parent == implementation_artifacts or path.parent.name == stem:
            results.append(path)
    return sorted(results)


class BmadStoryArtifactPathTests(unittest.TestCase):
    def test_temp_story_resolution_prefers_folder_and_falls_back_to_legacy_flat(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            story_key = "1-2-user-auth"

            legacy = legacy_story_path(root, story_key)
            legacy.write_text("Status: done\n", encoding="utf-8")
            self.assertEqual(resolve_story_file(root, story_key), legacy)

            canonical = canonical_story_path(root, story_key)
            canonical.parent.mkdir()
            canonical.write_text("Status: review\n", encoding="utf-8")
            self.assertEqual(resolve_story_file(root, story_key), canonical)

    def test_recursive_discovery_finds_folder_and_legacy_stories_without_review_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            canonical = canonical_story_path(root, "1-1-first-story")
            canonical.parent.mkdir()
            canonical.write_text("Status: done\n", encoding="utf-8")
            legacy = legacy_story_path(root, "1-2-legacy-story")
            legacy.write_text("Status: done\n", encoding="utf-8")
            review = root / "1-1-first-story" / "review-1-1-first-story-blind.md"
            review.write_text("review prompt", encoding="utf-8")

            self.assertEqual(discover_story_files(root), [canonical, legacy])

    def test_code_review_artifact_dir_uses_story_folder_for_legacy_flat_stories(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            story_key = "1-2-legacy-story"
            legacy = legacy_story_path(root, story_key)
            legacy.write_text("Status: review\n", encoding="utf-8")

            self.assertEqual(review_artifact_dir(root, legacy, story_key), root / story_key)
            self.assertEqual(review_artifact_dir(root, legacy), root / story_key)
            self.assertNotEqual(review_artifact_dir(root, legacy, story_key), root)

    def test_create_story_writes_folder_path_and_scans_previous_stories_recursively(self):
        text = read_skill("bmad-create-story/workflow.md")
        self.assertIn("{implementation_artifacts}/{{story_key}}/{{story_key}}.md", text)
        self.assertIn("Ensure the story artifact directory exists", text)
        self.assertIn("canonical folder-based story files first", text)
        self.assertIn("legacy flat story files", text)
        self.assertNotIn("`default_output_file` = `{implementation_artifacts}/{{story_key}}.md`", text)

    def test_dev_story_prefers_story_folder_and_preserves_legacy_fallback(self):
        text = read_skill("bmad-dev-story/workflow.md")
        self.assertIn("{implementation_artifacts}/{{story_key}}/{{story_key}}.md", text)
        self.assertIn("Fall back to legacy flat story file", text)
        self.assertIn("Preserve explicit story_path support", text)
        self.assertNotIn("Find matching story file in {implementation_artifacts} using story_key pattern: {{story_key}}.md", text)

    def test_code_review_routes_story_specific_artifacts_to_story_folder(self):
        gather = read_skill("bmad-code-review/steps/step-01-gather-context.md")
        review = read_skill("bmad-code-review/steps/step-02-review.md")
        present = read_skill("bmad-code-review/steps/step-04-present.md")
        self.assertIn("resolve `{spec_file}` by first checking `{implementation_artifacts}/{story_key}/{story_key}.md`", gather)
        self.assertIn("Set `{review_artifact_dir}` to `{implementation_artifacts}/{story_key}` whenever `{story_key}` is known", gather)
        self.assertIn("legacy flat `{implementation_artifacts}/{story_key}.md`, derive `{story_key}`", gather)
        self.assertIn("generate prompt files in `{review_artifact_dir}`", review)
        self.assertIn("`{review_artifact_dir}` MUST be `{implementation_artifacts}/{story_key}`", review)
        self.assertIn("review-{{story_key}}-<reviewer-role>-prompt.md", review)
        self.assertIn("Only `{deferred_work_file}` remains global", present)

    def test_sprint_and_related_workflows_are_folder_aware(self):
        sprint_planning = read_skill("bmad-sprint-planning/workflow.md")
        sprint_template = read_skill("bmad-sprint-planning/sprint-status-template.yaml")
        sprint_status = read_skill("bmad-sprint-status/workflow.md")
        retrospective = read_skill("bmad-retrospective/workflow.md")
        checkpoint = read_skill("bmad-checkpoint-preview/step-01-orientation.md")
        quick_dev = read_skill("bmad-quick-dev/step-01-clarify-and-route.md")

        self.assertIn("{story_location_absolute}/{story-key}/{story-key}.md", sprint_planning)
        self.assertIn("story_location points to the implementation artifact root that contains per-story folders", sprint_template)
        self.assertIn("story_location is the implementation artifact root that contains per-story folders", sprint_status)
        self.assertIn("{implementation_artifacts}/{{story_key}}/{{story_key}}.md", retrospective)
        self.assertIn("resolve the selected story to `{implementation_artifacts}/{story_key}/{story_key}.md` first", checkpoint)
        self.assertIn("folder-based BMAD story files", quick_dev)

    def test_no_active_story_workflow_instructs_flat_new_story_or_root_review_outputs(self):
        disallowed_snippets = {
            "bmad-create-story/workflow.md": [
                "`default_output_file` = `{implementation_artifacts}/{{story_key}}.md`",
            ],
            "bmad-dev-story/workflow.md": [
                "Find matching story file in {implementation_artifacts} using story_key pattern: {{story_key}}.md",
            ],
            "bmad-code-review/steps/step-02-review.md": [
                "generate prompt files in `{implementation_artifacts}` — one per reviewer role",
            ],
        }
        for relative_path, snippets in disallowed_snippets.items():
            text = read_skill(relative_path)
            for snippet in snippets:
                with self.subTest(relative_path=relative_path, snippet=snippet):
                    self.assertNotIn(snippet, text)


if __name__ == "__main__":
    unittest.main()
