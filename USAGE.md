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

This is normal for unsigned apps. **Use the terminal command below — it's
the only method that reliably works on macOS 15+.**

### Recommended — clear all extended attributes (one command)

```bash
xattr -cr /path/to/TestCaseExporter.app
```

Replace `/path/to/` with wherever you unzipped the app (e.g.
`~/Downloads/TestCaseExporter.app`). After this, the app launches with a
normal double-click — no warning.

> **Why `-cr` and not `-dr com.apple.quarantine`?** macOS quarantines every
> file inside the bundle, not just the `.app` wrapper. The `-cr` flag clears
> *all* extended attributes recursively; `-dr com.apple.quarantine` only
> drops one specific attribute, which can leave nested binaries (Chromium's
> framework) blocked and the app fails silently.

### Why "Open Anyway" alone often fails

Using **System Settings → Privacy & Security → Open Anyway** dismisses the
warning on the outer `.app` but leaves the quarantine flag set on every
nested binary. The app appears to launch and then immediately exits with
no error. If you've already clicked "Open Anyway" and the app still won't
launch, run the `xattr -cr` command above.

### Diagnosing a silent failure

If double-clicking still does nothing after `xattr -cr`, run the inner
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
