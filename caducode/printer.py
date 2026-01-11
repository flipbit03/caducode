"""Output formatting with Rich console."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from rich.console import Console, Group
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

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
        self._live: Live | None = None

    def _format_tokens(self, n: int) -> str:
        """Format token count as fixed-width 5 chars (e.g., '001.2k')."""
        k = n / 1000
        return f"{k:05.1f}k"

    def _prefix(self) -> str:
        """Return the prefix with timestamp and token count."""
        parts = []
        if self.show_timestamps:
            parts.append(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]")
        parts.append(f"[{self._format_tokens(self.total_tokens)}]")
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
        """Display generated code with syntax highlighting.

        This is first-class display for the agent's only tool.
        Shows a panel with the code description and syntax-highlighted Python.
        """
        if not self.show_code:
            return

        # Create header with action description
        header = Text()
        header.append("● ", style="bold yellow")
        header.append(description, style="italic yellow")

        # Syntax-highlighted Python code
        syntax = Syntax(
            code,
            "python",
            theme="monokai",
            line_numbers=True,
            word_wrap=True,
        )

        # Combine into a panel
        panel = Panel(
            Group(header, Text(""), syntax),
            title="[bold cyan]Agent Code[/bold cyan]",
            border_style="cyan",
            padding=(0, 1),
        )

        # Use Live for proper terminal resize handling
        with Live(panel, console=console, refresh_per_second=4, transient=False):
            pass  # Panel is displayed and properly handles terminal resize

    def debug_msg(self, label: str, message: str) -> None:
        """Print debug message (only if debug mode is enabled)."""
        if self.debug:
            console.print(f"{self._prefix()}[dim cyan][DEBUG {label}][/dim cyan] {message}")

    def debug_code(self, code: str) -> None:
        """Print debug code block (only if debug mode is enabled)."""
        if self.debug:
            console.print(f"{self._prefix()}[dim cyan][DEBUG CODE][/dim cyan]")
            console.print(f"[dim]{code}[/dim]")

    def action(self, description: str) -> None:
        """Print what the agent is currently doing."""
        console.print(f"{self._prefix()}[italic cyan]● {description}[/italic cyan]")
