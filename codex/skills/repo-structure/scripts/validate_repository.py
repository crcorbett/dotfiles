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
    ".agents/skills/docs-maintainer/SKILL.md",
    ".agents/skills/docs-maintainer/agents/openai.yaml",
    ".agents/skills/docs-maintainer/references/repository-profile.md",
]
missing = [path for path in required if not (root / path).is_file()]
if missing:
    raise SystemExit(f"missing repository files: {missing}")
frontend_composition = (
    root / "docs/architecture/frontend-composition.md"
).read_text()
for phrase in (
    "Routes and feature boundaries own data loading, Effect/service execution",
    "Presentation leaves receive narrow readonly values and action callbacks",
):
    if phrase not in frontend_composition:
        raise SystemExit(
            f"frontend composition missing boundary contract: {phrase}"
        )
leaf_boundary_contradiction = re.compile(
    r"\b(?:data-bearing\s+|presentation\s+)?(?:leaf|leaves)\s+"
    r"(?:should\s+)?own(?:s|ed|ing)?\s+(?:their\s+(?:own\s+)?)?"
    r"(?:the\s+)?(?:narrow\s+|specific\s+)?"
    r"(?:quer(?:y|ies)|reads?|data(?:\s+loading)?|fetch(?:ing)?|acquisition|"
    r"effects?(?:\s+execution)?|services?|rpc|mutations?|commands?|"
    r"shared\s+(?:state|workflows?))\b",
    re.IGNORECASE,
)
leaf_boundary_execution = re.compile(
    r"\b(?:presentation\s+|data-bearing\s+)?"
    r"(?:leaf|leaves|[A-Z][A-Za-z0-9]*Leaf)\b\s+"
    r"(?:components?\s+)?(?:should\s+)?(?:directly\s+)?"
    r"(?:calls?|uses?|reads?|fetches?|executes?|runs?|invokes?)\b"
    r".{0,140}\b(?:use(?:Suspense|Infinite)?Quer(?:y|ies)|useMutation|"
    r"Route\.use(?:LoaderData|Params|Search)|Effect\.run"
    r"(?:Sync|Promise|PromiseExit)|services?|rpc|queries|mutations?|"
    r"commands?|shared\s+atoms?)\b",
    re.IGNORECASE | re.DOTALL,
)
leaf_hook_execution = re.compile(
    r"\bfunction\s+[A-Z][A-Za-z0-9]*Leaf\s*\([^)]*\)\s*\{"
    r".{0,220}\b(?:use(?:Suspense|Infinite)?Quer(?:y|ies)|useMutation|"
    r"Route\.use(?:LoaderData|Params|Search)|Effect\.run"
    r"(?:Sync|Promise|PromiseExit))\b",
    re.IGNORECASE | re.DOTALL,
)
if (
    leaf_boundary_contradiction.search(frontend_composition)
    or leaf_boundary_execution.search(frontend_composition)
    or leaf_hook_execution.search(frontend_composition)
):
    raise SystemExit(
        "frontend composition assigns data or workflow execution to a presentation leaf"
    )
manifest = json.loads((root / "package.json").read_text())
effect = manifest["workspaces"]["catalogs"]["effect"]
if len(set(effect.values())) != 1:
    raise SystemExit("Effect catalog must be aligned exactly")
for workflow in (root / ".github/workflows").glob("*.yml"):
    for line in workflow.read_text().splitlines():
        if "uses:" in line and not re.search(r"@[0-9a-f]{40}(?:\s|#|$)", line):
            raise SystemExit(f"mutable action in {workflow.relative_to(root)}: {line.strip()}")
for skill in ("docs-maintainer", "package-structure", "prd-writer", "prd-review", "prd-implementer", "effect-client-wrapper"):
    skill_root = root / ".agents/skills" / skill
    if not (skill_root / "SKILL.md").is_file() or not (skill_root / "agents/openai.yaml").is_file():
        raise SystemExit(f"incomplete local skill: {skill}")
skill_link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
for markdown in (root / ".agents/skills").rglob("*.md"):
    for raw in skill_link_pattern.findall(markdown.read_text()):
        if raw.startswith(("http://", "https://", "#")):
            continue
        target = (markdown.parent / raw.split("#", 1)[0]).resolve()
        if root not in target.parents or not target.exists():
            raise SystemExit(f"broken local skill reference: {markdown.relative_to(root)} -> {raw}")
docs_skill = root / ".agents/skills/docs-maintainer"
docs_skill_text = (docs_skill / "SKILL.md").read_text()
if "references/repository-profile.md" not in docs_skill_text:
    raise SystemExit("docs-maintainer must route to its repository profile")
docs_profile = (docs_skill / "references/repository-profile.md").read_text()
for owner in ("docs/README.md", "docs/runbooks/", "docs/critical-journeys/journeys.json", "docs/proof/", "docs/governance/", "docs/evidence/"):
    if owner not in docs_profile:
        raise SystemExit(f"docs-maintainer profile missing owner: {owner}")
package_profile = (root / ".agents/skills/package-structure/references/repository-profile.md").read_text()
if "Documentation router:" in package_profile or "Runbook owner:" in package_profile:
    raise SystemExit("package profile must not compete with docs-maintainer ownership")
for package in ("domain", "rpc", "http-api"):
    subprocess.run(["python3", str(package_validator), str(root / "packages" / package)], check=True)
subprocess.run(["python3", str(root / "tools/governance/validate.py"), str(root)], check=True)
receipt = json.loads((root / "repo-structure.render.json").read_text())
if receipt.get("phase") not in {"rendered", "bootstrapped"}:
    raise SystemExit("render receipt needs rendered or bootstrapped phase")
if "alchemy" not in receipt.get("selectedVersions", {}):
    raise SystemExit("render receipt must select and qualify Alchemy explicitly")
print(json.dumps({"status":"passed","target":str(root),"postcondition":"repository topology, packages, governance, and render receipt validated","nonClaims":["No install, build, journey, or provider behavior is implied."]}))
