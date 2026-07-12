from __future__ import annotations

import json
import os
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable

from .errors import ConfigurationError, ExternalCommandError
from .models import RegistryEntry


@dataclass(frozen=True, slots=True)
class ProviderExecutionResult:
    provider_id: str
    text: str
    raw: dict[str, Any] | str
    usage: dict[str, Any] | None = None


def _render(value: Any, prompt: str) -> Any:
    if isinstance(value, str):
        return value.replace("{prompt}", prompt)
    if isinstance(value, list):
        return [_render(item, prompt) for item in value]
    if isinstance(value, dict):
        return {key: _render(item, prompt) for key, item in value.items()}
    return value


def _extract_path(payload: Any, path: list[Any]) -> Any:
    current = payload
    for part in path:
        if isinstance(part, int):
            if not isinstance(current, list):
                raise ConfigurationError(f"response path expected list before index {part}")
            current = current[part]
        else:
            if not isinstance(current, dict) or part not in current:
                raise ConfigurationError(f"response path key not found: {part}")
            current = current[part]
    return current


class CommandProviderAdapter:
    def __init__(self, runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run) -> None:
        self._runner = runner

    def execute(self, provider: RegistryEntry, prompt: str) -> ProviderExecutionResult:
        command = provider.config.get("command")
        if not isinstance(command, list) or not command or not all(isinstance(item, str) for item in command):
            raise ConfigurationError(f"{provider.id}: command must be a non-empty string list")
        rendered = [item.replace("{prompt}", prompt) for item in command]
        result = self._runner(rendered, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            raise ExternalCommandError((result.stderr or result.stdout or f"{provider.id} failed").strip())
        stdout = result.stdout.strip()
        if provider.config.get("output_format") == "text":
            return ProviderExecutionResult(provider.id, stdout, stdout)
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError as exc:
            raise ExternalCommandError(f"{provider.id} returned invalid JSON") from exc
        path = provider.config.get("response_text_path", ["result"])
        text = _extract_path(payload, path)
        if not isinstance(text, str):
            raise ConfigurationError(f"{provider.id}: extracted response is not text")
        usage = payload.get("usage") if isinstance(payload, dict) else None
        return ProviderExecutionResult(provider.id, text, payload, usage if isinstance(usage, dict) else None)


class HttpJsonProviderAdapter:
    def __init__(self, opener: Callable[..., Any] = urllib.request.urlopen) -> None:
        self._opener = opener

    def execute(self, provider: RegistryEntry, prompt: str) -> ProviderExecutionResult:
        endpoint = provider.config.get("endpoint")
        if not isinstance(endpoint, str) or not endpoint:
            raise ConfigurationError(f"{provider.id}: endpoint is required")
        body_template = provider.config.get("request_body")
        if not isinstance(body_template, dict):
            raise ConfigurationError(f"{provider.id}: request_body is required")
        headers = {"Content-Type": "application/json"}
        static_headers = provider.config.get("headers", {})
        if not isinstance(static_headers, dict):
            raise ConfigurationError(f"{provider.id}: headers must be an object")
        headers.update({str(key): str(value) for key, value in static_headers.items()})
        headers_env = provider.config.get("headers_env", {})
        if not isinstance(headers_env, dict):
            raise ConfigurationError(f"{provider.id}: headers_env must be an object")
        for header, env_name in headers_env.items():
            value = os.environ.get(str(env_name))
            if not value:
                raise ConfigurationError(f"{provider.id}: missing environment variable {env_name}")
            headers[str(header)] = value
        body = json.dumps(_render(body_template, prompt)).encode("utf-8")
        request = urllib.request.Request(endpoint, data=body, headers=headers, method="POST")
        try:
            with self._opener(request, timeout=float(provider.config.get("timeout_seconds", 120))) as response:
                raw = response.read().decode("utf-8")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise ExternalCommandError(f"{provider.id} HTTP request failed: {exc}") from exc
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ExternalCommandError(f"{provider.id} returned invalid JSON") from exc
        path = provider.config.get("response_text_path")
        if not isinstance(path, list) or not path:
            raise ConfigurationError(f"{provider.id}: response_text_path is required")
        text = _extract_path(payload, path)
        if not isinstance(text, str):
            raise ConfigurationError(f"{provider.id}: extracted response is not text")
        usage_path = provider.config.get("usage_path")
        usage = _extract_path(payload, usage_path) if isinstance(usage_path, list) and usage_path else None
        return ProviderExecutionResult(provider.id, text, payload, usage if isinstance(usage, dict) else None)


class ProviderExecutor:
    def __init__(self, command_adapter: CommandProviderAdapter | None = None, http_adapter: HttpJsonProviderAdapter | None = None) -> None:
        self.command_adapter = command_adapter or CommandProviderAdapter()
        self.http_adapter = http_adapter or HttpJsonProviderAdapter()

    def execute(self, provider: RegistryEntry, prompt: str) -> ProviderExecutionResult:
        if not provider.enabled:
            raise ConfigurationError(f"provider is disabled: {provider.id}")
        if provider.adapter in {"command", "cli"}:
            return self.command_adapter.execute(provider, prompt)
        if provider.adapter in {"http", "ollama", "api"}:
            return self.http_adapter.execute(provider, prompt)
        raise ConfigurationError(f"provider adapter is not directly executable: {provider.adapter}")
