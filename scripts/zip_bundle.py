#!/usr/bin/env python3
"""Zip dist/TestCaseExporter into dist/TestCaseExporter-<os>-<arch>.zip.

macOS .app bundles are zipped with `ditto` instead (handled in CI), since
Python's zipfile mangles framework symlinks and breaks Gatekeeper.
"""
from __future__ import annotations

import pathlib
import platform
import sys
import zipfile

APP = "TestCaseExporter"
DIST = pathlib.Path("dist")


def main() -> int:
    sysname = platform.system().lower()
    arch = platform.machine().lower()
    out = DIST / f"{APP}-{sysname}-{arch}.zip"
    if out.exists():
        out.unlink()

    src = DIST / APP
    if not src.exists():
        print(f"ERROR: {src} not found", file=sys.stderr)
        return 1

    print(f"Zipping {src} -> {out}")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
        for p in src.rglob("*"):
            if p.is_file():
                zf.write(p, p.relative_to(src.parent))

    size_mb = out.stat().st_size / 1024 / 1024
    print(f"wrote {out} ({size_mb:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
