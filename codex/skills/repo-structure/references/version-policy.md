# Version policy

`assets/version-snapshot.json` records a resolved date, exact package versions,
the Effect channel, the observed latest version, any supported-version
adjustment with compatibility evidence, and TanStack app compatibility notes.
Rendering performs no network access.
Rendered manifests retain the snapshot date and content digest, not its
machine-specific absolute path.

`resolve_versions.py` queries primary npm registry metadata and writes a
provisional snapshot. It resolves the Effect beta tag and requires `effect`,
`@effect/platform-bun`, `@effect/platform-node`, and `@effect/vitest` to match
exactly. Start and Router are separate values.

Before replacing the checked-in snapshot, render service, RPC, HTTP API, and a
full repo into clean fixtures; install; test source/declaration/default/publish
resolution; typecheck; test; and build. If unstable APIs break, select another
currently supported resolved version or leave the refresh blocked.
