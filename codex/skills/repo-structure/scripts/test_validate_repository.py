#!/usr/bin/env python3
"""Render one golden repository and prove required adversarial mutations fail."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path


skill = Path(__file__).resolve().parent.parent
skills_root = skill.parent


def run_validator(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(skill / "scripts/validate_repository.py"), str(root), "--package-skill-root", str(skills_root / "package-structure")],
        text=True, capture_output=True,
    )


with tempfile.TemporaryDirectory(prefix="repo-structure-cases-") as raw:
    temp = Path(raw)
    golden = temp / "golden"
    subprocess.run([
        "python3", str(skill / "scripts/render_repository.py"),
        "--target", str(golden), "--name", "governance-fixture",
        "--scope", "@fixture", "--source-condition", "@fixture/source",
        "--versions", str(skill / "assets/version-snapshot.json"),
        "--skills-root", str(skills_root),
    ], check=True, capture_output=True, text=True)
    if run_validator(golden).returncode != 0:
        raise SystemExit("golden fixture failed")

    cases = {}

    duplicate = temp / "duplicate-truth"
    shutil.copytree(golden, duplicate)
    path = duplicate / "docs/documentation-map.json"
    data = json.loads(path.read_text())
    data["owners"].append(dict(data["owners"][0]))
    path.write_text(json.dumps(data))
    cases["duplicate-truth"] = run_validator(duplicate).returncode != 0

    raw_id = temp / "raw-boundary"
    shutil.copytree(golden, raw_id)
    with (raw_id / "packages/domain/src/schemas.ts").open("a") as handle:
        handle.write("\nexport type RawBoundary = { readonly id: string };\n")
    cases["raw-boundary"] = run_validator(raw_id).returncode != 0

    helper = temp / "helper-sprawl"
    shutil.copytree(golden, helper)
    (helper / "packages/domain/src/utils.ts").write_text("export const passthrough = <A>(value: A) => value;\n")
    cases["helper-sprawl"] = run_validator(helper).returncode != 0

    unbounded = temp / "unbounded-receipt"
    shutil.copytree(golden, unbounded)
    (unbounded / "docs/proof/bad.receipt.json").write_text(json.dumps({"status":"passed","excerpt":"x" * 10000}))
    cases["unbounded-receipt"] = run_validator(unbounded).returncode != 0

    retirement = temp / "missing-retirement"
    shutil.copytree(golden, retirement)
    path = retirement / "docs/governance/feedback-controls.json"
    data = json.loads(path.read_text())
    del data["entries"][0]["retireWhen"]
    path.write_text(json.dumps(data))
    cases["missing-retirement"] = run_validator(retirement).returncode != 0

    missing_profile = temp / "missing-docs-maintainer-profile"
    shutil.copytree(golden, missing_profile)
    (missing_profile / ".agents/skills/docs-maintainer/references/repository-profile.md").unlink()
    cases["missing-docs-maintainer-profile"] = run_validator(missing_profile).returncode != 0

    broken_reference = temp / "broken-docs-maintainer-reference"
    shutil.copytree(golden, broken_reference)
    path = broken_reference / ".agents/skills/docs-maintainer/SKILL.md"
    path.write_text(path.read_text().replace("references/repository-profile.md", "references/missing-profile.md"))
    cases["broken-docs-maintainer-reference"] = run_validator(broken_reference).returncode != 0

    competing_owner = temp / "competing-doc-owner"
    shutil.copytree(golden, competing_owner)
    path = competing_owner / ".agents/skills/package-structure/references/repository-profile.md"
    path.write_text(path.read_text() + "\n- Documentation router: `README.md`\n")
    cases["competing-doc-owner"] = run_validator(competing_owner).returncode != 0

    undocumented_export = temp / "undocumented-package-export"
    shutil.copytree(golden, undocumented_export)
    path = undocumented_export / "packages/http-api/README.md"
    path.write_text(path.read_text().replace("- `./api`: public HTTP API contract.\n", ""))
    cases["undocumented-package-export"] = run_validator(undocumented_export).returncode != 0

    missing_runbook_applicability = temp / "missing-runbook-applicability"
    shutil.copytree(golden, missing_runbook_applicability)
    path = missing_runbook_applicability / "packages/rpc/README.md"
    path.write_text(path.read_text().replace("## Runbook applicability", "## Operations"))
    cases["missing-runbook-applicability"] = run_validator(missing_runbook_applicability).returncode != 0

    leaf_owned_boundary_work = temp / "leaf-owned-boundary-work"
    shutil.copytree(golden, leaf_owned_boundary_work)
    path = leaf_owned_boundary_work / "docs/architecture/frontend-composition.md"
    path.write_text(
        path.read_text().replace(
            "Routes and feature boundaries own data loading, Effect/service execution,\n"
            "mutations, commands, shared state, workflow/error policy, and SSR restoration.\n"
            "Presentation leaves receive narrow readonly values and action callbacks, then\n"
            "own rendering, accessibility, pure derivation, and genuinely local UI state.",
            "Routes own cross-feature orchestration and SSR restoration. A leaf owns its\n"
            "specific query, read, command, skeleton, and fallback."
        )
    )
    cases["leaf-owned-boundary-work"] = run_validator(
        leaf_owned_boundary_work
    ).returncode != 0

    leaf_hook_boundary_work = temp / "leaf-hook-boundary-work"
    shutil.copytree(golden, leaf_hook_boundary_work)
    path = leaf_hook_boundary_work / "docs/architecture/frontend-composition.md"
    path.write_text(
        path.read_text().replace(
            "Presentation leaves receive narrow readonly values and action callbacks, then\n"
            "own rendering, accessibility, pure derivation, and genuinely local UI state.",
            "Presentation leaves directly use useQuery and useMutation because they render\n"
            "the result."
        )
    )
    cases["leaf-hook-boundary-work"] = run_validator(
        leaf_hook_boundary_work
    ).returncode != 0

    if not all(cases.values()):
        raise SystemExit(json.dumps({"status":"failed","cases":cases}))
    print(json.dumps({"status":"passed","golden":"validated","adversarial":cases,"nonClaims":["No dependencies were installed and no provider behavior was tested."]}))
