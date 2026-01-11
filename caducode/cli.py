"""Command-line interface."""

from __future__ import annotations

import asyncio
import sys

import click

from . import __version__
from .agent import create_agent
from .config import DEFAULT_MODEL, DEFAULT_OLLAMA_URL
from .exceptions import ModelNotFoundError, OllamaConnectionError
from .models import validate_model
from .printer import Printer, console
from .prompts import get_cwd
from .repl import repl, run_prompt


async def main_repl(
    base_url: str,
    model_name: str,
    printer: Printer,
    prompt: str | None = None,
) -> None:
    """Main entry point for Rich CLI mode."""
    printer.system(f"[bold blue]CaduCode[/bold blue] v{__version__} - Minimalist coding agent")
    printer.system(f"Model: {model_name} @ {base_url}")
    printer.system(f"Working directory: {get_cwd()}")
    if printer.debug:
        printer.system("[dim cyan]Debug mode enabled[/dim cyan]")

    agent = create_agent(base_url, model_name, printer)

    if prompt:
        await run_prompt(agent, prompt, printer)
    else:
        printer.system('Type "exit" or "quit" to exit.\n')
        await repl(agent, printer)


def run_tui(
    base_url: str,
    model_name: str,
    *,
    debug: bool = False,
    show_code_results: bool = False,
) -> None:
    """Run the Textual TUI."""
    from .ui import CaduCodeApp

    app = CaduCodeApp(
        base_url=base_url,
        model_name=model_name,
        debug_mode=debug,
        show_code_results=show_code_results,
    )
    app.run()


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
@click.option("--debug", is_flag=True, help="Enable debug output")
@click.option("--show-code-results", is_flag=True, help="Show code execution results in TUI")
@click.option("--no-tui", is_flag=True, help="Use simple Rich CLI instead of TUI")
@click.option("--no-code", is_flag=True, help="Hide generated code (Rich CLI only)")
@click.option("--no-timestamp", is_flag=True, help="Disable timestamps (Rich CLI only)")
def cli(
    prompt: str | None,
    api_url: str,
    model: str,
    debug: bool,
    show_code_results: bool,
    no_tui: bool,
    no_code: bool,
    no_timestamp: bool,
) -> None:
    """CaduCode - Minimalist coding agent with a single run_python tool.

    If PROMPT is provided, runs that prompt and exits (uses Rich CLI mode).
    Otherwise, starts the interactive TUI (or Rich CLI with --no-tui).
    """
    # Validate model exists on the server
    try:
        validate_model(api_url, model)
    except OllamaConnectionError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)
    except ModelNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] Model '{e.model}' not found on {api_url}")
        console.print("\n[bold]Available models:[/bold]")
        for m in sorted(e.available):
            console.print(f"  • {m}")
        sys.exit(1)

    # Determine mode:
    # - Single prompt: always use Rich CLI (no TUI needed)
    # - Interactive + TTY + no --no-tui: use TUI
    # - Otherwise: use Rich CLI
    use_tui = (
        prompt is None
        and not no_tui
        and sys.stdin.isatty()
        and sys.stdout.isatty()
    )

    if use_tui:
        run_tui(api_url, model, debug=debug, show_code_results=show_code_results)
    else:
        printer = Printer(
            show_timestamps=not no_timestamp,
            show_code=not no_code,
            debug=debug,
        )
        asyncio.run(main_repl(api_url, model, printer, prompt))
