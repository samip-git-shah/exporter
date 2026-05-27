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

## macOS — first-run Gatekeeper warning

The app is ad-hoc signed but **not notarized** by Apple, so on macOS 15
(Sequoia) and newer you will see:

> *"Apple could not verify 'TestCaseExporter.app' is free of malware..."*

This is normal for unsigned apps. Choose one of the two unblock paths below.

### Option A — System Settings (no terminal needed)

1. Unzip the download and move `TestCaseExporter.app` to **Applications/** (or anywhere you like).
2. Double-click it — you will see the warning. Click **Done**.
3. Open **System Settings → Privacy & Security**.
4. Scroll to the *Security* section. You will see:
   *"TestCaseExporter.app was blocked to protect your Mac."*
5. Click **Open Anyway** → enter your password.
6. Double-click the app again — it launches.

You only need to do this once per machine.

### Option B — One terminal command (faster for technical users)

```bash
xattr -dr com.apple.quarantine /path/to/TestCaseExporter.app
```

Replace `/path/to/` with wherever you unzipped the app. After this, the app
launches with a normal double-click — no warning.

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
