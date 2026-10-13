#!/usr/bin/env python3
"""Localhost-only HTTP/JSON API and static UI for FloppyBootSuite."""
from __future__ import annotations
import json, os, subprocess, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "app" / "web"
HOST = os.environ.get("FLOPPY_APP_HOST", "127.0.0.1")
PORT = int(os.environ.get("FLOPPY_APP_PORT", "8765"))
MAX_BODY = 16_384
COMMANDS = {"build": ["make", "components", "image"], "verify": ["make", "verify"],
            "lint": ["make", "lint", "config-lint"], "clean": ["make", "clean"]}
FOLDERS = ("asm", "boot", "stage2", "firmware", "os", "examples", "tests", "tools",
           "scripts", "language", "docs", "config", "api", "app")

def project_files():
    items = []
    for folder in FOLDERS:
        base = ROOT / folder
        if base.is_dir():
            for path in sorted(base.rglob("*")):
                if path.is_file() and not any(p in {".git", "__pycache__", "build", "node_modules"} for p in path.parts):
                    items.append({"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size})
    return items

def run_command(name):
    if name not in COMMANDS:
        return {"ok": False, "error": "Unsupported command", "allowed": sorted(COMMANDS)}, 400
    try:
        result = subprocess.run(COMMANDS[name], cwd=ROOT, capture_output=True, text=True, timeout=180)
        return {"ok": result.returncode == 0, "command": COMMANDS[name], "returncode": result.returncode,
                "output": (result.stdout + result.stderr)[-12000:]}, 200
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "Command timed out after 180 seconds"}, 504
    except OSError as exc:
        return {"ok": False, "error": str(exc)}, 500

class Handler(BaseHTTPRequestHandler):
    server_version = "FloppyBootSuiteAPI/1.0"
    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))
    def send_json(self, payload, status=200):
        body = json.dumps(payload, indent=2).encode()
        self.send_response(status); self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body))); self.send_header("Cache-Control", "no-store")
        self.end_headers(); self.wfile.write(body)
    @staticmethod
    def which(program):
        import shutil
        return shutil.which(program) is not None
    def send_static(self, name, content_type):
        target = WEB / name
        if not target.is_file(): return self.send_json({"error": "UI asset missing", "file": name}, 404)
        body = target.read_bytes()
        self.send_response(200); self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body))); self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            return self.send_json({"ok": True, "app": "FloppyBootSuite", "apiVersion": "1.0", "root": str(ROOT)})
        if path == "/api/status":
            return self.send_json({"ok": True, "project": ROOT.name, "python": sys.version.split()[0],
                "nasmAvailable": self.which("nasm"), "makeAvailable": self.which("make"),
                "qemuAvailable": self.which("qemu-system-i386"), "imageExists": (ROOT / "build" / "floppy.img").is_file()})
        if path == "/api/files": return self.send_json({"files": project_files()})
        if path == "/api/settings":
            try: return self.send_json(json.loads((ROOT / "config" / "app_settings.json").read_text(encoding="utf-8")))
            except (OSError, json.JSONDecodeError) as exc: return self.send_json({"error": str(exc)}, 500)
        if path in ("/", "/index.html"): return self.send_static("index.html", "text/html; charset=utf-8")
        if path == "/app.css": return self.send_static("app.css", "text/css; charset=utf-8")
        if path == "/app.js": return self.send_static("app.js", "text/javascript; charset=utf-8")
        return self.send_json({"error": "Not found"}, 404)
    def do_POST(self):
        if urlparse(self.path).path != "/api/commands": return self.send_json({"error": "Not found"}, 404)
        if self.client_address[0] not in ("127.0.0.1", "::1"): return self.send_json({"error": "Local requests only"}, 403)
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > MAX_BODY: return self.send_json({"error": "Request body must be between 1 and 16384 bytes"}, 413)
            payload = json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError): return self.send_json({"error": "Expected a valid JSON body"}, 400)
        name = payload.get("command") if isinstance(payload, dict) else None
        result, status = run_command(name)
        return self.send_json(result, status)

def main():
    if HOST not in ("127.0.0.1", "localhost", "::1"):
        raise SystemExit("Refusing non-local bind. Use 127.0.0.1, localhost, or ::1.")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print("FloppyBootSuite UI: http://%s:%d" % ("127.0.0.1" if HOST == "::1" else HOST, PORT))
    print("API health: http://%s:%d/api/health" % ("127.0.0.1" if HOST == "::1" else HOST, PORT))
    try: server.serve_forever()
    except KeyboardInterrupt: print("\nStopping API server...")
    finally: server.server_close()

if __name__ == "__main__": main()
