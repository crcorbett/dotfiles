#!/usr/bin/env python3
"""Lint a portable visualisation-design record for high-risk omissions."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REQUIRED = (
    "question",
    "display_role",
    "data",
    "mark",
    "encoding",
    "scales",
    "form_choice",
    "hierarchy",
    "competence",
    "provenance",
)


def get(mapping: dict[str, Any], path: str) -> Any:
    value: Any = mapping
    for part in path.split("."):
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    return value


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: evaluate_spec.py CHART-SPEC.json", file=sys.stderr)
        return 2

    source = Path(sys.argv[1])
    try:
        spec = json.loads(source.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read {source}: {exc}", file=sys.stderr)
        return 2
    if not isinstance(spec, dict):
        print("ERROR: specification must be a JSON object", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []
    for field in REQUIRED:
        if not spec.get(field):
            errors.append(f"missing required field: {field}")

    mark = str(spec.get("mark", "")).lower()
    baseline = get(spec, "scales.y.baseline")
    if mark in {"bar", "area"} and baseline != 0:
        errors.append(f"{mark} requires scales.y.baseline = 0")
    if mark == "line" and baseline is None:
        warnings.append("line chart has no declared y baseline/domain rationale")

    if not get(spec, "integrity.design_invariance"):
        errors.append("record integrity.design_invariance for comparable observations")
    effect_ratio = get(spec, "integrity.visual_effect_ratio")
    if effect_ratio is not None:
        if not isinstance(effect_ratio, (int, float)) or isinstance(effect_ratio, bool):
            errors.append("integrity.visual_effect_ratio must be a number or null")
        elif not 0.95 <= effect_ratio <= 1.05:
            errors.append(
                "integrity.visual_effect_ratio must be between 0.95 and 1.05; "
                "redesign or explain the display"
            )
    elif not get(spec, "integrity.effect_ratio_note"):
        warnings.append("no visual-effect ratio or applicability note recorded")

    eyespan = get(spec, "comparison.eyespan")
    alternative_view = get(spec, "comparison.alternative_view")
    if eyespan is not True and not alternative_view:
        errors.append("record comparison.eyespan = true or a comparison.alternative_view")

    if not get(spec, "form_choice.chosen_form"):
        errors.append("record form_choice.chosen_form")
    if not get(spec, "form_choice.task_function"):
        errors.append("record form_choice.task_function from the data task")
    if not get(spec, "form_choice.candidate_catalogue"):
        errors.append("record form_choice.candidate_catalogue")
    candidates = get(spec, "form_choice.candidate_forms")
    if not isinstance(candidates, list) or len(candidates) < 2:
        errors.append("form_choice.candidate_forms needs at least two task-fit candidates")
    elif any(not isinstance(candidate, dict) or not candidate.get("form") or not candidate.get("fit") for candidate in candidates):
        errors.append("each form_choice.candidate_forms entry needs form and fit")
    alternatives = get(spec, "form_choice.alternatives_considered")
    if not isinstance(alternatives, list) or not alternatives:
        errors.append("form_choice.alternatives_considered needs at least one alternative")
    if get(spec, "form_choice.dual_scale.used") is True:
        if not get(spec, "form_choice.dual_scale.rationale"):
            errors.append("dual scale needs a rationale")
        if not get(spec, "form_choice.dual_scale.zero_alignment"):
            errors.append("dual scale needs a zero-alignment assessment")
        if not get(spec, "form_choice.dual_scale.alternative_considered"):
            errors.append("dual scale needs an aligned-panel or index alternative")

    for field in ("primary_evidence", "neutral_context", "accent_focus"):
        if not get(spec, f"hierarchy.{field}"):
            errors.append(f"record hierarchy.{field}")
    for field in ("substantive", "statistical", "visual"):
        if not get(spec, f"competence.{field}"):
            errors.append(f"record competence.{field}")

    if get(spec, "encoding.y") and not get(spec, "encoding.y.unit"):
        errors.append("quantitative y encoding needs a unit")
    colour = get(spec, "encoding.colour")
    if colour:
        if not get(spec, "encoding.colour.purpose"):
            errors.append("colour encoding needs a stated purpose")
        if not get(spec, "encoding.colour.necessity"):
            errors.append("colour encoding needs a necessity statement; prefer neutral non-focus marks")
        if not get(spec, "encoding.colour.semantic_rationale"):
            errors.append("colour encoding needs a semantic rationale; avoid false status signals")
    if not get(spec, "data.denominator"):
        warnings.append("no denominator recorded; state why it is not applicable")
    if not spec.get("uncertainty"):
        warnings.append("no uncertainty/missingness statement")
    if not spec.get("annotations"):
        warnings.append("no annotation or finding statement")
    if not get(spec, "accessibility.not_colour_only"):
        errors.append("accessibility.not_colour_only must be true")
    if not get(spec, "accessibility.reduced_size_checked"):
        warnings.append("reduced-size inspection has not been recorded")
    if spec.get("causal_claim") and not get(spec, "causal_design"):
        errors.append("causal claim needs a recorded causal design")
    if not get(spec, "review.builder"):
        errors.append("record review.builder")
    if not get(spec, "review.independent_reviewer"):
        errors.append("release review needs review.independent_reviewer")
    if not get(spec, "review.findings"):
        errors.append("release review needs concrete review.findings")
    if get(spec, "review.release_decision") != "pass":
        errors.append("release review must set review.release_decision = 'pass'")

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")
    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS: {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
