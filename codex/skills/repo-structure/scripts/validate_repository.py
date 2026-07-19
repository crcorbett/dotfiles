#!/usr/bin/env python3
"""Validate generated repository topology and contracts."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


SKILL = Path(__file__).resolve().parent.parent
PERSONAL_ROOT = "/" + "Users" + "/"

parser = argparse.ArgumentParser()
parser.add_argument("repository")
parser.add_argument("--package-skill-root")
args = parser.parse_args()

root = Path(args.repository).resolve(strict=True)
package_skill = (
    Path(args.package_skill_root).resolve(strict=True)
    if args.package_skill_root
    else (SKILL.parent / "package-structure").resolve(strict=True)
)
package_validator = package_skill / "scripts/validate_package.py"
if not package_validator.is_file():
    raise SystemExit(f"missing package validator: {package_validator}")
for path in root.rglob("*"):
    if not path.is_file():
        continue
    text = path.read_text(errors="ignore")
    if PERSONAL_ROOT in text:
        raise SystemExit(f"personal absolute path in {path.relative_to(root)}")
    if re.search(r"__[A-Z][A-Z0-9_]*__", text):
        raise SystemExit(f"unresolved template token in {path.relative_to(root)}")
required = [
    "AGENTS.md", "README.md", "package.json", "tsconfig.base.json", "turbo.json",
    "oxlint.config.ts", "oxfmt.config.ts", "knip.ts", "knip.production.ts",
    "apps/web/package.json", "apps/web/src/router.tsx", "apps/web/src/server.ts",
    "packages/domain/package.json", "packages/rpc/package.json", "packages/http-api/package.json",
    "packages/effect-start/package.json", "docs/architecture/effect-services.md",
    "docs/architecture/package-ownership.md", "docs/architecture/frontend-composition.md",
    "docs/architecture/testing-and-quality.md", "tools/oxlint/policy.test.ts",
    ".agents/skills/package-structure/SKILL.md",
]
missing = [path for path in required if not (root / path).is_file()]
if missing:
    raise SystemExit(f"missing repository files: {missing}")
manifest = json.loads((root / "package.json").read_text())
effect = manifest["workspaces"]["catalogs"]["effect"]
if len(set(effect.values())) != 1:
    raise SystemExit("Effect catalog must be aligned exactly")
for workflow in (root / ".github/workflows").glob("*.yml"):
    for line in workflow.read_text().splitlines():
        if "uses:" in line and not re.search(r"@[0-9a-f]{40}(?:\s|#|$)", line):
            raise SystemExit(f"mutable action in {workflow.relative_to(root)}: {line.strip()}")
for skill in ("package-structure", "prd-writer", "prd-review", "prd-implementer", "effect-client-wrapper"):
    skill_root = root / ".agents/skills" / skill
    if not (skill_root / "SKILL.md").is_file() or not (skill_root / "agents/openai.yaml").is_file():
        raise SystemExit(f"incomplete local skill: {skill}")
for package in ("domain", "rpc", "http-api"):
    subprocess.run(["python3", str(package_validator), str(root / "packages" / package)], check=True)
print(f"validated repository: {root}")
