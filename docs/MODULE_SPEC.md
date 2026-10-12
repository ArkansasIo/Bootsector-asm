# Module Specification

## Core
- BootManager: boot drive, boot state, stage handoff.
- BIOSServices: video, keyboard, disk wrappers.
- Stage2Loader: bounded reads and transfer of control.
- KernelEntry: OS entry contract; kernel currently builds separately.

## User interface
- ScreenRenderer: BIOS text output.
- MenuRouter: key-to-menu dispatch.
- MenuData: hard-coded assembly strings today; JSON schema for future generation.
- HelpPanel: controls and limitations.

## Firmware demonstration
- CMOSRTC: reads selected RTC registers; mode decoding and update synchronization remain TODO.
- BIOSBoundary: wrappers over existing firmware, not replacement firmware.

## Host tooling
- BuildOrchestrator: Python invokes NASM and validates output.
- MenuLinter: validates JSON menu metadata.
- ImageBuilder: creates raw test images.
- BootVerifier: size, signature, and image-layout checks.

## Future service contracts
Disk services should return explicit status, preserve source drive, validate sector ranges, retry after reset, and keep writes disabled by default.
