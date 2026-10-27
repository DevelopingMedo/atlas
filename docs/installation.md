# Atlas installieren und aktualisieren

## Einstieg ohne Klon

Der Installer `skills/atlas/scripts/atlas.py` benötigt Python 3.9+, keine
weiteren Python-Pakete und für Branch-/Tag-Downloads Zugriff auf GitHub.
OpenCode V2 ist das Zielformat der vorhandenen Rollen.

```sh
curl -fL https://raw.githubusercontent.com/DevelopingMedo/atlas/opencode/skills/atlas/scripts/atlas.py -o atlas-installer.py
python3 atlas-installer.py bootstrap --global --ref opencode
```

Bis zum Merge: `opencode` in URL **und** `--ref` durch
`docs/atlas-skill-distribution` ersetzen.

Der Bootstrap installiert nur den Einstiegsskill, `/atlas`, die Lizenz,
einen Installationsnachweis und das vollständige Paket als Datenarchiv im
Skill. Er setzt keine Modellpräferenzen. `/atlas` fragt gesammelt nach dem
gewünschten Umfang (Projekt/global) und persönlichen Modellen, installiert
die Dateien deterministisch und verwendet den bisherigen Modell-Dialog.
Der Bootstrap setzt keine noch nicht vorhandene Atlas-Rolle voraus.

Die alternativ per Skill-Installer installierte Quelle kann über
`@atlas Richte Atlas ein` gestartet werden. Ein bloßer `SKILL.md`-Download
registriert keinen Slash-Command. Das ist der Zweck des gemeinsamen Bootstrap.

## Direkte CLI

```sh
# Ziel ist das Projekt, nicht dessen .opencode-Unterordner:
python3 atlas-installer.py install --project /pfad/zum/projekt --ref opencode --dry-run
python3 atlas-installer.py install --project /pfad/zum/projekt --ref opencode

# Globale Installation bzw. explizites Konfigurationsverzeichnis:
python3 atlas-installer.py install --global --ref opencode
python3 atlas-installer.py install --target /pfad/zur/opencode-config --ref opencode

# Updates benötigen immer eine konkrete Quelle:
python3 atlas-installer.py update opencode --project /pfad/zum/projekt
python3 atlas-installer.py update v1.0.0 --global
```

`--global` berücksichtigt `OPENCODE_CONFIG_DIR`, sonst
`~/.config/opencode/`. `--target` benennt direkt das aktive
Konfigurationsverzeichnis; bei einem neuen projektlokalen Ziel verwende
`--project`, damit auch die Projekt-Instruction eingerichtet wird.
Eine vorhandene Installation merkt sich ihren Projektumfang im Nachweis.

Ein ohne `--ref` ausgeführtes `install` verwendet bevorzugt das bereits
mitgelieferte Paket, auch offline. Der eigentliche Modell-Dialog benötigt
weiterhin die lokale OpenCode-Installation. `bootstrap` und `update` holen
die angeforderte Quelle von GitHub. Branch und Tag gleichen Namens sind
mehrdeutig und werden abgelehnt, auch wenn beide denselben Commit nennen.
Release-Versionen entsprechen Git-Tags; ein Release-Asset ist für ein Update
nicht erforderlich. Ein unvollständiger alter Quellstand wird abgelehnt.

## Installierte Inhalte

| Inhalt | Pfad relativ zum Konfigurationsverzeichnis |
|---|---|
| Acht Rollen | `agents/*.md` |
| Gemeinsame Regeln | markierter Block in `AGENTS.md`, `SUBAGENTS.md` |
| Vier Guides | `guide/*.md` |
| Commands | `commands/atlas.md`, `commands/setup-atlas.md` |
| Ein Einstiegsskill und Modell-Referenz | `skills/atlas/` |
| Unveränderte Lizenz mit Commons Clause | `skills/atlas/LICENSE` |
| Vorlage für Modellpräferenzen | `atlas.json.example` |
| Quelle, Commit, Original-Prüfsummen | `.atlas-install.json` |

