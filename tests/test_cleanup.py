import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from aet_runtime.cleanup import SessionCleaner, write_session_marker


class CleanupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        self.now = datetime(2026, 7, 12, tzinfo=timezone.utc)

    def create_session(self, name, days_old):
        path = self.root / name
        write_session_marker(path, provider="claude-code", session_id=name, created_at=self.now - timedelta(days=days_old))
        return path

    def test_dry_run_reports_without_deleting(self):
        old = self.create_session("old", 60)
        result = SessionCleaner(self.root, retain_last=0, max_age_days=30).clean(dry_run=True, now=self.now)
        self.assertIn(old, result.deleted)
        self.assertTrue(old.exists())

    def test_apply_deletes_only_marked_old_sessions(self):
        old = self.create_session("old", 60)
        unmarked = self.root / "not-owned"
        unmarked.mkdir()
        result = SessionCleaner(self.root, retain_last=0, max_age_days=30).clean(dry_run=False, now=self.now)
        self.assertFalse(old.exists())
        self.assertTrue(unmarked.exists())
        self.assertIn(unmarked, result.skipped)

    def test_retain_last_wins_over_age(self):
        newest = self.create_session("newest", 40)
        older = self.create_session("older", 50)
        result = SessionCleaner(self.root, retain_last=1, max_age_days=30).clean(dry_run=False, now=self.now)
        self.assertTrue(newest.exists())
        self.assertFalse(older.exists())
        self.assertIn(newest, result.retained)

    def test_invalid_marker_is_skipped(self):
        invalid = self.root / "invalid"
        invalid.mkdir()
        (invalid / "aet-session.json").write_text("{}", encoding="utf-8")
        result = SessionCleaner(self.root, retain_last=0, max_age_days=0).clean(now=self.now)
        self.assertIn(invalid, result.skipped)
