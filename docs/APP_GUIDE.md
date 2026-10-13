# FloppyBootSuite Control Center

## Web app and API

From the repository root run:

\`\`\`sh
python3 app.py
\`\`\`

The launcher starts the localhost API and opens the dashboard. Default URL: \`http://127.0.0.1:8765\`. Stop with Ctrl+C. Use \`python3 app.py --no-browser\` to suppress browser opening or \`python3 app.py --port 9000\` for another local port.

## Desktop editor

Run \`python3 app.py --desktop\` to open the existing Tkinter assembly IDE. Shortcuts: Ctrl+O, Ctrl+S, F5 build, F6 lint, F9 QEMU.

## Views

- **Overview:** toolchain status and quick build/verification/lint actions.
- **Project files:** searchable file inventory.
- **Build & tests:** explicit build, verify, lint, and clean operations.
- **Settings:** read-only display of app settings.
- **Activity console:** command output and errors.

The dashboard is a project control surface, not a replacement for a full source editor. Use the desktop IDE or your preferred editor to change assembly source.

## Requirements

Python 3.10+ recommended. The web UI/API use only the standard library. NASM, GNU Make, and QEMU are optional but required for their respective build/emulator actions. Desktop mode needs Python with Tkinter and a compatible Make/NASM toolchain.

## Safety

The API runs only on loopback and rejects non-loopback bind addresses. The UI does not expose arbitrary shell commands. CMOS writes and physical disk writes remain disabled. Review the Makefile clean target before running clean in a customized checkout.
