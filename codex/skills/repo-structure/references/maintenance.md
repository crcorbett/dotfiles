# Maintenance

Canonical owners:

- package files: global `package-structure/assets` only;
- root/app/docs/tool files: `repo-structure/assets/repository`;
- resolved versions: `repo-structure/assets/version-snapshot.json`;
- local repository facts: each repo's local package profile;
- lint policy: generated `tools/oxlint` rule implementation/tests;
- skill baseline: renderer-resolved generic skills plus self-contained local
  router assets; rendered skills must not retain a global installation path.

Update one owner, render clean fixtures, run structural/metadata validation,
execute the ordered gate, scan stale patterns, and run fresh-context scenarios.
Record adopted/rejected upstream changes. Never copy global package templates
into this skill or a repository-local overlay.

Both renderers must run their structural validator against the staging tree
before the atomic rename. A successful render is never allowed to mean only
that files were copied.
