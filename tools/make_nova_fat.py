#!/usr/bin/env python3
"""Generate small experimental NOVA-FAT images.

FAT32 is standard-oriented. 64/96/128/256/512/1024-bit variants are custom
NOVA formats and are not official FAT filesystems.
"""
from pathlib import Path
import argparse

SECTOR = 512
FORMATS = {32: 4, 64: 8, 96: 12, 128: 16, 256: 32, 512: 64, 1024: 128}


def put(buf, off, value, width):
    buf[off:off + width] = int(value).to_bytes(width, "little")


def make(bits, output):
    entry_bytes = FORMATS[bits]
    sectors = 4096 if bits != 32 else 16384
    fat_offset = 1
    fat_sectors = 1024 if bits != 32 else 512
    data_offset = fat_offset + fat_sectors
    root_cluster = 2
    image = bytearray(sectors * SECTOR)

    magic = (b"NOVA32F0" if bits == 32 else f"NOVA{bits:04d}".encode()[:8])
    image[:8] = magic.ljust(8, b"\0")
    put(image, 8, 1, 4)
    put(image, 12, 0, 4)
    put(image, 16, sectors, 8)
    put(image, 24, fat_offset, 8)
    put(image, 32, fat_sectors, 8)
    put(image, 40, root_cluster, 8)
    put(image, 48, data_offset, 8)
    put(image, 56, SECTOR, 4)
    put(image, 60, 1, 4)
    put(image, 64, sectors - data_offset, 8)
    put(image, 72, 0x20261015, 8)
    image[510:512] = b"\x55\xAA"

    def fat_set(cluster, value):
        off = fat_offset * SECTOR + cluster * entry_bytes
        image[off:off + entry_bytes] = int(value).to_bytes(entry_bytes, "little")

    eoc = (1 << bits) - 1
    fat_set(0, eoc)
    fat_set(1, eoc)
    fat_set(root_cluster, eoc)

    root = (data_offset + root_cluster - 2) * SECTOR
    image[root:root + 32] = b"KERNEL.BIN".ljust(32, b"\0")
    put(image, root + 32, 0, 4)
    first = 3
    put(image, root + 36, first, entry_bytes)
    kernel = b"NOVA-OS KERNEL\r\n"
    put(image, root + 36 + entry_bytes, len(kernel), 8)
    fat_set(first, eoc)
    data = (data_offset + first - 2) * SECTOR
    image[data:data + len(kernel)] = kernel

    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_bytes(image)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("format", type=int, choices=FORMATS)
    ap.add_argument("-o", "--output", default=None)
    args = ap.parse_args()
    out = args.output or f"build/nova-fat{args.format}.img"
    make(args.format, out)
    print(f"created {out}")
