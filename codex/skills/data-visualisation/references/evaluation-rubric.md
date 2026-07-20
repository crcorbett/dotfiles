# Evaluation rubric

Score each criterion 0, 1, or 2: 0 = fails/missing, 1 = partial/qualified, 2 = visibly and evidentially passes. A blocking 0 prevents release. A self-score is provisional; a reviewer who did not build the visual must challenge each 2 from the rendered output, source data, and specification.

| Criterion | Pass condition | Blocking |
| --- | --- | --- |
| Question and role | One analytical question, audience/use, decision context, comparison, and display role drive the graphic | Yes |
| Competence gate | Domain meaning, statistical validity, and visual treatment are each defensible | Yes |
| Data contract | Unit, population, denominator, coverage, provenance, transformations, and material limitations are available | Yes |
| Proportional encoding | Visual measure is proportionate; baseline/domain and any visual/data effect check are defensible | Yes |
| Design invariance | Scales, intervals, units, colour order, and layout do not silently change; any discontinuity is explicit | Yes |
| Form choice | At least two candidate forms plus chart/table/text, small-multiple, indexed-panel, and dual-scale alternatives are considered against the task | Yes |
| Comparison | Relevant alternatives remain in eyespan or a clear overview preserves comparison | Yes |
| Micro/macro | Overview, detail, and context coexist without memory-heavy switches | No |
| Data density | The view contains enough evidence; any reduction is named and inspectable | No |
| Mark economy | Every non-data layer passes an erasability test; any measurable data-ink ratio is recorded without becoming a target; no chartjunk, fake 3D, moire, or redundant framing | Yes |
| Hierarchy | Primary evidence, neutral context, and accent focus are deliberate; guides are quiet | Yes |
| Colour necessity and access | Every hue communicates a necessary distinction without false status; non-focus marks are neutral; critical distinctions survive grayscale | Yes |
| Scale relationship | Any dual/broken scale is necessary, directly associated, and cannot imply forced correlation; zero aligns when relevant; a broken scale visibly marks its discontinuity and omitted range | Yes |
| Space/time relation | When geography, route, connection, exposure, or sequence is evidence, the visual preserves it or explicitly records the lost dimension and a usable alternative | Yes |
| Claim discipline | Correlation, observation, estimate, forecast, and causal claim are distinguished honestly | Yes |
| Annotation and integration | Direct labels, provenance, finding, event, definitions, and qualifications sit near evidence when material; spatial/sequence narratives retain their material relationship or name what was lost | No |
| Legibility and delivery | Intended, reduced, grayscale, and narrow views have no clipping, collision, off-canvas content, or unreadable essentials | Yes |
| Reproducibility | Code/spec/query and data version can recreate or challenge the graphic | Yes |
| Exception record | Every rule departure identifies competing evidence and why it improves truth and clarity | Yes |

## Release rule

Require every blocking row to score 2 and a total of at least 32/38. Record every 1 with a reason and follow-up. Include independent reviewer name, date, and concrete findings. When a check cannot be calculated, state why and give the next-best verification.

## Required review sequence

1. Reconcile plotted values, order, aggregation, and rounded labels against data.
2. Name the domain, statistical, and visual basis; reject if one is missing.
3. Generate candidate forms from the embedded taxonomy; try the closest two alternatives and record why the chosen form wins and whether the conclusion changes.
4. Reconcile a named render-layer inventory with the actual graphic. Remove each hue, accent, guide, annotation, container, and other non-data layer in turn. Retain it only if a necessary reading is lost. Record a data-ink ratio only when it can be measured honestly, with method and numerator/denominator; otherwise record why it cannot.
5. For perceptually sized comparisons, calculate or reason through visual/data effect proportionality.
6. Inspect full, embedded, reduced, grayscale, and narrow sizes; check every edge and use a reduced-attention hierarchy check. Where relevant, confirm ordered colour matches data order, every scale break is visibly labelled, and the spatial/temporal relation remains recoverable.
7. Have an independent reader name the question, comparison, evidence, and qualification. If the answer depends on code or a distant legend, revise.
