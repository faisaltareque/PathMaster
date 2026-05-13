# PathMaster — Codebase Summary

## Overview
**PathMaster** is a lightweight Python utility package for managing `sys.path` and listing directory contents. It solves the common pain point of messy relative path manipulations in projects with nested notebooks or scripts (e.g., importing from a project root when running code from a `notebooks/` subfolder).

## Project Structure
```
PathMaster//Users/faisaltarequeshohan/.zshrc
├── pathmaster/
│   └── __init__.py      # Core library — all public API lives here
├── setup.py              # Package distribution metadata (v0.1.1)
├── .gitignore
└── README.md             # Usage documentation
```

## Core API (3 functions)

| Function | Purpose |
|---|---|
| `pathmaster.add_path(custom_path: str)` | Adds an absolute directory path to `sys.path` (inserted at index 0 if not already present). Validates that the path exists and is a directory. |
| `pathmaster.add_parent(levels: int = 1)` | Walks up `levels` parent directories from the current working directory and adds the resolved parent to `sys.path`. Defaults to the immediate parent (`levels=1`). |
| `pathmaster.list_files(directory: str, absolute_path: bool = False) → List[str]` | Returns a list of filenames (or absolute paths) in the given directory. Returns empty list on invalid input. |

## Technical Details
- **Dependencies:** Zero external dependencies — uses only Python standard library (`sys`, `pathlib`, `typing`).
- **Python version:** Compatible with Python 3.x (uses `pathlib`, type hints).
- **Package name:** `pathmaster`
- **Version:** 0.1.1
- **Author:** Faisal Tareque
- **Install:** `pip install git+https://github.com/faisaltareque/PathMaster.git`

## Key Design Decisions
1. **Insert at index 0** — Paths are prepended (not appended) so they take priority over installed packages.
2. **Idempotent** — `add_path` checks if a path is already in `sys.path` before adding it.
3. **Silent validation** — Missing or invalid paths print a warning instead of raising exceptions.
4. **Single-file library** — All logic lives in `pathmaster/__init__.py`, keeping the package minimal and easy to maintain.

## Use Cases
- Jupyter notebooks in subdirectories importing from a shared `libs/` or `src/` folder
- Bootstrapping project-level imports without `PYTHONPATH` environment variable
- Quick directory listing for exploratory data science workflows
