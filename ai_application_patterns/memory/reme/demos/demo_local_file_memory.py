import asyncio
import argparse
import json
import os
from datetime import datetime
from pathlib import Path

from agentscope.message import Msg
from reme.core.enumeration import MemorySource

try:
    from reme.reme_light import ReMeLight
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Cannot import 'reme.reme_light'.\n"
        "You likely installed the wrong PyPI package named 'reme'.\n"
        "Run: bash setup.sh\n"
        "Then retry: source .venv/bin/activate && python demo_local_file_memory.py"
    ) from exc


SCRIPT_DIR = Path(__file__).resolve().parent


def print_tree(root: Path) -> None:
    if not root.exists():
        print(f"Working directory not found: {root}")
        return
    print("\nGenerated local memory files:")
    for path in sorted(root.rglob("*")):
        kind = "dir " if path.is_dir() else "file"
        print(f"- [{kind}] {path}")


def count_lines(text: str) -> int:
    if not text:
        return 0
    return len(text.splitlines())


def read_context_lines(file_path: Path, start_line: int, radius: int = 1) -> str:
    if not file_path.exists():
        return ""
    lines = file_path.read_text(encoding="utf-8").splitlines()
    if not lines:
        return ""
    start_idx = max(0, start_line - 1 - radius)
    end_idx = min(len(lines), start_line - 1 + radius + 1)
    picked = lines[start_idx:end_idx]
    with_numbers = [f"{start_idx + i + 1}: {line}" for i, line in enumerate(picked)]
    return "\n".join(with_numbers)


def show_storage_report(working_dir: Path) -> None:
    memory_dir = working_dir / "memory"
    dialog_dir = working_dir / "dialog"
    index_db = working_dir / "file_store" / "chroma.sqlite3"
    metadata_file = working_dir / "reme_file_metadata.json"

    memory_files = sorted(memory_dir.glob("*.md")) if memory_dir.exists() else []
    dialog_files = sorted(dialog_dir.glob("*.jsonl")) if dialog_dir.exists() else []

    print("\nStorage Health Report:")
    print(f"- Working dir: {working_dir}")
    print(f"- Memory files: {len(memory_files)}")
    print(f"- Dialog files: {len(dialog_files)}")
    print(f"- Index DB exists: {index_db.exists()}")
    print(f"- Metadata file exists: {metadata_file.exists()}")

    if memory_files:
        latest_memory = memory_files[-1]
        text = latest_memory.read_text(encoding="utf-8")
        print(f"- Latest memory file: {latest_memory}")
        print(f"- Latest memory line count: {count_lines(text)}")
    if dialog_files:
        latest_dialog = dialog_files[-1]
        text = latest_dialog.read_text(encoding="utf-8")
        print(f"- Latest dialog file: {latest_dialog}")
        print(f"- Latest dialog message count: {count_lines(text)}")


def today_memory_file(working_dir: Path) -> Path:
    memory_dir = working_dir / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    return memory_dir / f"{datetime.now().strftime('%Y-%m-%d')}.md"


def append_memory_entry(working_dir: Path, text: str) -> Path:
    file_path = today_memory_file(working_dir)
    if not file_path.exists():
        file_path.write_text("# Local Memory Journal\n\n", encoding="utf-8")
    timestamp = datetime.now().strftime("%H:%M:%S")
    with file_path.open("a", encoding="utf-8") as f:
        f.write(f"- [{timestamp}] {text}\n")
    return file_path


def parse_tool_response_as_json(response: object) -> list[dict]:
    content = getattr(response, "content", None)
    if not isinstance(content, list) or not content:
        return []
    first = content[0]
    if not isinstance(first, dict):
        return []
    text = first.get("text")
    if not isinstance(text, str):
        return []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


async def search_with_retry(reme: ReMeLight, query: str, max_results: int = 5) -> list[dict]:
    response = await reme.memory_search(query=query, max_results=max_results)
    hits = parse_tool_response_as_json(response)
    if hits:
        return hits
    # Give file watcher/indexing a chance to finish startup scan.
    await asyncio.sleep(1.5)
    response = await reme.memory_search(query=query, max_results=max_results)
    return parse_tool_response_as_json(response)


async def get_indexed_memory_files(reme: ReMeLight) -> list[str]:
    try:
        file_store = reme.service_context.file_stores["default"]
        files = await file_store.list_files(MemorySource.MEMORY)
        return sorted(files)
    except Exception:
        return []


def print_intro(mode: str, working_dir: Path) -> None:
    print("=== ReMe Local File Memory Interactive Demo ===")
    print(f"Mode: {mode}")
    print(f"Working dir: {working_dir}")
    print("Workflow:")
    print("1) Input memory text -> append to memory/YYYY-MM-DD.md")
    print("2) ReMe file watcher indexes local memory files")
    print("3) Query memory -> ReMeLight.memory_search")
    print("4) Session messages persist to dialog/YYYY-MM-DD.jsonl")
    print("")
    print("Menu:")
    print("1. Add memory")
    print("2. Search memory")
    print("3. Show storage details")
    print("4. Exit")


async def persist_dialog(memory, user_text: str) -> None:
    await memory.add(Msg(name="user", role="user", content=f"Memory input: {user_text}"))
    await memory.add(
        Msg(name="assistant", role="assistant", content="Saved this memory into local file storage.")
    )
    memory.clear_content()


