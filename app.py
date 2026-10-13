#!/usr/bin/env python3
"""Launch the FloppyBootSuite local web app/API or desktop assembly IDE."""
import argparse, os, sys, threading, time, urllib.request, webbrowser
from pathlib import Path
ROOT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description="FloppyBootSuite application launcher")
    parser.add_argument("--desktop", action="store_true", help="launch the existing Tkinter assembly IDE")
    parser.add_argument("--no-browser", action="store_true", help="start the API without opening a browser")
    parser.add_argument("--host", default="127.0.0.1", help="local bind address (localhost only)")
    parser.add_argument("--port", type=int, default=8765, help="local API/UI port")
    args = parser.parse_args()
    if args.desktop:
        os.execv(sys.executable, [sys.executable, str(ROOT / "scripts" / "asm_ide.py")])
    if args.host not in ("127.0.0.1", "localhost", "::1"): parser.error("Only localhost binding is supported.")
    if not 1 <= args.port <= 65535: parser.error("Port must be between 1 and 65535.")
    os.environ["FLOPPY_APP_HOST"] = args.host
    os.environ["FLOPPY_APP_PORT"] = str(args.port)
    if not args.no_browser:
        url = "http://%s:%d" % ("127.0.0.1" if args.host == "::1" else args.host, args.port)
        def open_when_ready():
            for _ in range(40):
                time.sleep(0.25)
                try:
                    urllib.request.urlopen(url + "/api/health", timeout=0.5).close()
                    webbrowser.open(url); return
                except Exception: continue
        threading.Thread(target=open_when_ready, daemon=True).start()
    from api.server import main as serve
    serve()

if __name__ == "__main__": main()
