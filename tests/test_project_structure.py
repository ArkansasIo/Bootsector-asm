"""Host-side tests for repository tooling and validation rules."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProjectStructureTests(unittest.TestCase):
    def test_core_boot_sources_exist(self):
        for relative in ("boot/boot.asm", "stage2/stage2.asm", "os/kernel.asm"):
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file())

    def test_stage1_source_declares_sector_signature(self):
        source = (ROOT / "boot/boot.asm").read_text(encoding="utf-8")
        self.assertIn("times 510-($-$$) db 0", source)
        self.assertIn("dw 0xAA55", source)

    def test_verifier_contains_key_layout_invariants(self):
        source = (ROOT / "tests/verify_boot.py").read_text(encoding="utf-8")
        for fragment in ('b"\\x55\\xaa"', "FLOPPY_SIZE", "image[:SECTOR] == boot",
                         "stage2 begins at LBA 1", "unused stage2 load-window bytes"):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, source)

    def test_ci_installs_nasm_and_runs_verification(self):
        workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("apt-get install -y nasm make python3", workflow)
        self.assertIn("make verify", workflow)


if __name__ == "__main__":
    unittest.main()
