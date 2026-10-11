#!/usr/bin/env python3
"""Scan a project tree and emit a structured markdown report for codebase docs.

Produces sections: MANIFESTS, STACK, STRUCTURE, TESTS, CI/CD, CONTAINERS,
SECURITY, and CODE METRICS. Stdlib only; safe to run from any project root.

Usage: python3 scan.py --output docs/codebase/.codebase-scan.txt
"""

from __future__ import annotations

import argparse
import contextlib
import os
import sys
from collections import Counter
from pathlib import Path

IGNORED = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    ".next",
    "out",
    "target",
    ".mypy_cache",
    ".ruff_cache",
    "coverage",
}

LANGUAGE_EXT = {
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".py": "python",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".rb": "ruby",
    ".php": "php",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".cs": "csharp",
    ".swift": "swift",
    ".kt": "kotlin",
    ".sh": "shell",
}

MANIFESTS = [
    "package.json",
    "pyproject.toml",
    "setup.py",
    "requirements.txt",
    "Pipfile",
    "go.mod",
    "Cargo.toml",
    "pom.xml",
    "build.gradle",
    "composer.json",
    "Gemfile",
    "Gemfile.lock",
]


def _walk(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED]
        for fn in filenames:
            yield Path(dirpath) / fn


def scan(root: Path) -> str:
    files = list(_walk(root))
    langs: Counter = Counter()
    lines_by_lang: Counter = Counter()
    manifests = [f.name for f in files if f.name in MANIFESTS and f.is_file()]
    test_markers = [
        f
        for f in files
        if ("test" in f.name.lower() or f.name in ("conftest.py",)) and f.suffix in LANGUAGE_EXT
    ]

    for f in files:
        if f.suffix in LANGUAGE_EXT and f.is_file():
            lang = LANGUAGE_EXT[f.suffix]
            langs[lang] += 1
            with contextlib.suppress(OSError):
                lines_by_lang[lang] += sum(1 for _ in f.open(encoding="utf-8", errors="ignore"))

    out: list[str] = ["# Codebase Scan", ""]

    out.append("## MANIFESTS")
    if manifests:
        out.extend(f"- {m}" for m in manifests)
    else:
        out.append("- (none found)")
    out.append("")

    out.append("## STACK (inferred from manifests)")
    stack = infer_stack(manifests, root)
    if stack:
        out.extend(f"- {s}" for s in stack)
    else:
        out.append("- (ambiguous — see stack-detection.md)")
    out.append("")

    out.append("## STRUCTURE (top-level)")
    for entry in sorted(root.iterdir()):
        kind = "dir" if entry.is_dir() else "file"
        if entry.name not in IGNORED:
            out.append(f"- [{kind}] {entry.name}")
    out.append("")

    out.append("## CODE METRICS (by language)")
    if langs:
        for lang, count in langs.most_common():
            out.append(f"- {lang}: {count} files, {lines_by_lang[lang]} lines")
    else:
        out.append("- (no recognized source files)")
    out.append("")

    out.append(f"## TESTS ({len(test_markers)} candidate files)")
    if test_markers:
        out.extend(f"- {f.relative_to(root)}" for f in test_markers[:50])
    else:
        out.append("- (none found)")
    out.append("")

    out.append("## CI/CD")
    ci = [
        f.name
        for f in files
        if f.name in ("Dockerfile", "docker-compose.yml")
        or (f.parts and ".github" in f.parts and "workflows" in f.parts)
    ]
    if ci:
        out.extend(f"- {c}" for c in sorted(set(ci)))
    else:
        out.append("- (none detected)")
    out.append("")

    out.append("## CONTAINERS & ORCHESTRATION")
    cont = [f.name for f in files if f.name in ("Dockerfile", "docker-compose.yml", "k8s.yaml")]
    if cont:
        out.extend(f"- {c}" for c in sorted(set(cont)))
    else:
        out.append("- (none detected)")
    out.append("")

    out.append("## SECURITY & COMPLIANCE")
    sec = [f.name for f in files if f.name in ("SECURITY.md", "sbom.json", ".snyk", ".env.example")]
    if sec:
        out.extend(f"- {s}" for s in sorted(set(sec)))
    else:
        out.append("- (none detected)")
    out.append("")

    return "\n".join(out) + "\n"


def infer_stack(manifests: list[str], root: Path) -> list[str]:
    stack: list[str] = []
    if "package.json" in manifests:
        try:
            import json

            pkg = json.loads((root / "package.json").read_text(encoding="utf-8"))
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            stack.append("typescript" if "typescript" in deps else "node")
        except (OSError, ValueError):
            stack.append("node")
    if "pyproject.toml" in manifests:
        stack.append("python")
    if "go.mod" in manifests:
        stack.append("go")
    if "Cargo.toml" in manifests:
        stack.append("rust")
    if "pom.xml" in manifests or "build.gradle" in manifests:
        stack.append("java")
    if "composer.json" in manifests:
        stack.append("php")
    return stack


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan a project for codebase docs.")
    parser.add_argument("--output", default=None, help="write the report to this path")
    parser.add_argument("--root", default=".", help="project root to scan (default: CWD)")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    report = scan(root)
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        print(f"scan written to {out}", file=sys.stderr)
    else:
        sys.stdout.write(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
