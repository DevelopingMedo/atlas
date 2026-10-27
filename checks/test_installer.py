"""Dateisystemtests für den Atlas-Installer; Ausführung vom Repository-Stamm:

    python3 -m unittest discover -s checks -v

Testaufbau und Pfade
-------------------
SOURCE ist der vorhandene Atlas-Checkout mit den Installationsquellen.
setUp() legt vor JEDEM Test ein eigenes temporäres Verzeichnis an. self.temp
verwaltet dieses Verzeichnis; self.root bezeichnet dessen Installationsziel:

    <temporäres Verzeichnis>/            # existiert direkt nach setUp()
        project/                        # wird erst beim Installieren angelegt
            .opencode/                  # self.root; anfangs ebenfalls nicht da

Das Paket wird lokal aus SOURCE gelesen. 'opencode' ist dabei die Bezeichnung
der Quelle, kein Auftrag für einen GitHub-Download. Manche Tests legen vor der
Installation bewusst eigene Regeln, Konfigurationen oder Rollen im Ziel an.
tearDown() entfernt nach jedem Test das komplette temporäre Verzeichnis.

Erwartete Struktur nach vollständiger Installation in ein leeres Projekt
----------------------------------------------------------------------
Alle folgenden Pfade liegen unter self.root, also project/.opencode/:

    .atlas-install.json                 # Quelle, Commit, Original-Prüfsummen
    .gitignore                          # gezielte Einträge für lokale Daten
    AGENTS.md                           # Atlas-Regeln zwischen Blockmarkern
    SUBAGENTS.md
    atlas.json.example                  # Vorlage, keine persönlichen Werte
    opencode.json                       # instructions: [".opencode/AGENTS.md"]
    agents/
        Analyze.md
        Auto.md
        Build.md
        Develop.md
        Orchestrate.md
        Plan.md
        Review.md
        Run.md
    guide/
        ARTIFACTS.md
        MCP.md
        PLANNING.md
        REPOSITORIES.md
    commands/
        atlas.md
        setup-atlas.md
    skills/
        atlas/
            LICENSE
            SKILL.md
            scripts/atlas.py
            references/model-setup.md
            assets/package.zip          # vollständiges Paket für das Setup

Der Bootstrap legt zunächst nur den Einstieg an: .atlas-install.json,
.gitignore, commands/atlas.md und skills/atlas/ einschließlich Paketarchiv.
Die Rollen, Guides und gemeinsamen Regeln kommen bei der Vollinstallation.
Eine persönliche atlas.json wird vom Installer NICHT erzeugt; die Tests legen
sie bei Bedarf selbst an. Bei vorhandener opencode.jsonc wird diese ergänzt,
statt daneben eine neue opencode.json anzulegen. Eigene Dateien bleiben stehen.

Was die Assertions tatsächlich belegen
------------------------------------
Der erste Test prüft ausgewählte Pfade, acht Rollen, vier Guides, den
Instruction-Eintrag, die Lizenz und die Wiederholbarkeit. Er vergleicht nicht
den gesamten Baum mit einer fest codierten Liste aller erwarteten Dateien.
files() erfasst Dateipfade und Bytes, um bei Wiederholung oder Konflikten den
Vorher-/Nachher-Zustand zu vergleichen; leere Ordner und Dateirechte fehlen darin.
Die Tests prüfen die Dateien auf der Platte, keine laufende OpenCode-Instanz.

Python-Lesehilfe: self entspricht ungefähr Java-this; setUp/tearDown sind wie
JUnit-BeforeEach/AfterEach. Methoden mit test_ werden automatisch ausgeführt.
Einrückungen begrenzen Blöcke. b'...' bezeichnet Bytes, '\n' einen Zeilenumbruch.
"""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

# __file__ ist diese Testdatei; parents[0] ist checks/, parents[1] der Repo-Stamm.
SOURCE = Path(__file__).resolve().parents[1]
# Lade den Installer über seinen Dateipfad als Modul namens atlas. Sein
# CLI-Hauptprogramm startet beim Import nicht; die Tests rufen Funktionen auf.
spec = importlib.util.spec_from_file_location('atlas', SOURCE / 'skills/atlas/scripts/atlas.py')
atlas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(atlas)


