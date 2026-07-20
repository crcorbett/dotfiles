# Chart selection

Use this self-contained taxonomy to generate candidates before choosing a form. It is not a recommendation engine: the analytical contract, integrity, accessibility, and target-size tests decide the final form.

| Data task | Start with these candidates | Decide with this test |
| --- | --- | --- |
| Comparison | Ordered dot plot, horizontal bar, table-graphic, slope/dumbbell for two fixed times | Can required values share a position scale? Is exact lookup material? |
| Trend over time | Line, dot/line, small multiples, indexed aligned panels | Are intervals regular and are events/context visible? Would area imply a cumulative story the data do not support? |
| Distribution | Raw/jittered points, histogram, ECDF, interval table-graphic | Does the form preserve shape, sample size, outliers, and uncertainty needed for the decision? |
| Relationship | Scatter, hexbin/density, small multiples, table for sparse lookup | Are measures comparable and is the claim descriptive unless causal design exists? |
| Part-to-whole | Sorted bar, 100% bar, stacked bar, table | Are there few immediately comparable parts and a clearly defined whole? Pie/doughnut is exceptional. |
| Geolocation | Point/rate map, grid/hexbin, small multiples, table | Is geography evidence, and are counts adjusted for exposure/population where needed? |
| Flow/process | Sankey/alluvial, connected matrix/table, small multiples | Do flow paths and conservation matter more than exact comparison? Can quantities and crossings be inspected? |
| Concept/hierarchy | Table, diagram, nested structure only when containment is the question | Is this quantitative evidence, or would text/table be clearer? |

## Selection record

For every non-trivial graphic, put these in `form_choice`:

1. `task_function`: the task in the table, expressed in question language.
2. `candidate_catalogue`: `embedded task taxonomy`, direct domain practice, or both.
3. `candidate_forms`: at least two forms with an evidence-based fit or rejection note.
4. `chosen_form`: the selected form's advantage for the reader's actual comparison.

Then run these eliminators:

- Reject a mark whose visual quantity is not the quantity being compared.
- Reject a form that hides a required denominator, distribution, uncertainty, interval, or spatial/time relation.
- Reject a form that makes the reader cross panels or use a legend for the central comparison when direct labels or an aligned alternative work.
- Reject ornamental radial, 3D, pictorial, bubble, or area treatments unless their extra visual weight earns its analytical role.
- Prefer a table or table-graphic when lookup, multiple exact values, or auditability dominates pattern discovery.

For a consequential explanatory display, compare two task-fit forms before implementation. Ask whether the conclusion, comparison, or implied importance changes when the same data become a dot plot, table-graphic, line, or area. Use this counterfactual to expose weak choices, not to optimise for novelty.
