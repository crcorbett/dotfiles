#!/usr/bin/env python3
"""Validate the shared PRD skills against bounded harness contradictions."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = Path(__file__).with_name("prd-harness-cases.json")
REQUIRED_TAGS = {"ritual", "vague-proof", "helper-sprawl", "effect-client-wrapper", "runbook", "retrieval", "delegation"}


def fail(invariant: str, target: str, recovery: str) -> int:
    print(json.dumps({"status": "failed", "invariant": invariant, "target": target, "recovery": recovery}))
    return 1


def main() -> int:
    cases: dict[str, Any] = json.loads(CASES_PATH.read_text())
    if cases.get("schemaVersion") != 1:
        return fail("supported case schema", str(CASES_PATH), "Set schemaVersion to 1.")

    checked_skills = 0
    for contract in cases.get("skills", []):
        skill_path = ROOT / "skills" / contract["name"] / "SKILL.md"
        text = skill_path.read_text()
        folded = " ".join(text.casefold().split())
        for phrase in contract["requiredPhrases"]:
            if " ".join(phrase.casefold().split()) not in folded:
                return fail("required harness phrase", f"{contract['name']}:{phrase}", "Restore the owning PRD contract and rerun this validator.")
        for phrase in contract["forbiddenPhrases"]:
            if " ".join(phrase.casefold().split()) in folded:
                return fail("forbidden contradictory phrase", f"{contract['name']}:{phrase}", "Remove the contradiction without weakening local-truth precedence.")
        for paragraph in (part for part in text.split("\n\n") if "deepwiki" in part.casefold()):
            lowered = paragraph.casefold()
            if not any(marker in lowered for marker in ("upstream", "third-party", "never use it to inspect", "do not use deepwiki to analyze")):
                return fail("DeepWiki is upstream-only", contract["name"], "Describe DeepWiki only as upstream package/library evidence and route local truth to the checkout.")
        checked_skills += 1

    observed_tags: set[str] = set()
    synthetic = cases.get("syntheticCases", [])
    for case in synthetic:
        decision = case.get("expectedDecision")
        if decision not in {"accept", "reject"}:
            return fail("synthetic decision is explicit", case.get("id", "unknown"), "Use accept or reject.")
        observed_tags.update(case.get("tags", []))
        if decision == "reject" and (not case.get("violatedInvariant") or not case.get("recovery")):
            return fail("rejection has invariant and recovery", case.get("id", "unknown"), "Add the violated invariant and bounded recovery hint.")
        if not case.get("owner"):
            return fail("synthetic case has semantic owner", case.get("id", "unknown"), "Name the earliest durable owner.")

    missing = sorted(REQUIRED_TAGS - observed_tags)
    if missing:
        return fail("required contradiction coverage", ",".join(missing), "Add a bounded synthetic case for every missing tag.")

    print(json.dumps({
        "status": "passed",
        "skills": checked_skills,
        "syntheticCases": len(synthetic),
        "tags": sorted(observed_tags),
        "postcondition": "Shared PRD skills retain the harness contract, reject seeded ritual and architecture contradictions, and restrict DeepWiki to upstream evidence.",
        "nonClaims": ["Static fixtures do not prove fresh-worker retrieval or repository-specific correctness."],
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
