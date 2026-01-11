"""Configuration constants for CaduCode."""

from pydantic_ai.settings import ModelSettings

DEFAULT_OLLAMA_URL = "http://cadumac:11434"
DEFAULT_MODEL = "qwen3-coder:30b"
MODEL_SETTINGS = ModelSettings(timeout=120)
