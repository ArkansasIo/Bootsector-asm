"""Unit tests for the local dashboard API contract."""
import unittest
from api.server import COMMANDS, ROOT, project_files, run_command

class AppApiTests(unittest.TestCase):
    def test_commands_are_allowlisted(self):
        self.assertEqual(set(COMMANDS), {"build", "verify", "lint", "clean"})
        self.assertTrue(all(isinstance(value, list) for value in COMMANDS.values()))

    def test_unknown_command_is_rejected(self):
        payload, status = run_command("run arbitrary shell")
        self.assertEqual(status, 400)
        self.assertFalse(payload["ok"])
        self.assertIn("allowed", payload)

    def test_file_inventory_uses_relative_paths(self):
        files = project_files()
        self.assertTrue(files)
        for item in files:
            self.assertFalse(item["path"].startswith("/"))
            self.assertNotIn("..", item["path"].split("/"))
            self.assertGreaterEqual(item["bytes"], 0)

    def test_settings_file_exists(self):
        self.assertTrue((ROOT / "config" / "app_settings.json").is_file())

if __name__ == "__main__":
    unittest.main()
