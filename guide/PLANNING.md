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
keine Shell-Freigabe erhält, führt `Run`, mit Sessionwahl nach `SUBAGENTS.md`, nötige Git-, Kopier- und
Commitbefehle im autorisierten Arbeitsbereich aus. Das delegiert nicht das
Schreiben des Plans und ist kein Grund für einen zusätzlichen Develop-Auftrag.

## Tatsächliche OpenCode-V2-Syntax

Grundlage: offizielle [V2-Agent-Dokumentation](https://dev.opencode.ai/v2/docs/agents/)
und [V2-Permissions](https://dev.opencode.ai/v2/docs/permissions/), geprüft gegen
die installierte CLI `opencode v2.1.3`.

- Markdown-Frontmatter verwendet `permissions` als geordnete Liste von
  `action`, `resource`, `effect`; die letzte passende Regel gewinnt.
- Die Aktion **`edit`** schützt alle drei Werkzeuge **edit, write und patch**;
  eine erfundene Aktion `patch` würde diesen Schutz nicht korrekt konfigurieren.
- Ressourcen sind normalisierte Pfade (intern relativ zur aktiven Location,
  extern kanonisch absolut) und keine Shell-Globs; `*` erfasst auch `/`, daher
  schließen die drei Muster Unterverzeichnisse ein.
- Die grundsätzliche Sperre der Rolle bleibt bestehen; nur die drei
  Planungsbereiche erhalten `edit: allow`, umgebungsdateiartige Namen bleiben
  zusätzlich von Edits ausgeschlossen. Bestehende Leseregeln werden dadurch
  nicht gelockert.
- Berührt ein Patch mehrere Ressourcen, genügt ein einziges `deny` für die
  Ablehnung. `execute` erlaubt Code Mode, nicht automatisch die darin
  aufgerufenen Werkzeuge: deren Permissions gelten weiter.

Diese Permissions sind keine Betriebssystem-Sandbox. Inhaltliche Autorisierung
und die Unterscheidung „Planungsunterlage statt Produktcode“ sind Rollenregeln.
Delegierte Agents verwenden eigene Permissions, nicht eine Schnittmenge mit
Plan — ein erlaubter Delegationsweg darf deshalb nicht zur Umgehung des
Plan-Schreibbereichs dienen. Eine abweichende aktive Location, spätere
Konfigurations-/Policyänderungen oder projektspezifische Freigaben verlangen
eine erneute Prüfung.

## Begrenzte Prüfung

Eine gezielte Probe (`tests/plan_permission_probe.py`, isoliertes HOME/XDG,
Kopie des Plan-Profils, synthetische Dateien, deterministischer Provider statt
echtem Modell) prüft Editieren in allen drei Bereichen, Schreiben, die Sperren
für Produktquellen/sonstige Markdown-/Konfigurationsdateien sowie normalisierte
Traversal- und absolute Produktpfade — anhand tatsächlicher Dateiinhalte und
Permission-Fehler, nicht nur des Exitcodes.

Das ist eine reine Strukturprüfung: Sie belegt Permission-Durchsetzung, aber
nicht, dass ein echtes Modell Aufgaben richtig als Planung einordnet,
unbekannte Ziele nachfragt oder nicht delegiert; solche Modellläufe bleiben
separat zu prüfen. Patch-/Mehrdatei-Operationen, Code-Mode-Verschachtelung,
Symlinks/Hardlinks und Betriebssystem-Sandboxing sind durch diese Probe
ebenfalls nicht abgedeckt.
