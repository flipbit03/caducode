"""Python code execution environment."""

from __future__ import annotations

import traceback
from typing import Any

from .printer import Printer

# Persistent execution environment for run_python
exec_globals: dict[str, Any] = {}
exec_locals: dict[str, Any] = {}


def execute_python(code: str, printer: Printer) -> list[Any]:
    """Execute Python code in the persistent environment.

    Args:
        code: Python code to execute.
        printer: Printer instance for output.

    Returns:
        List of values passed to _return(), or error traceback if exception raised.
    """
    results: list[Any] = []

    def _return(data: Any) -> None:
        """Return data to the LLM. Accumulates into results list."""
        printer.debug_msg("_return", repr(data))
        results.append(data)

    # Inject built-in function into execution scope
    exec_globals["_return"] = _return

    try:
        exec(code, exec_globals, exec_locals)  # noqa: S102
        result = results if results else ["Code block didn't _return() any data"]
        printer.debug_msg("TOOL RESULT", repr(result))
        return result
    except Exception:
        tb = traceback.format_exc()
        printer.debug_msg("TOOL ERROR", tb)
        return [f"Exception raised:\n{tb}"]
