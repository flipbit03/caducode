"""Ollama model validation and fetching."""

from __future__ import annotations

import sys

import httpx

from .printer import console


def get_available_models(base_url: str) -> list[str]:
    """Fetch available models from Ollama API."""
    try:
        response = httpx.get(f"{base_url}/api/tags", timeout=10)
        response.raise_for_status()
        data = response.json()
        return [model["name"] for model in data.get("models", [])]
    except httpx.RequestError as e:
        console.print(f"[bold red]Error:[/bold red] Could not connect to Ollama at {base_url}")
        console.print(f"[dim]{e}[/dim]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] Failed to fetch models: {e}")
        sys.exit(1)


def validate_model(base_url: str, model: str) -> None:
    """Validate that the requested model exists on the Ollama server."""
    available = get_available_models(base_url)
    if model not in available:
        console.print(f"[bold red]Error:[/bold red] Model '{model}' not found on {base_url}")
        console.print("\n[bold]Available models:[/bold]")
        for m in sorted(available):
            console.print(f"  • {m}")
        sys.exit(1)