class InstallerTest(unittest.TestCase):
    def setUp(self):
        """Frische Sandbox und lokales Quellpaket vor jedem einzelnen Test."""
        self.temp = tempfile.TemporaryDirectory()
        # / verbindet Path-Bestandteile. Diese Zuweisung erzeugt noch keine Ordner.
        self.root = Path(self.temp.name) / 'project/.opencode'
        self.package = atlas.local_package(SOURCE, 'opencode')

    def tearDown(self):
        """Sandbox samt installierten und vom Test ergänzten Dateien entfernen."""
        self.temp.cleanup()

    def install(self, package=None, phase='installed', **options):
        """Echten Installer für self.root aufrufen; keine OpenCode-Session starten.

        **options sammelt weitere benannte Argumente, etwa dry_run=True, und
        reicht sie weiter. package or self.package verwendet ohne eigenes
        Paket das vorbereitete Standardpaket. with begrenzt die Umleitung
        der normalen Konsolenausgabe auf einen Textpuffer im Arbeitsspeicher.
        """
        with contextlib.redirect_stdout(io.StringIO()):
            return atlas.install(self.root, package or self.package, phase, project=True, **options)

    def files(self):
        """Schnappschuss als Dictionary: relativer Dateipfad -> unveränderte Bytes.

        Die Dictionary-Comprehension entspricht einer Schleife: rglob('*')
        besucht rekursiv alle Einträge, is_file() wählt Dateien aus und
        relative_to(self.root) entfernt den zufälligen temporären Basispfad.
        So erkennen Vergleiche neue, entfernte und inhaltlich geänderte Dateien.
        """
        return {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}

    def changed(self, name, data):
        """Neues Quellpaket simulieren, in dem genau eine Datei anderen Inhalt hat.

        dict(...) kopiert die Zuordnungen; **{name: data} ersetzt den benannten
        Dateieintrag. 'a' * 40 erzeugt eine künstliche Commit-ID. Das originale
        self.package bleibt erhalten; dieser Aufruf schreibt keine Dateien.
        """
        return dict(self.package, commit='a' * 40, files=dict(self.package['files'], **{name: data}))

    def test_bootstrap_then_full_install_and_repeat(self):
        """Leeres Projekt: Einstieg installieren, Baum vervollständigen, wiederholen."""
        self.install(phase='bootstrap')
        self.assertTrue((self.root / 'commands/atlas.md').is_file())
        self.assertFalse((self.root / 'agents/Auto.md').exists())
        # Den Baum aus dem Bootstrap-Archiv vervollständigen, ohne neuen Download.
        cached = atlas.decode_package((self.root / atlas.PAYLOAD).read_bytes())
        self.install(cached)
        self.assertEqual(len(list((self.root / 'agents').glob('*.md'))), 8)
        self.assertEqual(len(list((self.root / 'guide').glob('*.md'))), 4)
        self.assertTrue((self.root / 'commands/setup-atlas.md').is_file())
        self.assertEqual(json.loads((self.root / 'opencode.json').read_text())['instructions'], ['.opencode/AGENTS.md'])
        self.assertFalse((self.root / 'atlas.json').exists())
        # Wiederholung darf weder Dateiinhalte ändern noch den Regelblock doppeln.
        before = self.files()
        self.install()
        self.assertEqual(self.files(), before)
        self.assertEqual((self.root / 'AGENTS.md').read_text().count(atlas.BEGIN), 1)
        self.assertEqual((self.root / 'skills/atlas/LICENSE').read_bytes(), (SOURCE / 'LICENSE').read_bytes())

    def test_update_preserves_models_custom_files_rules_and_jsonc(self):
        """Eigene Regeln/JSONC vorbereiten; Update erhält atlas.json und Own.md."""
        self.root.mkdir(parents=True)
        custom = b'# Team rules\nUse Java 21.\n'
        (self.root / 'AGENTS.md').write_bytes(custom)
        config = b'{ // keep\n "model": "provider/model", "instructions": ["TEAM.md",],\n}\n'
        (self.root / 'opencode.jsonc').write_bytes(config)
        self.install()
        # Diese beiden Dateien stammen vom Nutzer, nicht aus dem Atlas-Paket.
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
        """Auto.md lokal UND im neuen Paket ändern: gesamtes Update muss stoppen."""
        self.install()
        (self.root / 'agents/Auto.md').write_bytes(b'local\n')
        before = self.files()
        # assertRaisesRegex ist ähnlich assertThrows plus Prüfung der Fehlermeldung.
        with self.assertRaisesRegex(atlas.AtlasError, 'agents/Auto.md'):
            self.install(self.changed('agents/Auto.md', b'upstream\n'))
        self.assertEqual(self.files(), before)

    def test_unchanged_upstream_keeps_local_edit_and_local_deletion(self):
        """Nur Run ändert sich im Paket; eigenes Auto und gelöschtes MCP bleiben so."""
        self.install()
        (self.root / 'agents/Auto.md').write_bytes(b'local\n')
        (self.root / 'guide/MCP.md').unlink()
        self.install(self.changed('agents/Run.md', b'updated Run\n'))
        self.assertEqual((self.root / 'agents/Auto.md').read_bytes(), b'local\n')
        self.assertFalse((self.root / 'guide/MCP.md').exists())

    def test_local_deletion_conflicts_when_upstream_changed(self):
        """Lokal gelöschtes Auto kollidiert mit neuer Auto-Version im Quellpaket."""
        self.install()
        (self.root / 'agents/Auto.md').unlink()
        before = self.files()
        with self.assertRaises(atlas.AtlasError):
            self.install(self.changed('agents/Auto.md', b'changed\n'))
        self.assertEqual(self.files(), before)

    def test_existing_role_collision_and_dry_run(self):
        """Vorschau legt nichts an; bereits vorhandene eigene Auto-Rolle ist Konflikt."""
        self.install(dry_run=True)
        self.assertFalse(self.root.exists())
        (self.root / 'agents').mkdir(parents=True)
        (self.root / 'agents/Auto.md').write_bytes(b'my own Auto\n')
        before = self.files()
        with self.assertRaises(atlas.AtlasError):
            self.install()
        self.assertEqual(self.files(), before)

    def test_rule_block_edit_conflicts_but_surrounding_edits_survive(self):
        """Eigener Text um den Regelblock bleibt; konkurrierende Blockänderung stoppt."""
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
        """Ungültige Konfiguration und agents-Link nach außerhalb werden abgelehnt."""
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
        """Paket identisch bauen/einlesen; manipuliertes Auto muss Prüfsumme verletzen."""
        data = atlas.encode_package(self.package)
        self.assertEqual(atlas.encode_package(self.package), data)
        self.assertEqual(atlas.decode_package(data), self.package)
        stream = io.BytesIO()
        # BytesIO ist ein Bytepuffer: Hier entstehen ZIPs im Speicher, keine Zielordner.
        with zipfile.ZipFile(io.BytesIO(data)) as original, zipfile.ZipFile(stream, 'w') as modified:
            for name in original.namelist():
                modified.writestr(name, b'changed' if name == 'agents/Auto.md' else original.read(name))
        with self.assertRaisesRegex(atlas.AtlasError, 'Checksum'):
            atlas.decode_package(stream.getvalue())

    def test_incomplete_source_and_missing_update_argument_write_nothing(self):
        """Fehlende Paketdateien oder Update-Quelle dürfen das Ziel nicht erzeugen."""
        with self.assertRaisesRegex(atlas.AtlasError, 'Incomplete'):
            # lambda ist eine anonyme Funktion; jede angefragte Datei gilt als fehlend.
            atlas.collect_files(lambda name: None)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            atlas.main(['update', '--target', str(self.root)])
        self.assertFalse(self.root.exists())

    def test_unknown_and_ambiguous_refs_have_no_fallback(self):
        """GitHub-Antworten simulieren: unbekannte/mehrdeutige Quelle wird abgelehnt."""
        # patch.object ersetzt request nur im with-Block und stellt es danach wieder her.
        with patch.object(atlas, 'request', return_value=None), self.assertRaisesRegex(atlas.AtlasError, 'Unknown'):
            atlas.resolve_ref('missing')
        value = json.dumps({'object': {'type': 'commit', 'sha': 'a' * 40}}).encode()
        with patch.object(atlas, 'request', return_value=value), self.assertRaisesRegex(atlas.AtlasError, 'ambiguous'):
            atlas.resolve_ref('both')

    def test_pinned_archive_is_used_after_branch_resolution(self):
        """Archivdownload muss den aufgelösten Commit verwenden, nicht den Branch."""
        import tarfile
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode='w:gz') as archive:
            for name in atlas.REQUIRED:
                content = (SOURCE / name).read_bytes()
                info = tarfile.TarInfo('repo-123/' + name)
                info.size = len(content)
                archive.addfile(info, io.BytesIO(content))
        ref = json.dumps({'object': {'type': 'commit', 'sha': 'b' * 40}}).encode()
        # Antworten nacheinander: Branch gefunden, kein gleichnamiger Tag, Quellarchiv.
        with patch.object(atlas, 'request', side_effect=[ref, None, stream.getvalue()]) as request:
            package = atlas.download_package('opencode')
        self.assertEqual(package['commit'], 'b' * 40)
        self.assertTrue(request.call_args.args[0].endswith('/tarball/' + 'b' * 40))

    def test_write_failure_restores_originals_and_state(self):
        """Beim zweiten Dateiaustausch Fehler auslösen und vollständige Rücknahme prüfen."""
        self.install()
        before = self.files()
        real_replace = atlas.os.replace
        calls = []
        def fail_once(source, target):
            # Nur den zweiten Aufruf sabotieren; die anderen verwenden echtes os.replace.
            calls.append(target)
            if len(calls) == 2:
                raise OSError('disk full')
            return real_replace(source, target)
        with patch.object(atlas.os, 'replace', side_effect=fail_once), self.assertRaises(OSError):
            self.install(self.changed('agents/Auto.md', b'new Auto\n'))
        self.assertEqual(self.files(), before)

    def test_release_skill_installs_offline(self):
        """Skill-ZIP lokal bauen/entpacken und dessen Installer als Prozess ausführen.

        Das Modell-Setup ist nicht Teil dieses Tests. 'release' und 'extracted'
        liegen neben project/ in derselben Sandbox. Der Installer verwendet
        das gebündelte Paket; der Test sperrt das Netzwerk nicht technisch.
        """
        output = Path(self.temp.name) / 'release'
        with contextlib.redirect_stdout(io.StringIO()):
            atlas.main(['package', '--source', str(SOURCE), '--ref', 'release-test', '--output', str(output)])
        extracted = Path(self.temp.name) / 'extracted'
        with zipfile.ZipFile(output / 'atlas-skill.zip') as archive:
            archive.extractall(extracted)
        installer = extracted / 'atlas/scripts/atlas.py'
        import subprocess
        # sys.executable wählt denselben Python-Interpreter wie der laufende Test.
        # capture_output sammelt Ausgaben; sie erscheinen bei einem Fehler als Diagnose.
        result = subprocess.run([atlas.sys.executable, str(installer), 'install', '--project', str(self.root.parent)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        state = json.loads((self.root / atlas.STATE).read_text())
        self.assertEqual(state['ref'], 'release-test')
        self.assertEqual(state['phase'], 'installed')
        self.assertEqual(len(list((self.root / 'agents').glob('*.md'))), 8)

    def test_jsonc_edge_cases_and_duplicate_keys(self):
        """Kommentare/leere Arrays erhalten; doppelte Schlüssel und kaputtes JSON ablehnen."""
        for config in [b'{}', b'{/* before */}', b'{"model":"https://example.com" /* comment */}',
                       b'{"instructions": []}', b'{"instructions": [/* comment */]}',
                       b'{"instructions": ["TEAM.md" /* trailing comment */]}']:
            result = atlas.add_instruction(config)
            # Zwei Rückgabewerte entpacken; die Tokens in _ werden hier nicht benötigt.
            parsed, _ = atlas.jsonc_tokens(result.decode())
            self.assertIn('.opencode/AGENTS.md', parsed['instructions'])
            self.assertEqual(atlas.add_instruction(result), result)
        with self.assertRaises(atlas.AtlasError):
            atlas.add_instruction(b'{"instructions":[],"instructions":[]}')
        with self.assertRaises(atlas.AtlasError):
            atlas.add_instruction(b'{"invalid": 1 2}')


# Beim direkten Start dieser Datei die Tests ausführen; beim Importieren nicht.
if __name__ == '__main__':
    unittest.main()
