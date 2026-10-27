import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

SOURCE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('atlas', SOURCE / 'skills/atlas/scripts/atlas.py')
atlas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(atlas)


class InstallerTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'project/.opencode'
        self.package = atlas.local_package(SOURCE, 'opencode')

    def tearDown(self):
        self.temp.cleanup()

    def install(self, package=None, phase='installed', **options):
        with contextlib.redirect_stdout(io.StringIO()):
            return atlas.install(self.root, package or self.package, phase, project=True, **options)

    def files(self):
        return {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}

    def changed(self, name, data):
        return dict(self.package, commit='a' * 40, files=dict(self.package['files'], **{name: data}))

    def test_bootstrap_then_full_install_and_repeat(self):
        self.install(phase='bootstrap')
        self.assertTrue((self.root / 'commands/atlas.md').is_file())
        self.assertFalse((self.root / 'agents/Auto.md').exists())
        cached = atlas.decode_package((self.root / atlas.PAYLOAD).read_bytes())
        self.install(cached)
        self.assertEqual(len(list((self.root / 'agents').glob('*.md'))), 8)
        self.assertEqual(len(list((self.root / 'guide').glob('*.md'))), 4)
        self.assertTrue((self.root / 'commands/setup-atlas.md').is_file())
        self.assertEqual(json.loads((self.root / 'opencode.json').read_text())['instructions'], ['.opencode/AGENTS.md'])
        self.assertFalse((self.root / 'atlas.json').exists())
        before = self.files()
        self.install()
        self.assertEqual(self.files(), before)
        self.assertEqual((self.root / 'AGENTS.md').read_text().count(atlas.BEGIN), 1)
        self.assertEqual((self.root / 'skills/atlas/LICENSE').read_bytes(), (SOURCE / 'LICENSE').read_bytes())

    def test_update_preserves_models_custom_files_rules_and_jsonc(self):
        self.root.mkdir(parents=True)
        custom = b'# Team rules\nUse Java 21.\n'
        (self.root / 'AGENTS.md').write_bytes(custom)
        config = b'{ // keep\n "model": "provider/model", "instructions": ["TEAM.md",],\n}\n'
        (self.root / 'opencode.jsonc').write_bytes(config)
        self.install()
        personal = b'{"atlas-setup":true,"models":{"fast":null},"extra":{"keep":7}}'
        (self.root / 'atlas.json').write_bytes(personal)
        (self.root / 'agents/Own.md').write_text('My agent')
        after_config = (self.root / 'opencode.jsonc').read_bytes()
        self.install(self.changed('agents/Auto.md', b'new role\n'))
        self.assertEqual((self.root / 'agents/Auto.md').read_bytes(), b'new role\n')
        self.assertEqual((self.root / 'atlas.json').read_bytes(), personal)
        self.assertEqual((self.root / 'agents/Own.md').read_text(), 'My agent')
        self.assertTrue((self.root / 'AGENTS.md').read_bytes().startswith(custom))
        self.assertEqual((self.root / 'opencode.jsonc').read_bytes(), after_config)
        self.assertIn(b'// keep', after_config)
        self.assertIn(b'"model": "provider/model"', after_config)
        self.assertIn(b'"TEAM.md"', after_config)

    def test_upstream_and_local_edit_conflict_writes_nothing(self):
        self.install()
        (self.root / 'agents/Auto.md').write_bytes(b'local\n')
        before = self.files()
        with self.assertRaisesRegex(atlas.AtlasError, 'agents/Auto.md'):
            self.install(self.changed('agents/Auto.md', b'upstream\n'))
        self.assertEqual(self.files(), before)

    def test_unchanged_upstream_keeps_local_edit_and_local_deletion(self):
        self.install()
        (self.root / 'agents/Auto.md').write_bytes(b'local\n')
        (self.root / 'guide/MCP.md').unlink()
        self.install(self.changed('agents/Run.md', b'updated Run\n'))
        self.assertEqual((self.root / 'agents/Auto.md').read_bytes(), b'local\n')
        self.assertFalse((self.root / 'guide/MCP.md').exists())

    def test_local_deletion_conflicts_when_upstream_changed(self):
        self.install()
        (self.root / 'agents/Auto.md').unlink()
        before = self.files()
        with self.assertRaises(atlas.AtlasError):
            self.install(self.changed('agents/Auto.md', b'changed\n'))
        self.assertEqual(self.files(), before)

    def test_existing_role_collision_and_dry_run(self):
        self.install(dry_run=True)
        self.assertFalse(self.root.exists())
        (self.root / 'agents').mkdir(parents=True)
        (self.root / 'agents/Auto.md').write_bytes(b'my own Auto\n')
        before = self.files()
        with self.assertRaises(atlas.AtlasError):
            self.install()
        self.assertEqual(self.files(), before)

    def test_rule_block_edit_conflicts_but_surrounding_edits_survive(self):
        self.install()
        path = self.root / 'AGENTS.md'
        path.write_text('# Custom\n' + path.read_text() + '\nMy footer\n')
        self.install(self.changed('AGENTS.md', b'new shared rules\n'))
        self.assertTrue(path.read_text().startswith('# Custom\n'))
        self.assertTrue(path.read_text().endswith('My footer\n'))
        path.write_text(path.read_text().replace('new shared rules', 'my shared rules'))
        before = self.files()
        with self.assertRaises(atlas.AtlasError):
            self.install(self.changed('AGENTS.md', b'another upstream\n'))
        self.assertEqual(self.files(), before)

    def test_bad_jsonc_and_symlink_stop_before_writes(self):
        self.root.mkdir(parents=True)
        (self.root / 'opencode.jsonc').write_text('{bad json}')
        before = self.files()
        with self.assertRaises(atlas.AtlasError):
            self.install()
        self.assertEqual(self.files(), before)
        (self.root / 'opencode.jsonc').unlink()
        outside = Path(self.temp.name) / 'outside'
        outside.mkdir()
        (self.root / 'agents').symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(atlas.AtlasError, 'Symlink'):
            self.install()
        self.assertEqual(list(outside.iterdir()), [])

    def test_package_roundtrip_is_deterministic_and_checks_hashes(self):
        data = atlas.encode_package(self.package)
        self.assertEqual(atlas.encode_package(self.package), data)
        self.assertEqual(atlas.decode_package(data), self.package)
        stream = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(data)) as original, zipfile.ZipFile(stream, 'w') as modified:
            for name in original.namelist():
                modified.writestr(name, b'changed' if name == 'agents/Auto.md' else original.read(name))
        with self.assertRaisesRegex(atlas.AtlasError, 'Checksum'):
            atlas.decode_package(stream.getvalue())

    def test_incomplete_source_and_missing_update_argument_write_nothing(self):
        with self.assertRaisesRegex(atlas.AtlasError, 'Incomplete'):
            atlas.collect_files(lambda name: None)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            atlas.main(['update', '--target', str(self.root)])
        self.assertFalse(self.root.exists())

    def test_unknown_and_ambiguous_refs_have_no_fallback(self):
        with patch.object(atlas, 'request', return_value=None), self.assertRaisesRegex(atlas.AtlasError, 'Unknown'):
            atlas.resolve_ref('missing')
        value = json.dumps({'object': {'type': 'commit', 'sha': 'a' * 40}}).encode()
        with patch.object(atlas, 'request', return_value=value), self.assertRaisesRegex(atlas.AtlasError, 'ambiguous'):
            atlas.resolve_ref('both')

    def test_pinned_archive_is_used_after_branch_resolution(self):
        import tarfile
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode='w:gz') as archive:
            for name in atlas.REQUIRED:
                content = (SOURCE / name).read_bytes()
                info = tarfile.TarInfo('repo-123/' + name)
                info.size = len(content)
                archive.addfile(info, io.BytesIO(content))
        ref = json.dumps({'object': {'type': 'commit', 'sha': 'b' * 40}}).encode()
        with patch.object(atlas, 'request', side_effect=[ref, None, stream.getvalue()]) as request:
            package = atlas.download_package('opencode')
        self.assertEqual(package['commit'], 'b' * 40)
        self.assertTrue(request.call_args.args[0].endswith('/tarball/' + 'b' * 40))

    def test_write_failure_restores_originals_and_state(self):
        self.install()
        before = self.files()
        real_replace = atlas.os.replace
        calls = []
        def fail_once(source, target):
            calls.append(target)
            if len(calls) == 2:
                raise OSError('disk full')
            return real_replace(source, target)
        with patch.object(atlas.os, 'replace', side_effect=fail_once), self.assertRaises(OSError):
            self.install(self.changed('agents/Auto.md', b'new Auto\n'))
        self.assertEqual(self.files(), before)

    def test_jsonc_edge_cases_and_duplicate_keys(self):
        for config in [b'{}', b'{/* before */}', b'{"model":"https://example.com" /* comment */}',
                       b'{"instructions": []}', b'{"instructions": [/* comment */]}',
                       b'{"instructions": ["TEAM.md" /* trailing comment */]}']:
            result = atlas.add_instruction(config)
            parsed, _ = atlas.jsonc_tokens(result.decode())
            self.assertIn('.opencode/AGENTS.md', parsed['instructions'])
            self.assertEqual(atlas.add_instruction(result), result)
        with self.assertRaises(atlas.AtlasError):
            atlas.add_instruction(b'{"instructions":[],"instructions":[]}')
        with self.assertRaises(atlas.AtlasError):
            atlas.add_instruction(b'{"invalid": 1 2}')


if __name__ == '__main__':
    unittest.main()
