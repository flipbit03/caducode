"""Custom exceptions for CaduCode."""


class CaduCodeError(Exception):
    """Base exception for CaduCode."""


class ModelNotFoundError(CaduCodeError):
    """Raised when requested model is not available on the server."""

    def __init__(self, model: str, available: list[str]) -> None:
        self.model = model
        self.available = available
        super().__init__(f"Model '{model}' not found. Available: {', '.join(sorted(available))}")


class OllamaConnectionError(CaduCodeError):
    """Raised when connection to Ollama server fails."""

    def __init__(self, url: str, cause: Exception | None = None) -> None:
        self.url = url
        self.cause = cause
        msg = f"Could not connect to Ollama at {url}"
        if cause:
            msg += f": {cause}"
        super().__init__(msg)
