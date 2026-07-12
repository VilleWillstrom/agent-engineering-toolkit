import json
import os
import subprocess
import unittest
from unittest.mock import patch

from aet_runtime.adapters import CommandProviderAdapter, HttpJsonProviderAdapter, ProviderExecutor
from aet_runtime.errors import ConfigurationError, ExternalCommandError
from aet_runtime.models import RegistryEntry


class FakeResponse:
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.payload


class AdapterTests(unittest.TestCase):
    def test_command_adapter_substitutes_prompt_and_parses_result(self):
        captured = {}

        def runner(command, **kwargs):
            captured["command"] = command
            return subprocess.CompletedProcess(command, 0, json.dumps({"result": "done", "usage": {"input_tokens": 3}}), "")

        provider = RegistryEntry.from_dict({
            "id": "worker", "enabled": True, "adapter": "command", "capabilities": ["code"],
            "command": ["worker", "--prompt", "{prompt}"], "response_text_path": ["result"]
        })
        result = CommandProviderAdapter(runner).execute(provider, "hello")
        self.assertEqual(["worker", "--prompt", "hello"], captured["command"])
        self.assertEqual("done", result.text)
        self.assertEqual(3, result.usage["input_tokens"])

    def test_command_adapter_rejects_failure(self):
        def runner(command, **kwargs):
            return subprocess.CompletedProcess(command, 2, "", "quota exceeded")

        provider = RegistryEntry.from_dict({
            "id": "worker", "enabled": True, "adapter": "command", "capabilities": [], "command": ["worker", "{prompt}"]
        })
        with self.assertRaisesRegex(ExternalCommandError, "quota exceeded"):
            CommandProviderAdapter(runner).execute(provider, "hello")

    def test_http_adapter_renders_nested_prompt_and_extracts_path(self):
        captured = {}

        def opener(request, timeout):
            captured["body"] = json.loads(request.data)
            captured["headers"] = dict(request.header_items())
            return FakeResponse({"steps": [{"content": [{"text": "answer"}]}]})

        provider = RegistryEntry.from_dict({
            "id": "gemini", "enabled": True, "adapter": "http", "capabilities": ["code"],
            "endpoint": "https://example.invalid/interactions",
            "headers_env": {"x-goog-api-key": "TEST_API_KEY"},
            "request_body": {"model": "model", "store": False, "input": "{prompt}"},
            "response_text_path": ["steps", -1, "content", 0, "text"]
        })
        with patch.dict(os.environ, {"TEST_API_KEY": "secret"}):
            result = HttpJsonProviderAdapter(opener).execute(provider, "hello")
        self.assertEqual("hello", captured["body"]["input"])
        self.assertEqual("answer", result.text)
        self.assertEqual("secret", captured["headers"]["X-goog-api-key"])

    def test_http_adapter_requires_configured_secret(self):
        provider = RegistryEntry.from_dict({
            "id": "remote", "enabled": True, "adapter": "http", "capabilities": [],
            "endpoint": "https://example.invalid", "headers_env": {"Authorization": "MISSING_KEY"},
            "request_body": {"input": "{prompt}"}, "response_text_path": ["text"]
        })
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ConfigurationError, "MISSING_KEY"):
                HttpJsonProviderAdapter(lambda *args, **kwargs: None).execute(provider, "hello")

    def test_executor_rejects_disabled_provider(self):
        provider = RegistryEntry.from_dict({"id": "off", "enabled": False, "adapter": "http", "capabilities": []})
        with self.assertRaisesRegex(ConfigurationError, "disabled"):
            ProviderExecutor().execute(provider, "hello")
