# Testing

Run `make components && make image && make verify`.
Run the floppy UI in QEMU with `make run`.
Create/run MBR handoff image with `make mbr-image` and `qemu-system-i386 -drive file=build/mbr-test.img,format=raw -boot c`.

Check menu choices 1-5, return with B/Backspace/Escape, and Q to reboot from main screen. Use disposable emulator images only; do not use unfinished writer code against important media.
