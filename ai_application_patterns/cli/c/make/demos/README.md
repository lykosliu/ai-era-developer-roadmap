---
name: Demos
description: Hands-on examples and runnable code.
---

## Overview
This directory contains runnable GNU Make demos for C CLI projects.
The demos emphasize Make as a unified command entrypoint and task runner, with incremental rebuild as a built-in bonus.

## Prerequisites
- `make` (GNU Make is recommended)
- `cc` or `gcc`/`clang`
- macOS or Linux shell

Check and run everything:

```bash
bash setup.sh
```

## Demo Structure
- `demo_single_file/`: smallest command contract (`help/build/run/verify/clean`).
- `demo_incremental_rebuild/`: dependency-aware build + same command contract.
- `demo_task_entrypoint/`: AI workflow contract (`prepare/train/eval/report/pipeline/verify`).

## Demo 1: Single File Command Entry

```bash
cd demo_single_file
make help
make run
make verify
make clean
```

Expected behavior:
- `make run` compiles and runs the CLI app via one entrypoint;
- developers do not need to remember compile/link/run details.

## Demo 2: Build/Run as Standard Targets

```bash
cd demo_incremental_rebuild
make help
make run
sleep 1 && touch math_utils.h
make build
make verify
```

Expected behavior:
- `make run` executes compile + run as one command;
- after touching `math_utils.h`, `make build` rebuilds only affected objects then relinks.

## Demo 3: AI Workflow Entry Targets

```bash
cd demo_task_entrypoint
make help
make pipeline
make verify
make clean
```

Expected behavior:
- `make pipeline` runs `prepare -> train -> eval -> report` in declared order;
- each step writes simple artifacts to show a reproducible workflow contract.

## What to Observe
- one stable interface: `make <target>`;
- discoverable commands via `make help`;
- machine-checkable result via `make verify`;
- explicit dependency chain between workflow steps;
- `.PHONY` targets represent command-style actions;
- file targets still benefit from incremental rebuild decisions.
