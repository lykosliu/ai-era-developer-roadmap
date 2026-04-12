---
name: Demos
description: Hands-on examples and runnable code.
---

## Overview

This demo shows how to create and verify a minimal "Hello World" Python CLI project that runs with `uvx`.
The process is fully step-by-step and uses only files in this directory.

## Prerequisites

- macOS or Linux shell
- Python 3.10+

Run environment check and install `uv` if missing:

```bash
bash setup.sh
```

## Files in This Demo Directory

- `setup.sh`: checks Python and `uv`/`uvx`; installs `uv` when missing.
- `hello_uvx_project/`: a minimal Python package exposing `hello-uvx`.

## Step 1: Create Project Skeleton

```bash
mkdir hello_uvx_project
cd hello_uvx_project
```

## Step 2: Initialize Project with `uv init`

```bash
uv init --name hello-uvx
```

## Step 3: Update `pyproject.toml`

Open `hello_uvx_project/pyproject.toml` and ensure it contains:

```toml
[project]
name = "hello-uvx"
version = "0.1.0"
description = "A minimal uvx hello world tool"
requires-python = ">=3.10"

[project.scripts]
hello-uvx = "hello_uvx.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## Step 4: Create Python Package Files

```bash
mkdir -p src/hello_uvx
```

Create `hello_uvx_project/src/hello_uvx/__init__.py`:

```python
# package marker
```

Create `hello_uvx_project/src/hello_uvx/cli.py`:

```python
import sys


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "World"
    print(f"Hello, {name}!")
```

## Step 5: Verify with `uvx`

```bash
uvx --from . hello-uvx
uvx --from . hello-uvx Trae
```

Expected output:

```text
Hello, World!
Hello, Trae!
```

## Step 6: Verify Executable Resolution Behavior

- `uvx` resolves the package from `--from .`.
- It builds/installs the tool into an isolated runtime environment.
- It finds the console executable `hello-uvx` from `[project.scripts]`.
- It runs the command with your arguments and returns output.

## Common Mistakes

- **Missing entry point:** `hello-uvx` is not defined in `[project.scripts]`.
- **Wrong module path:** `hello_uvx.cli:main` does not match file/function names.
- **Wrong command order:** place `--from` before the executable name.

Correct form:

```bash
uvx --from . hello-uvx [args...]
```
