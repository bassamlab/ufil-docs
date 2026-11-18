#!/usr/bin/env python3
"""Turn a copy of the documentation into the public version that is mirrored to GitHub.

- Deletes every file and directory below src/ whose name contains "uofa" (like the workspace
  mirror, the UofA data must not be published).
- Deletes every block between the reStructuredText comments ".. internal-only-begin" and
  ".. internal-only-end" (inclusive), e.g. GitLab URLs, submodule instructions and links to
  removed pages.
- Activates every ".. public-only" block: its indented content is a comment in the internal
  documentation and becomes regular content in the public one. Use it for the public replacement
  of an internal-only block, e.g.

      .. internal-only-begin

      git clone --recurse-submodules ssh://git@git.unibw.de:2222/...

      .. internal-only-end

      .. public-only

         git clone https://github.com/bassamlab/ufil.git

Markers may be indented (e.g. inside a list); the content keeps the indentation of the marker.

Usage: scripts/strip_internal.py <documentation root>
"""
import re
import shutil
import sys
from pathlib import Path

INTERNAL_BLOCK = re.compile(
    r"^[ \t]*\.\. internal-only-begin.*?^[ \t]*\.\. internal-only-end[^\n]*\n?", re.M | re.S)
PUBLIC_MARKER = re.compile(r"^([ \t]*)\.\. public-only[ \t]*$")


def activate_public_blocks(text: str) -> tuple[str, int]:
    lines = text.split("\n")
    out, count, i = [], 0, 0
    while i < len(lines):
        match = PUBLIC_MARKER.match(lines[i])
        if not match:
            out.append(lines[i])
            i += 1
            continue
        indent = len(match.group(1))
        block = []
        i += 1
        # The comment body: blank lines and lines indented deeper than the marker.
        while i < len(lines) and (not lines[i].strip() or
                                  len(lines[i]) - len(lines[i].lstrip()) > indent):
            block.append(lines[i])
            i += 1
        while block and not block[-1].strip():  # keep trailing blank lines outside the block
            block.pop()
            i -= 1
        body = [line for line in block if line.strip()]
        if not body:
            sys.exit("empty public-only block")
        shift = min(len(line) - len(line.lstrip()) for line in body) - indent
        out.extend(" " * indent + line[indent + shift:] if line.strip() else "" for line in block)
        count += 1
    return "\n".join(out), count


def main(root: Path) -> None:
    src = root / "src"
    for path in sorted(src.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        if "uofa" in path.name.lower() and path.exists():
            shutil.rmtree(path) if path.is_dir() else path.unlink()
            print(f"removed {path.relative_to(root)}")
    for rst in src.rglob("*.rst"):
        text = rst.read_text(encoding="utf-8")
        text, removed = INTERNAL_BLOCK.subn("", text)
        text, activated = activate_public_blocks(text)
        if removed or activated:
            rst.write_text(text, encoding="utf-8")
            print(f"{rst.relative_to(root)}: removed {removed} internal, "
                  f"activated {activated} public block(s)")
    leftovers = [str(p.relative_to(root)) for p in src.rglob("*.rst")
                 if re.search(r"internal-only-|\.\. public-only", p.read_text(encoding="utf-8"))]
    if leftovers:
        sys.exit(f"unbalanced internal-only/public-only markers in: {', '.join(leftovers)}")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "."))
