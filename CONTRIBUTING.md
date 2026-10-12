# Contributing

- Keep the first-stage boot sector exactly 512 bytes.
- Keep Stage 2 at or below the initial 4096-byte read limit.
- Document memory ranges, routine inputs/outputs, and register clobbers.
- Do not add physical disk writes to the boot UI without explicit safeguards.
- Add host-side tests for image layout and data-driven menu validation.
- Test in an emulator before claiming boot support.
- Distinguish implemented behavior from planned architecture in documentation.
