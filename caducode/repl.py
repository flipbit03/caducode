"""Interactive REPL loop."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic_ai import Agent

from .config import MODEL_SETTINGS
from .printer import Printer, console

if TYPE_CHECKING:
    from pydantic_ai.messages import ModelMessage


async def run_prompt(agent: Agent[None, str], prompt: str, printer: Printer) -> None:
    """Run a single prompt and print the result."""
    printer.user(prompt)
    printer.debug_msg("AGENT", "Starting agent.run()...")
    try:
        result = await agent.run(
            prompt,
            model_settings=MODEL_SETTINGS,
        )
        printer.debug_msg("AGENT", "agent.run() completed")
        if result.output and result.output.strip():
            printer.assistant(result.output, usage=result.usage())
    except Exception as e:
        printer.error(str(e))


async def repl(agent: Agent[None, str], printer: Printer) -> None:
    """Run the interactive REPL loop."""
    message_history: list[ModelMessage] = []

    while True:
        try:
            prompt_prefix = f"{printer._prefix()}[bold green]USER >>[/bold green] "
            console.print(prompt_prefix, end="")
            user_input = input()
        except (EOFError, KeyboardInterrupt):
            printer.system("\nGoodbye!")
            break

        if user_input.lower() in ("exit", "quit"):
            printer.system("Goodbye!")
            break

        if not user_input.strip():
            continue

        printer.debug_msg("AGENT", "Starting agent.run()...")
        try:
            result = await agent.run(
                user_input,
                message_history=message_history,
                model_settings=MODEL_SETTINGS,
            )
            printer.debug_msg("AGENT", "agent.run() completed")
            message_history = list(result.all_messages())

            if result.output and result.output.strip():
                printer.assistant(result.output, usage=result.usage())

        except Exception as e:
            printer.error(str(e))
