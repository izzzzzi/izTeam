#!/usr/bin/env python3
"""
repo-map.py — generates a ranked symbol map of a codebase.

Usage:
    python3 repo-map.py [root_dir] [--budget=N] [--fresh]

Output: .repo-map file in root_dir (structured text, not JSON).

Design:
    - Python 3 stdlib only (no pip install)
    - Regex-based symbol extraction for TS/JS, Python, Go, Rust, Java + fallback
    - Ranked by import frequency (most-imported files first)
    - Binary search to fit within char budget
"""

import os
import re
import sys
import datetime
import argparse
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_BUDGET = 8000  # chars ≈ 2000 tokens

IGNORED_DIRS = {
    "node_modules", ".git", ".next", ".nuxt", "dist", "build", "out",
    "__pycache__", ".mypy_cache", ".pytest_cache", "venv", ".venv",
    "env", ".env", "vendor", "target", ".claude", ".conventions",
    "coverage", ".turbo", ".cache", ".parcel-cache",
}

SOURCE_EXTENSIONS = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
    ".py",
    ".go",
    ".rs",
    ".java", ".kt",
    ".vue", ".svelte",
}

BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp",
    ".woff", ".woff2", ".ttf", ".eot",
    ".zip", ".tar", ".gz", ".br",
    ".pdf", ".mp3", ".mp4", ".mov", ".avi",
    ".lock", ".map",
}

# ---------------------------------------------------------------------------
# Symbol extraction patterns (per language group)
# ---------------------------------------------------------------------------

# TypeScript / JavaScript
TS_PATTERNS = [
    # export function name / export async function name
    (r"export\s+(?:async\s+)?function\s+(\w+)", "function"),
    # export const name / export let name
    (r"export\s+(?:const|let|var)\s+(\w+)", "const"),
    # export default function name
    (r"export\s+default\s+(?:async\s+)?function\s+(\w+)", "function"),
    # export class name
    (r"export\s+(?:abstract\s+)?class\s+(\w+)", "class"),
    # export interface name
    (r"export\s+interface\s+(\w+)", "interface"),
    # export type name
    (r"export\s+type\s+(\w+)", "type"),
    # export enum name
    (r"export\s+enum\s+(\w+)", "enum"),
]

# Python
PY_PATTERNS = [
    (r"^class\s+(\w+)", "class"),
    (r"^def\s+(\w+)", "function"),
    (r"^async\s+def\s+(\w+)", "function"),
    # module-level assignments (ALL_CAPS or PascalCase only — skip _private)
    (r"^([A-Z][A-Z_0-9]+)\s*=", "const"),
    (r"^([A-Z][a-zA-Z0-9]+)\s*=", "const"),
]

# Go
GO_PATTERNS = [
    (r"^func\s+(\w+)", "function"),
    (r"^func\s+\([^)]+\)\s+(\w+)", "method"),
    (r"^type\s+(\w+)\s+struct", "struct"),
    (r"^type\s+(\w+)\s+interface", "interface"),
    (r"^type\s+(\w+)", "type"),
    (r"^var\s+(\w+)", "var"),
    (r"^const\s+(\w+)", "const"),
]

# Rust
RS_PATTERNS = [
    (r"^pub\s+(?:async\s+)?fn\s+(\w+)", "function"),
    (r"^pub\s+struct\s+(\w+)", "struct"),
    (r"^pub\s+enum\s+(\w+)", "enum"),
    (r"^pub\s+trait\s+(\w+)", "trait"),
    (r"^pub\s+type\s+(\w+)", "type"),
    (r"^pub\s+const\s+(\w+)", "const"),
    (r"^pub\s+static\s+(\w+)", "static"),
    (r"^pub\s+mod\s+(\w+)", "mod"),
]

# Java / Kotlin
JAVA_PATTERNS = [
    (r"(?:public|protected)\s+(?:static\s+)?(?:final\s+)?class\s+(\w+)", "class"),
    (r"(?:public|protected)\s+(?:static\s+)?(?:final\s+)?interface\s+(\w+)", "interface"),
    (r"(?:public|protected)\s+(?:static\s+)?(?:final\s+)?enum\s+(\w+)", "enum"),
    (r"(?:public|protected)\s+(?:static\s+)?(?:[\w<>\[\],\s]+)\s+(\w+)\s*\(", "method"),
]

# Fallback — exported / public symbols
FALLBACK_PATTERNS = [
    (r"export\s+(?:async\s+)?function\s+(\w+)", "function"),
    (r"export\s+(?:const|let|var)\s+(\w+)", "const"),
    (r"export\s+(?:abstract\s+)?class\s+(\w+)", "class"),
    (r"^class\s+(\w+)", "class"),
    (r"^def\s+(\w+)", "function"),
    (r"^pub\s+fn\s+(\w+)", "function"),
]

