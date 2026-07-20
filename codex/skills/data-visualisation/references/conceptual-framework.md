# Conceptual framework

## The job

Build a visual argument from evidence. Preserve the analytical question, comparison, unit, denominator, time/space context, and material uncertainty. The goal is access to complexity, not a sparse aesthetic.

## The analytical contract

Establish these facts before drawing:

1. **Question and decision:** What comparison or pattern matters, to whom, and for what decision?
2. **Evidence:** What is the observation unit, population, coverage, denominator, provenance, and material limitation?
3. **Transformation:** What filtering, binning, aggregation, normalisation, adjustment, model, or projection changed the raw data?
4. **Integrity:** Which visual measure represents each number? Could scale, area, perspective, changing units, or design variation alter perceived effect?
5. **Reading architecture:** What supports overview, close detail, and contextual challenge? Which comparison must remain in the eyespan?
6. **Form and delivery:** Is the right surface text, table, table-graphic, chart, or small multiples? What must survive at narrow size?
7. **Competence:** Can the maker defend domain meaning, statistical validity, and visual treatment separately?

## Grammar of graphics, strengthened by visual reasoning

Describe a visualisation as:

`data -> transform -> mark -> encode -> scale -> coordinate -> facet -> guide -> annotate -> inspect`

| Element | Decide explicitly | Test |
| --- | --- | --- |
| Data | Grain, source, population, exclusions | A polished display must not conceal weak data. |
| Transform | Filter, aggregate, calculate, bin, rank, normalise, adjust | Disclose the transform and retain a route to challenge it. |
| Mark | Point, line, rule, text, rect, area, geoshape | The mark itself must be informative; avoid decorative volume or perspective. |
| Encode | Position, length, area, colour, shape | Prefer common-scale position; keep visual effect proportionate to data effect. |
| Scale | Domain, baseline, interval, type, direction | Show data variation, not changing design or units. |
| Coordinate | Cartesian, geographic, polar, space-time | Preserve meaningful dimensions and state material compromises. |
| Facet | Repeat frame by group, time, or scenario | Hold design constant so change belongs to data. |
| Guide | Labels, reference rules, direct values, grid | Make guides quieter than data; prefer direct labels before legends. |
| Annotate | Finding, event, qualification, source | Place explanation at the evidence. |
| Inspect | Full/reduced/grayscale/edge review | Check hierarchy, clipping, vibration, and false inference. |

## Hierarchy and colour budget

Declare three levels: **primary evidence** answers the question, **neutral context** enables comparison, and **accent focus** identifies a question-relevant reference, exception, selected series, or meaningful group. A named category is not automatically accent-worthy. If direct labels or position already identify it, neutral treatment is usually clearer.

For a dense relationship, make context marks quiet and directly identify only important points/groups. For a ranking with a named focus, use neutral comparators plus an accent focus and benchmark. For many individually important series, first test small multiples, indexing, or a table rather than spending many strong hues.

## Scales, alternatives, and exceptions

Dual and broken scales need an explicit burden of proof. A second scale may be economical, but it must not manufacture correspondence: align zero when relevant, associate labels directly with series, and prefer aligned panels or indexing when those tests fail.

Rules guide choices; they do not replace seeing. A justified exception records competing evidence, rejected alternatives, and why the final reading is clearer and more truthful.

## Three readings and eyespan

Every substantial graphic should support:

- **Macro:** overall structure or trajectory.
- **Micro:** individual observations, values, labels, or local anomalies.
- **Context:** source, transformation, uncertainty, and explanatory narrative.

Keep needed comparisons on one view where practical. If interaction or paging separates them, provide an overview, aligned defaults, and a table/download path.
