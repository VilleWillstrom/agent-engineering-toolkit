import json
import tempfile
import unittest
from pathlib import Path

from aet_runtime.errors import ConfigurationError, ProviderNotFoundError
from aet_runtime.registry import ExtensionRegistry


class RegistryTests(unittest.TestCase):
    def write_registry(self, data):
        temp = tempfile.TemporaryDirectory()
        path = Path(temp.name) / "registry.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        self.addCleanup(temp.cleanup)
        return path

    def test_choose_prefers_priority_then_cost(self):
        path = self.write_registry({"schema_version": 1, "providers": [
            {"id": "cheap", "enabled": True, "adapter": "http", "capabilities": ["code"], "priority": 10, "cost_weight": 0.2},
            {"id": "strong", "enabled": True, "adapter": "http", "capabilities": ["code"], "priority": 20, "cost_weight": 2.0}
        ]})
        registry = ExtensionRegistry.load(path, kind="provider", list_key="providers")
        self.assertEqual("strong", registry.choose(["code"]).id)

    def test_prefer_local_adds_local_bonus(self):
        path = self.write_registry({"schema_version": 1, "providers": [
            {"id": "cloud", "enabled": True, "adapter": "http", "capabilities": ["review"], "priority": 100, "cost_weight": 1},
            {"id": "local", "enabled": True, "adapter": "ollama", "capabilities": ["review"], "priority": 1, "cost_weight": 1, "local": True}
        ]})
        registry = ExtensionRegistry.load(path, kind="provider", list_key="providers")
        self.assertEqual("local", registry.choose(["review"], prefer_local=True).id)

    def test_disabled_provider_is_not_selected(self):
        path = self.write_registry({"schema_version": 1, "providers": [
            {"id": "off", "enabled": False, "adapter": "http", "capabilities": ["code"]}
        ]})
        registry = ExtensionRegistry.load(path, kind="provider", list_key="providers")
        with self.assertRaises(ProviderNotFoundError):
            registry.choose(["code"])

    def test_duplicate_id_is_rejected(self):
        path = self.write_registry({"schema_version": 1, "providers": [
            {"id": "same", "enabled": True, "adapter": "http", "capabilities": []},
            {"id": "same", "enabled": True, "adapter": "http", "capabilities": []}
        ]})
        with self.assertRaises(ConfigurationError):
            ExtensionRegistry.load(path, kind="provider", list_key="providers")

    def test_invalid_adapter_is_rejected(self):
        path = self.write_registry({"schema_version": 1, "providers": [
            {"id": "bad", "enabled": True, "adapter": "magic", "capabilities": []}
        ]})
        with self.assertRaises(ConfigurationError):
            ExtensionRegistry.load(path, kind="provider", list_key="providers")
