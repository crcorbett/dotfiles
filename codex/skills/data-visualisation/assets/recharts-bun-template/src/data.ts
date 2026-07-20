export type ComparisonRow = Readonly<{
  label: string;
  value: number;
  isFocus: boolean;
}>;

const source: readonly ComparisonRow[] = [
  { label: "North", value: 81, isFocus: false },
  { label: "East", value: 78, isFocus: false },
  { label: "Focus", value: 74, isFocus: true },
  { label: "South", value: 69, isFocus: false }
];

export const rows = [...source]
  .sort((left, right) => right.value - left.value)
  .map((row, index) => ({ ...row, rank: source.length - index - 1, display: `${row.value}%` }));

export const benchmark = 76;
