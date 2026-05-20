#!/bin/bash
# Unix/Linux/Mac launcher for Test Case Exporter.
# Prefers a bundled executable (no Python required); falls back to source mode.

set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

# 1. Bundled .app (macOS, produced by build.py)
if [ -d "dist/TestCaseExporter.app" ]; then
    echo "Launching bundled TestCaseExporter.app..."
    open -W "dist/TestCaseExporter.app"
    exit 0
fi

# 2. Bundled --onedir build (Linux + macOS fallback)
if [ -x "dist/TestCaseExporter/TestCaseExporter" ]; then
    echo "Launching bundled TestCaseExporter..."
    exec "dist/TestCaseExporter/TestCaseExporter"
fi

# 3. Source mode — needs Python 3.7+ on the user's machine.
echo "No bundled build found — running from source via launch.py."
if command -v python3 &> /dev/null; then
    exec python3 launch.py
elif command -v python &> /dev/null; then
    exec python launch.py
fi

echo ""
echo "ERROR: Python is not installed and no bundled build was found."
echo "Either install Python 3.7+ or run build.py to produce a bundle."
exit 1
