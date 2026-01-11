"""Scrollable message history widget."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from rich.markdown import Markdown
from rich.text import Text
from textual.events import Resize
from textual.widgets import RichLog

from ...utils import create_code_panel, get_timestamp


@dataclass
class StoredMessage:
    """A stored message for re-rendering on resize."""

    kind: Literal["message", "code"]
    role: Literal["user", "assistant", "system", "error"] | None = None
    content: str = ""
    tokens: int = 0
    timestamp: str = ""
    # For code blocks
    code: str = ""
    description: str = ""
    result: str | None = None


class MessageView(RichLog):
    """Scrollable view of conversation messages with Rich rendering."""

    def __init__(
        self,
        id: str | None = None,  # noqa: A002
        show_code_results: bool = False,
    ) -> None:
        super().__init__(highlight=True, markup=True, wrap=True, id=id)
        self.total_tokens = 0
        self.show_code_results = show_code_results
        self._messages: list[StoredMessage] = []

    def _render_message(self, msg: StoredMessage) -> None:
        """Render a single stored message."""
        if msg.kind == "message":
            if msg.role == "user":
                header = Text()
                header.append(f"[{msg.timestamp}] ", style="dim")
                header.append("USER >> ", style="bold green")
                header.append(msg.content)
                self.write(header)

            elif msg.role == "assistant":
                header = Text()
                header.append(f"[{msg.timestamp}] ", style="dim")
                header.append("Assistant:", style="bold magenta")
                self.write(header)
                self.write(Markdown(msg.content))
                self.write("")

            elif msg.role == "system":
                text = Text()
                text.append(f"[{msg.timestamp}] ", style="dim")
                text.append(msg.content, style="dim cyan")
                self.write(text)

            elif msg.role == "error":
                text = Text()
                text.append(f"[{msg.timestamp}] ", style="dim")
                text.append("Error: ", style="bold red")
                text.append(msg.content, style="red")
                self.write(text)

        elif msg.kind == "code":
            panel = create_code_panel(
                msg.code,
                msg.description,
                result=msg.result,
                show_result=self.show_code_results,
            )
            self.write(panel)

    def _rerender_all(self) -> None:
        """Clear and re-render all messages."""
        self.clear()
        for msg in self._messages:
            self._render_message(msg)

    def on_resize(self, event: Resize) -> None:
        """Re-render all messages when the widget is resized."""
        self._rerender_all()

    def add_message(
        self,
        role: Literal["user", "assistant", "system", "error"],
        content: str,
        tokens: int = 0,
    ) -> None:
        """Add a message to the view."""
        self.total_tokens += tokens
        ts = get_timestamp()

        msg = StoredMessage(
            kind="message",
            role=role,
            content=content,
            tokens=tokens,
            timestamp=ts,
        )
        self._messages.append(msg)
        self._render_message(msg)

    def add_code_block(
        self,
        code: str,
        description: str,
        result: str | None = None,
    ) -> None:
        """Add a code execution block to the view."""
        msg = StoredMessage(
            kind="code",
            code=code,
            description=description,
            result=result,
        )
        self._messages.append(msg)
        self._render_message(msg)

    def clear_history(self) -> None:
        """Clear both the view and message history."""
        self._messages.clear()
        self.total_tokens = 0
        self.clear()
