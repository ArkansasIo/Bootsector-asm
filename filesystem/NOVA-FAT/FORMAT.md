# NOVA-FAT Experimental Formats

## FAT32

Uses the conventional FAT32 model: BPB, reserved sectors, FAT copies, root directory cluster, and data clusters.

## NOVA-FAT64/96/128/256/512/1024

These are custom formats. Each uses a fixed-width little-endian allocation-table entry:

- FAT64: 8 bytes
- FAT96: 12 bytes
- FAT128: 16 bytes
- FAT256: 32 bytes
- FAT512: 64 bytes
- FAT1024: 128 bytes

`0` represents a free cluster. An allocation entry with every pointer bit set represents end-of-chain.

The header contains a magic identifier, version, flags, total sectors, FAT offset/size, root cluster, data offset, sector geometry, cluster count, and volume ID.

These formats are intended for OS/filesystem research and emulation; they are not standardized FAT implementations.