LANG_PATTERNS = {
    ".ts": TS_PATTERNS, ".tsx": TS_PATTERNS,
    ".js": TS_PATTERNS, ".jsx": TS_PATTERNS,
    ".mjs": TS_PATTERNS, ".cjs": TS_PATTERNS,
    ".vue": TS_PATTERNS, ".svelte": TS_PATTERNS,
    ".py": PY_PATTERNS,
    ".go": GO_PATTERNS,
    ".rs": RS_PATTERNS,
    ".java": JAVA_PATTERNS, ".kt": JAVA_PATTERNS,
}

# ---------------------------------------------------------------------------
# Import detection patterns (who imports whom)
# ---------------------------------------------------------------------------

# JS/TS: import ... from './path' or require('./path')
TS_IMPORT_RE = re.compile(
    r"""(?:import\s+.*?from\s+['"]([^'"]+)['"]|require\s*\(\s*['"]([^'"]+)['"]\s*\))"""
)

# Python: from package import ... or import package
PY_IMPORT_RE = re.compile(
    r"""^(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))""", re.MULTILINE
)

# Go: import "path"
GO_IMPORT_RE = re.compile(r"""["']([^"']+)["']""")

# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------


def collect_source_files(root: str) -> list[str]:
    """Walk the tree, return relative paths of source files."""
    files = []
    root_path = Path(root).resolve()
    for dirpath, dirnames, filenames in os.walk(root_path):
        # prune ignored dirs in-place
        dirnames[:] = [
            d for d in dirnames
            if d not in IGNORED_DIRS and not d.startswith(".")
        ]
        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if ext in SOURCE_EXTENSIONS and ext not in BINARY_EXTENSIONS:
                full = os.path.join(dirpath, fname)
                rel = os.path.relpath(full, root_path)
                files.append(rel)
    return sorted(files)


