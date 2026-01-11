"""Shared utilities for CaduCode."""

from __future__ import annotations

from datetime import datetime

from rich.console import Group
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text


def format_tokens(count: int) -> str:
    """Format token count as 'XXX.Xk'."""
    return f"{count / 1000:05.1f}k"


def get_timestamp(fmt: str = "%H:%M:%S") -> str:
    """Get current timestamp in specified format."""
    return datetime.now().strftime(fmt)


def create_code_panel(
    code: str,
    description: str,
    result: str | None = None,
    show_result: bool = False,
) -> Panel:
    """Create a Rich Panel for displaying code.

    Args:
        code: The Python code to display.
        description: Description of what the code does.
        result: Execution result (optional).
        show_result: Whether to show the result.

    Returns:
        A Rich Panel with syntax-highlighted code.
    """
    # Header with description
    header = Text()
    header.append("● ", style="bold yellow")
    header.append(description, style="italic yellow")

    # Syntax-highlighted code
    syntax = Syntax(
        code,
        "python",
        theme="monokai",
        line_numbers=True,
        word_wrap=True,
    )

    # Build panel content
    parts: list[Text | Syntax] = [header, Text(""), syntax]

    # Add result if enabled and available
    if show_result and result is not None:
        parts.append(Text(""))
        result_text = Text()
        result_text.append("Result: ", style="bold")
        # Truncate long results
        display_result = result if len(result) < 500 else result[:500] + "..."
        result_text.append(display_result, style="green")
        parts.append(result_text)

    return Panel(
        Group(*parts),
        title="[bold cyan]Agent Code[/bold cyan]",
        border_style="cyan",
        padding=(0, 1),
        expand=False,
    )
