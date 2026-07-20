# D3 modules playbook

Use D3 as small, typed utilities around a Recharts composition. Do not let a low-level drawing API replace the design record or turn chart code into untyped imperative state.

| Need | Module | Typed result passed to chart |
| --- | --- | --- |
| Median, extent, grouping, bins, sort | `d3-array` | number, tuple, or typed derived rows |
| Number/date formatting | `d3-format`, `d3-time-format` | formatter function used in labels/tooltips |
| Custom scale | `d3-scale` | mapping used by a typed custom SVG shape |
| Custom curve/path | `d3-shape` | path string or generator output |
| Force/layout | focused D3 layout module | typed coordinates plus an explicit interaction/accessibility plan |

```ts
import { median, sort } from "d3-array";

type Row = Readonly<{ label: string; value: number }>;

const ordered = sort(rows, (a, b) => b.value - a.value);
const benchmark = median(rows, (row) => row.value);
if (benchmark === undefined) throw new Error("Benchmark requires at least one row");
```

Record every calculation in the chart specification. If a D3-generated path, scale, or layout prevents direct reading, add labels, summary text, and an audit table.
