NASM ?= nasm
BUILD := build
BOOT := $(BUILD)/boot.bin
STAGE2 := $(BUILD)/stage2.bin
MBR := $(BUILD)/mbr.bin
VBR_MBR := $(BUILD)/vbr_mbr.bin
KERNEL := $(BUILD)/kernel.bin
CMOS := $(BUILD)/cmos.bin
OOP_DEMO := $(BUILD)/oop-counter.bin
IMAGE := $(BUILD)/floppy.img

.PHONY: all components image run verify mbr-image lint scripted-build oop-demo clean
all: image

$(BUILD):
	mkdir -p $(BUILD)

$(BOOT): boot/boot.asm | $(BUILD)
	$(NASM) -f bin $< -o $@
	test "$$(wc -c < $@)" -eq 512

$(STAGE2): stage2/stage2.asm | $(BUILD)
	$(NASM) -f bin $< -o $@
	test "$$(wc -c < $@)" -le 4096

$(MBR): boot/mbr.asm | $(BUILD)
	$(NASM) -f bin $< -o $@
	test "$$(wc -c < $@)" -eq 512

$(VBR_MBR): boot/vbr_mbr.asm | $(BUILD)
	$(NASM) -f bin $< -o $@
	test "$$(wc -c < $@)" -eq 512

$(KERNEL): os/kernel.asm | $(BUILD)
	$(NASM) -f bin $< -o $@

$(CMOS): firmware/cmos.asm | $(BUILD)
	$(NASM) -f bin $< -o $@

$(OOP_DEMO): examples/oop_counter.asm | $(BUILD)
	$(NASM) -f bin $< -o $@

components: $(BOOT) $(STAGE2) $(MBR) $(VBR_MBR) $(KERNEL) $(CMOS) $(OOP_DEMO)

image: $(BOOT) $(STAGE2)
	dd if=/dev/zero of=$(IMAGE) bs=512 count=2880 status=none
	dd if=$(BOOT) of=$(IMAGE) bs=512 count=1 conv=notrunc status=none
	dd if=$(STAGE2) of=$(IMAGE) bs=512 seek=1 conv=notrunc status=none
	truncate -s 1474560 $(IMAGE)
	@echo "Built $(IMAGE)"

run: image
	qemu-system-i386 -drive file=$(IMAGE),if=floppy,format=raw -boot a

verify: image
	python3 tests/verify_boot.py

mbr-image: components
	python3 tools/make_mbr_image.py

scripted-build:
	python3 scripts/build.py

lint:
	python3 scripts/menu_lint.py

oop-demo: $(OOP_DEMO)
	@echo "Built standalone demo at $(OOP_DEMO); it needs a loader to execute."

clean:
	rm -f $(BOOT) $(STAGE2) $(MBR) $(VBR_MBR) $(KERNEL) $(CMOS) $(OOP_DEMO) $(IMAGE) $(BUILD)/mbr-test.img
