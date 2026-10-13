# FloppyBoot Assembly Language Toolkit

The project language is NASM x86 assembly targeting 16-bit real mode for boot and firmware examples. NASM macros/includes are compile-time language facilities; JSON is host-side configuration/menu data, not a runtime language.

## Conventions
- NASM Intel syntax, `BITS 16`, and `ORG` for flat binaries.
- Shared includes under `asm/lib/` and `firmware/`.
- Pseudo-OOP data layouts and documented register-based calling conventions.
- Python tooling for builds, linting, image verification, and IDE actions.
- Raw binary output; boot components do not use a C runtime or linker.

See `docs/LANGUAGE_REFERENCE.md`, `docs/ASSEMBLY_LIBRARIES.md`, and `docs/IDE_GUIDE.md`.
