# Planungsdateien durch Plan pflegen

`Plan` darf beauftragte Tickets, Architekturunterlagen und Implementierungshinweise
selbst speichern und aktualisieren. Dafür ist kein Wechsel zu `Develop` nötig.
Die Produktimplementierung bleibt bei `Develop`, tiefe Bestands- und
Ursachenrecherche bei `Analyze`.

## Enger Schreibbereich und Autorisierung

Die mitgelieferte Rolle gibt nur diese projektbezogenen Bereiche für
Markdown-Planungsunterlagen frei:

- `docs/planning/tickets/*.md`
- `docs/planning/architecture/*.md`
- `docs/planning/implementation/*.md`

Ein Auftrag muss den Planungsbereich und die beauftragten Dateien autorisieren.
Die Permission allein ist keine inhaltliche Schreibfreigabe. Produktquellen,
Produktkonfigurationen und beliebige andere Markdown-Dateien bleiben gesperrt.
Auch unter den freigegebenen Pfaden darf Plan keine Produktimplementierung
ablegen. Keine Symlinks aus Planungsbereichen auf Produktdateien verwenden.

Bei unbekanntem Ziel liefert Plan die Planung als Antwort und klärt nur das
nötige Schreibziel. Er rät keinen Pfad, ändert keine Permissions und delegiert
das bloße Speichern nicht als Umgehung an Develop. Verwendet ein Projekt andere
Planungsbereiche, muss der Konfigurationsverantwortliche deren genaue Pfade
ausdrücklich vereinbaren und die drei Pfadregeln entsprechend eng ersetzen;
keine Freigabe für `*.md`, `docs/*` oder Produktkonfigurationen ergänzen.

Bei nachgewiesener Repository-Arbeit gelten auch für Plan die Regeln aus
`REPOSITORIES.md`: ohne ausdrückliche Originalautorisierung eine separate Kopie,
nachvollziehbare Commits und keine fremden Änderungen überschreiben. Da Plan
keine Shell-Freigabe erhält, führt ein frischer `Run` nötige Git-, Kopier- und
Commitbefehle im autorisierten Arbeitsbereich aus. Das delegiert nicht das
Schreiben des Plans und ist kein Grund für einen zusätzlichen Develop-Auftrag.

## Tatsächliche OpenCode-V2-Syntax

Grundlage: offizielle [V2-Agent-Dokumentation](https://dev.opencode.ai/v2/docs/agents/)
und [V2-Permissions](https://dev.opencode.ai/v2/docs/permissions/), geprüft gegen
die installierte CLI `opencode v2.1.3`.

- Markdown-Frontmatter verwendet `permissions` als geordnete Liste von
  `action`, `resource`, `effect`. Die letzte passende Regel gewinnt.
- Die Aktion **`edit`** schützt alle drei Werkzeuge **edit, write und patch**.
  Eine Freigabe für eine erfundene Aktion `patch` würde diesen Schutz nicht
  korrekt konfigurieren.
- Ressourcen sind normalisierte Pfade. Interne Pfade sind relativ zur aktiven
  Location, externe Pfade kanonisch absolut. `*` erfasst auch `/`, daher schließen
  die drei Muster Unterverzeichnisse ein; es sind keine Shell-Globs.
- Die grundsätzliche Sperre der Rolle bleibt bestehen. Nur die drei
  Planungsbereiche erhalten `edit: allow`; danach bleiben umgebungsdateiartige
  Namen zusätzlich von Edits ausgeschlossen. Bestehende Leseregeln werden durch
  diese Änderung nicht gelockert.
- Berührt ein Patch mehrere Ressourcen, genügt ein einziges `deny` für die
  Ablehnung der Operation. `execute` erlaubt Code Mode, nicht automatisch die
  darin aufgerufenen Werkzeuge: deren Permissions gelten weiter.

Diese Permissions sind keine Betriebssystem-Sandbox. Insbesondere sind
inhaltliche Autorisierung und die Unterscheidung „Planungsunterlage statt
Produktcode“ Rollenregeln. Delegierte Agents verwenden eigene Permissions,
nicht eine Schnittmenge mit Plan. Ein erlaubter Delegationsweg darf deshalb
nicht zur Umgehung des Plan-Schreibbereichs dienen. Eine abweichende aktive
Location, spätere Konfigurations-/Policyänderungen oder projektspezifische
Freigaben verlangen eine erneute Prüfung.

## Begrenzte Prüfung

Die gezielte Probe unter `tests/plan_permission_probe.py` verwendet ausschließlich
ein isoliertes HOME, eigene XDG-Verzeichnisse, eine Kopie des Plan-Profils und
synthetische Dateien. Ein lokaler deterministischer Provider liefert feste
Werkzeugaufrufe statt eines echten Modells; keine Credentials, MCP-Geräte,
Installation oder Umschaltung der persönlichen Konfiguration.

```bash
python3 tests/plan_permission_probe.py --opencode /absoluter/pfad/zu/opencode
```

Die Probe prüft Editieren in allen drei Bereichen (auch verschachtelt), Schreiben,
die Sperren für Produktquellen, sonstige Markdown- und Konfigurationsdateien
sowie normalisierte Traversal- und absolute Produktpfade. Sie prüft Dateiinhalte
und tatsächliche Permission-Fehler statt nur den Exitcode. Logs und `report.json`
bleiben im ignorierten `work/agent-artifacts/pkg03/probe-*/` der Source-Kopie.

Strukturprüfung (Regeln und Profilladen), tatsächliche Werkzeugausführung in
der installierten Laufzeit und Modellverhalten sind getrennte Nachweise.
Ein synthetischer Provider belegt Permission-Durchsetzung, aber nicht, dass
ein echtes Modell Aufgaben richtig als Planung einordnet, unbekannte Ziele
nachfragt oder nicht delegiert. Solche Modellläufe bleiben separat zu prüfen.
Patch-/Mehrdatei-Operationen und Code-Mode-Verschachtelung sind durch die
offizielle Permissions-Dokumentation beschrieben, aber nicht durch diese
Edit-/Write-Probe ausgeführt. Sie ist ebenso wenig eine Symlink-/Hardlink-
oder Betriebssystem-Sandbox-Prüfung.
