# Evaluation rubric

Score each criterion 0, 1, or 2: 0 = fails/missing, 1 = partial/qualified, 2 = visibly and evidentially passes. A blocking 0 prevents release. A self-score is provisional; a reviewer who did not build the visual must challenge each 2 from the rendered output, source data, and specification.

| Criterion | Pass condition | Blocking |
| --- | --- | --- |
| Question and role | One analytical question, audience/use, decision context, comparison, and display role drive the graphic | Yes |
| Competence gate | Domain meaning, statistical validity, and visual treatment are each defensible | Yes |
| Data contract | Unit, population, denominator, coverage, provenance, transformations, and material limitations are available | Yes |
| Proportional encoding | Visual measure is proportionate; baseline/domain and any visual/data effect check are defensible | Yes |
| Design invariance | Scales, intervals, units, and layout do not silently change | Yes |
| Form choice | At least two candidate forms plus chart/table/text, small-multiple, indexed-panel, and dual-scale alternatives are considered against the task | Yes |
| Comparison | Relevant alternatives remain in eyespan or a clear overview preserves comparison | Yes |
| Micro/macro | Overview, detail, and context coexist without memory-heavy switches | No |
| Data density | The view contains enough evidence; any reduction is named and inspectable | No |
| Mark economy | Data/guides/annotations earn their ink; no chartjunk, fake 3D, moire, or redundant framing | Yes |
| Hierarchy | Primary evidence, neutral context, and accent focus are deliberate; guides are quiet | Yes |
| Colour necessity and access | Every hue communicates a necessary distinction without false status; non-focus marks are neutral; critical distinctions survive grayscale | Yes |
| Scale relationship | Any dual/broken scale is necessary, directly associated, and cannot imply forced correlation; zero aligns when relevant | Yes |
| Claim discipline | Correlation, observation, estimate, forecast, and causal claim are distinguished honestly | Yes |
| Annotation and integration | Direct labels, provenance, finding, event, definitions, and qualifications sit near evidence when material | No |
| Legibility and delivery | Intended, reduced, grayscale, and narrow views have no clipping, collision, off-canvas content, or unreadable essentials | Yes |
| Reproducibility | Code/spec/query and data version can recreate or challenge the graphic | Yes |
| Exception record | Every rule departure identifies competing evidence and why it improves truth and clarity | Yes |

## Release rule

Require every blocking row to score 2 and a total of at least 30/36. Record every 1 with a reason and follow-up. Include independent reviewer name, date, and concrete findings. When a check cannot be calculated, state why and give the next-best verification.

## Required review sequence

1. Reconcile plotted values, order, aggregation, and rounded labels against data.
2. Name the domain, statistical, and visual basis; reject if one is missing.
3. Generate candidate forms from the embedded taxonomy; try the closest two alternatives and record why the chosen form wins and whether the conclusion changes.
4. Remove each hue, accent, guide, and annotation in turn. Retain it only if a necessary reading is lost.
5. For perceptually sized comparisons, calculate or reason through visual/data effect proportionality.
6. Inspect full, embedded, reduced, grayscale, and narrow sizes; check every edge and use a reduced-attention hierarchy check.
7. Have an independent reader name the question, comparison, evidence, and qualification. If the answer depends on code or a distant legend, revise.
