# CaduCode

A minimalist coding agent with a single tool: `run_python`.

## Philosophy

Instead of providing 20+ specialized tools (read_file, write_file, grep, list_dir, run_command, etc.), CaduCode gives the LLM **one tool**: `run_python(code: str, description: str)`.

The LLM becomes a code generator. Any task you request, the agent solves by writing Python code. If Python can do it, the agent can do it.

## Features

- **Single tool simplicity**: One `run_python` tool handles everything
- **Textual TUI**: Full terminal UI with scrollable history, resize support, and syntax highlighting
- **Persistent execution environment**: Variables, imports, and definitions survive between calls
- **Full Python access**: Filesystem, network, subprocess - no restrictions
- **Self-correcting**: Exceptions are returned to the LLM for analysis and retry
- **Token tracking**: Live token counter in the input bar
- **Fallback Rich CLI**: Simple mode for single prompts or piped input

## Requirements

- Python 3.14+
- An Ollama server with a capable model

## Installation

```bash
# Clone and install as a tool
git clone https://github.com/flipbit03/caducode
cd caducode
uv tool install .
```

## Usage

### Interactive TUI (default)

```bash
caducode
```

Starts the full Textual TUI with scrollable message history, fixed input bar, and resize support.

### Single Prompt

```bash
caducode "list all Python files in this directory"
```

Run a single prompt and exit (uses Rich CLI mode).

### Options

```
--api-url TEXT       Ollama API URL (default: http://cadumac:11434)
--model TEXT         Model to use (default: qwen3-coder:30b)
--debug              Enable debug output
--show-code-results  Show code execution results in TUI
--no-tui             Use simple Rich CLI instead of TUI
--no-code            Hide generated code (Rich CLI only)
--no-timestamp       Disable timestamps (Rich CLI only)
```

## How It Works

The agent has access to a single tool that executes Python code:

```python
run_python(code: str, description: str) -> list[Any]
```

Inside the code, one special function is available:

- `_return(data)` - The only way to get data back. Call this with any data you want the LLM to see. Multiple calls accumulate into a list.

## Stack

- **Python**: 3.14
- **Package Manager**: uv
- **Agent Framework**: PydanticAI
- **LLM Provider**: Ollama (via OpenAI-compatible API)
- **TUI**: Textual
- **Rich CLI**: Rich

## License

MIT
