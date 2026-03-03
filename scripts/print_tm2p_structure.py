#!/usr/bin/env python3
"""
Print the folder structure of the `tm2p` package to a file.

Rules:
- Ignore folders and files whose names start with "_".
- For files, replace the filename by the first class name defined in the file (if any).
- Use ASCII symbols `|`, `+`, `--` to show tree structure.

Usage:
    python scripts/print_tm2p_structure.py --root tm2p --out tm2p_structure.txt
"""
import argparse
import ast
import os
from typing import List


def get_first_class_name(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        tree = ast.parse(src, filename=path)
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                return node.name
    except Exception:
        pass
    # fallback: filename without suffix
    return os.path.splitext(os.path.basename(path))[0]


def build_tree_lines(root: str) -> List[str]:
    lines: List[str] = []

    def visit(path: str, prefix: str):
        try:
            entries = sorted(os.listdir(path))
        except OSError:
            return
        # filter out names starting with '_'
        entries = [e for e in entries if not e.startswith("_")]
        for idx, name in enumerate(entries):
            full = os.path.join(path, name)
            is_last = idx == len(entries) - 1
            connector = "+-- " if is_last else "|-- "
            if os.path.isdir(full):
                lines.append(prefix + connector + name + "/")
                new_prefix = prefix + ("    " if is_last else "|   ")
                visit(full, new_prefix)
            else:
                # For files, replace display with class name when possible
                if name.endswith(".py"):
                    display = get_first_class_name(full)
                else:
                    display = name
                lines.append(prefix + connector + display)

    root_name = os.path.basename(os.path.normpath(root))
    lines.append(root_name + "/")
    visit(root, "")
    return lines


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="tm2p", help="Root package/folder to scan")
    parser.add_argument("--out", default="tm2p_structure.txt", help="Output file path")
    args = parser.parse_args()

    if not os.path.isdir(args.root):
        raise SystemExit(f"Root not found or not a directory: {args.root}")

    lines = build_tree_lines(args.root)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Wrote structure to {args.out}")


if __name__ == "__main__":
    main()
