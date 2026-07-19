# Tooling and documentation

The generated ordered gate is format check, Oxlint, repository policy-rule
tests, development and production Knip, TypeScript, Vitest, then Turbo build.
`tools/oxlint` owns policy rules and
positive/negative fixtures for source-condition order, runtime execution,
generic client escape hatches, and Layer root exports.

The TanStack app's `check-types` script invokes Vite once before `tsc` so the
framework generates `routeTree.gen.ts`; generated route output is never stored
as a template.

Documentation must include root/app/package READMEs; architecture pages for
package ownership, Effect services, frontend composition, testing/quality, and
tooling; product-spec and exec-plan indexes; and a portable local
docs-maintainer with its own repository owner/check profile. Validate
links, commands, export paths, metadata, and stale paths—not only presence.

The governance validator checks unique semantic owners, lifecycle and
retirement metadata, local links, critical-journey oracles, automation and
feedback controls, compatibility provenance, config digests, lockfile phase,
limitations, and non-claims. Receipts are bounded envelopes; detailed output is
stored by path/digest rather than embedded without limit. Failed and
inconclusive evidence is preserved outside default navigation with provenance.

Knip has development and production graphs. CI runs the same ordered gate after
`bun install --frozen-lockfile`; the first generated lockfile is intentionally
created by the user during bootstrap.
