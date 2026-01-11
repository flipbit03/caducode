# CaduCode

A minimalist coding agent with a single tool: `run_python`.

## Philosophy

Instead of providing 20+ specialized tools (read_file, write_file, grep, list_dir, run_command, etc.), CaduCode gives the LLM **one tool**: `run_python(code: str, description: str)`.

The LLM becomes a code generator. Any task you request, the agent solves by writing Python code. If Python can do it, the agent can do it.

## Features

- **Single tool simplicity**: One `run_python` tool handles everything
- **Persistent execution environment**: Variables, imports, and definitions survive between calls
- **Full Python access**: Filesystem, network, subprocess - no restrictions
- **Self-correcting**: Exceptions are returned to the LLM for analysis and retry
- **Token tracking**: Displays cumulative token usage across the session
- **Rich terminal UI**: Colored, formatted output with timestamps

## Requirements

- Python 3.14+
- An Ollama server with a capable model

## Installation

```bash
# Clone and install
git clone https://github.com/cadu/caducode
cd caducode
uv pip install -e .
```

## Usage

### Interactive REPL

```bash
caducode
```

This starts an interactive session where you can chat with the agent.

### Single Prompt

```bash
caducode "list all Python files in this directory"
```

Run a single prompt and exit.

### Options

```
--api-url TEXT     Ollama API URL (default: http://cadumac:11434)
--model TEXT       Model to use (default: qwen3-coder:30b)
--debug            Enable debug output (tool calls, code, etc.)
--no-timestamp     Disable timestamps on messages
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
- **Framework**: PydanticAI
- **LLM Provider**: Ollama (via OpenAI-compatible API)
- **UI**: Rich (colored terminal output)

## License

MIT
