# TC-Exporter — End-user installation guide

Download the zip for your operating system from the
[latest GitHub Release](https://github.com/samip-git-shah/exporter/releases/latest):

| OS | File |
|---|---|
| Windows 10/11 | `TestCaseExporter-windows-x64.zip` |
| macOS (Apple Silicon) | `TestCaseExporter-darwin-arm64.zip` |
| Linux (x86_64) | `TestCaseExporter-linux-x64.zip` |

No Python, no `pip`, no internet required at runtime — Chromium and all
dependencies are bundled inside the zip.

---

## macOS — first-run setup

The app is ad-hoc signed but **not notarized** by Apple, so on macOS 15
(Sequoia) and newer macOS will silently block it from launching unless
you clear quarantine flags first. The zip ships with a setup script that
does this for you.

### Recommended — run Setup.command once

1. Unzip `TestCaseExporter-darwin-arm64.zip`. You will see a folder
   `TestCaseExporter/` containing two items:
   - `TestCaseExporter.app`
   - `Setup.command`
2. Double-click **Setup.command**.
3. The first time you run it, macOS will warn that it can't verify the
   developer. Click **Done**, then go to
   **System Settings → Privacy & Security**, scroll to *Security*, click
   **Open Anyway** next to "Setup.command was blocked", and confirm with
   your password.
4. Run **Setup.command** again. It clears the quarantine flags on the
   bundled app (one-time, takes a few seconds) and launches the app.
5. From now on, just double-click `TestCaseExporter.app` directly — no
   warnings, no setup.

### Manual alternative — terminal command

If the Setup.command path doesn't work, open Terminal and run:

```bash
xattr -cr /path/to/TestCaseExporter.app
```

Replace `/path/to/` with wherever you unzipped the app. After this, the
app launches normally on double-click.

> **Why this is needed:** macOS quarantines every file inside the bundle,
> not just the `.app` wrapper. Apple's "Open Anyway" only clears the
> wrapper, leaving nested Chromium framework binaries blocked — the app
> appears to launch and then immediately exits with no error. `xattr -cr`
> (and Setup.command, which calls it) clears *every* nested file.

### Diagnosing a silent failure

If double-clicking still does nothing after the steps above, run the inner
binary directly so any error becomes visible:

```bash
/path/to/TestCaseExporter.app/Contents/MacOS/TestCaseExporter
```

Then send the terminal output to support — that's the actionable error.

---

## Windows — first-run SmartScreen warning

The `.exe` is unsigned, so Windows Defender SmartScreen will show:

> *"Windows protected your PC"*

To bypass:

1. Unzip the download.
2. Double-click `TestCaseExporter\TestCaseExporter.exe`.
3. On the SmartScreen warning, click **More info**.
4. Click **Run anyway**.

Only needed on first launch. For subsequent launches just double-click.

---

## Linux — system library prerequisites

Chromium (bundled inside the zip) dynamically links against a handful of
system libraries that ship with most desktop distributions but may be
missing on minimal/server installs. If the app fails to launch, install:

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

Then run:

```bash
./TestCaseExporter/TestCaseExporter
```

---

## Where the app stores logs

A file named `app.log` is written **next to the executable** (or, on macOS,
inside `TestCaseExporter.app/Contents/MacOS/`). Send this file along with
any bug report.
