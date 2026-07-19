#!/usr/bin/env python3
"""Render a repository atomically and compose canonical package assets."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


SKILL = Path(__file__).resolve().parent.parent
SCOPE = re.compile(r"^@[a-z0-9][a-z0-9._-]*$")


def resolve_skill(skills_root: Path, name: str) -> Path:
    skill = (skills_root / name).resolve(strict=True)
    if not (skill / "SKILL.md").is_file():
        raise ValueError(f"missing {name} skill at {skill}")
    return skill


def load_package_renderer(package_skill: Path):
    renderer = package_skill / "scripts/render_package.py"
    if not renderer.is_file():
        raise ValueError(f"missing package renderer at {renderer}")
    spec = importlib.util.spec_from_file_location("package_renderer", renderer)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {renderer}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def target_path(raw: str) -> Path:
    path = Path(raw)
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError("target must be absolute and contain no '..'")
    parent = path.parent.resolve(strict=True)
    if path.exists() or path.is_symlink():
        raise ValueError("target must not exist")
    if parent.is_symlink() or path.resolve(strict=False) in {Path("/"), Path.home().resolve()}:
        raise ValueError("unsafe target")
    return parent / path.name


def copy_assets(stage: Path, replacements: dict[str, str]) -> None:
    root = SKILL / "assets/repository"
    for source in sorted(root.rglob("*")):
        if source.is_symlink():
            raise ValueError(f"asset symlink forbidden: {source}")
        if not source.is_file():
            continue
        relative = Path(str(source.relative_to(root)).removesuffix(".tmpl"))
        output = stage / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        text = source.read_text()
        for old, new in replacements.items():
            text = text.replace(old, new)
        output.write_text(text)


def install_skill_baseline(stage: Path, skills_root: Path) -> None:
    destination = stage / ".agents/skills"
    for name in ("prd-writer", "prd-review", "prd-implementer", "effect-client-wrapper"):
        source = resolve_skill(skills_root, name)
        target = destination / name
        target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / "SKILL.md", target / "SKILL.md")
        if (source / "agents/openai.yaml").is_file():
            (target / "agents").mkdir(exist_ok=True)
            shutil.copy2(source / "agents/openai.yaml", target / "agents/openai.yaml")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--scope", required=True)
    parser.add_argument("--source-condition", required=True)
    parser.add_argument("--versions", required=True)
    parser.add_argument("--skills-root")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9][a-z0-9._-]*", args.name):
        raise ValueError("invalid repository name")
    if not SCOPE.fullmatch(args.scope):
        raise ValueError("invalid package scope")
    target = target_path(args.target)
    skills_root = (
        Path(args.skills_root).resolve(strict=True)
        if args.skills_root
        else SKILL.parent
    )
    package_skill = resolve_skill(skills_root, "package-structure")
    versions_path = Path(args.versions).resolve(strict=True)
    versions = json.loads(versions_path.read_text())
    packages = versions["packages"]
    effect_versions = {packages[name] for name in ("effect", "@effect/platform-bun", "@effect/platform-node", "@effect/vitest")}
    if len(effect_versions) != 1:
        raise ValueError("Effect ecosystem versions must match exactly")
    replacements = {"__REPO_NAME__": args.name, "__SCOPE__": args.scope, "__SOURCE_CONDITION__": args.source_condition, "__RESOLVED_AT__": versions["resolvedAt"]}
    replacements.update({f"__VERSION_{name.upper().replace('@', '').replace('/', '_').replace('-', '_')}__": value for name, value in packages.items()})
    stage = Path(tempfile.mkdtemp(prefix=f".{target.name}.stage-", dir=target.parent))
    try:
        copy_assets(stage, replacements)
        install_skill_baseline(stage, skills_root)
        package_renderer = load_package_renderer(package_skill)
        for kind, directory, package_name in (
            ("effect-service", "domain", f"{args.scope}/domain"),
            ("rpc", "rpc", f"{args.scope}/rpc"),
            ("http-api", "http-api", f"{args.scope}/http-api"),
        ):
            namespace = argparse.Namespace(
                kind=kind,
                target=str(stage / "packages" / directory),
                package_name=package_name,
                source_condition=args.source_condition,
                versions=str(versions_path),
                domain_package=None if kind == "effect-service" else f"{args.scope}/domain",
            )
            package_renderer.render(namespace)
        manifest = {
            "name": args.name,
            "scope": args.scope,
            "sourceCondition": args.source_condition,
            "versionSnapshot": {
                "resolvedAt": versions["resolvedAt"],
                "sha256": hashlib.sha256(versions_path.read_bytes()).hexdigest(),
            },
        }
        (stage / "repo-structure.render.json").write_text(json.dumps(manifest, indent=2) + "\n")
        subprocess.run(
            [
                "python3",
                str(SKILL / "scripts/validate_repository.py"),
                str(stage),
                "--package-skill-root",
                str(package_skill),
            ],
            check=True,
        )
        os.replace(stage, target)
    except BaseException:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    print(target)


if __name__ == "__main__":
    main()
