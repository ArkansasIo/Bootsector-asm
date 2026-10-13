# Assembly library catalog

| Include | Purpose | Contract |
|---|---|---|
| `asm/lib/console.inc` | BIOS teletype output | DS:SI string; AL character |
| `asm/lib/hex.inc` | Print byte in hexadecimal | AL input |
| `asm/lib/keyboard.inc` | Read/check key | BIOS INT 16h |
| `asm/lib/disk_chs.inc` | CHS read/reset wrapper | BIOS INT 13h |
| `asm/lib/memory.inc` | Copy/fill bytes | DS:SI, ES:DI, CX |
| `firmware/bios_services.inc` | BIOS video/print/key/disk helpers | Real mode |
| `firmware/cmos.inc` | CMOS byte read | AL index -> AL value |

These are source-level includes, not separately linked binaries. Include each once per assembled module and respect the register contracts.
