#!/usr/bin/env python3
"""Guard the standalone method against losing a required coverage module."""

from __future__ import annotations

from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
COVERAGE = SKILL_ROOT / "references" / "embedded-coverage.md"

REQUIRED_MODULES = {
    "unified visual argument": ("rules 1 and 22", "question, evidence, comparison, and qualification"),
    "retained dimensions and disclosed loss": ("rules 6 and 15", "grain, denominator, transformation"),
    "overview, detail, and context": ("rules 9 and 11", "macro pattern, local inspection"),
    "layering and separation": ("rules 17, 25, and 29", "primary evidence dominates"),
    "repeated frames and small multiples": ("rules 5 and 10", "mark, scale, interval, and order"),
    "colour as evidence": ("rules 18 to 21 and 31", "ordered colour agrees"),
    "narrative through time and space": ("rules 15 and 32", "event/route order"),
    "proportional graphical integrity": ("rules 3 to 7", "visual/data effect"),
    "three independent competences": ("rule 2", "domain, statistical, and visual"),
    "mark economy and revision": ("rules 14, 23 to 25", "erasability test"),
    "appropriate reading surface": ("rules 8, 12, 13, and 16", "table-graphic, chart, and small-multiple"),
    "dense and exact reading": ("examples 1, 4, and 7", "density, exact lookup"),
    "scale relationship and discontinuity": ("rule 26", "visibly marked"),
    "editorial production": ("rules 22, 27 to 30", "full/reduced/grayscale/narrow"),
    "exceptions and independent challenge": ("rules 33 and 34", "separate reviewer"),
}

REQUIRED_SURFACES = (
    "SKILL.md",
    "references/foundations.md",
    "references/conceptual-framework.md",
    "references/rulebook.md",
    "references/evaluation-rubric.md",
    "references/chart-selection.md",
    "references/editorial-production.md",
    "references/examples.md",
    "assets/chart-spec.template.json",
    "scripts/evaluate_spec.py",
)


def main() -> int:
    text = COVERAGE.read_text(encoding="utf-8").lower()
    missing_modules = [module for module, links in REQUIRED_MODULES.items() if module not in text or any(link not in text for link in links)]
    missing_surfaces = [surface for surface in REQUIRED_SURFACES if not (SKILL_ROOT / surface).is_file()]
    if missing_modules:
        raise SystemExit(f"FAIL: coverage ledger is missing modules: {', '.join(missing_modules)}")
    if missing_surfaces:
        raise SystemExit(f"FAIL: required skill surfaces are missing: {', '.join(missing_surfaces)}")
    print(f"PASS: {len(REQUIRED_MODULES)} method-rule-evidence coverage modules and {len(REQUIRED_SURFACES)} skill surfaces")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
