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
    if any(part in {"node_modules", "dist", ".git", ".output", ".turbo"} for part in path.parts):
        continue
    text = path.read_text(errors="ignore")
    if PERSONAL_ROOT in text:
        raise SystemExit(f"personal absolute path in {path.relative_to(root)}")
    if re.search(r"__[A-Z][A-Z0-9_]*__|\*\*[A-Z][A-Z0-9_]*\*\*", text):
        raise SystemExit(f"unresolved template token in {path.relative_to(root)}")
required = [
    "AGENTS.md", "README.md", "ARCHITECTURE.md", "package.json", "tsconfig.base.json", "tsconfig.infrastructure.json", "turbo.json",
    "oxlint.config.ts", "oxfmt.config.ts", "knip.ts", "knip.production.ts",
    "apps/web/package.json", "apps/web/src/router.tsx", "apps/web/src/server.ts",
    "packages/domain/package.json", "packages/rpc/package.json", "packages/http-api/package.json",
    "packages/effect-start/package.json", "docs/architecture/effect-services.md",
    "alchemy.run.ts", "docs/README.md", "docs/documentation-map.json",
    "docs/documentation-map.schema.json", "docs/architecture/cloudflare-alchemy.md",
    "docs/architecture/transports.md",
    "docs/runbooks/README.md", "docs/runbooks/_template.md",
    "docs/critical-journeys/README.md", "docs/critical-journeys/journeys.json",
    "docs/proof/README.md", "docs/proof/proof-packet.template.json", "docs/governance/authority.md",
    "docs/governance/automation-register.json", "docs/governance/feedback-controls.json",
    "docs/evidence/README.md", "tools/governance/validate.py",
    "tools/governance/schemas/bounded-receipt.schema.json",
    "tools/governance/schemas/proof-packet.schema.json",
    "tools/governance/schemas/task-plan.schema.json",
    "repo-structure.render.json",
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
subprocess.run(["python3", str(root / "tools/governance/validate.py"), str(root)], check=True)
receipt = json.loads((root / "repo-structure.render.json").read_text())
if receipt.get("phase") not in {"rendered", "bootstrapped"}:
    raise SystemExit("render receipt needs rendered or bootstrapped phase")
if "alchemy" not in receipt.get("selectedVersions", {}):
    raise SystemExit("render receipt must select and qualify Alchemy explicitly")
print(json.dumps({"status":"passed","target":str(root),"postcondition":"repository topology, packages, governance, and render receipt validated","nonClaims":["No install, build, journey, or provider behavior is implied."]}))
