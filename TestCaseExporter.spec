# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for TC-Exporter.

Goal: ship a self-contained --onedir bundle that runs without Python or internet.
Chromium is installed into the playwright package via PLAYWRIGHT_BROWSERS_PATH=0
in build.py, so PyInstaller's collect_data_files("playwright") picks it up.
"""

import os
import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# ---- App resources -----------------------------------------------------------
datas = [
    ("logo.png", "."),
]

# customtkinter ships JSON themes + fonts that must travel with the bundle.
datas += collect_data_files("customtkinter")

# tkcalendar ships locale .msg files used by Babel.
datas += collect_data_files("tkcalendar")

# Babel locale data (tkcalendar depends on it).
datas += collect_data_files("babel")

# Playwright + bundled Chromium (installed via PLAYWRIGHT_BROWSERS_PATH=0).
datas += collect_data_files("playwright", include_py_files=False)

# reportlab fonts/ttfs.
datas += collect_data_files("reportlab")

# python-docx default templates.
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
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

# Icon: Windows wants .ico, macOS wants .icns. Use only if present beside the spec.
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
