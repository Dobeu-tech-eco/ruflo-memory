#!/usr/bin/env python3
"""Tests for the Codex Cloud instruction-budget guard."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACK = Path(__file__).resolve().parent
CHECKER = PACK / "check_instruction_budget.py"


class InstructionBudgetTests(unittest.TestCase):
    def test_live_pack_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(CHECKER)],
            cwd=str(PACK),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ok:", result.stdout)

    def test_cloud_paste_is_under_2kib(self) -> None:
        size = len(
            (PACK / "cloud-custom-instructions.md").read_text(encoding="utf-8").encode("utf-8")
        )
        self.assertLessEqual(size, 2048)
        self.assertGreater(size, 400)

    def test_readme_cites_official_cloud_docs(self) -> None:
        text = (PACK / "README.md").read_text(encoding="utf-8")
        self.assertIn("https://learn.chatgpt.com/docs/cloud", text)
        self.assertIn("https://learn.chatgpt.com/docs/environments/cloud-environment", text)
        self.assertIn("https://learn.chatgpt.com/docs/agent-configuration/agents-md", text)

    def test_refusals_are_compact_not_a_section(self) -> None:
        text = (PACK / "cloud-custom-instructions.md").read_text(encoding="utf-8")
        self.assertIn("Refuse:", text)
        self.assertNotIn("## 12. Hard refusals", text)
        self.assertNotIn("Hard refusals", text)

    def test_threat_model_is_archive_not_product_app(self) -> None:
        text = (PACK / "security-threat-model.md").read_text(encoding="utf-8")
        self.assertIn("Are there any attack vectors you are most concerned about?", text)
        self.assertIn("Which parts of the application should we focus on?", text)
        self.assertIn("Is there anything else we should know about this repository?", text)
        self.assertIn("session/memory archive", text.lower())
        self.assertIn("not a product app", text.lower())
        lowered = text.lower()
        self.assertIn("secret", lowered)
        self.assertIn("prompt injection", lowered)
        self.assertIn("sessions/", lowered)
        self.assertIn("https://learn.chatgpt.com/docs/security/threat-model", text)
        self.assertNotRegex(text, r"sk-[A-Za-z0-9]{10,}")
        self.assertNotRegex(text, r"ghp_[A-Za-z0-9]+")
        self.assertNotRegex(text, r"xox[baprs]-")
        self.assertNotIn("ck_wNN", text)

    def test_oversized_cloud_paste_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)
            dest.joinpath("cloud-custom-instructions.md").write_text(
                "x" * 3000, encoding="utf-8"
            )
            dest.joinpath("dobeu-tech-eco-system-prompt.md").write_text(
                "fallback " * 200, encoding="utf-8"
            )
            dest.joinpath("README.md").write_text(
                "cloud-custom-instructions.md\nDo not paste\n", encoding="utf-8"
            )
            dest.joinpath("AGENTS.template.md").write_text(
                "cloud-custom-instructions.md\ndo not paste\n", encoding="utf-8"
            )
            dest.joinpath("check_instruction_budget.py").write_text(
                CHECKER.read_text(encoding="utf-8"), encoding="utf-8"
            )
            result = subprocess.run(
                [sys.executable, str(dest / "check_instruction_budget.py")],
                cwd=str(dest),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must stay", result.stderr)


if __name__ == "__main__":
    unittest.main()
