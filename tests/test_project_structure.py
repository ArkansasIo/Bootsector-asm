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

    def test_verifier_checks_boot_image_layout(self):
        source = (ROOT / "tests/verify_boot.py").read_text(encoding="utf-8")
        self.assertIn("boot[510:512] == b\"\\x55\\xaa\"", source)
        self.assertIn("len(image) == 1_474_560", source)
        self.assertIn("image[:512] == boot", source)
        self.assertIn("image[512:512+len(stage2)] == stage2", source)

    def test_ci_installs_nasm_and_runs_verification(self):
        workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("apt-get install -y nasm make python3", workflow)
        self.assertIn("make verify", workflow)


if __name__ == "__main__":
    unittest.main()
