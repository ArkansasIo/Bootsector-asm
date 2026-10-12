#!/usr/bin/env python3
from pathlib import Path
import sys

required = [Path("build/boot.bin"), Path("build/stage2.bin"), Path("build/floppy.img")]
for p in required:
    if not p.exists():
        sys.exit(f"FAIL: missing {p}; run make image")
boot, stage2, image = (p.read_bytes() for p in required)
checks = [
    (len(boot) == 512, f"boot sector size: {len(boot)} bytes, expected 512"),
    (boot[510:512] == b"\x55\xaa", "boot signature must be 55 AA"),
    (0 < len(stage2) <= 4096, f"stage2 size: {len(stage2)} bytes, maximum 4096"),
    (len(image) == 1_474_560, f"floppy image size: {len(image)} bytes"),
    (image[:512] == boot, "image sector 0 matches boot.bin"),
    (image[512:512+len(stage2)] == stage2, "stage2 begins at LBA 1"),
]
failed = False
for ok, message in checks:
    print(("PASS: " if ok else "FAIL: ") + message)
    failed |= not ok
sys.exit(1 if failed else 0)
