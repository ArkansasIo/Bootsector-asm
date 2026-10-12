# Memory Map

| Physical range | Purpose |
|---|---|
| 00000-003FF | Interrupt Vector Table |
| 00400-004FF | BIOS Data Area |
| 07A00-07BFF | Stage-two stack region |
| 07C00-07DFF | Stage-one boot sector |
| 08000-08FFF | Stage-two load window (4096 bytes max) |
| A0000+ | Video/adapter region |

Available RAM varies. This prototype does not yet query INT 12h or E820.
