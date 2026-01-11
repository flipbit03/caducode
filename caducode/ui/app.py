"""Main Textual application for CaduCode."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from pydantic_ai import Agent, RunContext
from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header

from ..config import (
    DEFAULT_MODEL,
    DEFAULT_OLLAMA_URL,
    MODEL_SETTINGS,
    create_ollama_model,
)
from ..execution import execute_python
from ..printer import Printer
from ..prompts import create_system_prompt, get_cwd
from .widgets import InputBar, MessageView

if TYPE_CHECKING:
    from pydantic_ai.messages import ModelMessage


class CaduCodeApp(App[None]):
    """Textual TUI for CaduCode agent."""

    TITLE = "CaduCode"
    CSS_PATH = Path(__file__).parent / "styles" / "app.tcss"

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("ctrl+l", "clear", "Clear"),
        Binding("escape", "focus_input", "Focus Input", show=False),
    ]

    def __init__(
        self,
        base_url: str = DEFAULT_OLLAMA_URL,
        model_name: str = DEFAULT_MODEL,
        debug_mode: bool = False,
        show_code_results: bool = False,
    ) -> None:
        super().__init__()
        self.base_url = base_url
        self.model_name = model_name
        self.debug_mode = debug_mode
        self.show_code_results = show_code_results
        self.message_history: list[ModelMessage] = []
        self._agent: Agent[None, str] | None = None

    def compose(self) -> ComposeResult:
        """Create the UI layout."""
        yield Header()
        yield MessageView(id="message-view", show_code_results=self.show_code_results)
        yield InputBar(id="input-bar")

    def on_mount(self) -> None:
        """Initialize when app is mounted."""
        self._agent = self._create_agent()

        view = self.query_one("#message-view", MessageView)
        view.add_message("system", f"CaduCode - Model: {self.model_name} @ {self.base_url}")
        view.add_message("system", f"Working directory: {get_cwd()}")
        view.add_message("system", 'Type a message or "exit" to quit.')

        self.query_one("#input-bar", InputBar).focus_input()

    def _create_agent(self) -> Agent[None, str]:
        """Create the PydanticAI agent with TUI integration."""
        model = create_ollama_model(self.base_url, self.model_name)

        agent: Agent[None, str] = Agent(
            model=model,
            system_prompt=create_system_prompt(),
        )

        app = self

        @agent.tool
        def run_python(ctx: RunContext[None], code: str, description: str) -> list[Any]:
            """Execute Python code and display in TUI."""
            del ctx

            # Quiet printer for execution (no output to console)
            printer = Printer(show_code=False, show_timestamps=False, debug=app.debug_mode)
            result = execute_python(code, printer)

            # Display code block in TUI
            result_str = repr(result) if result else "No output"
            app.call_from_thread(app._add_code_block, code, description, result_str)

            return result

        return agent

    def _add_code_block(self, code: str, description: str, result: str) -> None:
        """Add code block to message view (called from thread)."""
        view = self.query_one("#message-view", MessageView)
        view.add_code_block(code, description, result)

    def _update_token_counter(self) -> None:
        """Update the token counter in the input bar."""
        view = self.query_one("#message-view", MessageView)
        input_bar = self.query_one("#input-bar", InputBar)
        input_bar.update_tokens(view.total_tokens)

    @on(InputBar.Submitted)
    def on_input_submitted(self, event: InputBar.Submitted) -> None:
        """Handle user input submission."""
        message = event.value

        if message.lower() in ("exit", "quit"):
            self.exit()
            return

        view = self.query_one("#message-view", MessageView)
        view.add_message("user", message)
        self.run_agent(message)

    @work(exclusive=True)
    async def run_agent(self, message: str) -> None:
        """Run the agent in a background worker."""
        input_bar = self.query_one("#input-bar", InputBar)
        view = self.query_one("#message-view", MessageView)

        try:
            input_bar.set_loading(True)

            if self._agent is None:
                view.add_message("error", "Agent not initialized")
                return

            result = await self._agent.run(
                message,
                message_history=self.message_history,
                model_settings=MODEL_SETTINGS,
            )

            self.message_history = list(result.all_messages())

            usage = result.usage()
            tokens = usage.total_tokens if usage else 0
            if result.output and result.output.strip():
                view.add_message("assistant", result.output, tokens=tokens)

            self._update_token_counter()

        except Exception as e:
            view.add_message("error", str(e))

        finally:
            input_bar.set_loading(False)

    async def action_quit(self) -> None:
        """Quit the application."""
        self.exit()

    async def action_clear(self) -> None:
        """Clear the message view."""
        view = self.query_one("#message-view", MessageView)
        view.clear_history()
        self._update_token_counter()
        view.add_message("system", "Cleared. Ready for input.")

    async def action_focus_input(self) -> None:
        """Focus the input bar."""
        self.query_one("#input-bar", InputBar).focus_input()
