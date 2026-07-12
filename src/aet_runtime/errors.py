class AetError(Exception):
    """Base exception for expected AET runtime failures."""


class ConfigurationError(AetError):
    """Raised when a registry or runtime configuration is invalid."""


class ProviderNotFoundError(AetError):
    """Raised when no enabled provider can satisfy a capability request."""


class ExternalCommandError(AetError):
    """Raised when an external command exits unsuccessfully."""
