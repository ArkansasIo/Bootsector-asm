#!/usr/bin/env python3
"""Build 10 MiB unformatted MBR handoff test image; emulator use only."""
from pathlib import Path
import struct

root = Path(__file__).resolve().parents[1]
build = root / "build"
mbr = (build / "mbr.bin").read_bytes()
vbr = (build / "vbr_mbr.bin").read_bytes()
stage2 = (build / "stage2.bin").read_bytes()

for name, data in (("mbr.bin", mbr), ("vbr_mbr.bin", vbr)):
    if len(data) != 512 or data[510:512] != b"\x55\xaa":
        raise SystemExit(f"{name} must be 512 bytes with 55 AA signature")
if len(stage2) > 4096:
    raise SystemExit("stage2 exceeds 8-sector read window")

size = 10 * 1024 * 1024
image = bytearray(size)
image[:512] = mbr
entry = bytearray(16)
entry[0] = 0x80
entry[1:4] = bytes([0x00, 0x02, 0x00])  # start CHS sector 2 = LBA 1
entry[4] = 0xDA  # custom test partition type
entry[5:8] = bytes([0x01, 0x11, 0x13])  # test-image placeholder end CHS
struct.pack_into("<I", entry, 8, 1)
struct.pack_into("<I", entry, 12, size // 512 - 1)
image[446:462] = entry
image[512:1024] = vbr
image[1024:1024 + len(stage2)] = stage2
out = build / "mbr-test.img"
out.write_bytes(image)
print(f"Wrote {out}: {len(image)} bytes")
print("This is an unformatted MBR handoff test image, not an installable disk.")
