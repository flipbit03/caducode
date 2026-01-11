"""Command-line interface."""

from __future__ import annotations

import asyncio

import click

from . import __version__
from .agent import create_agent
from .config import DEFAULT_MODEL, DEFAULT_OLLAMA_URL
from .models import validate_model
from .printer import Printer
from .prompts import get_cwd
from .repl import repl, run_prompt


async def main(
    base_url: str,
    model_name: str,
    printer: Printer,
    prompt: str | None = None,
    *,
    debug: bool = False,
) -> None:
    """Main entry point."""
    printer.system(f"[bold blue]CaduCode[/bold blue] v{__version__} - Minimalist coding agent")
    printer.system(f"Model: {model_name} @ {base_url}")
    printer.system(f"Working directory: {get_cwd()}")
    if debug:
        printer.system("[dim cyan]Debug mode enabled[/dim cyan]")

    agent = create_agent(base_url, model_name, printer, debug=debug)

    if prompt:
        await run_prompt(agent, prompt, printer)
    else:
        printer.system('Type "exit" or "quit" to exit.\n')
        await repl(agent, printer)


@click.command()
@click.argument("prompt", required=False)
@click.option(
    "--api-url",
    default=DEFAULT_OLLAMA_URL,
    help=f"Ollama API URL (default: {DEFAULT_OLLAMA_URL})",
)
@click.option(
    "--model",
    default=DEFAULT_MODEL,
    help=f"Model to use (default: {DEFAULT_MODEL})",
)
@click.option("--debug", is_flag=True, help="Enable debug output (tool calls, code, etc.)")
@click.option("--no-timestamp", is_flag=True, help="Disable timestamps on messages")
def cli(
    prompt: str | None, api_url: str, model: str, debug: bool, no_timestamp: bool
) -> None:
    """CaduCode - Minimalist coding agent with a single run_python tool.

    If PROMPT is provided, runs that prompt and exits.
    Otherwise, starts an interactive REPL.
    """
    printer = Printer(show_timestamps=not no_timestamp, debug=debug)

    # Validate model exists on the server
    validate_model(api_url, model)

    asyncio.run(main(api_url, model, printer, prompt, debug=debug))
