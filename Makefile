NASM ?= nasm
PYTHON ?= python3
BUILD := build
BOOT := $(BUILD)/boot.bin
STAGE2 := $(BUILD)/stage2.bin
MBR := $(BUILD)/mbr.bin
VBR_MBR := $(BUILD)/vbr_mbr.bin
KERNEL := $(BUILD)/kernel.bin
CMOS := $(BUILD)/cmos.bin
RTC_DEMO := $(BUILD)/rtc-snapshot-demo.bin
LIB_DEMO := $(BUILD)/library-demo.bin
OOP_DEMO := $(BUILD)/oop-counter.bin
IMAGE := $(BUILD)/floppy.img

.PHONY: all components image run verify mbr-image lint config-lint scripted-build oop-demo ide clean
all: image

$(BUILD):
	mkdir -p $(BUILD)

$(BOOT): boot/boot.asm | $(BUILD)
	$(NASM) -f bin -I ./ $< -o $@
	test "$$(wc -c < $@)" -eq 512

$(STAGE2): stage2/stage2.asm | $(BUILD)
	$(NASM) -f bin -I ./ $< -o $@
	test "$$(wc -c < $@)" -le 4096

$(MBR): boot/mbr.asm | $(BUILD)
	$(NASM) -f bin -I ./ $< -o $@
	test "$$(wc -c < $@)" -eq 512

$(VBR_MBR): boot/vbr_mbr.asm | $(BUILD)
	$(NASM) -f bin -I ./ $< -o $@
	test "$$(wc -c < $@)" -eq 512

$(KERNEL): os/kernel.asm | $(BUILD)
	$(NASM) -f bin -I ./ $< -o $@

$(CMOS): firmware/cmos.asm | $(BUILD)
	$(NASM) -f bin -I ./ $< -o $@

$(RTC_DEMO): firmware/rtc_snapshot_demo.asm | $(BUILD)
	$(NASM) -f bin -I ./ $< -o $@

$(LIB_DEMO): examples/library_demo.asm | $(BUILD)
	$(NASM) -f bin -I ./ $< -o $@

$(OOP_DEMO): examples/oop_counter.asm | $(BUILD)
	$(NASM) -f bin -I ./ $< -o $@

components: $(BOOT) $(STAGE2) $(MBR) $(VBR_MBR) $(KERNEL) $(CMOS) $(RTC_DEMO) $(LIB_DEMO) $(OOP_DEMO)

image: $(BOOT) $(STAGE2)
	dd if=/dev/zero of=$(IMAGE) bs=512 count=2880 status=none
	dd if=$(BOOT) of=$(IMAGE) bs=512 count=1 conv=notrunc status=none
	dd if=$(STAGE2) of=$(IMAGE) bs=512 seek=1 conv=notrunc status=none
	truncate -s 1474560 $(IMAGE)
	@echo "Built $(IMAGE)"

run: image
	qemu-system-i386 -drive file=$(IMAGE),if=floppy,format=raw -boot a

verify: image
	$(PYTHON) tests/verify_boot.py

mbr-image: components
	$(PYTHON) tools/make_mbr_image.py

scripted-build:
	$(PYTHON) scripts/build.py

lint:
	$(PYTHON) scripts/menu_lint.py

config-lint:
	$(PYTHON) scripts/config_lint.py

ide:
	$(PYTHON) scripts/asm_ide.py

oop-demo: $(OOP_DEMO)
	@echo "Built standalone demo at $(OOP_DEMO); it needs a loader to execute."

clean:
	rm -f $(BOOT) $(STAGE2) $(MBR) $(VBR_MBR) $(KERNEL) $(CMOS) $(RTC_DEMO) $(LIB_DEMO) $(OOP_DEMO) $(IMAGE) $(BUILD)/mbr-test.img
