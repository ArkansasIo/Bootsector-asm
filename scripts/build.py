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
    ("boot/boot.asm", "boot.bin", True),
    ("stage2/stage2.asm", "stage2.bin", False),
    ("boot/mbr.asm", "mbr.bin", True),
    ("boot/vbr_mbr.asm", "vbr_mbr.bin", True),
    ("firmware/cmos.asm", "cmos.bin", False),
    ("os/kernel.asm", "kernel.bin", False),
    ("examples/oop_counter.asm", "oop-counter.bin", False),
]
BUILD.mkdir(parents=True, exist_ok=True)
errors = []
for source, output, is_sector in TARGETS:
    src, dst = ROOT / source, BUILD / output
    if not src.is_file():
        errors.append(f"missing source: {source}")
        continue
    result = subprocess.run([NASM, "-f", "bin", str(src), "-o", str(dst)], cwd=ROOT)
    if result.returncode:
        errors.append(f"NASM failed: {source}")
        continue
    data = dst.read_bytes()
    if is_sector and (len(data) != 512 or data[510:512] != b"\x55\xaa"):
        errors.append(f"{output} must be 512 bytes with 55 AA signature")
    else:
        print(f"PASS {output}: {len(data)} bytes")
if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print("All declared assembly targets built.")
