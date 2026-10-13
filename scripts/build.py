#!/usr/bin/env python3
"""Build declared NASM components without shell interpolation."""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
NASM = shutil.which("nasm")
if not NASM:
    sys.exit("NASM was not found on PATH. Install NASM and retry.")

TARGETS = [
    ("boot/boot.asm", "boot.bin", "sector"),
    ("stage2/stage2.asm", "stage2.bin", "stage2"),
    ("boot/mbr.asm", "mbr.bin", "sector"),
    ("boot/vbr_mbr.asm", "vbr_mbr.bin", "sector"),
    ("firmware/cmos.asm", "cmos.bin", "binary"),
    ("firmware/rtc_snapshot_demo.asm", "rtc-snapshot-demo.bin", "binary"),
    ("os/kernel.asm", "kernel.bin", "binary"),
    ("examples/oop_counter.asm", "oop-counter.bin", "binary"),
    ("examples/library_demo.asm", "library-demo.bin", "binary"),
]
BUILD.mkdir(parents=True, exist_ok=True)
errors = []
for source, output, kind in TARGETS:
    src, dst = ROOT / source, BUILD / output
    if not src.is_file():
        errors.append(f"missing source: {source}")
        continue
    result = subprocess.run([NASM, "-I", str(ROOT) + "/", "-f", "bin", str(src), "-o", str(dst)], cwd=ROOT)
    if result.returncode:
        errors.append(f"NASM failed: {source}")
        continue
    data = dst.read_bytes()
    if kind == "sector" and (len(data) != 512 or data[510:512] != b"\x55\xaa"):
        errors.append(f"{output} must be 512 bytes with 55 AA signature")
    elif kind == "stage2" and not (0 < len(data) <= 4096):
        errors.append(f"{output} must be 1..4096 bytes")
    else:
        print(f"PASS {output}: {len(data)} bytes")
if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print("All declared assembly targets built.")
