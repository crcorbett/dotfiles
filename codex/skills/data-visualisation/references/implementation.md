# Implementation

Use this file as the offline route map. The library playbooks contain the API patterns, type boundaries, commands, and failure checks needed for normal work; do not fetch chart documentation before using them.

| Need | Read | Default |
| --- | --- | --- |
| TypeScript React chart | [Recharts playbook](libraries/recharts/patterns.md) | Strict React + Recharts, run with Bun |
| Typed calculation, custom scale/path/layout | [D3 modules](libraries/d3/modules.md) | Import only the needed D3 module and pass typed output to Recharts |
| Copyable Bun starter | [Recharts Bun template](../assets/recharts-bun-template) | Copy, install packages, typecheck, build, render |
| Python declarative chart | [Python grammar](libraries/python/grammar.md) | Altair or plotnine |

## Delivery rules

- Define a concrete row type and validate source data at the boundary. Do not pass loose records through chart code.
- Keep transformations typed, testable, and visible in the portable specification.
- Prefer SVG for modest mark counts and inspectability. Use Canvas/WebGL only when density or interaction requires it, with accessible summary and data/spec access.
- Use a restricted point/line scale only when zero is not the meaningful comparator; state the exact domain. Bars and areas start at zero.
- Install packages from the local cache or package registry only to execute a project. The skill's design and API guidance is bundled here and needs no web lookup.

## Spec lint

Write a portable JSON record and run:

```bash
python3 scripts/evaluate_spec.py path/to/chart-spec.json
```

The linter catches high-risk omissions; it cannot judge hierarchy, rendering, or truth of assertions. Always complete the human rubric and independent rendered review.
