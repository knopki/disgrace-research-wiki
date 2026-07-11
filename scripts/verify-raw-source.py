#!/usr/bin/env python3
"""
verify-raw-source.py — Post-creation convention checker for raw paper sources.

Usage:
    python3 scripts/verify-raw-source.py <raw-dir-path>

Example:
    python3 scripts/verify-raw-source.py raw/papers/2022-01-wei-chain-of-thought/

Checks:
  - Directory exists and contains files
  - .md file is a named file (firstauthorYYYYfeature.md), NOT index.md
  - PDF file is present (.pdf extension)
  - .md file has YAML frontmatter (surrounded by ---)
  - .md file contains a markdown link to the PDF
  - .md file has an h1 (# Title) after frontmatter
  - No extra sections after abstract in the .md (h2+ sections are forbidden)

Exit code 0 = all checks pass. 1 = one or more checks failed.
"""

import os
import re
import sys


def main():
    raw_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    raw_dir = raw_dir.rstrip("/")

    if not os.path.isdir(raw_dir):
        print(f"FAIL: {raw_dir} is not a directory or doesn't exist")
        sys.exit(1)

    files = os.listdir(raw_dir)
    md_files = [f for f in files if f.endswith(".md")]
    pdf_files = [f for f in files if f.endswith(".pdf")]

    errors = []
    warnings = []

    # --- Check 1: At least one markdown and one PDF ---
    if not md_files:
        errors.append("No .md file found in raw directory")
    if not pdf_files:
        errors.append("No .pdf file found in raw directory")

    # --- Check 2: Named file convention ---
    for mf in md_files:
        if mf == "index.md":
            errors.append(
                f"NAMED FILE VIOLATION: {mf} — papers MUST use named file "
                f"(firstauthorYYYYfeature.md), not index.md"
            )
        elif not re.match(r"^[a-z][a-z]+[12][0-9]{3}[a-z]+\.md$", mf):
            warnings.append(
                f"Unconventional filename: {mf} — expected pattern like "
                f"'firstauthorYYYYslug.md' (e.g., hinton2015distill.md)"
            )

    # --- Check 3: PDF link exists in .md ---
    for mf in md_files:
        path = os.path.join(raw_dir, mf)
        md_content = open(path).read()

        # Check frontmatter
        fm_match = re.match(r"^---\s*\n(.*?)\n---", md_content, re.DOTALL)
        if not fm_match:
            errors.append(f"{mf}: missing YAML frontmatter (--- ... ---)")
        else:
            fm_body = fm_match.group(1)
            if "source_url:" not in fm_body:
                warnings.append(f"{mf}: frontmatter may be missing source_url")
            if "ingested:" not in fm_body:
                warnings.append(f"{mf}: frontmatter may be missing ingested date")

        # Check PDF link
        for pf in pdf_files:
            if f"]({pf})" in md_content:
                break
            if f"]({os.path.basename(pf)})" in md_content:
                break
        else:
            if pdf_files:
                # Check for relative path reference
                found = False
                for pf in pdf_files:
                    if pf in md_content:
                        found = True
                        break
                if not found:
                    errors.append(
                        f"{mf}: no markdown link to PDF {pdf_files[0]} found in body. "
                        f"Expected something like '[filename.pdf](filename.pdf)'"
                    )

        # Check h1 heading after frontmatter
        body_after_fm = md_content.split("---", 2)
        if len(body_after_fm) > 2:
            body = body_after_fm[2]
            h1_match = re.search(r"^#\s+.+", body, re.MULTILINE)
            if not h1_match:
                errors.append(f"{mf}: missing h1 heading (# Title) after frontmatter")

        # Check no extra sections after abstract
        # Allowed: frontmatter, h1, PDF link line(s), ## Abstract, abstract text
        # Forbidden: ## Key Results, ## Architecture, etc.
        forbidden_h2 = re.findall(
            r"^##\s+(?!Abstract)(?!BibTeX)", body, re.MULTILINE
        )
        if forbidden_h2:
            errors.append(
                f"{mf}: forbidden sections found after abstract: "
                f"{', '.join(forbidden_h2)}. "
                f"Only ## Abstract is permitted."
            )

    # --- Report ---
    if errors:
        print("ERRORS:")
        for e in errors:
            print(f"  [FAIL] {e}")
    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  [WARN] {w}")

    status = "PASS" if not errors else "FAIL"
    print(f"\nResult: {status} ({len(errors)} errors, {len(warnings)} warnings)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
