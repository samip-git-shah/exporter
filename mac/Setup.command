#!/bin/bash
# TestCaseExporter — first-run setup for macOS.
#
# macOS quarantines every file inside an unsigned .app downloaded from the
# internet, not just the outer bundle. Apple's "Open Anyway" only clears
# the wrapper, leaving nested Chromium framework binaries blocked — so the
# app launches and immediately exits with no error.
#
# This script clears extended attributes recursively on the bundled .app,
# then launches it.

set -e

HERE="$(cd "$(dirname "$0")" && pwd)"
APP="$HERE/TestCaseExporter.app"

if [ ! -d "$APP" ]; then
    echo "ERROR: TestCaseExporter.app not found next to this script."
    echo "       Expected at: $APP"
    echo ""
    echo "Make sure you unzipped the download and that Setup.command sits"
    echo "in the same folder as TestCaseExporter.app."
    read -n 1 -s -r -p "Press any key to close..."
    exit 1
fi

echo "Clearing macOS quarantine flags on TestCaseExporter.app..."
xattr -cr "$APP"
echo "Done."
echo ""
echo "Launching TestCaseExporter..."
open "$APP"
echo ""
echo "You can close this window. Future launches: just double-click TestCaseExporter.app."
