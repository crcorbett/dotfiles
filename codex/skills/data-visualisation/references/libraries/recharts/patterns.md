# Recharts playbook

## Default composition

Use strict TypeScript with typed rows, `ResponsiveContainer`, a chart container, axes, one or more marks, reference marks, direct labels, and a custom tooltip only when interaction adds real value. Set `isAnimationActive={false}` for editorial/static renders. Keep `accessibilityLayer` enabled.

| Task | Components | Notes |
| --- | --- | --- |
| Ordered comparison | `ScatterChart`, `Scatter`, `XAxis`, `YAxis`, `ReferenceLine` | Use a numeric x and ordered categorical/rank y; custom `shape` can draw direct values. |
| Time series | `LineChart`, `Line`, axes, `ReferenceLine` | Maintain regular time intervals; directly label endpoints when possible. |
| Magnitude comparison | `BarChart`, `Bar`, `LabelList` | Set numeric axis domain to include zero. |
| Distribution/relationship | `ScatterChart`, `Scatter`, `ReferenceLine` | Subdue context, directly identify exceptions, avoid colour-by-default. |
| Shared overlays | `ComposedChart` | Use only compatible marks on one meaningful scale. |

## Type boundary

```tsx
type RateRow = Readonly<{
  country: string;
  ratePct: number;
  isFocus: boolean;
}>;

function assertRateRow(value: RateRow): RateRow {
  if (!value.country || !Number.isFinite(value.ratePct)) throw new Error("Invalid rate row");
  return value;
}
```

Validate every imported/API row before chart transforms. Derive sort order, formatted labels, benchmark flags, and accent flags in typed functions rather than mutating unknown objects in a component.

## Required Recharts controls

- Set explicit numeric `domain`, `ticks`, `unit`, and axis labels when scale reasoning matters.
- Use `ReferenceLine` for a data-built target, event, median, or zero rule; label it directly.
- Use `LabelList` or typed custom SVG shapes for values/endpoint labels before adding a legend.
- Set `cursor={false}` when hover framing would distract from a static editorial reading.
- Render a separate narrow composition when labels or axis density fail; do not rely on automatic shrinking alone.

## Verify with Bun

```bash
bun run typecheck
bun run test
bun run build
bun run render
```

`render` must open the built app in a browser and save intended-size and narrow evidence. Test source reconciliation separately from visual rendering.
