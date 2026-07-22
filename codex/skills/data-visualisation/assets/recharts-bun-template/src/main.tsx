import { createRoot } from "react-dom/client";
import { CartesianGrid, ReferenceLine, ResponsiveContainer, Scatter, ScatterChart, XAxis, YAxis } from "recharts";
import { benchmark, rows, type ComparisonRow } from "./data";

type DotProps = Readonly<{
  cx?: number;
  cy?: number;
  payload?: ComparisonRow & { rank: number; display: string };
}>;

function DirectValueDot({ cx, cy, payload }: DotProps) {
  if (cx === undefined || cy === undefined || payload === undefined) return null;
  const fill = payload.isFocus ? "#0072B2" : "#8A8A8A";
  return (
    <g aria-label={`${payload.label}: ${payload.display}`}>
      <circle cx={cx} cy={cy} r="5" fill={fill} stroke="white" />
      <text x={cx + 8} y={cy + 4} fontSize="12" fill="#303030">{payload.display}</text>
    </g>
  );
}

function App() {
  const labels = new Map(rows.map((row) => [row.rank, row.label]));
  return (
    <main style={{ width: "min(760px, calc(100vw - 32px))", margin: "24px auto", fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ fontSize: 22, fontWeight: 500, margin: 0 }}>Focus is below the benchmark</h1>
      <p style={{ margin: "4px 0 14px" }}>Illustrative rate comparison (%)</p>
      <ResponsiveContainer width="100%" height={280}>
        <ScatterChart accessibilityLayer margin={{ top: 18, right: 50, bottom: 36, left: 4 }}>
          <CartesianGrid vertical stroke="#e5e5e5" horizontal={false} />
          <XAxis type="number" dataKey="value" domain={[60, 90]} ticks={[60, 70, 80, 90]} unit="%" />
          <YAxis type="number" dataKey="rank" domain={[-0.5, rows.length - 0.5]} ticks={rows.map((row) => row.rank)} width={80} tickFormatter={(rank: number) => labels.get(rank) ?? ""} />
          <ReferenceLine x={benchmark} stroke="#5e5e5e" strokeDasharray="5 4" label={{ value: `Benchmark ${benchmark}%`, position: "insideTopRight" }} />
          <Scatter data={rows} dataKey="value" shape={<DirectValueDot />} isAnimationActive={false} />
        </ScatterChart>
      </ResponsiveContainer>
      <p style={{ fontSize: 12, color: "#555" }}>Illustrative values only. Replace with validated source data, provenance, and qualification.</p>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
