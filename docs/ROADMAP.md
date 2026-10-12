# Roadmap

Implemented in this starter:
- BIOS stage 1 and stage 2 console
- text menus/submenus
- MBR and test partition VBR
- CMOS/RTC register demo
- separate real-mode kernel demo
- build and verification scripts

Planned:
- robust disk retry/reset and EDD/LBA support
- valid FAT12 BPB and volume format
- FAT12 root-directory and cluster-chain loader
- kernel loading integrated into stage 2
- memory detection and diagnostics
- host-side sector-by-sector clone tool with bounds validation and checksums
- automated emulator smoke tests
