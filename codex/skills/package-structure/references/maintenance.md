# Maintenance

Canonical ownership:

- `assets/<variant>` owns generated files.
- `references/variants.md` owns human variant selection.
- `scripts/render_package.py` owns rendering and write safety.
- `scripts/validate_package.py` owns structural/semantic package checks.
- `scripts/validate_ecosystem.py` owns scoped stale-pattern checks.
- repository-local profiles own only local facts.

Profiles route the docs index, architecture, runbooks, proof, critical journeys,
authority, evidence/archive, README rules, exact checks, generated owners,
exceptions, and mirror policy. Do not copy those local facts into this global
skill.

When Effect or transport APIs change:

1. research the upstream library through DeepWiki/official versioned sources;
2. update the appropriate canonical asset and reference;
3. render every variant from a provisional snapshot;
4. install, resolve exports, typecheck, test, and build all variants;
5. replace the snapshot only after compatibility passes;
6. rerun structural validation and fresh-context scenarios.

Do not copy templates into repository-local overlays. Update a local profile
only when that repository's facts changed.
