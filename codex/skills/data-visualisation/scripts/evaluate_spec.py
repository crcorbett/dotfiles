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
    "mark_economy",
    "spatial_narrative",
    "provenance",
)


def get(mapping: dict[str, Any], path: str) -> Any:
    value: Any = mapping
    for part in path.split("."):
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    return value


def meaningful(value: Any) -> bool:
    """Reject empty and placeholder prose where a concrete record is required."""
    if not isinstance(value, str) or not value.strip():
        return False
    return value.strip().lower() not in {"none", "n/a", "na", "not applicable", "any", "whatever", "trust me"}


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

    erasability = get(spec, "mark_economy.erasability")
    if not isinstance(erasability, list) or not erasability:
        errors.append("mark_economy.erasability needs one structured entry per non-data layer")
    elif any(
        not isinstance(layer, dict)
        or not meaningful(layer.get("layer"))
        or layer.get("role") not in {"guide", "annotation", "access", "container", "reference", "provenance", "uncertainty"}
        or not meaningful(layer.get("reading_lost"))
        for layer in erasability
    ):
        errors.append("each mark_economy.erasability entry needs layer, role, and reading_lost")
    data_ink_ratio = get(spec, "mark_economy.data_ink.ratio")
    if data_ink_ratio is not None:
        if not isinstance(data_ink_ratio, (int, float)) or isinstance(data_ink_ratio, bool):
            errors.append("mark_economy.data_ink.ratio must be a number from 0 to 1 or null")
        elif not 0 <= data_ink_ratio <= 1:
            errors.append("mark_economy.data_ink.ratio must be between 0 and 1")
        if get(spec, "mark_economy.data_ink.method") not in {"manual-vector-measurement", "estimated-pixel-area"}:
            errors.append("a measured data-ink ratio needs a declared measurement method")
        data_measure = get(spec, "mark_economy.data_ink.data_measure")
        total_measure = get(spec, "mark_economy.data_ink.total_measure")
        if not isinstance(data_measure, (int, float)) or isinstance(data_measure, bool) or not isinstance(total_measure, (int, float)) or isinstance(total_measure, bool) or total_measure <= 0:
            errors.append("a measured data-ink ratio needs numeric positive data_measure and total_measure")
        elif abs(data_ink_ratio - data_measure / total_measure) > 0.01:
            errors.append("data-ink ratio must agree with data_measure / total_measure within 0.01")
    elif get(spec, "mark_economy.data_ink.method") != "not-applicable":
        errors.append("an unmeasured data-ink ratio must set method = not-applicable")
    for field in ("basis", "data_geometry", "non_data_geometry"):
        if not meaningful(get(spec, f"mark_economy.data_ink.{field}")):
            errors.append(f"record mark_economy.data_ink.{field}")

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

    discontinuity_used = get(spec, "scales.discontinuity.used")
    if discontinuity_used not in {True, False}:
        errors.append("record scales.discontinuity.used as true or false")
    elif discontinuity_used:
        if get(spec, "scales.discontinuity.axis") not in {"x", "y", "both"}:
            errors.append("scale discontinuity needs scales.discontinuity.axis = x, y, or both")
        omitted_range = get(spec, "scales.discontinuity.omitted_range")
        if not isinstance(omitted_range, list) or len(omitted_range) != 2 or any(not isinstance(value, (int, float, str)) or (isinstance(value, str) and not meaningful(value)) for value in omitted_range):
            errors.append("scale discontinuity needs a two-value scales.discontinuity.omitted_range")
        if get(spec, "scales.discontinuity.visible_marker") not in {"axis-gap", "zigzag"}:
            errors.append("scale discontinuity needs visible_marker = axis-gap or zigzag")
        if not meaningful(get(spec, "scales.discontinuity.label")):
            errors.append("scale discontinuity needs a non-placeholder label")
        if not meaningful(get(spec, "scales.discontinuity.alternative_considered")):
            errors.append("scale discontinuity needs a non-placeholder alternative_considered")

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
        ordering = get(spec, "encoding.colour.ordering")
        kind = get(spec, "encoding.colour.ordering.kind")
        if not isinstance(ordering, dict) or kind not in {"none", "nominal", "ordered", "sequential"}:
            errors.append("colour ordering needs kind = none, nominal, ordered, or sequential")
        elif kind in {"ordered", "sequential"}:
            if get(spec, "encoding.colour.ordering.data_order") not in {"ascending", "descending", "chronological"}:
                errors.append("ordered colour needs data_order = ascending, descending, or chronological")
            domain = get(spec, "encoding.colour.ordering.domain")
            palette = get(spec, "encoding.colour.ordering.palette")
            if not isinstance(domain, list) or len(domain) < 2:
                errors.append("ordered colour needs a domain with at least two values")
            if not isinstance(palette, list) or len(palette) < 2 or any(not isinstance(value, str) or not value.startswith("#") for value in palette):
                errors.append("ordered colour needs a hex palette with at least two values")
            if get(spec, "encoding.colour.ordering.visual_progression") not in {"light-to-dark", "dark-to-light", "low-to-high", "high-to-low"}:
                errors.append("ordered colour needs a declared visual_progression")
        elif kind == "nominal" and not meaningful(get(spec, "encoding.colour.ordering.data_order")):
            errors.append("nominal colour needs an explicit data_order statement")
        elif kind == "none" and not get(spec, "encoding.colour.ordering.data_order"):
            errors.append("colour ordering kind none still needs an explicit data_order statement")
    spatial = get(spec, "spatial_narrative")
    if get(spec, "spatial_narrative.applicable") not in {True, False}:
        errors.append("record spatial_narrative.applicable as true or false")
    elif spatial and spatial.get("applicable"):
        for field in ("evidence_relation", "preserved_by", "lost_dimension", "alternative_view"):
            if not meaningful(get(spec, f"spatial_narrative.{field}")):
                errors.append(f"spatial narrative needs spatial_narrative.{field}")
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
    print(f"PASS: specification preflight; {len(warnings)} warning(s). Rendered visual review remains required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
