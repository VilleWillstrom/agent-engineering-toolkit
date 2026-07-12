import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from aet_runtime.cli import main


class CliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        team = self.root / ".agent-team"
        team.mkdir()
        (team / "providers.json").write_text(json.dumps({"schema_version": 1, "providers": [
            {"id": "codex", "enabled": True, "adapter": "builtin", "capabilities": ["code"], "priority": 100}
        ]}), encoding="utf-8")
        (team / "platforms.json").write_text(json.dumps({"schema_version": 1, "platforms": []}), encoding="utf-8")
        (team / "session-cleanup.json").write_text(json.dumps({"aet_session_root": ".agent-team/runtime/sessions", "retain_last": 1, "max_age_days": 30}), encoding="utf-8")

    def run_cli(self, *args):
        output = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            code = main(["--root", str(self.root), *args])
        return code, output.getvalue(), error.getvalue()

    def test_provider_choose(self):
        code, output, _ = self.run_cli("providers", "choose", "--capability", "code")
        self.assertEqual(0, code)
        self.assertEqual("codex", output.strip())

    def test_doctor_ok(self):
        code, output, _ = self.run_cli("doctor", "--strict")
        self.assertEqual(0, code)
        self.assertEqual("ok", json.loads(output)["status"])

    def test_cleanup_missing_root_is_safe(self):
        code, output, _ = self.run_cli("cleanup")
        self.assertEqual(0, code)
        self.assertEqual([], json.loads(output)["deleted"])

    def test_unknown_capability_returns_error(self):
        code, _, error = self.run_cli("providers", "choose", "--capability", "ui_design")
        self.assertEqual(1, code)
        self.assertIn("no enabled provider supports", error)
