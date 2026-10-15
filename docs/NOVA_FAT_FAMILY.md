# NOVA FAT Family

This repository now documents an experimental filesystem family for the boot-sector/OS work:

- FAT32 — standard-oriented FAT32 implementation.
- NOVA-FAT64
- NOVA-FAT96
- NOVA-FAT128
- NOVA-FAT256
- NOVA-FAT512
- NOVA-FAT1024

FAT32 is the conventional FAT filesystem. FAT64 through FAT1024 are custom NOVA formats and are **not official FAT standards**.

## Allocation entry widths

| Format | Entry width | Bytes |
|---|---:|---:|
| FAT32 | 32-bit | 4 |
| NOVA-FAT64 | 64-bit | 8 |
| NOVA-FAT96 | 96-bit | 12 |
| NOVA-FAT128 | 128-bit | 16 |
| NOVA-FAT256 | 256-bit | 32 |
| NOVA-FAT512 | 512-bit | 64 |
| NOVA-FAT1024 | 1024-bit | 128 |

The higher-width formats use fixed-width little-endian cluster pointers. Their theoretical address spaces are mathematical format limits, not claims that current storage hardware can provide volumes of those sizes.

## Boot integration

The existing BIOS bootstrap remains the boot entry point. The next production step is a filesystem-aware loader that locates `KERNEL.BIN` by parsing the selected filesystem rather than using fixed-sector loading.
