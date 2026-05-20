"""PyInstaller runtime hook: point Playwright at the bundled Chromium.

Chromium is copied next to the executable post-build (see TestCaseExporter.spec),
not packed into _MEIPASS, because PyInstaller's data-collection step does not
preserve macOS framework symlinks. This hook runs *before* main.py imports
playwright and tells it where to find the bundled browser.
"""
import os
import sys
from pathlib import Path


def _browsers_dir() -> Path:
    exe = Path(sys.executable).resolve()
    # macOS .app bundle: ms-playwright/ lives in Contents/Resources
    if sys.platform == "darwin" and exe.parent.name == "MacOS":
        return exe.parents[1] / "Resources" / "ms-playwright"
    # Windows / Linux onedir: ms-playwright/ lives next to the exe
    return exe.parent / "ms-playwright"


os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(_browsers_dir())
