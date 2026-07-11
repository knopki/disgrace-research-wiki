#!/usr/bin/env python3
"""
fix-pipe-corruption.py — Detect and repair pipe corruption in wiki .md files.

Pipe corruption happens when an agent copies from read_file's LINE_NUM|CONTENT
display and accidentally includes the line-number-separator pipe in a patch
string. The fuzzy matcher then writes the pipe into the file content.

Three corruption patterns (see SKILL.md Pitfalls):
  1. `|- ` instead of `- `  (list-item dash gets a leading pipe)
  2. `|> ` instead of `> `  (blockquote marker gets a leading pipe)
  3. Bare `|` on an otherwise-empty line (pipe floats into whitespace)

Usage:
    python3 fix-pipe-corruption.py <path> [<path> ...]

Each path is checked for corruption, reported, and fixed in-place.
Backups are NOT created — the script is idempotent and only removes pipes
that the corruption rules target.

Exit code:
    0 — no corruption found (or all corruption fixed)
    1 — one or more files could not be read/written

Examples:
    python3 fix-pipe-corruption.py index.md
    python3 fix-pipe-corruption.py wiki/*.md
    find wiki/ -name '*.md' -exec python3 fix-pipe-corruption.py {} +
"""

import os
import re
import sys


PATTERNS = {
    "pipe-dash-space": (re.compile(r"^\|- ", re.MULTILINE), "- "),
    "pipe-gt-space": (re.compile(r"^\|> ", re.MULTILINE), "> "),
    "stray-pipe-eol": (re.compile(r"^\|$", re.MULTILINE), ""),
}


def check_and_fix(path: str) -> tuple[list[str], str | None]:
    """
    Return (issues_found, fixed_content_or_None).
    issues_found is a list of human-readable messages.
    If no issues, fixed_content is None.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()
    except FileNotFoundError:
        return [f"FILE NOT FOUND: {path}"], None
    except OSError as e:
        return [f"READ ERROR: {path} — {e}"], None

    issues: list[str] = []
    fixed = original

    for label, (pattern, replacement) in PATTERNS.items():
        matches = pattern.findall(fixed)
        if matches:
            count = len(matches)
            issues.append(f"  {label}: {count} occurrence(s)")
            fixed = pattern.sub(replacement, fixed)

    if not issues:
        return [], None

    return issues, fixed


def main() -> None:
    paths = sys.argv[1:]
    if not paths:
        print("Usage: fix-pipe-corruption.py <path> [<path> ...]", file=sys.stderr)
        sys.exit(1)

    any_failures = False

    for path in paths:
        issues, fixed = check_and_fix(path)
        if not issues:
            print(f"  ✓ {path} — clean")
            continue

        if fixed is None:
            # Read error
            for msg in issues:
                print(f"  ✗ {msg}", file=sys.stderr)
            any_failures = True
            continue

        # Write the fixed content
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(fixed)
        except OSError as e:
            print(f"  ✗ {path} — WRITE FAILED: {e}", file=sys.stderr)
            any_failures = True
            continue

        print(f"  ✗ {path} — FIXED:")
        for msg in issues:
            print(msg)

    total = len(paths)
    fixed_count = total - len(
        [p for p in paths if os.path.isfile(p) and not check_and_fix(p)[0]]
    )
    print(f"\nResult: {total} file(s), {fixed_count} fixed")
    sys.exit(1 if any_failures else 0)


if __name__ == "__main__":
    main()
