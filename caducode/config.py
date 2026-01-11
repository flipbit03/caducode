"""Configuration constants for CaduCode."""

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.settings import ModelSettings

DEFAULT_OLLAMA_URL = "http://cadumac:11434"
DEFAULT_MODEL = "qwen3-coder:30b"
MODEL_SETTINGS = ModelSettings(timeout=120)


def create_ollama_model(base_url: str, model_name: str) -> OpenAIChatModel:
    """Create an Ollama-based OpenAI chat model.

    Args:
        base_url: Ollama API base URL.
        model_name: Name of the model to use.

    Returns:
        Configured OpenAIChatModel.
    """
    return OpenAIChatModel(
        model_name=model_name,
        provider=OllamaProvider(base_url=f"{base_url}/v1"),
    )
