import json
import tempfile
import unittest
from pathlib import Path

from aet_runtime.errors import ConfigurationError
from aet_runtime.registry_edit import add_registry_entry


class RegistryEditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.registry = self.root / "providers.json"
        self.registry.write_text(json.dumps({"schema_version": 1, "providers": []}), encoding="utf-8")

    def definition(self, entry_id="new"):
        path = self.root / f"{entry_id}.json"
        path.write_text(json.dumps({
            "id": entry_id, "enabled": False, "adapter": "http", "capabilities": ["code"]
        }), encoding="utf-8")
        return path

    def test_adds_valid_definition_atomically(self):
        entry_id = add_registry_entry(self.registry, list_key="providers", definition_path=self.definition())
        self.assertEqual("new", entry_id)
        self.assertEqual("new", json.loads(self.registry.read_text())["providers"][0]["id"])

    def test_rejects_duplicate(self):
        definition = self.definition()
        add_registry_entry(self.registry, list_key="providers", definition_path=definition)
        with self.assertRaisesRegex(ConfigurationError, "duplicate"):
            add_registry_entry(self.registry, list_key="providers", definition_path=definition)
