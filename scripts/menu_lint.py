#!/usr/bin/env python3
"""Validate menu JSON structure and duplicate IDs/keys."""
import json
from pathlib import Path
import sys
path = Path(__file__).resolve().parents[1] / "examples" / "scripted_menu.json"
data = json.loads(path.read_text(encoding="utf-8"))
menus = data.get("menus")
if not isinstance(menus, list) or not menus:
    sys.exit("ERROR: menus must be a non-empty array")
ids = set()
for menu in menus:
    mid = menu.get("id")
    if not mid or mid in ids:
        sys.exit(f"ERROR: missing or duplicate menu ID: {mid!r}")
    ids.add(mid)
    keys = set()
    for entry in menu.get("entries", []):
        key = entry.get("key")
        if not isinstance(key, str) or len(key) != 1:
            sys.exit(f"ERROR: menu {mid}: key must be one character")
        if key.upper() in keys:
            sys.exit(f"ERROR: menu {mid}: duplicate key {key}")
        keys.add(key.upper())
        if not entry.get("label") or not entry.get("target"):
            sys.exit(f"ERROR: menu {mid}: entries need label and target")
print(f"PASS: validated {len(menus)} menus")
