"""Output formatting with Rich console."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.console import Console
from rich.markdown import Markdown

from .utils import create_code_panel, format_tokens, get_timestamp

if TYPE_CHECKING:
    from pydantic_ai.usage import RunUsage

console = Console()


class Printer:
    """Centralized printer with timestamps, code display, and debug control."""

    def __init__(
        self,
        *,
        show_timestamps: bool = True,
        show_code: bool = True,
        debug: bool = False,
    ) -> None:
        self.show_timestamps = show_timestamps
        self.show_code = show_code
        self.debug = debug
        self.total_tokens = 0

    def _prefix(self) -> str:
        """Return the prefix with timestamp and token count."""
        parts = []
        if self.show_timestamps:
            parts.append(f"[{get_timestamp('%d/%m/%Y %H:%M:%S')}]")
        parts.append(f"[{format_tokens(self.total_tokens)}]")
        return f"[dim]{' '.join(parts)}[/dim] "

    def add_usage(self, usage: RunUsage) -> None:
        """Add usage from a turn to the running total."""
        self.total_tokens += usage.total_tokens

    def user(self, message: str) -> None:
        """Print user message."""
        console.print(f"{self._prefix()}[bold green]USER >>[/bold green] {message}")

    def assistant(self, message: str, usage: RunUsage | None = None) -> None:
        """Print assistant message with optional usage update."""
        if usage:
            self.add_usage(usage)
        console.print("")
        console.print(f"{self._prefix()}[bold magenta]Assistant:[/bold magenta]")
        console.print("")
        console.print(Markdown(message))
        console.print("\n")

    def system(self, message: str) -> None:
        """Print system message (banner, info, etc.)."""
        console.print(f"{self._prefix()}{message}")

    def error(self, message: str) -> None:
        """Print error message."""
        console.print(f"{self._prefix()}[bold red]Error:[/bold red] {message}")

    def code(self, code: str, description: str) -> None:
        """Display generated code with syntax highlighting."""
        if not self.show_code:
            return
        panel = create_code_panel(code, description)
        console.print(panel)

    def debug_msg(self, label: str, message: str) -> None:
        """Print debug message (only if debug mode is enabled)."""
        if self.debug:
            console.print(f"{self._prefix()}[dim cyan][DEBUG {label}][/dim cyan] {message}")
