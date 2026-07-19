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

    if not all(cases.values()):
        raise SystemExit(json.dumps({"status":"failed","cases":cases}))
    print(json.dumps({"status":"passed","golden":"validated","adversarial":cases,"nonClaims":["No dependencies were installed and no provider behavior was tested."]}))
