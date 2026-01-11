"""Agent creation and configuration."""

from __future__ import annotations

from typing import Any

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

from .execution import execute_python
from .printer import Printer
from .prompts import create_system_prompt


def create_agent(
    base_url: str, model_name: str, printer: Printer, *, debug: bool = False
) -> Agent[None, str]:
    """Create and configure the PydanticAI agent.

    Args:
        base_url: Ollama API base URL.
        model_name: Name of the model to use.
        printer: Printer instance for output.
        debug: Enable debug output.

    Returns:
        Configured PydanticAI agent.
    """
    del debug  # Reserved for future use

    model = OpenAIChatModel(
        model_name=model_name,
        provider=OllamaProvider(base_url=f"{base_url}/v1"),
    )

    agent: Agent[None, str] = Agent(
        model=model,
        system_prompt=create_system_prompt(),
    )

    @agent.tool
    def run_python(ctx: RunContext[None], code: str, description: str) -> list[Any]:
        """Execute arbitrary Python code in a persistent environment.

        Args:
            ctx: PydanticAI run context (required).
            code: Python code to execute.
            description: Short description of what this code does (shown to user).

        Returns:
            List of values passed to _return(), or error traceback if exception raised.
        """
        del ctx  # Unused but required by PydanticAI

        # First-class code display (can be disabled with --no-code)
        printer.code(code, description)
        printer.debug_msg("TOOL CALL", "run_python")

        return execute_python(code, printer)

    return agent
