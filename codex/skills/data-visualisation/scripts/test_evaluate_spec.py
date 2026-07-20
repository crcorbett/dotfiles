#!/usr/bin/env python3
"""Minimal regression tests for evaluate_spec.py."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).with_name("evaluate_spec.py")


def run(spec: dict[str, object]) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        json.dump(spec, handle)
        path = Path(handle.name)
    try:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(path)], text=True, capture_output=True, check=False
        )
    finally:
        path.unlink(missing_ok=True)


BASE = {
    "question": "How did weekly completion change?",
    "display_role": "description",
    "data": {"denominator": "eligible sessions"},
    "mark": "line",
    "encoding": {"y": {"field": "completion_rate", "unit": "%"}},
    "scales": {
        "y": {"baseline": 0},
        "discontinuity": {
            "used": False,
            "axis": None,
            "omitted_range": None,
            "visible_marker": None,
            "label": None,
            "alternative_considered": "not applicable",
        },
    },
    "integrity": {
        "design_invariance": "One shared y scale and identical mark construction for every week.",
        "visual_effect_ratio": 1.0,
    },
    "mark_economy": {
        "erasability": [
            {
                "layer": "quiet grid",
                "role": "guide",
                "reading_lost": "Readers cannot interpolate rates reliably at the intended size.",
            },
            {
                "layer": "release rule",
                "role": "annotation",
                "reading_lost": "The release event lacks its precise temporal context.",
            },
        ],
        "data_ink": {
            "ratio": None,
            "method": "not-applicable",
            "basis": "Raster output does not allow a meaningful separation of data and non-data ink.",
            "data_measure": None,
            "total_measure": None,
            "data_geometry": "Weekly line and points.",
            "non_data_geometry": "Grid, release rule, labels, and source text.",
        },
    },
    "spatial_narrative": {
        "applicable": False,
        "evidence_relation": "not applicable",
        "preserved_by": "not applicable",
        "lost_dimension": "none",
        "alternative_view": "not applicable",
    },
    "comparison": {"eyespan": True, "alternative_view": "none needed"},
    "form_choice": {
        "task_function": "trend over time",
        "candidate_catalogue": "embedded task taxonomy",
        "candidate_forms": [
            {"form": "line chart", "fit": "Keeps the regular weekly sequence visible."},
            {"form": "table", "fit": "Supports lookup but weakens change detection."},
        ],
        "chosen_form": "A line retains weekly sequence.",
        "alternatives_considered": ["A table supports lookup but weakens change detection."],
        "dual_scale": {
            "used": False,
            "rationale": "not applicable",
            "zero_alignment": "not applicable",
            "alternative_considered": "not applicable",
        },
    },
    "hierarchy": {
        "primary_evidence": "Weekly completion line.",
        "neutral_context": "Quiet grid and release rule.",
        "accent_focus": "Release rule only.",
    },
    "competence": {
        "substantive": "Completion informs service quality.",
        "statistical": "Descriptive census with stated limitation.",
        "visual": "A common-scale line preserves weekly sequence.",
    },
    "review": {
        "builder": "chart maker",
        "independent_reviewer": "editorial reviewer",
        "findings": "No clipped text at intended or reduced size.",
        "release_decision": "pass",
    },
    "provenance": "warehouse query 2026-07-20",
    "uncertainty": "No confidence interval; descriptive census of eligible sessions.",
    "annotations": "Release on 14 May.",
    "accessibility": {"not_colour_only": True, "reduced_size_checked": True},
}


def main() -> int:
    passing = run(BASE)
    assert passing.returncode == 0, passing.stdout + passing.stderr

    misleading_bar = {**BASE, "mark": "bar", "scales": {"y": {"baseline": 40}}}
    failing = run(misleading_bar)
    assert failing.returncode == 1, failing.stdout + failing.stderr
    assert "requires scales.y.baseline = 0" in failing.stdout

    distorted = {
        **BASE,
        "integrity": {**BASE["integrity"], "visual_effect_ratio": 1.2},
    }
    failing = run(distorted)
    assert failing.returncode == 1, failing.stdout + failing.stderr
    assert "visual_effect_ratio must be between 0.95 and 1.05" in failing.stdout

    gratuitous_colour = {
        **BASE,
        "encoding": {**BASE["encoding"], "colour": {"field": "region", "purpose": "identity"}},
    }
    failing = run(gratuitous_colour)
    assert failing.returncode == 1, failing.stdout + failing.stderr
    assert "colour encoding needs a necessity statement" in failing.stdout

    colour_without_semantics = {
        **BASE,
        "encoding": {
            **BASE["encoding"],
            "colour": {
                "field": "focus",
                "purpose": "highlight",
                "necessity": "The focus must be immediately identifiable.",
            },
        },
    }
    failing = run(colour_without_semantics)
    assert failing.returncode == 1, failing.stdout + failing.stderr
    assert "colour encoding needs a semantic rationale" in failing.stdout

    missing_erasability = {
        **BASE,
        "mark_economy": {
            "erasability": [],
            "data_ink": {
                "ratio": None,
                "method": "not-applicable",
                "basis": "not measurable",
                "data_measure": None,
                "total_measure": None,
                "data_geometry": "marks",
                "non_data_geometry": "guides",
            },
        },
    }
    failing = run(missing_erasability)
    assert failing.returncode == 1, failing.stdout + failing.stderr
    assert "mark_economy.erasability needs one structured entry" in failing.stdout

    hidden_scale_break = {
        **BASE,
        "scales": {**BASE["scales"], "discontinuity": {"used": True}},
    }
    failing = run(hidden_scale_break)
    assert failing.returncode == 1, failing.stdout + failing.stderr
    assert "scale discontinuity needs a two-value scales.discontinuity.omitted_range" in failing.stdout

    invalid_colour_order = {
        **BASE,
        "encoding": {
            **BASE["encoding"],
            "colour": {
                "field": "month",
                "purpose": "measure",
                "necessity": "Month order needs an additional visual cue.",
                "semantic_rationale": "The treatment encodes time, not status.",
                "ordering": {"kind": "sequential", "data_order": "whatever", "domain": ["Jan", "Feb"], "palette": ["#ffffff", "#000000"], "visual_progression": "any"},
            },
        },
    }
    failing = run(invalid_colour_order)
    assert failing.returncode == 1, failing.stdout + failing.stderr
    assert "ordered colour needs data_order = ascending, descending, or chronological" in failing.stdout

    incomplete_spatial_record = {
        **BASE,
        "spatial_narrative": {"applicable": True, "evidence_relation": "not applicable", "preserved_by": "not applicable", "lost_dimension": "not applicable", "alternative_view": "not applicable"},
    }
    failing = run(incomplete_spatial_record)
    assert failing.returncode == 1, failing.stdout + failing.stderr
    assert "spatial narrative needs spatial_narrative.evidence_relation" in failing.stdout

    fake_scale_break = {
        **BASE,
        "scales": {
            **BASE["scales"],
            "discontinuity": {
                "used": True,
                "axis": "y",
                "omitted_range": ["not applicable", "not applicable"],
                "visible_marker": "none",
                "label": "none",
                "alternative_considered": "none",
            },
        },
    }
    failing = run(fake_scale_break)
    assert failing.returncode == 1, failing.stdout + failing.stderr
    assert "scale discontinuity needs visible_marker = axis-gap or zigzag" in failing.stdout

    ungrounded_ratio = {
        **BASE,
        "mark_economy": {
            **BASE["mark_economy"],
            "data_ink": {
                "ratio": 0.999,
                "method": "trust me",
                "basis": "trust me",
                "data_measure": None,
                "total_measure": None,
                "data_geometry": "marks",
                "non_data_geometry": "guides",
            },
        },
    }
    failing = run(ungrounded_ratio)
    assert failing.returncode == 1, failing.stdout + failing.stderr
    assert "a measured data-ink ratio needs a declared measurement method" in failing.stdout

    unexplained_dual_scale = {
        **BASE,
        "form_choice": {
            **BASE["form_choice"],
            "dual_scale": {"used": True, "rationale": "", "zero_alignment": "", "alternative_considered": ""},
        },
    }
    failing = run(unexplained_dual_scale)
    assert failing.returncode == 1, failing.stdout + failing.stderr
    assert "dual scale needs a rationale" in failing.stdout

    missing_candidate_review = {
        **BASE,
        "form_choice": {**BASE["form_choice"], "candidate_forms": []},
    }
    failing = run(missing_candidate_review)
    assert failing.returncode == 1, failing.stdout + failing.stderr
    assert "candidate_forms needs at least two task-fit candidates" in failing.stdout
    print("PASS: evaluate_spec regression tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
