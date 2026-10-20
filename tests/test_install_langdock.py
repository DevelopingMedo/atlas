import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location("installer", Path(__file__).resolve().parents[1] / "install_langdock.py")
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)
FAKE_KEY = "test-token-not-a-real-key"


class InstallerTests(unittest.TestCase):
    def setUp(self):
        root = Path(tempfile.gettempdir()) / "opencode"
        root.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="langdock-installer-", dir=root)
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)

    def test_snapshot(self):
        providers = installer.providers()
        self.assertEqual([len(p["models"]) for p in providers.values()], [6, 10, 2])
        for provider in providers.values():
            self.assertEqual(provider["env"], ["LANGDOCK_API_KEY"])
            self.assertEqual(provider["settings"]["apiKey"], "{env:LANGDOCK_API_KEY}")
            for mid, model in provider["models"].items():
                self.assertNotIn("5.6", mid)
                self.assertFalse(mid.startswith("models/"))
                if mid.startswith("gpt-"):
                    self.assertTrue(model["package"].endswith("/responses"))
                    self.assertEqual(model["settings"], {"store": False})

    def test_merge_preserves_unrelated_settings(self):
        old = {"mcp": {"servers": {"custom": {"url": "http://localhost/mcp"}}},
               "agents": {"custom": {"disabled": False}}, "default_agent": "custom",
               "providers": {"other": {"models": {"mine": {}}}},
               "permissions": [{"action": "read", "resource": "*", "effect": "allow"}],
               "experimental": {"other": True, "policies": [{"action": "provider.use", "resource": "x", "effect": "deny"}]}}
        before = json.dumps(old)
        merged = installer.merge_config(old)
        self.assertEqual(json.dumps(old), before)
        for field in ("mcp", "agents", "default_agent"):
            self.assertEqual(merged[field], old[field])
        self.assertEqual(merged["providers"]["other"], old["providers"]["other"])
        self.assertEqual(merged["permissions"][:-2], old["permissions"])
        self.assertEqual(merged["experimental"]["policies"][:-2], old["experimental"]["policies"])
        self.assertEqual(installer.merge_config(merged), merged)

    def test_provider_conflict_is_not_overwritten(self):
        with self.assertRaises(installer.SetupError):
            installer.merge_config({"providers": {"langdock": {"name": "Other setup"}}})

    def test_jsonc_strings_comments_trailing_commas_and_bom(self):
        text = '\ufeff{ // comment\n "url": "https://example/a/*b*/", "s": "comma,}", /* c */ "a": [1,],}'
        self.assertEqual(installer.parse_config(text), {"url": "https://example/a/*b*/", "s": "comma,}", "a": [1]})
        with self.assertRaises(installer.SetupError):
            installer.parse_config('{"provider": {}}')
        with self.assertRaises(json.JSONDecodeError):
            installer.parse_config('{broken}')

    def test_blocks_are_idempotent_and_preserve_surroundings(self):
        first = installer.block("# user settings\n", "content")
        self.assertEqual(installer.block(first, "content"), first)
        self.assertTrue(first.startswith("# user settings\n"))
        with self.assertRaises(installer.SetupError):
            installer.block(installer.BEGIN, "content")

    def test_read_helper_refuses_secrets_and_symlinks(self):
        for name in (".env", ".env.local", "example.env", "app.env.test"):
            with self.assertRaises(installer.SetupError):
                installer.read_regular(self.home / name)
        if os.name != "nt":
            link = self.home / "config.json"
            link.symlink_to(self.home / "missing")
            with self.assertRaises(installer.SetupError):
                installer.read_regular(link)

    def test_secret_is_exclusive_private_and_validated(self):
        # A synthetic fixture, never the real .env or real environment value.
        path = self.home / "credential.fixture"
        installer.create_secret(path, FAKE_KEY)
        if os.name != "nt":
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
        with self.assertRaises(FileExistsError):
            installer.create_secret(path, "different-dummy")
        for key in ("", "line\nbreak", "quote'", "$(command)", "two words"):
            with self.assertRaises(installer.SetupError):
                installer.create_secret(self.home / "invalid.fixture", key)
        self.assertFalse((self.home / "invalid.fixture").exists())

    def test_windows_acl_precedes_secret_write_and_failure_removes_empty_file(self):
        path = self.home / "windows.fixture"
        def protect(target, exe):
            self.assertEqual(target.stat().st_size, 0)
            self.assertEqual(exe, "mock-powershell")
        with patch.object(installer, "protect_windows", side_effect=protect) as acl:
            installer.create_secret(path, FAKE_KEY, True, "mock-powershell")
            acl.assert_called_once()
        failed = self.home / "failed.fixture"
        with patch.object(installer, "protect_windows", side_effect=RuntimeError("mock ACL failure")):
            with self.assertRaises(RuntimeError):
                installer.create_secret(failed, FAKE_KEY, True, "mock-powershell")
        self.assertFalse(failed.exists())

    def test_windows_profiles_are_discovered_without_loading_them(self):
        secret = self.home / "credentials.fixture"
        profiles = [self.home / "WindowsPowerShell" / "profile.ps1", self.home / "PowerShell" / "profile.ps1"]
        with patch.object(installer.shutil, "which", side_effect=["powershell.exe", "pwsh.exe"]), \
             patch.object(installer, "powershell", side_effect=[str(p) for p in profiles]) as ps:
            targets, executable = installer.shell_targets(self.home, secret, True)
        self.assertEqual(set(targets), set(profiles))
        self.assertEqual(executable, "powershell.exe")
        self.assertTrue(all("$PROFILE.CurrentUserAllHosts" in call.args[1] for call in ps.call_args_list))
        self.assertNotIn("Invoke-Expression", next(iter(targets.values())))
        self.assertEqual(installer.ps_quote("O'Brien"), "'O''Brien'")

    def test_version_check_rejects_v1_and_accepts_v2(self):
        with patch.object(installer.shutil, "which", return_value="mock-opencode"), \
             patch.object(installer.subprocess, "run") as run:
            run.return_value.returncode = 0
            run.return_value.stdout = "opencode v1.9.0\n"
            with self.assertRaises(installer.SetupError):
                installer.verify_opencode()
            run.return_value.stdout = "opencode v2.0.27\n"
            installer.verify_opencode()

    def test_windows_save_secures_empty_file_and_writes_profile_bom(self):
        path = self.home / "profile.ps1"
        def protect(target, exe):
            self.assertEqual(target.stat().st_size, 0)
        with patch.object(installer, "protect_windows", side_effect=protect) as acl:
            installer.save(path, "# Grüße\n", executable="mock-powershell", encoding="utf-8-sig")
            acl.assert_called_once()
        self.assertTrue(path.read_bytes().startswith(b"\xef\xbb\xbf"))
        self.assertEqual(installer.read_regular(path), "# Grüße\n")
        path.write_bytes("# UTF16-Profil\n".encode("utf-16"))
        self.assertEqual(installer.read_regular(path), "# UTF16-Profil\n")

    @unittest.skipUnless(Path("/bin/bash").exists(), "Bash not available")
    def test_bash_loader_with_spaces_quotes_and_tracing(self):
        secret = self.home / "space and 'quote.fixture"
        installer.create_secret(secret, FAKE_KEY)
        (self.home / ".bash_profile").write_text("# existing\n")
        with patch.object(installer.os, "environ", {}):
            targets, _ = installer.shell_targets(self.home, secret, False)
        self.assertIn(self.home / ".bash_profile", targets)
        self.assertIn(self.home / ".zshrc", targets)
        loader = targets[self.home / ".bashrc"]
        result = subprocess.run(["/bin/bash", "-c", loader + '\n test "$LANGDOCK_API_KEY" = ' + FAKE_KEY],
                                env={}, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout + result.stderr, "")
        traced = subprocess.run(["/bin/bash", "-xc", loader + '\n test -z "${LANGDOCK_API_KEY+x}"'],
                                env={}, capture_output=True, text=True)
        self.assertEqual(traced.returncode, 0)
        self.assertNotIn(FAKE_KEY, traced.stdout + traced.stderr)

    def test_full_install_in_fake_home_and_existing_secret_refusal(self):
        config = self.home / ".config" / "opencode"
        config.mkdir(parents=True)
        original = '{"default_agent":"keep", "mcp":{"servers":{}}, /* keep in backup */}'
        (config / "opencode.jsonc").write_text(original)
        (self.home / ".bashrc").write_text("# keep my settings\n")
        output = io.StringIO()
        with patch.object(installer.os, "environ", {}), \
             patch.object(installer, "verify_opencode"), \
             patch.object(installer.getpass, "getpass", return_value=FAKE_KEY) as prompt, \
             contextlib.redirect_stdout(output):
            installer.install(self.home, False)
            with self.assertRaises(installer.SetupError):
                installer.install(self.home, False)
            prompt.assert_called_once()
        # Deliberately only stat .env; never read it, even in this test home.
        if os.name != "nt":
            self.assertEqual(stat.S_IMODE((config / ".env").stat().st_mode), 0o600)
        current = json.loads((config / "opencode.jsonc").read_text())
        self.assertEqual(current["default_agent"], "keep")
        self.assertEqual(current["mcp"], {"servers": {}})
        self.assertEqual(current["providers"], installer.providers())
        self.assertEqual((config / "opencode.jsonc.langdock.bak").read_text(), original)
        self.assertTrue((self.home / ".bashrc").read_text().startswith("# keep my settings"))
        for path in (config / "opencode.jsonc", config / "AGENTS.md", self.home / ".bashrc"):
            self.assertNotIn(FAKE_KEY, path.read_text())
        self.assertNotIn(FAKE_KEY, output.getvalue())
        self.assertIn(".env.*", (config / ".gitignore").read_text())

    def test_windows_install_path_with_mocked_profile_and_acl(self):
        config = self.home / "custom-config"
        profile = self.home / "PowerShell" / "profile.ps1"
        with patch.object(installer.os, "environ", {"OPENCODE_CONFIG_DIR": str(config)}), \
             patch.object(installer, "verify_opencode"), \
             patch.object(installer, "shell_targets", return_value=({profile: "# mocked PowerShell loader"}, "mock-powershell")), \
             patch.object(installer, "protect_windows") as acl, \
             patch.object(installer.getpass, "getpass", return_value=FAKE_KEY), \
             contextlib.redirect_stdout(io.StringIO()):
            installer.install(self.home, True)
        self.assertGreaterEqual(acl.call_count, 5)
        self.assertTrue(profile.read_bytes().startswith(b"\xef\xbb\xbf"))
        self.assertEqual(json.loads((config / "opencode.json").read_text())["providers"], installer.providers())
        self.assertTrue((config / ".env").is_file())  # Metadata only, no secret-file read.


if __name__ == "__main__":
    unittest.main()
