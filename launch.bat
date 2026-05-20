@echo off
REM Windows launcher for Test Case Exporter.
REM Prefers a bundled executable (no Python required); falls back to source mode.

setlocal
cd /d "%~dp0"

REM 1. Bundled --onedir build produced by build.py
if exist "dist\TestCaseExporter\TestCaseExporter.exe" (
    echo Launching bundled TestCaseExporter...
    start "" "dist\TestCaseExporter\TestCaseExporter.exe"
    exit /b 0
)

REM 2. Source mode - needs Python 3.7+ installed.
echo No bundled build found - running from source via launch.py.
python launch.py
if errorlevel 1 (
    echo.
    echo Python not found! Trying python3...
    python3 launch.py
)
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed and no bundled build was found.
    echo Either install Python 3.7+ from https://www.python.org/
    echo or run "python build.py" to produce a self-contained bundle.
    pause
    exit /b 1
)
endlocal