Projektlokal lautet das Konfigurationsverzeichnis `<projekt>/.opencode/`.
Dort wird `instructions` in `opencode.json(c)` gezielt ergänzt.
Andere Einstellungen, Kommentare und vorhandene Instruction-Einträge bleiben
bestehen. Global wird der markierte Regelblock aus `AGENTS.md` automatisch
geladen. Eigene Regeln außerhalb des Blocks bleiben bestehen. Relative
Dateiverweise in Rollen und Guides behalten ihre Verzeichnisstruktur.

Atlas kopiert keine fremden Repository-Dateien, `.git`-Metadaten, Secrets
oder die breite Quellrepo-`.gitignore`. Die Ziel-Ignore-Datei erhält nur
Einträge für persönliche `atlas.json`, Installationsnachweis und Paketcache.
Eine schon getrackte persönliche Datei führt vor dem Schreiben zum Abbruch;
der Installer ändert keinen Git-Index.

## Eigene Anpassungen und Konflikte

Der Installer prüft zuerst alle Dateien gegen die letzten Original-Prüfsummen.
Unveränderte verwaltete Dateien erhalten den neuen Paketstand. Lokal geänderte
oder gelöschte Dateien bleiben bestehen, wenn sich ihr Original nicht geändert
hat. Weicht auch das neue Original ab, wird das gesamte Update vor dem Schreiben
abgebrochen. Dasselbe gilt für eigene Dateien, die einen neuen Paketpfad belegen.

Änderungen außerhalb des Atlas-Regelblocks werden beibehalten. Änderungen im
Block werden wie lokale Änderungen an einer verwalteten Datei behandelt.
Die persönliche `atlas.json` wird weder als Paketinhalt verwaltet noch durch
ein Update neu gespeichert. Der Skill fragt beim Update keine Modelle ab.

Es gibt keinen Force-Schalter. Kläre die genannten Konfliktdateien gezielt:
eigene Variante behalten oder einen bewusst angepassten neuen Stand übernehmen.
Sichere deine Variante vor einer manuellen Auflösung. Lösche nicht pauschal den
Installationsnachweis; sonst fehlt die Vergleichsbasis. Bei Schreibfehlern
versucht der Installer, alle bereits betroffenen Dateien wiederherzustellen.
Ein Stromausfall oder harter Prozessabbruch ist keine atomare Transaktion
über mehrere Dateien. Für normale Ausnahmen wird der Nachweis nicht als
abgeschlossen hinterlassen.

## Paketbau und Prüfungen

Aus einem Checkout:

```sh
python3 -m unittest discover -s checks -v
python3 skills/atlas/scripts/atlas.py package --source . --ref opencode --output dist
```

Der Paketbau liest nur die explizite Laufzeit-Dateiliste. Das Paket enthält
ein Manifest mit SHA-256-Prüfsummen und Quellcommit. Der Release-Workflow baut
auf PRs gegen `opencode` sowie bei manuellem Start; bei einem `v*`-Tag
veröffentlicht er die drei Assets `atlas-skill.zip`, `atlas-package.zip` und
`atlas.py`. Das ZIP enthält genau einen Skill und keine zweite handgepflegte
Kopie der Rollen im Quellrepo. Ein Tag wird durch diesen PR nicht angelegt.

Die Prüfungen decken CLI, Payload, Erstinstallation, Wiederholung, JSONC,
Konflikte, lokale Löschungen, Symlinks und Wiederherstellung bei Schreibfehlern
ab. Die aktive Registrierung und der vollständige Modell-Dialog müssen
zusätzlich in einer OpenCode-V2-Instanz geprüft werden. Geprüfte Python-
Dateioperationen sind kein Nachweis für jede macOS-/Windows-Installation.

Grundlagen: [Commands](https://opencode.ai/v2/docs/commands/),
[Skills](https://opencode.ai/v2/docs/skills/),
[Instructions](https://opencode.ai/v2/docs/instructions/),
[Config](https://opencode.ai/v2/docs/config/).
