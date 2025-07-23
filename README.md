# AI-Agent-Practise

A small playground project that combines a **Gemini-powered coding agent** with a **terminal-based calculator app**.  
It demonstrates how to expose a set of secure helper tools (list files, read files, run code, write files) to a Large Language Model and let the model interact with the local file system in a controlled sandbox.

---

## Contents

| Path | Purpose |
|------|---------|
| `main.py` | Command-line entry-point that starts the Gemini agent. |
| `functions/` | Tool implementations + JSON schemas the model can call. |
| `calculator/` | Simple calculator package used as the agent sandbox. |
| `tests.py` <br> `calculator/tests.py` | Unit tests for the agent utilities and calculator logic. |

```
ai-agent-practise/
├── main.py                 # Agent runner
├── functions/              # Tooling exposed to the model
│   ├── get_files_info.py   # list / read / write helpers
│   ├── run_python.py       # safe Python execution helper
│   └── llm_schemas.py      # aggregates the tool schemas
├── calculator/             # Example sandbox project
│   ├── main.py             # CLI wrapper around the calculator
│   └── pkg/
│       ├── calculator.py   # expression evaluator
│       └── render.py       # fancy ASCII renderer
└── pyproject.toml          # Poetry/uv dependency spec
```

---

## Prerequisites

* **Python 3.10+**
* An environment variable `GEMINI_API_KEY` containing a valid Google AI key
* `uv` (or `pip`) for dependency installation

Install dependencies:
```bash
uv pip install -r pyproject.toml   # or: pip install -r requirements.txt
```

---

## Running the agent

```bash
# Syntax
python main.py "<your prompt>" [--verbose]

# Example
python main.py "List files in calculator/pkg and show calculator.py"
```

The agent will:
1. Send your prompt to Gemini together with the available tool schemas.
2. Loop up to 20 turns, executing any requested tool calls (`get_files_info`, `get_file_content`, `run_python_file`, `write_file`).
3. Print the model’s final textual response.

Use `--verbose` to print token statistics and tool return values.

---

## Calculator CLI

Inside the sandbox the file `calculator/main.py` exposes a tiny infix calculator:

```bash
cd calculator
python main.py "3 * 4 + 5"
```

It evaluates the expression and renders a nice ASCII art box with the result.

---

## Running tests

```bash
python -m unittest discover -s . -p "tests.py"
```

---

## Extending the agent

1. Add a new helper in `functions/your_tool.py` and define its `Schema`.
2. Export the schema in `functions/llm_schemas.py` and import the callable in `main.py`’s `functions_mapping`.
3. The next time you run the agent, the model will be able to call your new tool.

Be sure every tool validates the requested path with `check_working_directory` to keep execution inside the sandbox.

---

## Git workflow tips

* First-time push:
  ```bash
  git remote add origin https://github.com/Reve1ation/ai-agent-practise.git
  git branch -M main
  git push -u origin main
  ```
* To unstage a file (e.g. `uv.lock`):
  ```bash
  git restore --staged uv.lock   # or: git reset HEAD -- uv.lock
  ```
* Add patterns you never want in Git to `.gitignore`.

---

## License

MIT – see `LICENSE` (or choose another licence).
