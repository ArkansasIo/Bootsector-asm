# Test Matrix

| Test | Command / method | Expected result |
|---|---|---|
| Assemble components | python3 scripts/build.py | All declared targets assemble |
| Validate menu schema | python3 scripts/menu_lint.py | PASS with menu count |
| Build floppy image | make image | 1,474,560-byte image |
| Verify floppy image | make verify | Size, signature, and layout checks pass |
| Boot floppy | make run | Stage 2 menu appears in QEMU |
| Build MBR image | make mbr-image | 10 MiB unformatted test image |
| Boot MBR image | QEMU with -boot c | MBR -> VBR -> stage 2 menu |
| OOP demo | Build a dedicated test harness | Counter should print 1 through 5 |

The OOP counter is a standalone flat binary, not a bootable disk image. It requires a dedicated test loader or test floppy wrapper before it can be executed in QEMU.