async def run_interactive(reme: ReMeLight, mode: str, working_dir: Path) -> None:
    memory = reme.get_in_memory_memory()
    while True:
        print_intro(mode=mode, working_dir=working_dir)
        choice = input("Select an option (1-4): ").strip()
        if choice == "1":
            text = input("Enter memory text: ").strip()
            if not text:
                print("Empty input ignored.\n")
                continue
            file_path = append_memory_entry(working_dir, text)
            await persist_dialog(memory, text)
            # Allow file watcher a short time to refresh local index.
            await asyncio.sleep(0.4)
            print(f"Saved to: {file_path}\n")
            continue
        if choice == "2":
            query = input("Enter search query: ").strip()
            if not query:
                print("Empty query ignored.\n")
                continue
            hits = await search_with_retry(reme, query=query, max_results=5)
            if not hits:
                indexed_files = await get_indexed_memory_files(reme)
                print("No memory hits after retry.")
                print(f"- Indexed memory files: {len(indexed_files)}")
                if indexed_files:
                    print("- Indexed file list:")
                    for f in indexed_files:
                        print(f"  - {f}")
                print("")
                continue
            print(f"\nSearch results (query='{query}', hits={len(hits)}):")
            for i, hit in enumerate(hits, start=1):
                path = hit.get("path", "")
                score = hit.get("score", "")
                start_line = hit.get("start_line", "")
                snippet = str(hit.get("snippet", "")).strip().replace("\n", " ")
                print(f"{i}. score={score} path={path} line={start_line}")
                print(f"   snippet: {snippet}")
                if path and isinstance(start_line, int):
                    context = read_context_lines(Path(path), start_line=start_line, radius=1)
                    if context:
                        print("   context:")
                        for line in context.splitlines():
                            print(f"   {line}")
            print("")
            continue
        if choice == "3":
            show_storage_report(working_dir)
            print_tree(working_dir)
            today_file = today_memory_file(working_dir)
            if today_file.exists():
                print(f"\nCurrent memory file: {today_file}")
                print(today_file.read_text(encoding="utf-8"))
            print("")
            continue
        if choice == "4":
            print("Bye.")
            return
        print("Invalid option.\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ReMe local file memory demo")
    parser.add_argument(
        "--mode",
        choices=["fts", "semantic", "semantic-local"],
        default="fts",
        help=(
            "Retrieval mode: "
            "fts (no embedding), "
            "semantic (OpenAI-compatible embedding API), "
            "semantic-local (in-process sentence-transformers)."
        ),
    )
    parser.add_argument(
        "--working-dir",
        default=None,
        help="Custom working directory. Defaults to mode-specific directory under script path.",
    )
    parser.add_argument(
        "--embedding-model",
        default="text-embedding-3-small",
        help="Embedding model name for semantic mode (OpenAI-compatible API).",
    )
    return parser.parse_args()


def resolve_working_dir(mode: str, custom_working_dir: str | None) -> Path:
    if custom_working_dir:
        return Path(custom_working_dir).expanduser().resolve()
    if mode == "semantic":
        suffix = "semantic"
    elif mode == "semantic-local":
        suffix = "semantic_local"
    else:
        suffix = "fts"
    return (SCRIPT_DIR / f".reme_local_demo_{suffix}").resolve()


def build_reme(mode: str, working_dir: Path, embedding_model: str) -> ReMeLight:
    if mode == "semantic":
        base_url = os.getenv("EMBEDDING_BASE_URL", "")
        if not base_url:
            print(
                "Semantic mode expects EMBEDDING_BASE_URL to point to an OpenAI-compatible embedding service.\n"
                "Example: local vLLM/Infinity service endpoint."
            )
        return ReMeLight(
            working_dir=str(working_dir),
            default_file_store_config={"fts_enabled": True, "vector_enabled": True},
            default_embedding_model_config={"backend": "openai", "model_name": embedding_model},
            enable_load_env=True,
        )

    if mode == "semantic-local":
        from local_embedding_backend import register_local_embedding_backend

        register_local_embedding_backend()
        return ReMeLight(
            working_dir=str(working_dir),
            default_file_store_config={"fts_enabled": True, "vector_enabled": True},
            default_embedding_model_config={"backend": "local_st", "model_name": embedding_model},
            enable_load_env=True,
        )

    return ReMeLight(
        working_dir=str(working_dir),
        default_file_store_config={"fts_enabled": True, "vector_enabled": False},
        enable_load_env=True,
    )


async def main() -> None:
    args = parse_args()
    working_dir = resolve_working_dir(args.mode, args.working_dir)
    print(f"Using working dir: {working_dir}")
    reme = build_reme(args.mode, working_dir, args.embedding_model)
    try:
        await reme.start()
    except Exception as exc:
        print(f"Failed to start ReMe in mode={args.mode}.")
        print(f"Reason: {exc}")
        if args.mode == "semantic-local":
            print("Tip: check sentence-transformers + torch + numpy version compatibility in this venv.")
        return
    try:
        await run_interactive(reme, mode=args.mode, working_dir=working_dir)
    finally:
        try:
            await reme.close()
        except Exception as exc:  # pragma: no cover
            print(f"close() warning: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
