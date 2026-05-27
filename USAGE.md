# TC-Exporter — End-user installation & usage guide

Download the zip for your operating system from the
[latest GitHub Release](https://github.com/samip-git-shah/exporter/releases/latest):

| OS | File |
|---|---|
| Windows 10/11 | `TestCaseExporter-windows-x64.zip` |
| macOS (Apple Silicon) | `TestCaseExporter-darwin-arm64.zip` |
| Linux (x86_64) | `TestCaseExporter-linux-x64.zip` |

No Python, no `pip`, no internet required at runtime — Chromium and all
dependencies are bundled inside the zip.

> **Where to put the unzipped folder:** anywhere you have write access —
> `~/Applications/`, `~/Documents/TC-Exporter/`, your Desktop, etc. The app
> is fully self-contained; it does not install anything globally.

---

## macOS

### First-time launch (one-time setup, ~1 minute)

1. **Unzip** `TestCaseExporter-darwin-arm64.zip`. You will see a folder
   `TestCaseExporter/` containing two items:
   - `TestCaseExporter.app`
   - `Setup.command`
2. **Move the entire `TestCaseExporter/` folder** to where you want to
   keep it (e.g. `~/Applications/TestCaseExporter/`). Keep
   `Setup.command` next to the `.app` — the script looks for the app in
   the same folder it lives in.
3. **Double-click `Setup.command`**.
4. macOS will warn that the developer can't be verified:
   > *"Apple could not verify 'Setup.command' is free of malware..."*
   Click **Done**.
5. Open **System Settings → Privacy & Security**. Scroll to the *Security*
   section. You will see:
   > *"Setup.command was blocked to protect your Mac."*
   Click **Open Anyway** and enter your password.
6. **Double-click `Setup.command` again**. A Terminal window opens, the
   script clears macOS quarantine flags from the bundled app (a few
   seconds), and the TestCaseExporter app launches automatically.
7. You can close the Terminal window once the app is open.

### Regular use (every time after the first launch)

- **Double-click `TestCaseExporter.app`** — no warnings, no setup.
- *Optional:* drag `TestCaseExporter.app` to your **Dock** for one-click
  launching, or to your **Applications** folder so it appears in
  Spotlight (⌘ + Space → type "Test Case Exporter" → Enter).

### Troubleshooting macOS

| Symptom | Fix |
|---|---|
| Setup.command opens Terminal but the app doesn't launch | Run `xattr -cr /path/to/TestCaseExporter.app` manually |
| App launches and immediately exits with no error | Same as above — quarantine flags weren't cleared on nested binaries |
| Setup.command says "TestCaseExporter.app not found" | Make sure the `.app` and `Setup.command` are in the same folder |

For a silent crash, run the inner binary directly so the actual error
prints to the terminal:

```bash
/path/to/TestCaseExporter.app/Contents/MacOS/TestCaseExporter
```

---

## Windows

### First-time launch (one-time setup, ~30 seconds)

1. **Unzip** `TestCaseExporter-windows-x64.zip`. You will see a folder
   `TestCaseExporter\` containing the executable and supporting files.
2. **Move the folder** to where you want to keep it (e.g.
   `C:\Users\<you>\AppData\Local\TestCaseExporter\` or anywhere else).
   Keep all the files in the folder together — the executable depends on
   the DLLs and `_internal\` folder beside it.
3. **Double-click `TestCaseExporter.exe`** inside the folder.
4. Windows Defender SmartScreen will warn:
   > *"Windows protected your PC"*
   Click **More info** → **Run anyway**.
5. The app launches.

### Regular use (every time after the first launch)

- **Double-click `TestCaseExporter.exe`** — no warnings.
- *Optional shortcuts:*
  - Right-click `TestCaseExporter.exe` → **Send to → Desktop (create
    shortcut)** for a Desktop icon.
  - Right-click `TestCaseExporter.exe` → **Pin to Start** or **Pin to
    taskbar** for one-click launching.

### Troubleshooting Windows

| Symptom | Fix |
|---|---|
| "Windows protected your PC" with no "Run anyway" link | Right-click the .exe → **Properties** → check **Unblock** at the bottom → **OK**, then double-click again |
| Antivirus quarantines the .exe | Add an exception for the `TestCaseExporter\` folder in your antivirus settings |
| Missing DLL errors | Make sure you copied the *entire* unzipped folder, not just the .exe |

---

## Linux

### First-time launch (one-time setup, ~1 minute)

1. **Unzip** the download:
   ```bash
   unzip TestCaseExporter-linux-x64.zip
   ```
2. **Install Chromium runtime libraries** (most desktop distros already
   have them; required on minimal/server installs):

   **Debian / Ubuntu**
   ```bash
   sudo apt-get install -y libgbm1 libnss3 libxkbcommon0 libasound2 \
       libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxdamage1 \
       libxcomposite1 libxrandr2 libpango-1.0-0 libcairo2
   ```

   **Fedora / RHEL**
   ```bash
   sudo dnf install -y mesa-libgbm nss libxkbcommon alsa-lib atk \
       at-spi2-atk cups-libs libdrm libXdamage libXcomposite libXrandr \
       pango cairo
   ```
3. **Launch the app**:
   ```bash
   ./TestCaseExporter/TestCaseExporter
   ```

### Regular use (every time after the first launch)

From the terminal:
```bash
./TestCaseExporter/TestCaseExporter
```

Or create a `.desktop` entry so it appears in your application launcher
(GNOME / KDE / XFCE):

```bash
cat > ~/.local/share/applications/testcaseexporter.desktop <<EOF
[Desktop Entry]
Type=Application
Name=Test Case Exporter
Exec=$HOME/path/to/TestCaseExporter/TestCaseExporter
Icon=$HOME/path/to/TestCaseExporter/_internal/logo.png
Terminal=false
Categories=Office;Utility;
EOF
```

Replace `$HOME/path/to/` with the actual unzipped location. After this,
search for "Test Case Exporter" in your application menu.

### Troubleshooting Linux

| Symptom | Fix |
|---|---|
| `error while loading shared libraries: libgbm.so.1` | Install the runtime libraries listed in step 2 |
| `Permission denied` running the binary | `chmod +x TestCaseExporter/TestCaseExporter` |
| Blank window or Chromium fails to start | Run from terminal to see the error; usually a missing system library |

---

## Using the app

Once launched, the GUI walks you through:

1. **Connect to TargetProcess** — paste your TargetProcess URL and
   credentials (these are not persisted to disk).
2. **Select what to export** — pick the project, iteration, or specific
   test case IDs you want to export.
3. **Choose output format** — Word (`.docx`), PDF, or Excel.
4. **Pick a destination folder** — the app writes the export files there.
5. **Click Export** — a Chromium window may briefly appear in the
   background while the app scrapes the test cases; let it finish.

Exports complete in seconds for small selections, longer for large
projects. A progress indicator shows what's happening.

---

## Where the app stores logs

A file named `app.log` is written next to the executable (Windows /
Linux) or inside `TestCaseExporter.app/Contents/MacOS/` (macOS). Send
this file with any bug report — it captures the full sequence of what
the app did and where it failed.

## Where to report issues

Open an issue at
[github.com/samip-git-shah/exporter/issues](https://github.com/samip-git-shah/exporter/issues)
with:
- Your OS + version
- The version you downloaded (the release tag, e.g. `v1.0.1`)
- A description of what you were doing
- The contents of `app.log`
