---
name: data-visualisation
description: Design, implement, and critically evaluate evidence-first data visualisations. Use when turning a dataset, analysis, dashboard, chart brief, or existing graphic into an honest, legible, grammar-of-graphics visualisation in TypeScript or Python, especially when comparisons, time, uncertainty, causal claims, distributions, dense tables, small multiples, or analytical annotations matter.
---

# Data Visualisation

Create graphics that make evidence, comparison, and uncertainty inspectable. This skill is self-contained: use its embedded methods, rules, examples, and library playbooks without fetching design or chart-documentation websites. Treat rendering as the final test of a visual argument, not the design process.

## Read before work

- Read [foundations.md](references/foundations.md) for the embedded analytical and visual method.
- Read [conceptual-framework.md](references/conceptual-framework.md) for the grammar, hierarchy, comparison, and scale model.
- Read [chart-selection.md](references/chart-selection.md) while choosing a form; it includes the complete candidate-form taxonomy and elimination tests.
- Read [rulebook.md](references/rulebook.md) for non-negotiable practices and anti-patterns.
- Read [editorial-production.md](references/editorial-production.md) for explanatory, responsive, dense, or narrative graphics.
- Read [evaluation-rubric.md](references/evaluation-rubric.md) before delivery; use it to self-critique the rendered result.
- Read [implementation.md](references/implementation.md) only after choosing the form. It routes to self-contained Recharts, D3, and Python library playbooks.
- Read [examples.md](references/examples.md) for compact good/bad transformations.

## Workflow

1. State one analytical question. Name the audience, decision, comparison, and what evidence would change the conclusion. Classify the role: description, exploration, lookup, explanation, or monitoring.
2. Audit the data: grain, unit, denominator, coverage, missingness, transformations, provenance, uncertainty, and whether values can be compared. Do not turn descriptive data into a causal claim. Confirm substantive, statistical, and visual competence separately.
3. Write a grammar record: `data -> transform -> mark -> encode -> scale -> coordinate -> facet -> guide -> annotate -> inspect`. Record the essential eyespan comparison and the reading lost if each colour is removed. Start from [chart-spec.template.json](assets/chart-spec.template.json).
4. Generate at least two task-fit forms from [chart-selection.md](references/chart-selection.md), then reject candidates that fail the evidence, comparison, accessibility, or target-size test. Record why the chosen form wins.
5. Implement TypeScript graphics with strict React + Recharts, executed with Bun. Add small typed D3 modules only for calculations, scales, layouts, paths, or interaction that Recharts cannot express. Do not use Vega or Vega-Lite for TypeScript delivery. Use the embedded library playbooks; use Python only when it is the requested delivery surface or an analysis-first workflow is clearer.
6. Render at intended size. Inspect labels, ordering, baselines, visual-effect proportionality, annotations, overlap, colour dependence, grayscale, reduced size, and narrow layout where relevant.
7. Run `scripts/evaluate_spec.py`, complete the human rubric, and have a reviewer other than the builder challenge the rendered output, data, and specification. Fix every blocking finding or state the limitation on the graphic.
8. Deliver the visual, source/specification, provenance, transformations, uncertainty, and independent review record.

## Required deliverables

Include these in every non-trivial visualisation task:

- One analytical question and target audience/use.
- Plot specification and source data location/query.
- Rendered visual with title, units, provenance, and material qualifications.
- Candidate-form record.
- Evaluation scorecard, including all blocking checks and independent reviewer findings.

## Hard stops

Do not ship a visualisation with misleading area/length, hidden denominator, unjustified truncated baseline, unexplained aggregation, colour with no necessary information job, inaccessible colour-only distinction, unexamined dual scale, unlabelled transformation, or causal language unsupported by the data.

Do not certify a visual until it clears the embedded rulebook and blocking rubric checks, and an independent reviewer has inspected the rendered output.
