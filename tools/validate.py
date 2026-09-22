#!/usr/bin/env python3
"""Validate package structure and publication hygiene; no prose quality scoring.

Usage: python tools/validate.py [repository-root]
Only the Python standard library is required. Diagnostics never echo matched text.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit


TEXT_SUFFIXES = {".md", ".markdown", ".json", ".yaml", ".yml", ".toml", ".txt",
                 ".py", ".sh", ".ps1", ".html", ".css", ".js", ".ini", ".cfg"}
PATTERNS = {
    "absolute-drive-path": re.compile(r"(?<![\w])\b[A-Za-z]:[\\/](?:<[^>\r\n]+>|[^\s`\"'<>|)])+"),
    "user-home-path": re.compile(r"(?<![\w])/(?:Users|home)/[^/\s`\"'<>]+|(?<![\w])/(?:root)(?:/|\b)"),
    "chat-session-url": re.compile(r"https?://(?:chatgpt\.com|chat\.openai\.com)/(?:c|share)/[A-Za-z0-9-]+", re.I),
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"),
    "service-token": re.compile(r"\b(?:sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|xox[baprs]-[A-Za-z0-9-]{20,}|AKIA[0-9A-Z]{16})\b"),
    "credential-assignment": re.compile(r"\b(?:api[_-]?key|secret[_-]?key|access[_-]?token|auth[_-]?token|password)\b[\"']?\s*[:=]\s*[\"']([A-Za-z0-9_./+=-]{20,})[\"']", re.I),
}


def placeholder(value: str) -> bool:
    """Accept explicit template variables, not ordinary Chinese task wording."""
    return bool(re.search(r"\$\{[^}]+\}|\$(?:HOME|CODEX_HOME|env:)\b|\{\{[^}]+\}\}|<[^>]+>|\[[^]]+\]|(?:^|[/\\])(?:path[-_]?to|your[-_][^/\\]+|占位[^/\\]*|待填[^/\\]*)(?:[/\\]|$)|…", value, re.I))


def mask_code(text: str, inline: bool = True) -> str:
    """Keep line numbers while omitting fenced, indented and inline code."""
    lines = []
    fence = None
    for line in text.splitlines(keepends=True):
        match = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence:
            if re.match(r"^ {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*$", line):
                fence = None
            lines.append("\n" if line.endswith("\n") else "")
        elif match:
            fence = match.group(1)
            lines.append("\n" if line.endswith("\n") else "")
        elif line.startswith(("    ", "\t")):
            lines.append("\n" if line.endswith("\n") else "")
        else:
            lines.append(re.sub(r"(`+).*?\1", lambda m: " " * len(m.group()), line) if inline else line)
    return "".join(lines)


def headings(text: str) -> set[str]:
    # Keep inline code content in headings; GitHub includes it in the anchor.
    text = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.S)
    clean = mask_code(text, inline=False)
    clean = re.sub(r"(`+)(.*?)\1", r"\2", clean)
    anchors = set(re.findall(r"<(?:a|h[1-6])\b[^>]*\b(?:id|name)=[\"']([^\"']+)[\"']", clean, re.I))
    used = set()
    lines = clean.splitlines()
    for index, line in enumerate(lines):
        atx = re.match(r"^ {0,3}#{1,6}\s+(.+?)(?:\s+#+)?\s*$", line)
        title = atx.group(1) if atx else None
        if title is None and index + 1 < len(lines) and line.strip() and re.fullmatch(r" {0,3}(?:=+|-+)\s*", lines[index + 1]):
            title = line.strip()
        if title is None:
            continue
        title = re.sub(r"!?\[([^]]+)\]\([^)]*\)", r"\1", title)
        title = html.unescape(re.sub(r"<[^>]+>", "", title)).lower()
        slug = "".join(c for c in title if c in "-_ " or unicodedata.category(c)[0] in "LNM").replace(" ", "-")
        candidate, suffix = slug, 0
        while candidate in used:
            suffix += 1
            candidate = f"{slug}-{suffix}"
        used.add(candidate)
        anchors.add(candidate)
    return anchors


def destinations(text: str):
    """Yield destinations and offsets for inline and reference-style links."""
    clean = mask_code(text)
    definitions = {}
    definition_spans = []
    for match in re.finditer(r"^ {0,3}\[([^]\n]+)\]:\s*(<[^>\n]+>|\S+)", clean, re.M):
        definitions[" ".join(match.group(1).split()).casefold()] = match.group(2)
        definition_spans.append(match.span())
        yield match.group(2), match.start()
    for start, end in reversed(definition_spans):
        clean = clean[:start] + " " * (end - start) + clean[end:]
    inline = re.compile(r"!?\[([^]\n]*)\]\(\s*(<[^>\n]+>|(?:[^\s()\\]|\\.|\([^()]*\))*)(?:\s+[\"'][^\n]*?[\"'])?\s*\)")
    for match in inline.finditer(clean):
        yield match.group(2), match.start()
    # Definitions are checked even when unused; references need no second check.
    for match in re.finditer(r"!?\[([^]\n]+)\]\[([^]\n]*)\]", clean):
        label = " ".join((match.group(2) or match.group(1)).split()).casefold()
        if label not in definitions and not placeholder(match.group(2)):
            yield None, match.start()


class Validator:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.errors: list[tuple[str, int, str]] = []
        self.texts: dict[Path, str] = {}

    def error(self, path: Path, line: int, kind: str):
        self.errors.append((path.relative_to(self.root).as_posix(), line, kind))

    def load(self):
        for path in sorted(self.root.rglob("*")):
            relative = path.relative_to(self.root)
            if ".git" in relative.parts or "__pycache__" in relative.parts or not path.is_file() or path.is_symlink():
                continue
            if path.suffix.lower() not in TEXT_SUFFIXES and path.suffix and not path.name.startswith("."):
                continue
            try:
                self.texts[path] = path.read_text(encoding="utf-8-sig")
            except UnicodeError:
                self.error(path, 1, "invalid-utf8-text")

    def metadata(self):
        path = self.root / "SKILL.md"
        text = self.texts.get(path, "")
        front = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|$)", text, re.S)
        if not front:
            self.error(path, 1, "missing-skill-frontmatter")
            return
        fields = {}
        for match in re.finditer(r"^[ \t]*(name|description|version):[ \t]*(.*?)[ \t]*$", front.group(1), re.M):
            fields[match.group(1)] = match.group(2).strip("\"'")
        for key in ("name", "description", "version"):
            if not fields.get(key):
                self.error(path, 1, f"missing-frontmatter-{key}")
        if fields.get("name") != "chinese-writing":
            self.error(path, 1, "invalid-skill-name")

    def links(self):
        anchor_cache = {p: headings(t) for p, t in self.texts.items() if p.suffix.lower() in {".md", ".markdown"}}
        for path in anchor_cache:
            text = self.texts[path]
            for raw, offset in destinations(text):
                # mask_code preserves newlines but not offsets; count in its output.
                line = mask_code(text)[:offset].count("\n") + 1
                if raw is None:
                    self.error(path, line, "undefined-link-reference")
                    continue
                value = raw[1:-1] if raw.startswith("<") and raw.endswith(">") else raw
                if placeholder(value) or not value or value.startswith("//"):
                    continue
                value = re.sub(r"\\([() ])", r"\1", value)
                try:
                    parts = urlsplit(value)
                except ValueError:
                    self.error(path, line, "invalid-link-target")
                    continue
                if parts.scheme or parts.netloc:
                    continue
                target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
                if not target.is_relative_to(self.root):
                    self.error(path, line, "local-link-outside-repository")
                elif not target.exists():
                    self.error(path, line, "missing-local-link-target")
                elif parts.fragment and target in anchor_cache and unquote(parts.fragment) not in anchor_cache[target]:
                    self.error(path, line, "missing-local-link-anchor")

    def benchmark(self):
        path = self.root / "assets" / "benchmark-cases.json"
        try:
            data = json.loads(self.texts.get(path, ""))
        except json.JSONDecodeError as exc:
            self.error(path, exc.lineno, "invalid-benchmark-json")
            return
        if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
            self.error(path, 1, "invalid-benchmark-cases")
            return
        cases = data["cases"]
        if type(data.get("case_count")) is not int or data["case_count"] != len(cases):
            self.error(path, 1, "benchmark-case-count-mismatch")
        ids = set()
        for index, case in enumerate(cases, 1):
            prefix = f"benchmark-case-{index}"
            if not isinstance(case, dict):
                self.error(path, 1, prefix + "-invalid-object")
                continue
            identifier = case.get("id")
            if not isinstance(identifier, str) or not identifier.strip():
                self.error(path, 1, prefix + "-missing-id")
            elif identifier in ids:
                self.error(path, 1, prefix + "-duplicate-id")
            else:
                ids.add(identifier)
            for key in ("writer_packet", "reviewer_key"):
                if not isinstance(case.get(key), dict) or not case[key]:
                    self.error(path, 1, prefix + "-missing-" + key)
            reviewer = case.get("reviewer_key")
            questions = reviewer.get("comprehension_questions") if isinstance(reviewer, dict) else None
            if not isinstance(questions, list) or not questions:
                self.error(path, 1, prefix + "-missing-comprehension-questions")
                continue
            for question in questions:
                if not isinstance(question, dict) or any(not isinstance(question.get(key), str) or not question[key].strip() for key in ("question", "answer")):
                    self.error(path, 1, prefix + "-missing-question-or-answer")

    def hygiene(self):
        for path, text in self.texts.items():
            for kind, pattern in PATTERNS.items():
                for match in pattern.finditer(text):
                    value = match.group(1) if kind == "credential-assignment" else match.group()
                    if placeholder(value):
                        continue
                    # Explicit dummy tokens are documentation, not credentials.
                    if kind in {"service-token", "credential-assignment"} and (re.search(r"(?:example|placeholder|your[_-]|replace[_-])", value, re.I) or len(set(value)) <= 2):
                        continue
                    self.error(path, text[:match.start()].count("\n") + 1, kind)

    def run(self) -> int:
        self.load()
        self.metadata()
        self.links()
        self.benchmark()
        self.hygiene()
        for path, line, kind in sorted(set(self.errors)):
            print(f"{path}:{line}: {kind}")
        if self.errors:
            print(f"Validation failed: {len(set(self.errors))} issue(s).")
            return 1
        print(f"Validation passed: {len(self.texts)} text files; no writing quality score is assigned.")
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error("repository root must be an existing directory")
    return Validator(args.root).run()


if __name__ == "__main__":
    sys.exit(main())
