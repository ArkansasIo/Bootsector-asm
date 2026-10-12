# Architecture

## Boot planes
1. Firmware plane: BIOS firmware and interrupt services.
2. Bootstrap plane: MBR for partitioned test image, or floppy boot sector for floppy image.
3. Loader plane: VBR and Stage 2 menu.
4. Kernel plane: separate real-mode kernel demo, not yet automatically loaded.
5. Services plane: planned disk I/O, FAT12 parser, diagnostics.
6. Host tools plane: build scripts, image builder and tests.

## Module tree
- BootManager
  - BIOSInit
  - Stage2Loader
  - BootDriveContext
- UserInterface
  - MainMenu
  - SubmenuRouter
  - ScreenRenderer
  - InputDispatcher
- DiskServices (planned)
  - SectorReader
  - CHSToLBA
  - FAT12Parser
  - RootDirectoryReader
  - ClusterChainReader
- Diagnostics (planned)
  - BootReport
  - MemoryMap
  - ImageVerifier
- HostTools
  - ImageBuilder
  - BootSectorVerifier
  - QEMULauncher

## Data and ownership
Stage 1 must remain 512 bytes, with its partition table/signature arrangement respected for MBR mode. Use stage 2's fixed load window cautiously, and never overwrite the running loader or stack. Disk writes are excluded from the boot menu prototype.
