"""Validate canonical Agent Skills before they are loaded or released."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
KNOWN_TOOLS = {
    "learning-assistant_get_resource",
    "learning-assistant_list_resources",
}
SECRET_PATTERNS = (
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


def parse_skill(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing opening YAML frontmatter delimiter")
    try:
        frontmatter_text, body = text[4:].split("\n---\n", 1)
    except ValueError as error:
        raise ValueError("missing closing YAML frontmatter delimiter") from error
    frontmatter = yaml.safe_load(frontmatter_text) or {}
    if not isinstance(frontmatter, dict):
        raise ValueError("frontmatter must be a mapping")
    return frontmatter, body


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        frontmatter, body = parse_skill(path)
    except ValueError as error:
        return [str(error)]

    name = frontmatter.get("name")
    description = frontmatter.get("description")
    if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
        errors.append("name must use lowercase letters, digits, and single hyphens")
    elif name != path.parent.name:
        errors.append("name must match the containing directory")
    if not isinstance(description, str) or not 1 <= len(description) <= 1024:
        errors.append("description must contain 1-1024 characters")
    if "## Use this skill when" not in body:
        errors.append("missing 'Use this skill when' section")
    if "## Do not use this skill when" not in body:
        errors.append("missing 'Do not use this skill when' section")
    if "## Evaluation cases" not in body:
        errors.append("missing evaluation cases")

    referenced_tools = set(re.findall(r"`(learning-assistant_[a-z_]+)`", body))
    unknown_tools = referenced_tools - KNOWN_TOOLS
    if unknown_tools:
        errors.append(f"unknown MCP tools: {', '.join(sorted(unknown_tools))}")
    if any(pattern.search(path.read_text(encoding="utf-8")) for pattern in SECRET_PATTERNS):
        errors.append("possible credential or private key detected")
    return errors


def validate_skills(skills_root: Path, repository_root: Path | None = None) -> int:
    skill_files = sorted(skills_root.glob("*/SKILL.md"))
    if not skill_files:
        print("ERROR no skills found", file=sys.stderr)
        return 1
    failed = False
    for skill_file in skill_files:
        errors = validate_skill(skill_file)
        display_path = (
            skill_file.relative_to(repository_root) if repository_root is not None else skill_file
        )
        if errors:
            failed = True
            print(f"FAIL {display_path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {display_path}")
    return 1 if failed else 0
