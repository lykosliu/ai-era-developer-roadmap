---
name: make
description: A simple tool to build C command-line programs and rebuild only changed parts.
---

## Overview
`make` is often used as a project's command entrypoint, not only as a C compiler wrapper.
You can use one `Makefile` as the team's "command menu" for build, run, test, lint, packaging, and AI workflow tasks.

In a Makefile, the core unit is a rule:

```make
target: prerequisites
	recipe
```

- `target`: a task name or a file to produce.
- `prerequisites`: dependencies required before the target runs.
- `recipe`: shell commands to execute.

For file targets (like binaries), `make` gives incremental rebuilds.
For phony targets (like `test`, `train`, `eval`), `make` acts like a lightweight task runner.
GNU Make is the dominant implementation on Linux and macOS, and the GNU Make manual is the authoritative reference for advanced behavior.

## Why it matters
- **One entrypoint for all commands:** developers and AI agents can use `make <target>` instead of remembering many scripts.
- **Incremental rebuild performance:** file-based targets recompile only changed parts.
- **Standardized team workflow:** `make setup`, `make test`, `make release` are easy to document and review.
- **CI/local parity:** same target names work on local machines and CI pipelines.
- **Low overhead:** no extra task-runner dependency is required for many projects.

## Key Principles

### 0. Basic Makefile syntax (quick reference)
The minimal rule format:

```make
target: prerequisites
	recipe
```

- `target`: task name or output file name.
- `prerequisites`: files or other targets that must be ready first.
- `recipe`: shell command lines; each line must start with a tab.

Common variable syntax:

```make
CC := cc
CFLAGS := -Wall -Wextra -std=c11
TARGET := app
SRC := main.c
```

- `:=` assigns immediately (recommended for predictable values).
- `=` assigns recursively (expanded later when used).
- Use variables via `$(NAME)`.

Automatic variables inside recipes:

```make
$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $< -o $@
```

- `$@`: current target name.
- `$<`: first prerequisite.
- `$^`: all prerequisites.

Order-only prerequisite syntax:

```make
$(OUT_DIR)/prepared.txt: | $(OUT_DIR)
	echo "dataset=demo" > $(OUT_DIR)/prepared.txt
	echo "status=prepared" >> $(OUT_DIR)/prepared.txt
```

- `|` splits prerequisites into two groups.
- Left side (before `|`) is normal prerequisites.
- Right side (after `|`) is order-only prerequisites.
- Order-only prerequisite means: it must exist before recipe runs, but its timestamp changes do not force target rebuild.
- In this example, `$(OUT_DIR)` must be created first, but touching the directory should not trigger rebuilding `prepared.txt`.

Phony targets for command-style tasks:

```make
.PHONY: help clean test
```

Execution basics:
- `make` runs the first target (default target).
- `make <target>` runs a specific target.
- `make -j` enables parallel execution when dependencies allow.

### 1. `make` can run both file targets and task targets
Use file targets for compilation outputs and phony targets for "commands as tasks":

```make
.PHONY: build run test
build: app
run: build
	./app
test:
	pytest -q
```

### 2. Dependencies control execution order
Without prerequisites, `make` cannot infer order or rebuild triggers:

```make
app: main.c
	cc main.c -o app
```

This dependency model is why Makefiles exist: declare relationships, then let `make` run only necessary steps.

When checking whether a file target needs rebuild, `make` compares file modification time (`mtime`):
- target missing -> rebuild;
- any normal prerequisite newer than target -> rebuild;
- otherwise -> skip recipe and report up-to-date behavior.

### 3. First target is the default command
Running `make` without arguments executes the first target, so many teams use a default `help` or `all` target.

### 4. Recipe lines require tabs
Each recipe line must start with a tab character. Spaces are a common source of Makefile errors.

### 5. `.PHONY` is required for command-style targets
Targets such as `clean`, `test`, `train`, and `eval` usually do not create same-name files, so mark them as phony:

```make
.PHONY: clean test train eval
```

### 6. Variables keep targets clean and reusable
Variables such as `CC`, `CFLAGS`, and `TARGET` keep commands short and consistent across targets.

### 7. Parallel execution is built in
`make -j` runs independent targets in parallel when dependency constraints allow it.

### 8. Why `make` may skip but `make clean` always runs
- `make` (or `make app`) may skip compilation when target files are already up to date.
- `make clean` is typically declared as `.PHONY`, so it is treated as an action target, not a file target.
- As a result, `clean` runs whenever requested, while build targets run only when rebuild is needed.

## AI Context
- **Agent-friendly command contract:** AI coding agents can reliably call `make build`, `make test`, `make eval` as stable interfaces.
- **Natural-language to target mapping:** "run evaluation" maps cleanly to `make eval`, reducing ambiguity in automation.
- **Reproducible AI workflows:** targets such as `prepare`, `train`, `eval`, and `report` are explicit and versioned.
- **Cross-stack orchestration:** one Makefile can coordinate C binaries, Python scripts, and Node utilities.
- **Fast iteration:** file dependencies avoid unnecessary rebuilds when only part of the pipeline changes.

## References
- [Makefile Tutorial By Example](https://makefiletutorial.com/#why-do-makefiles-exist)
- [GNU Make Manual (Edition 0.77, GNU Make 4.4.1)](https://www.gnu.org/software/make/manual/make.html)
- [Linux Survey: make && makefile (Aliyun Developer Community)](https://developer.aliyun.com/article/1351438)
