#!/usr/bin/env python3
"""TC-Exporter build script.

Run on each target OS to produce a self-contained --onedir bundle that needs
no Python install and no internet at runtime. Chromium is installed inside
the playwright package via PLAYWRIGHT_BROWSERS_PATH=0 so PyInstaller bundles
it alongside the rest of the package data.

Usage:
    python build.py                 # full build (recommended)
    python build.py --skip-install  # reuse the existing build venv
    python build.py --clean         # wipe build/, dist/, build venv first
"""
from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD_VENV = ROOT / ".build-venv"
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"
SPEC_FILE = ROOT / "TestCaseExporter.spec"
REQS = ROOT / "requirements.txt"
APP_NAME = "TestCaseExporter"


def run(cmd: list[str], env: dict | None = None) -> None:
    print(f"\n$ {' '.join(str(c) for c in cmd)}")
    subprocess.check_call(cmd, cwd=ROOT, env=env)


def venv_python() -> Path:
    if platform.system() == "Windows":
        return BUILD_VENV / "Scripts" / "python.exe"
    return BUILD_VENV / "bin" / "python"


def ensure_venv() -> None:
    if BUILD_VENV.exists():
        print(f"Reusing build venv at {BUILD_VENV}")
        return
    print(f"Creating build venv at {BUILD_VENV}")
    run([sys.executable, "-m", "venv", str(BUILD_VENV)])


def install_deps() -> None:
    py = str(venv_python())
    run([py, "-m", "pip", "install", "--upgrade", "pip", "wheel", "setuptools"])
    run([py, "-m", "pip", "install", "-r", str(REQS)])

    # Install Chromium *inside* the playwright package so PyInstaller bundles it.
    env = os.environ.copy()
    env["PLAYWRIGHT_BROWSERS_PATH"] = "0"
    print("\nInstalling Chromium into the playwright package (PLAYWRIGHT_BROWSERS_PATH=0)")
    subprocess.check_call([py, "-m", "playwright", "install", "chromium"], cwd=ROOT, env=env)


def clean() -> None:
    for path in (DIST_DIR, BUILD_DIR, BUILD_VENV):
        if path.exists():
            print(f"Removing {path}")
            shutil.rmtree(path, ignore_errors=True)


def build_bundle() -> None:
    py = str(venv_python())
    env = os.environ.copy()
    env["PLAYWRIGHT_BROWSERS_PATH"] = "0"  # so the spec hook resolves chromium correctly

    # Wipe stale build/ and dist/ for the app to keep the bundle clean.
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR, ignore_errors=True)
    app_dist = DIST_DIR / APP_NAME
    if app_dist.exists():
        shutil.rmtree(app_dist, ignore_errors=True)
    app_bundle = DIST_DIR / f"{APP_NAME}.app"
    if app_bundle.exists():
        shutil.rmtree(app_bundle, ignore_errors=True)

    run([py, "-m", "PyInstaller", "--noconfirm", str(SPEC_FILE)], env=env)


def package_zip() -> Path | None:
    """Zip the onedir bundle for easy distribution."""
    src = DIST_DIR / APP_NAME
    if not src.exists():
        print(f"WARNING: expected {src} not found; skipping zip step")
        return None

    sysname = platform.system().lower()
    arch = platform.machine().lower()
    out = DIST_DIR / f"{APP_NAME}-{sysname}-{arch}.zip"
    if out.exists():
        out.unlink()

    print(f"\nZipping bundle to {out}")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
        for path in src.rglob("*"):
            zf.write(path, path.relative_to(DIST_DIR))
    print(f"  size: {out.stat().st_size / 1024 / 1024:.1f} MB")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clean", action="store_true", help="wipe build/, dist/, and the build venv first")
    parser.add_argument("--skip-install", action="store_true", help="reuse the existing build venv (faster rebuilds)")
    parser.add_argument("--no-zip", action="store_true", help="skip the final zip step")
    args = parser.parse_args()

    print(f"=== TC-Exporter build :: {platform.system()} {platform.machine()} ===")

    if args.clean:
        clean()

    ensure_venv()
    if not args.skip_install:
        install_deps()

    build_bundle()

    if not args.no_zip:
        package_zip()

    print("\n✅ Build complete.")
    print(f"   Bundle: {DIST_DIR / APP_NAME}")
    if platform.system() == "Darwin":
        print(f"   App:    {DIST_DIR / (APP_NAME + '.app')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
