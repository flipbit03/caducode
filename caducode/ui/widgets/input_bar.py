"""Fixed bottom input bar widget."""

from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.message import Message
from textual.widgets import Input, Static

from ...utils import format_tokens


class InputBar(Static):
    """Fixed input bar at the bottom of the screen."""

    class Submitted(Message):
        """Posted when user submits input."""

        def __init__(self, value: str) -> None:
            self.value = value
            super().__init__()

    def __init__(self, id: str | None = None) -> None:  # noqa: A002
        super().__init__(id=id)
        self._loading = False

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        with Horizontal(id="input-container"):
            yield Static("USER >> ", id="input-prompt")
            yield Input(placeholder="Type a message...", id="user-input")
            yield Static(format_tokens(0), id="token-counter")

    @on(Input.Submitted)
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        if self._loading:
            return

        value = event.value.strip()
        if not value:
            return

        event.input.clear()
        self.post_message(self.Submitted(value))

    def set_loading(self, loading: bool) -> None:
        """Set loading state (disables input)."""
        self._loading = loading
        input_widget = self.query_one("#user-input", Input)
        input_widget.disabled = loading

        prompt = self.query_one("#input-prompt", Static)
        if loading:
            prompt.update("● Thinking... ")
            prompt.add_class("loading")
        else:
            prompt.update("USER >> ")
            prompt.remove_class("loading")
            input_widget.focus()

    def update_tokens(self, total_tokens: int) -> None:
        """Update the token counter display."""
        counter = self.query_one("#token-counter", Static)
        counter.update(format_tokens(total_tokens))

    def focus_input(self) -> None:
        """Focus the input widget."""
        self.query_one("#user-input", Input).focus()
