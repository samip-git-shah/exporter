# TC-Exporter — building self-contained bundles

The build produces a **`--onedir` bundle per OS** that includes the Python
interpreter, all third-party libraries, and **Playwright's Chromium browser**.
End users do not need Python and do not need internet access at runtime.

## Two ways to run TC-Exporter

| Mode | What the user needs | Command |
|---|---|---|
| **Bundled** (recommended) | Nothing — just unzip and double-click | `dist/TestCaseExporter/TestCaseExporter[.exe]` |
| **Source** (fallback for devs) | Python 3.7+ installed | `launch.bat` / `launch.sh` |

The launcher scripts auto-detect which mode applies.

## Building

You must build separately on each OS you want to support — PyInstaller does
not cross-compile, and Chromium binaries are platform-specific.

### Easiest path: GitHub Actions (build all OSes from any machine)

If you only have a Mac (or only Windows), push the repo to GitHub and let
[`.github/workflows/build.yml`](.github/workflows/build.yml) build every OS
for you on real GitHub-hosted runners.

1. Create a GitHub repo and push this directory to it
2. Go to the **Actions** tab → "Build TC-Exporter bundles" → **Run workflow**
   (or just push a commit / tag `vX.Y.Z`)
3. After ~10–15 min per OS, download the four zips from the run's
   **Artifacts** section: `windows-x64`, `linux-x64`, `macos-x64`, `macos-arm64`
4. Tagging a commit `vX.Y.Z` additionally creates a GitHub Release with the
   four zips attached for one-click download by your users

Free for public repos; private repos get 2,000 free Actions minutes/month.

### Local path: build on each OS yourself

### Prerequisites
- Python 3.10–3.12 installed and on `PATH`
- ~3 GB free disk space (interpreter + Chromium + intermediate build/)

### One command

```bash
python build.py
```

That does the following:
1. Creates `.build-venv/`
2. `pip install -r requirements.txt`
3. `PLAYWRIGHT_BROWSERS_PATH=0 playwright install chromium` — installs Chromium
   *inside* the playwright package so PyInstaller bundles it
4. Runs PyInstaller with `TestCaseExporter.spec`
5. Zips the result into `dist/TestCaseExporter-<os>-<arch>.zip`

Useful flags:
- `python build.py --skip-install` — skip steps 2–3 on rebuilds
- `python build.py --clean` — wipe `build/`, `dist/`, and `.build-venv/` first
- `python build.py --no-zip` — leave the bundle unzipped only

### Output

| Platform | Output |
|---|---|
| Windows | `dist/TestCaseExporter/TestCaseExporter.exe` (+ `.zip`) |
| macOS | `dist/TestCaseExporter.app` and `dist/TestCaseExporter/` (+ `.zip`) |
| Linux | `dist/TestCaseExporter/TestCaseExporter` (+ `.zip`) |

Bundle size is roughly **250–350 MB** unzipped (Chromium accounts for ~170 MB).

## Distributing

Send the zip from `dist/` to end users. They:
1. Unzip
2. Double-click the executable (Windows) or `.app` (macOS), or run the binary
   from a terminal (Linux)

No Python install, no `pip install`, no `playwright install`, no internet.

## Notes & caveats

- **Linux**: Chromium still depends on a handful of system libraries
  (libgbm, libnss3, libxkbcommon0, etc.). If a target Linux box is missing
  them, install with `apt install libgbm1 libnss3 libxkbcommon0` etc. For a
  truly portable Linux build, package as AppImage or Flatpak.
- **macOS Gatekeeper**: an unsigned `.app` will be blocked on first run.
  Right-click → Open the first time, or sign + notarize for production
  distribution.
- **Windows SmartScreen**: an unsigned `.exe` will warn users on first run.
  Code-sign the binary for a clean install experience.
- **Icons**: drop `logo.ico` (Windows) or `logo.icns` (macOS) beside
  `TestCaseExporter.spec` and they'll be picked up automatically.
- **App writes `app.log`** alongside the executable when frozen, alongside
  `main.py` when running from source.
