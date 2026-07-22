#!/usr/bin/env python3
"""Focused integration tests for the bounded shared-skill projector."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PROJECTOR = REPOSITORY_ROOT / "scripts" / "project-codex-skills.py"
MANIFEST = json.loads((REPOSITORY_ROOT / "codex" / "skills" / "manifest.json").read_text())


class ProjectCodexSkillsTests(unittest.TestCase):
    def invoke(self, *arguments: str) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
        completed = subprocess.run(
            [sys.executable, str(PROJECTOR), *arguments],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        return completed, json.loads(completed.stdout)

    def run_projector(self, *arguments: str) -> dict[str, object]:
        completed, result = self.invoke(*arguments)
        self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
        return result

    def test_manifest_names_both_owned_installed_projections(self) -> None:
        self.assertEqual(MANIFEST["schemaVersion"], 2)
        self.assertEqual(
            MANIFEST["installedProjections"],
            [
                {"id": "agents", "path": "~/.agents/skills", "role": "primary"},
                {"id": "codex", "path": "~/.codex/skills", "role": "compatibility"},
            ],
        )

    def test_two_target_install_check_and_rollback_preserves_unlisted_data(self) -> None:
        with tempfile.TemporaryDirectory(prefix="project-codex-skills-test-") as temporary:
            root = Path(temporary)
            agents = root / "agents" / "skills"
            codex = root / "codex" / "skills"
            for target in (agents, codex):
                (target / "unlisted-skill").mkdir(parents=True)
                (target / "unlisted-skill" / "keep.txt").write_text("retain me\n")
            (agents / "voice").mkdir()
            (agents / "voice" / "SKILL.md").write_text("prior agents voice\n")
            (codex / "voice").mkdir()
            (codex / "voice" / "SKILL.md").write_text("prior codex voice\n")

            targets = ("--target-root", str(agents), "--target-root", str(codex))
            installed = self.run_projector("--install", *targets)
            self.assertEqual(installed["status"], "passed")
            self.assertEqual(len(installed["projections"]), 2)
            for projection in installed["projections"]:
                self.assertTrue(Path(projection["backup"]).is_dir())
            for target in (agents, codex):
                self.assertEqual((target / "unlisted-skill" / "keep.txt").read_text(), "retain me\n")

            checked = self.run_projector("--check", *targets)
            self.assertEqual(checked["status"], "passed")
            self.assertEqual(len(checked["projections"]), 2)
            backup_id = Path(installed["projections"][0]["backup"]).name

            rolled_back = self.run_projector("--rollback", backup_id, *targets)
            self.assertEqual(rolled_back["status"], "passed")
            self.assertEqual((agents / "voice" / "SKILL.md").read_text(), "prior agents voice\n")
            self.assertEqual((codex / "voice" / "SKILL.md").read_text(), "prior codex voice\n")
            self.assertEqual((agents / "unlisted-skill" / "keep.txt").read_text(), "retain me\n")
            self.assertEqual((codex / "unlisted-skill" / "keep.txt").read_text(), "retain me\n")

    def test_second_target_failure_restores_first_target(self) -> None:
        with tempfile.TemporaryDirectory(prefix="project-codex-skills-recovery-") as temporary:
            root = Path(temporary)
            agents = root / "agents" / "skills"
            codex = root / "codex" / "skills"
            codex.mkdir(parents=True)
            os.symlink(root / "missing-voice", codex / "voice")
            targets = ("--target-root", str(agents), "--target-root", str(codex))

            completed, failed = self.invoke("--install", *targets)
            self.assertNotEqual(completed.returncode, 0)
            self.assertEqual(failed["status"], "failed")
            self.assertIn("restored completed targets", failed["error"])
            self.assertIn("Inspect the named target receipt", failed["recovery"])
            self.assertFalse((agents / "prd-writer").exists())
            self.assertTrue((codex / "voice").is_symlink())


if __name__ == "__main__":
    unittest.main()
