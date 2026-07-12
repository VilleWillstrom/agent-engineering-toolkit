import subprocess
import unittest

from aet_runtime.errors import ExternalCommandError
from aet_runtime.github_checks import GitHubChecksMonitor


class GitHubChecksTests(unittest.TestCase):
    def test_builds_watch_command_and_parses_success(self):
        captured = {}

        def runner(command, **kwargs):
            captured["command"] = command
            return subprocess.CompletedProcess(command, 0, '[{"name":"tests","state":"SUCCESS","bucket":"pass","link":"x"}]', "")

        summary = GitHubChecksMonitor(runner).fetch("42", repo="owner/repo", watch=True, interval=15)
        self.assertEqual(["gh", "pr", "checks", "42", "--json", "name,state,bucket,link", "--repo", "owner/repo", "--watch", "--interval", "15"], captured["command"])
        self.assertTrue(summary.all_terminal)
        self.assertTrue(summary.all_successful)

    def test_pending_check_is_not_successful(self):
        def runner(command, **kwargs):
            return subprocess.CompletedProcess(command, 0, '[{"name":"tests","state":"IN_PROGRESS","bucket":"pending"}]', "")

        summary = GitHubChecksMonitor(runner).fetch("42")
        self.assertFalse(summary.all_terminal)
        self.assertFalse(summary.all_successful)

    def test_nonzero_exit_raises(self):
        def runner(command, **kwargs):
            return subprocess.CompletedProcess(command, 1, "", "not authenticated")

        with self.assertRaisesRegex(ExternalCommandError, "not authenticated"):
            GitHubChecksMonitor(runner).fetch("42")

    def test_invalid_json_raises(self):
        def runner(command, **kwargs):
            return subprocess.CompletedProcess(command, 0, "not-json", "")

        with self.assertRaisesRegex(ExternalCommandError, "invalid JSON"):
            GitHubChecksMonitor(runner).fetch("42")
