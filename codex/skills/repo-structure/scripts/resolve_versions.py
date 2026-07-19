#!/usr/bin/env python3
"""Resolve a provisional version snapshot from npm registry metadata."""

from __future__ import annotations

import argparse
import datetime
import json
import subprocess
from pathlib import Path


EFFECT = ["effect", "@effect/platform-bun", "@effect/platform-node", "@effect/vitest"]
LATEST = [
    "@tanstack/react-start", "@tanstack/react-router", "react", "react-dom",
    "typescript", "vite", "vitest", "turbo", "oxlint", "oxfmt", "knip",
    "bun", "@changesets/cli", "@types/bun", "@types/react", "@types/react-dom",
    "@vitejs/plugin-react",
]


def npm(package: str, field: str) -> str:
    return subprocess.run(
        ["npm", "view", package, field, "--json"],
        check=True, capture_output=True, text=True,
    ).stdout.strip().strip('"')


parser = argparse.ArgumentParser()
parser.add_argument("--output", required=True)
args = parser.parse_args()
packages = {name: npm(name, "dist-tags.beta") for name in EFFECT}
if len(set(packages.values())) != 1:
    raise SystemExit(f"Effect beta versions are not aligned: {packages}")
packages.update({name: npm(name, "version") for name in LATEST})
packages["alchemy"] = npm("alchemy", "dist-tags.next")
snapshot = {
    "resolvedAt": datetime.date.today().isoformat(),
    "effectChannel": "beta",
    "tanstackAppVerbatimModuleSyntax": False,
    "sources": {
        "npmRegistry": "https://registry.npmjs.org/",
        "effect": "https://www.npmjs.com/package/effect",
        "tanstackStart": "https://www.npmjs.com/package/@tanstack/react-start",
        "alchemy": "https://www.npmjs.com/package/alchemy",
        "alchemyCloudflare": "https://v2.alchemy.run/cloudflare/",
        "cloudflareWorkers": "https://developers.cloudflare.com/workers/",
    },
    "compatibilityDecisions": [
        {
            "id": "effect-ecosystem",
            "status": "requires-qualification",
            "decision": "Provisional registry selection; render and verify every package and repository fixture before adoption.",
            "evidence": "No compatibility evidence exists until fixture verification completes.",
        },
        {
            "id": "tanstack-start",
            "status": "requires-qualification",
            "decision": "Provisional independent Start and Router selection.",
            "evidence": "The rendered app fixture must typecheck, test, and build before adoption.",
        },
        {
            "id": "alchemy-cloudflare",
            "status": "requires-qualification",
            "decision": "Provisional Alchemy next-tag selection; beta compatibility is never assumed.",
            "evidence": "The preview-only Cloudflare Website scaffold must typecheck and build; provider deployment is outside qualification.",
        },
    ],
    "packages": packages,
}
Path(args.output).write_text(json.dumps(snapshot, indent=2) + "\n")
print(args.output)
