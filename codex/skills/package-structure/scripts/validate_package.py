#!/usr/bin/env python3
"""Validate generated or existing package boundaries."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


FORBIDDEN_SOURCE = {
    "generic SDK callback": re.compile(r"readonly\s+(use|withClient)\s*[:(]"),
    "runtime class policy": re.compile(r"\binstanceof\b"),
    "legacy Context tag": re.compile(r"Context\.Tag\b"),
    "package-local runtime execution": re.compile(r"Effect\.run(?:Promise|Sync)\b"),
}
PERSONAL_ROOT = "/" + "Users" + "/"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


root = Path(sys.argv[1]).resolve(strict=True)
for path in root.rglob("*"):
    if not path.is_file():
        continue
    text = path.read_text(errors="ignore")
    if PERSONAL_ROOT in text:
        fail(f"{path.relative_to(root)} contains a personal absolute path")
    if re.search(r"__[A-Z][A-Z0-9_]*__", text):
        fail(f"{path.relative_to(root)} contains an unresolved template token")
manifest_path = root / "package.json"
if not manifest_path.is_file():
    fail("missing package.json")
manifest = json.loads(manifest_path.read_text())
exports = manifest.get("exports")
if not isinstance(exports, dict) or not exports:
    fail("package exports must be explicit")
publish = manifest.get("publishConfig", {}).get("exports", {})
source_conditions: set[str] = set()
for name, value in exports.items():
    if not isinstance(value, dict):
        fail(f"export {name} must be an object")
    keys = list(value)
    conditions = [key for key in keys if key not in {"types", "default", "import"}]
    source_conditions.update(conditions)
    for condition in conditions:
        target = value[condition]
        if isinstance(target, str) and target.startswith("./src"):
            if keys.index(condition) > keys.index("types"):
                fail(f"export {name} must place source before types")
            if not (root / target).is_file():
                fail(f"export {name} source target does not exist: {target}")
    if "types" in value and "default" in value and keys.index("types") > keys.index("default"):
        fail(f"export {name} must place types before default")
for value in publish.values() if isinstance(publish, dict) else []:
    if isinstance(value, dict) and source_conditions.intersection(value):
        fail("publish exports must omit repository source conditions")
for path in (root / "src").rglob("*.ts"):
    text = path.read_text()
    for label, pattern in FORBIDDEN_SOURCE.items():
        if pattern.search(text):
            fail(f"{path.relative_to(root)} contains {label}")
service = root / "src/service.ts"
if service.is_file():
    text = service.read_text()
    if "Context.Service" not in text:
        fail("service.ts must define Context.Service")
    if "Layer." in text:
        fail("service.ts must not define a Layer")
    for implementation_marker in (
        "Client.make(",
        "ClientEffect",
        "RawClient",
        "layerLive",
        "layerMock",
    ):
        if implementation_marker in text:
            fail(f"service.ts contains implementation marker {implementation_marker}")
print(f"validated package {manifest.get('name')} at {root}")