def extract_symbols(filepath: str, root: str) -> list[tuple[str, str]]:
    """Extract (name, kind) pairs from a source file."""
    ext = os.path.splitext(filepath)[1].lower()
    patterns = LANG_PATTERNS.get(ext, FALLBACK_PATTERNS)
    compiled = [(re.compile(p), k) for p, k in patterns]

    full_path = os.path.join(root, filepath)
    try:
        with open(full_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except (OSError, IOError):
        return []

    # For Python: only match top-level symbols (no leading whitespace)
    python_mode = ext == ".py"

    symbols = []
    seen = set()
    for line in content.split("\n"):
        stripped = line.strip()
        # In Python, skip indented lines (methods inside classes)
        if python_mode and line != stripped and not line.startswith("class "):
            # Check if this is a top-level definition (no indent)
            if line[0:1] in (" ", "\t"):
                continue
        for pattern, kind in compiled:
            m = pattern.search(stripped)
            if m:
                name = m.group(1)
                # skip private/dunder
                if name.startswith("_") and not name.startswith("__"):
                    continue
                key = (name, kind)
                if key not in seen:
                    seen.add(key)
                    symbols.append(key)
    return symbols


def count_imports(files: list[str], root: str) -> dict[str, int]:
    """Count how many files import each file (simplified resolution)."""
    import_counts: dict[str, int] = defaultdict(int)
    # Build a lookup: basename without ext → relative path
    basename_to_paths: dict[str, list[str]] = defaultdict(list)
    for f in files:
        stem = Path(f).stem
        # handle index files: use parent dir name
        if stem == "index":
            parent = str(Path(f).parent)
            basename_to_paths[parent].append(f)
        basename_to_paths[stem].append(f)
        # also map full path without ext
        no_ext = str(Path(f).with_suffix(""))
        basename_to_paths[no_ext].append(f)

    root_path = Path(root).resolve()

    for filepath in files:
        ext = os.path.splitext(filepath)[1].lower()
        full_path = os.path.join(root_path, filepath)
        try:
            with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except (OSError, IOError):
            continue

        imported_specs = set()

        if ext in (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".vue", ".svelte"):
            for m in TS_IMPORT_RE.finditer(content):
                spec = m.group(1) or m.group(2)
                if spec and (spec.startswith(".") or spec.startswith("/")):
                    imported_specs.add(spec)
        elif ext == ".py":
            for m in PY_IMPORT_RE.finditer(content):
                spec = m.group(1) or m.group(2)
                if spec:
                    imported_specs.add(spec)
        elif ext == ".go":
            for m in GO_IMPORT_RE.finditer(content):
                imported_specs.add(m.group(1))

        # Resolve specs to files
        file_dir = str(Path(filepath).parent)
        for spec in imported_specs:
            resolved = _resolve_import(spec, file_dir, basename_to_paths)
            if resolved and resolved != filepath:
                import_counts[resolved] += 1

    return dict(import_counts)


def _resolve_import(
    spec: str, from_dir: str, lookup: dict[str, list[str]]
) -> str | None:
    """Try to resolve an import specifier to a relative file path."""
    # Normalize relative paths
    if spec.startswith("./") or spec.startswith("../"):
        resolved = os.path.normpath(os.path.join(from_dir, spec))
        # Try exact match, then with common extensions
        if resolved in lookup:
            return lookup[resolved][0]
        for ext in (".ts", ".tsx", ".js", ".jsx", ".py"):
            candidate = resolved + ext
            if candidate in lookup:
                return lookup[candidate][0]
        # Try as directory with index
        if resolved in lookup:
            return lookup[resolved][0]

    # Try basename match
    parts = spec.replace("/", ".").replace("\\", ".").split(".")
    basename = parts[-1] if parts else spec
    if basename in lookup:
        return lookup[basename][0]

    return None


def build_repo_map(
    root: str, budget: int = DEFAULT_BUDGET
) -> str:
    """Build the full repo map string, fitting within budget."""
    files = collect_source_files(root)
    if not files:
        return "# repo-map: no source files found\n"

    # Extract symbols per file
    file_symbols: dict[str, list[tuple[str, str]]] = {}
    for f in files:
        syms = extract_symbols(f, root)
        if syms:
            file_symbols[f] = syms

    # Count imports for ranking
    import_counts = count_imports(files, root)

    # Rank files: import count desc, then alphabetical
    ranked_files = sorted(
        file_symbols.keys(),
        key=lambda f: (-import_counts.get(f, 0), f),
    )

    # Build header
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    header = f"# repo-map: generated {now} | budget:{budget} | files:{len(ranked_files)}\n"

    # Binary search: find max number of files that fit in budget
    def render(file_list: list[str]) -> str:
        lines = [header]
        for filepath in file_list:
            lines.append(f"{filepath}:")
            for name, kind in file_symbols[filepath]:
                lines.append(f"  {name} ({kind})")
            lines.append("")
        return "\n".join(lines)

    # Try all files first
    full = render(ranked_files)
    if len(full) <= budget:
        return full

    # Binary search for max count
    lo, hi = 1, len(ranked_files)
    best = 1
    while lo <= hi:
        mid = (lo + hi) // 2
        candidate = render(ranked_files[:mid])
        if len(candidate) <= budget:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1

    result = render(ranked_files[:best])

    # Update header with truncation note
    truncated_header = (
        f"# repo-map: generated {now} | budget:{budget} "
        f"| files:{best}/{len(ranked_files)} (truncated)\n"
    )
    result = truncated_header + result[len(header):]
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Generate a ranked symbol map of a codebase."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Root directory to scan (default: current dir)",
    )
    parser.add_argument(
        "--budget",
        type=int,
        default=DEFAULT_BUDGET,
        help=f"Max output size in chars (default: {DEFAULT_BUDGET})",
    )
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Force regeneration even if .repo-map is fresh",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print to stdout instead of writing .repo-map file",
    )

    args = parser.parse_args()
    root = os.path.abspath(args.root)

    if not os.path.isdir(root):
        print(f"Error: {root} is not a directory", file=sys.stderr)
        sys.exit(1)

    output_path = os.path.join(root, ".repo-map")

    # Freshness check (skip if --fresh)
    if not args.fresh and os.path.exists(output_path):
        stat = os.stat(output_path)
        age_hours = (
            datetime.datetime.now().timestamp() - stat.st_mtime
        ) / 3600
        if age_hours < 24:
            # Check if there are new commits since .repo-map was generated
            try:
                import subprocess
                result = subprocess.run(
                    ["git", "log", "--oneline", "--since",
                     datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
                     "--", "."],
                    capture_output=True, text=True, cwd=root, timeout=5
                )
                if result.returncode == 0 and not result.stdout.strip():
                    print(f".repo-map is fresh ({age_hours:.1f}h old, no new commits). Use --fresh to force.", file=sys.stderr)
                    sys.exit(0)
            except (FileNotFoundError, subprocess.TimeoutExpired):
                # git not available or timeout — regenerate
                pass

    repo_map = build_repo_map(root, args.budget)

    if args.stdout:
        print(repo_map)
    else:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(repo_map)
        lines = repo_map.count("\n")
        print(f"Wrote {output_path} ({len(repo_map)} chars, {lines} lines)", file=sys.stderr)


if __name__ == "__main__":
    main()
