#!/usr/bin/env python3
"""Validate repository JSON configuration without third-party packages."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    "config/boot_options.json",
    "config/app_settings.json",
    "firmware/bios_profile.json",
    "firmware/cmos_registers.json",
    "examples/scripted_menu.json",
]
errors = []
for relative in FILES:
    path = ROOT / relative
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            errors.append(f"{relative}: root must be an object")
            continue
        if "schema_version" in value and not isinstance(value["schema_version"], int):
            errors.append(f"{relative}: schema_version must be an integer")
        print(f"PASS {relative}")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{relative}: {exc}")
if errors:
    print("\n".join("FAIL " + e for e in errors), file=sys.stderr)
    raise SystemExit(1)
print("All configuration files are valid JSON.")
