#!/usr/bin/env python3
"""Validate, install, or roll back the bounded shared Codex skill projection."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPOSITORY_ROOT / "codex" / "skills"
MANIFEST_PATH = SOURCE_ROOT / "manifest.json"


class ProjectionError(RuntimeError):
    pass


def digest_tree(root: Path) -> tuple[int, str]:
    if not root.is_dir() or root.is_symlink():
        raise ProjectionError(f"skill source must be a real directory: {root}")
    rows: list[str] = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ProjectionError(f"symlinks are forbidden in projected skills: {path}")
        if path.is_file():
            relative = path.relative_to(root).as_posix()
            rows.append(f"{relative}\t{hashlib.sha256(path.read_bytes()).hexdigest()}\n")
    return len(rows), hashlib.sha256("".join(rows).encode()).hexdigest()


def projection_digest(skills: list[dict[str, Any]]) -> str:
    rows = [
        f"{item['name']}\t{item['fileCount']}\t{item['treeDigest']}\n"
        for item in sorted(skills, key=lambda item: item["name"])
    ]
    return hashlib.sha256("".join(rows).encode()).hexdigest()


def load_manifest() -> dict[str, Any]:
    data = json.loads(MANIFEST_PATH.read_text())
    required = {
        "schemaVersion",
        "sourceRepository",
        "sourcePath",
        "installedProjection",
        "projectionDigest",
        "skills",
    }
    if set(data) - (required | {"$schema"}) or not required <= set(data):
        raise ProjectionError("manifest keys do not match the projection contract")
    if data["schemaVersion"] != 1 or data["sourcePath"] != "codex/skills":
        raise ProjectionError("unsupported skill manifest")
    names = [item["name"] for item in data["skills"]]
    if names != sorted(names) or len(names) != len(set(names)):
        raise ProjectionError("manifest skill names must be unique and sorted")
    return data


def verify_source(manifest: dict[str, Any]) -> None:
    for item in manifest["skills"]:
        count, digest = digest_tree(SOURCE_ROOT / item["name"])
        if (count, digest) != (item["fileCount"], item["treeDigest"]):
            raise ProjectionError(
                f"source digest mismatch for {item['name']}: expected "
                f"{item['fileCount']}/{item['treeDigest']}, got {count}/{digest}"
            )
    if projection_digest(manifest["skills"]) != manifest["projectionDigest"]:
        raise ProjectionError("projection digest does not match manifest entries")


def validate_target_root(target_root: Path) -> Path:
    target = target_root.expanduser().absolute()
    home = Path.home().resolve()
    if target in {Path("/"), home}:
        raise ProjectionError(f"unsafe target root: {target}")
    if target.exists() and target.is_symlink():
        raise ProjectionError(f"target root may not be a symlink: {target}")
    if target.parent == target:
        raise ProjectionError(f"target root has no safe parent: {target}")
    return target


def source_revision() -> dict[str, Any]:
    revision = subprocess.run(
        ["git", "-C", str(REPOSITORY_ROOT), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    dirty = subprocess.run(
        ["git", "-C", str(REPOSITORY_ROOT), "status", "--porcelain", "--", "codex/skills", "scripts/project-codex-skills.py"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return {"repository": str(REPOSITORY_ROOT), "revision": revision, "dirty": bool(dirty)}


def check_projection(manifest: dict[str, Any], target: Path) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    for item in manifest["skills"]:
        installed = target / item["name"]
        try:
            count, digest = digest_tree(installed)
            passed = (count, digest) == (item["fileCount"], item["treeDigest"])
            checks.append({"skill": item["name"], "status": "passed" if passed else "failed", "fileCount": count, "treeDigest": digest})
        except ProjectionError as error:
            checks.append({"skill": item["name"], "status": "failed", "error": str(error)})
    return checks


def backup_id(manifest: dict[str, Any]) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    return f"{timestamp}-{manifest['projectionDigest'][:12]}"


def copy_validated_source(manifest: dict[str, Any], staging: Path) -> None:
    for item in manifest["skills"]:
        destination = staging / item["name"]
        shutil.copytree(SOURCE_ROOT / item["name"], destination)
        count, digest = digest_tree(destination)
        if (count, digest) != (item["fileCount"], item["treeDigest"]):
            raise ProjectionError(f"staged projection failed validation for {item['name']}")


def install(manifest: dict[str, Any], target: Path) -> dict[str, Any]:
    target.mkdir(parents=True, exist_ok=True)
    backup_root = target.parent / "codex-skill-projection-backups"
    backup = backup_root / backup_id(manifest)
    if backup.exists():
        raise ProjectionError(f"backup already exists: {backup}")
    backup.mkdir(parents=True)
    moved: list[str] = []
    installed: list[str] = []
    previous_projection: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="codex-skills-stage-", dir=target.parent) as temporary:
        staging = Path(temporary)
        copy_validated_source(manifest, staging)
        try:
            for item in manifest["skills"]:
                name = item["name"]
                current = target / name
                if current.is_symlink():
                    raise ProjectionError(f"installed skill may not be a symlink: {current}")
                if current.exists():
                    count, digest = digest_tree(current)
                    previous_projection.append({"skill": name, "fileCount": count, "treeDigest": digest})
                    os.replace(current, backup / name)
                    moved.append(name)
                os.replace(staging / name, current)
                installed.append(name)
        except Exception:
            for name in reversed(installed):
                current = target / name
                if current.exists():
                    shutil.rmtree(current)
            for name in reversed(moved):
                os.replace(backup / name, target / name)
            raise
    checks = check_projection(manifest, target)
    if any(check["status"] != "passed" for check in checks):
        raise ProjectionError("installed projection failed readback; run rollback with the receipt backup")
    receipt = {
        "status": "passed",
        "operation": "install",
        "source": source_revision(),
        "projectionDigest": manifest["projectionDigest"],
        "skills": [item["name"] for item in manifest["skills"]],
        "target": str(target),
        "backup": str(backup),
        "previousProjection": previous_projection,
        "checks": checks,
        "postcondition": "Every named installed skill matches the canonical manifest after atomic per-skill replacement.",
        "nonclaims": ["Unlisted installed skills were not inspected or changed.", "This receipt does not publish or push the source repository."],
    }
    (backup / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return receipt


def rollback(manifest: dict[str, Any], target: Path, requested: str) -> dict[str, Any]:
    backup_root = (target.parent / "codex-skill-projection-backups").resolve()
    backup = (backup_root / requested).resolve()
    if backup.parent != backup_root or not backup.is_dir():
        raise ProjectionError(f"rollback backup is not an exact backup id under {backup_root}")
    receipt_path = backup / "receipt.json"
    if not receipt_path.is_file():
        raise ProjectionError(f"rollback backup has no installation receipt: {receipt_path}")
    receipt = json.loads(receipt_path.read_text())
    prior = {item["skill"]: item for item in receipt.get("previousProjection", [])}
    available = [item["name"] for item in manifest["skills"] if (backup / item["name"]).is_dir()]
    if not available:
        raise ProjectionError(f"backup contains none of the manifest skills: {backup}")
    for name in available:
        if name not in prior:
            raise ProjectionError(f"rollback receipt has no digest for {name}")
        count, digest = digest_tree(backup / name)
        if (count, digest) != (prior[name]["fileCount"], prior[name]["treeDigest"]):
            raise ProjectionError(f"rollback backup digest mismatch for {name}")
    quarantine = backup_root / f"pre-rollback-{backup_id(manifest)}"
    quarantine.mkdir(parents=True)
    restored: list[str] = []
    try:
        for name in available:
            current = target / name
            if current.is_symlink():
                raise ProjectionError(f"installed skill may not be a symlink: {current}")
            if current.exists():
                os.replace(current, quarantine / name)
            os.replace(backup / name, current)
            restored.append(name)
    except Exception:
        for name in reversed(restored):
            current = target / name
            if current.exists():
                os.replace(current, backup / name)
            if (quarantine / name).exists():
                os.replace(quarantine / name, current)
        raise
    return {
        "status": "passed",
        "operation": "rollback",
        "restored": restored,
        "restoredProjection": [prior[name] for name in restored],
        "target": str(target),
        "replacedProjectionBackup": str(quarantine),
        "postcondition": "The selected last-known-good skill directories replaced the corresponding installed projection.",
        "nonclaims": ["Skills absent from the selected backup were not changed."],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--install", action="store_true")
    action.add_argument("--rollback", metavar="BACKUP_ID")
    parser.add_argument("--target-root", type=Path, default=Path.home() / ".codex" / "skills")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        manifest = load_manifest()
        verify_source(manifest)
        target = validate_target_root(args.target_root)
        if args.check:
            checks = check_projection(manifest, target)
            passed = all(check["status"] == "passed" for check in checks)
            result = {
                "status": "passed" if passed else "failed",
                "operation": "check",
                "source": source_revision(),
                "projectionDigest": manifest["projectionDigest"],
                "target": str(target),
                "checks": checks,
                "postcondition": "Every named installed skill matches the canonical manifest." if passed else "At least one named installed skill differs from the canonical manifest.",
                "recovery": None if passed else "Review the bounded checks, then run --install or restore an identified backup.",
            }
        elif args.install:
            result = install(manifest, target)
        else:
            result = rollback(manifest, target, args.rollback)
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "passed" else 1
    except (OSError, ProjectionError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "failed", "error": str(error), "recovery": "Correct the exact reported invariant; no publication or network operation was attempted."}, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
