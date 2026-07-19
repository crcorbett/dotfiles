#!/usr/bin/env python3
from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
personal_root = "/" + "Users" + "/"
skill = (root / "SKILL.md").read_text()
metadata = (root / "agents/openai.yaml").read_text()
assert "$repo-structure" in metadata
assert personal_root not in skill
for path in root.rglob("*"):
    if path.is_file() and path.suffix in {".md", ".py", ".yaml", ".tmpl", ".json"}:
        assert personal_root not in path.read_text(errors="ignore"), path
for match in re.finditer(r"\]\((references/[^)]+)\)", skill):
    assert (root / match.group(1)).is_file(), match.group(1)
assert (root.parent / "package-structure/SKILL.md").is_file()
assert not list(root.rglob("routeTree.gen.ts"))
assert not list(root.rglob("bun.lock"))
print(f"validated metadata, references, and generated exclusions: {root}")
