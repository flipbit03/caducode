# CaduCode Development Guide

## Project Overview

CaduCode is a minimalist coding agent with a single `run_python` tool. Instead of providing many specialized tools, the LLM writes Python code to accomplish any task.

## Tech Stack

- **Python**: 3.14+
- **Package Manager**: `uv` (use `uv run`, `uv pip install`, etc.)
- **LLM Framework**: PydanticAI
- **LLM Provider**: Ollama (via OpenAI-compatible API)
- **TUI Framework**: Textual (built on Rich)
- **CLI**: Click
- **Output Formatting**: Rich

## Project Structure

```
caducode/
├── __init__.py      # Package exports, version
├── cli.py           # Click CLI, mode selection (TUI vs Rich CLI)
├── config.py        # Configuration constants (URLs, model settings)
├── agent.py         # PydanticAI agent creation (Rich CLI mode)
├── execution.py     # Python code execution environment
├── models.py        # Ollama model validation
├── printer.py       # Rich console output formatting
├── prompts.py       # System prompt generation
├── repl.py          # Rich CLI REPL loop
├── py.typed         # PEP 561 type marker
└── ui/              # Textual TUI
    ├── __init__.py
    ├── app.py       # Main Textual App
    ├── styles/
    │   └── app.tcss # Textual CSS styles
    └── widgets/
        ├── __init__.py
        ├── input_bar.py    # Bottom input widget
        └── message_view.py # Scrollable message history
```

## Commands

```bash
# Run the TUI (default)
uv run caducode

# Run with Rich CLI instead
uv run caducode --no-tui

# Single prompt (uses Rich CLI)
uv run caducode "your prompt here"

# Run linters
uv run ruff check caducode/
uv run mypy caducode/

# Install in dev mode
uv pip install -e .
```

## Code Style

- **Type hints**: All functions fully typed, mypy strict mode
- **Linting**: ruff with rules E, F, I, N, W, UP, B, C4, SIM
- **Line length**: 100 characters
- **Imports**: Use `from __future__ import annotations` for forward refs

## Architecture Notes

### Two UI Modes

1. **Textual TUI** (default): Full terminal UI with scrollable history, fixed input bar, resize support
2. **Rich CLI** (fallback): Simple REPL with Rich formatting, used for single prompts or `--no-tui`

### Agent Tool

The agent has ONE tool: `run_python(code: str, description: str)`

- Executes Python via `exec()` in persistent globals/locals
- `_return(data)` function injected for LLM to return data
- Exceptions captured and returned for self-correction

### Code Display

- TUI: Code blocks in `MessageView` with syntax highlighting
- Rich CLI: Code panels via `Printer.code()`
- Both use Rich's `Syntax` with monokai theme

## Testing

```bash
# Test TUI imports
uv run python -c "from caducode.ui import CaduCodeApp; print('OK')"

# Test CLI help
uv run caducode --help

# Test Rich CLI mode
uv run caducode --no-tui "what is 2+2?"
```

## Key Classes

- `CaduCodeApp` (`ui/app.py`): Main Textual application, manages agent lifecycle
- `MessageView` (`ui/widgets/message_view.py`): RichLog-based scrollable history
- `InputBar` (`ui/widgets/input_bar.py`): Fixed bottom input with token counter
- `Printer` (`printer.py`): Rich console output for CLI mode
- `create_agent()` (`agent.py`): PydanticAI agent factory for CLI mode

## Configuration

Defaults in `config.py`:
- `DEFAULT_OLLAMA_URL`: Ollama server URL
- `DEFAULT_MODEL`: Default model name
- `MODEL_SETTINGS`: PydanticAI timeout settings

## Git Workflow

- Main development on feature branches
- No Co-Authored-By in commits
- No "Generated with Claude Code" footers
