# AI Agent

A command-line AI coding agent built in Python on top of Google's Gemini API. The agent accepts a natural-language prompt, plans a sequence of tool calls, and operates on a sandboxed working directory — listing files, reading source, writing changes, and executing Python scripts to verify its work.

This project was built as a hands-on study of how modern function-calling agents are constructed end-to-end: the tool schema, the model loop, the sandbox boundary, and the prompt scaffolding that ties them together.

## Learning objectives

- Implement tool/function calling against an LLM provider (Google Gemini)
- Design a constrained execution environment with path-traversal protection
- Build a multi-step reasoning loop where the model chooses, sequences, and reacts to tool results
- Structure a Python project with clean separation between tool definitions, schemas, and the agent driver
- Practice writing unit tests for each tool in isolation before wiring them into the agent

## How it works

The agent is given a system prompt describing four capabilities, then handed a user request via the CLI. Gemini decides which tool to call (if any), the corresponding Python function is executed against a fixed working directory, and the result is returned to the model so it can either call another tool or produce a final answer.

```
User prompt ──► Gemini (with tool schemas) ──► function call
                        ▲                            │
                        │                            ▼
                  tool result ◄──── sandboxed execution
```

### Available tools

| Tool | Description |
| --- | --- |
| `get_files_info` | List files in a directory, with size and `is_dir` flags |
| `get_file_content` | Read a file's contents (truncated at 10,000 characters) |
| `write_file` | Create or overwrite a file, creating parent directories as needed |
| `run_python_file` | Execute a Python file with optional CLI args (30-second timeout) |

Every tool resolves paths against an absolute working directory and rejects any request that would escape it.

## Project structure

```
.
├── main.py                  # CLI entry point and Gemini client setup
├── prompts.py               # System prompt defining the agent's capabilities
├── call_function.py         # Aggregates tool schemas for the Gemini client
├── config.py                # Shared constants (file read limits, etc.)
├── functions/               # Tool implementations + schemas
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
├── calculator/              # Sample target directory the agent operates on
└── test_*.py                # Per-tool unit tests
```

The `calculator/` directory is a small, intentionally imperfect Python app the agent can be pointed at — for example, asking it to find a bug, read the source, edit a file, and re-run the tests.

## Setup

Requires Python 3.10+ and a Gemini API key.

```bash
# Clone and enter the project
git clone https://github.com/builder7489/AiAgent.git
cd AiAgent

# Install dependencies (uv recommended; pip works too)
uv sync
# or:
pip install -e .

# Add your API key
echo "GEMINI_API_KEY=your_key_here" > .env
```

## Usage

```bash
# Ask the agent a question
python main.py "List the files in the calculator directory"

# Verbose mode prints token usage
python main.py --verbose "Read calculator/main.py and explain what it does"
```

## Running the tests

Each tool has its own unit test file that exercises it directly, without involving the model:

```bash
python test_get_files_info.py
python test_get_file_content.py
python test_write_file.py
python test_run_python_file.py
```

## Status and roadmap

This is an active project. Current state:

- ✅ All four tool functions implemented with sandbox enforcement
- ✅ Tool schemas registered with the Gemini client
- ✅ Single-turn function-call detection (the agent identifies the tool to call)
- ✅ **Agent loop** — executing the requested tool, feeding results back, and iterating until a final response (with a max-iteration safety cap) is the next milestone
- ✅ **Tool-result routing** — a dispatcher that maps function-call names to the actual Python implementations
- 🚧 **End-to-end demo** — a worked example showing the agent diagnosing and fixing a bug in `calculator/`

## Tech stack

- Python 3.10+
- [`google-genai`](https://pypi.org/project/google-genai/) — Gemini API client
- [`python-dotenv`](https://pypi.org/project/python-dotenv/) — environment variable loading
- [`uv`](https://github.com/astral-sh/uv) — dependency management