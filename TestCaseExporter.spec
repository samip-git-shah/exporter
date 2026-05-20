# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for TC-Exporter.

Goal: ship a self-contained --onedir bundle that runs without Python or internet.

Chromium is installed into the playwright package via
`PLAYWRIGHT_BROWSERS_PATH=0 playwright install chromium` in build.py / CI.
We deliberately exclude that browser tree from PyInstaller's data collection
because PyInstaller flattens macOS framework symlinks (Versions/Current,
Resources, Helpers), corrupting Chromium.app. Instead we copy the browser
tree post-COLLECT with `shutil.copytree(..., symlinks=True)` and route
Playwright to it via rthooks/playwright_browsers.py.
"""

import os
import shutil
import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules


# ---- App resources -----------------------------------------------------------
datas = [
    ("logo.png", "."),
]

# customtkinter ships JSON themes + fonts that must travel with the bundle.
datas += collect_data_files("customtkinter")

# tkcalendar locale data + Babel locale data (tkcalendar dep).
datas += collect_data_files("tkcalendar")
datas += collect_data_files("babel")

# Playwright Python sources only — explicitly drop the bundled-browsers tree.
# We re-add it post-COLLECT, preserving symlinks.
_playwright_data = collect_data_files("playwright", include_py_files=False)
_playwright_data = [
    (src, dst) for src, dst in _playwright_data if ".local-browsers" not in src
]
datas += _playwright_data

# reportlab fonts/ttfs and python-docx default templates.
datas += collect_data_files("reportlab")
datas += collect_data_files("docx")


# ---- Hidden imports ----------------------------------------------------------
hiddenimports = []
hiddenimports += collect_submodules("playwright")
hiddenimports += collect_submodules("customtkinter")
hiddenimports += collect_submodules("tkcalendar")
hiddenimports += ["babel.numbers", "babel.dates"]


# ---- Analysis ----------------------------------------------------------------
a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=["rthooks/playwright_browsers.py"],
    excludes=[],
    noarchive=False,
)


# Belt-and-braces: drop any .local-browsers entries Playwright's bundled hook
# may have re-added to a.datas / a.binaries.
def _strip_browsers(toc):
    return [entry for entry in toc if ".local-browsers" not in entry[0]
            and ".local-browsers" not in entry[1]]


a.datas = _strip_browsers(a.datas)
a.binaries = _strip_browsers(a.binaries)


pyz = PYZ(a.pure, a.zipped_data)


# ---- Icon -------------------------------------------------------------------
_icon_candidates = {"win32": "logo.ico", "darwin": "logo.icns"}
_icon = _icon_candidates.get(sys.platform)
_icon = _icon if _icon and Path(_icon).exists() else None


exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="TestCaseExporter",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=_icon,
)


coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="TestCaseExporter",
)


# macOS: also produce a .app bundle.
if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="TestCaseExporter.app",
        icon=_icon,
        bundle_identifier="com.sycamore.tcexporter",
        info_plist={
            "CFBundleShortVersionString": "1.0.0",
            "NSHighResolutionCapable": "True",
        },
    )


# ---- Post-build: copy Chromium tree, preserving symlinks --------------------
def _copy_playwright_browsers() -> None:
    import playwright

    src = (
        Path(playwright.__file__).resolve().parent
        / "driver" / "package" / ".local-browsers"
    )
    if not src.exists():
        # Some versions store the tree elsewhere — try driver/.local-browsers as fallback.
        alt = Path(playwright.__file__).resolve().parent / "driver" / ".local-browsers"
        if alt.exists():
            src = alt
        else:
            raise SystemExit(
                f"ERROR: Playwright browsers not found at {src} or {alt}. "
                "Did you run `PLAYWRIGHT_BROWSERS_PATH=0 playwright install chromium` "
                "before PyInstaller?"
            )

    dist = Path(DISTPATH)
    targets = []

    onedir = dist / "TestCaseExporter"
    if onedir.exists():
        # PyInstaller 6.x onedir layout puts non-script datas under _internal/
        internal = onedir / "_internal"
        targets.append((internal if internal.exists() else onedir) / "ms-playwright")

    if sys.platform == "darwin":
        appdir = dist / "TestCaseExporter.app" / "Contents" / "Resources"
        if appdir.exists():
            targets.append(appdir / "ms-playwright")

    if not targets:
        print("WARNING: no PyInstaller output directory found to copy Chromium into")
        return

    for dst in targets:
        if dst.exists():
            shutil.rmtree(dst)
        print(f"Copying Chromium tree:\n  src: {src}\n  dst: {dst}")
        shutil.copytree(src, dst, symlinks=True)


_copy_playwright_browsers()
