"""Ollama model validation and fetching."""

from __future__ import annotations

import httpx

from .exceptions import ModelNotFoundError, OllamaConnectionError


def get_available_models(base_url: str) -> list[str]:
    """Fetch available models from Ollama API.

    Args:
        base_url: Ollama API base URL.

    Returns:
        List of available model names.

    Raises:
        OllamaConnectionError: If connection to Ollama fails.
    """
    try:
        response = httpx.get(f"{base_url}/api/tags", timeout=10)
        response.raise_for_status()
        data = response.json()
        return [model["name"] for model in data.get("models", [])]
    except httpx.RequestError as e:
        raise OllamaConnectionError(base_url, e) from e
    except Exception as e:
        raise OllamaConnectionError(base_url, e) from e


def validate_model(base_url: str, model: str) -> None:
    """Validate that the requested model exists on the Ollama server.

    Args:
        base_url: Ollama API base URL.
        model: Model name to validate.

    Raises:
        OllamaConnectionError: If connection to Ollama fails.
        ModelNotFoundError: If model is not available.
    """
    available = get_available_models(base_url)
    if model not in available:
        raise ModelNotFoundError(model, available)
