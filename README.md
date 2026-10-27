# Atlas

**Klare Rollen tragen komplexe Aufgaben.**

Atlas bietet klare Agent-Rollen für OpenCode. Frische Kontexte, gezielte Delegation und kompakte Übergaben halten größere Aufgaben übersichtlich. Planung, Analyse, Umsetzung und Ausführung greifen ineinander. Wichtige Erkenntnisse bleiben erhalten und erreichen die passende Rolle. Für transparente, fokussierte Zusammenarbeit.

## Der Grundgedanke

Ein guter Agent muss nicht die gesamte Unterhaltung, jeden Build-Log und alle Werkzeugantworten gleichzeitig im Kopf behalten. Atlas verteilt Arbeit auf klar beschriebene Rollen — nicht um Tokens um jeden Preis zu sparen, sondern um den Kontext einer Rolle so groß zu halten, wie die Aufgabe es erfordert. Neue eigenständige Aufgaben beginnen mit frischem Kontext und gezielter Übergabe, ohne Gesamtchat; zusammengehörige Folgefragen gehen möglichst an dieselbe Fachsession. Zurück kommen Ergebnis, belastbare Belege und wichtige neue Erkenntnisse.

Der Name greift das Bild des Atlas auf: Komplexe Aufgaben werden von einer nachvollziehbaren Struktur getragen. Die Rollen unterstützen einander; der Orchestrator hält den Gesamtauftrag zusammen.

## Die Rollen

| Rolle | Aufgabe |
|---|---|
| **Orchestrate** | Arbeit verteilen, Ergebnisse einordnen und den Nutzer auf dem Laufenden halten |
| **Plan** | Architektur, Lösungswege und Arbeitspakete entwickeln |
| **Analyze** | Zusammenhänge und Ursachen mit Belegen untersuchen |
| **Develop** | Abgegrenzte Änderungen umsetzen und passende Tests ergänzen |
| **Run** | Befehle, Tests, Dienste und MCP-Aufträge gemeinsam ausführen; große Ausgaben und Antworten verdichten |
| **Review** | Ergebnisse unabhängig auf Fehler und Regressionen prüfen |
| **Auto** | Ohne Rückfragen fast alle Werkzeuge nutzen und einen Auftrag eigenständig bearbeiten |
| **Build** | Wie Auto eigenständig arbeiten, aber vor jedem Shell-Befehl eine Nutzerbestätigung einholen |

Auto und Build eignen sich für zusammenhängende Arbeit in einer Session; Build fügt dabei eine Pflichtbestätigung vor jedem Shell-Befehl hinzu. Orchestrate koordiniert Aufgaben, die von gezielter Aufteilung profitieren. Ob Review dauerhaft als eigenständige Rolle bestehen bleibt oder nur noch begrenzt optional zum Einsatz kommt, ist offen; bis dahin gilt die Rolle unverändert wie oben beschrieben.

## Kontext wird bei Bedarf geladen

Der globale Einstieg bleibt kurz. Ein Agent erhält sein eigenes Rollenprofil; die Delegationsanleitung wird erst vor einer Delegation gelesen, die Artefaktanleitung bei großen Ausgaben, Git-Regeln erst bei tatsächlicher Repository-Arbeit.

Rohdaten bleiben beim ausführenden Spezialisten oder in gezielt referenzierten Artefakten. Wichtige Zusatzfunde gehen als Beleg, Bedeutung, Auswirkung und offene Fragen an den Parent. Im Hauptchat erscheinen kurze Ankündigungen und relevante Zwischenstände; der Nutzer muss keine Child-Sessions durchsuchen.

Eine Fachsession wird nur bei erneutem fachlichem Bedarf fortgesetzt, nicht laufend. Die genauen Regeln zu Fortsetzung, Ersatzübergabe und Session-Zuordnung durch Orchestrate stehen in [SUBAGENTS.md](SUBAGENTS.md).

## Wenn eine Umsetzung neue Fragen aufwirft

```mermaid
sequenceDiagram
    participant O as Orchestrate
    participant A as Analyze
    participant D as Develop

    O->>A: neues Feature zur Analyse
    activate A
    A-->>O: Analyse erledigt (analyse-ergebnis.md)
    deactivate A

    O->>D: Umsetzung beauftragen
    activate D
    Note over D: liest analyse-ergebnis.md
    D-->>O: Pause – Nachanalyse nötig
    deactivate D

    O->>A: ursprüngliche Session mit Frage und neuen Belegen fortsetzen
    activate A
    A-->>O: Annahmen geprüft, Nachanalyse erledigt
    deactivate A

    O->>D: möglichst dieselbe Session mit aktualisiertem Auftrag fortsetzen
```

Develop meldet eine Informationslücke oder widerlegte Annahme mit neuen Belegen und aktuellem Arbeits-/Commitstand an seinen Parent zurück; dieser setzt möglichst die ursprüngliche Analyze-Session fort und danach möglichst dieselbe Develop-Session mit aktualisiertem Auftrag. Das ist eine Rückgabe an den Parent, keine Rückdelegation an einen weiteren Analyze. Die genauen Regeln dazu (Ersatzübergabe, Zuständigkeiten, Umfangserweiterung) stehen in [SUBAGENTS.md](SUBAGENTS.md#gezielte-nachanalyse).

## Repository-Struktur

```text
.
├── AGENTS.md
├── SUBAGENTS.md
├── agents/       # Native OpenCode-V2-Rollen als Markdown
├── commands/     # /atlas und /setup-atlas
├── skills/atlas/ # Ein Einstiegsskill mit Installer und Modell-Setup
├── atlas.json.example  # Vorlage für persönliche Modellpräferenzen
├── guide/        # Bedarfsanleitungen: ARTIFACTS.md, MCP.md, PLANNING.md, REPOSITORIES.md
├── checks/       # Installer-Regressionstests
├── .github/workflows/release.yml # Pakete und versionierte Releases
├── README.md
├── LICENSE
└── .gitignore
```

Die Rollen verwenden das native Rollenformat von OpenCode. Modelle und persönliche MCP-Verbindungen sind nicht festgelegt.

## Installieren

Voraussetzung: **OpenCode V2 und Python 3.9 oder neuer**. Du brauchst keinen
Atlas-Klon. Lade einmal den kleinen Installer und registriere damit Skill
und Command (nach dem Merge dieses PRs in `opencode`):

```sh
curl -fL https://raw.githubusercontent.com/DevelopingMedo/atlas/opencode/skills/atlas/scripts/atlas.py -o atlas-installer.py
python3 atlas-installer.py bootstrap --global --ref opencode
```

Rufe danach in OpenCode auf:

```text
/atlas
```

Der Dialog klärt Projekt oder global und deine Modellpräferenzen. Danach
richtet er alle acht Rollen, gemeinsame Regeln, vier Guides und Commands ein.
Die Installation ist wiederholbar; vorhandene eigene Dateien werden erhalten.
Ein optionaler Standardagent wird nicht automatisch umgestellt.

Für einen rein projektlokalen Einstieg ersetzt du `--global` durch
`--project /pfad/zum/projekt`. Bei einem abweichenden aktiven globalen
Konfigurationsverzeichnis kannst du `--target /pfad/zur/config` verwenden.

**Diesen noch nicht gemergten PR testen:** In beiden Installationszeilen
`opencode` durch `docs/atlas-skill-distribution` ersetzen. Dadurch stammen
Installer und Paket aus demselben Implementierungsbranch.

### Aktualisieren

```text
/atlas update opencode
/atlas update v1.0.0
```

Der zweite Aufruf setzt einen tatsächlich veröffentlichten Tag voraus.
Eine Quelle ist Pflicht. Branches werden einmalig auf einen Commit aufgelöst;
alle Dateien kommen aus diesem Stand. Persönliche `atlas.json` und eigene
Dateien bleiben erhalten. Bei kollidierenden Änderungen stoppt der Installer
**vor dem Schreiben** und nennt die betroffenen Pfade. Es gibt keinen
Force-Schalter und keinen automatischen Merge durch das Modell.

Der Nachweis `.atlas-install.json` enthält Quelle, Commit und Prüfsummen der
Originaldateien. Er ist getrennt von deinen Modellpräferenzen. Eigene
Änderungen und Löschungen bleiben erhalten, solange der neue Paketstand nicht
mit ihnen kollidiert. Vorhandene identische manuelle Kopien können übernommen
werden; abweichende Altdateien werden als Konflikte gemeldet.

### Skill-Paket und Releases

Bei einem `v*`-Tag baut der Workflow ein Release mit `atlas-skill.zip`
(ein Skill einschließlich Payload), `atlas-package.zip` und dem standalone
Installer `atlas.py`. Ein eigenes Marketplace-Repo ist nicht nötig.
Die Veröffentlichung erfolgt erst, wenn du einen Tag pushst.

Für Skill-Installer gibt es genau den Einstieg `atlas`. Nach dem Merge kann
er auch mit `npx skills add https://github.com/DevelopingMedo/atlas/tree/opencode/skills/atlas -a opencode -g --copy`
installiert werden. Der erste Aufruf ist dann `@atlas Richte Atlas ein`;
dieser registriert bei der vollständigen Einrichtung auch `/atlas`.
Verwende dabei `--copy`, da der Atlas-Installer keine Skill-Symlinks überschreibt.
Der Bootstrap oben stellt `/atlas` bereits vor dem ersten Setup bereit.

Alle Dateipfade, CLI-Aufrufe und Grenzen stehen in
[Installation und Updates](docs/installation.md).

MCP-Tools und -Ressourcen sind nur für Auto und Run freigegeben. Diese Rollenregel gilt für alle MCP-Server und alle Betriebssysteme. Andere Rollen delegieren MCP-Aufträge an Run. Rollenbezogene Berechtigungen blenden die Werkzeuge aus und sperren Aufrufe, schalten aber nicht die Serverprozesse ab. Persönliche Endpunkte, Zugangsdaten und rechnerabhängige Installationen bleiben außerhalb der allgemeinen Agent-Regeln. Details: [guide/MCP.md](guide/MCP.md).

## Persönliches Setup

Mit `/setup-atlas` stimmst du Atlas auf deine verfügbaren Modelle ab. Wir empfehlen, das Setup nach der Installation durchzuführen. Steht in `atlas.json` der boolesche Wert `"atlas-setup": true`, entfällt der Setup-Hinweis. Fehlt die Datei oder ist das Flag nicht gesetzt, empfiehlt der Agent das Setup einmal pro Hauptsession und bearbeitet den Auftrag weiter. Subagents wiederholen den Hinweis nicht.

`/setup-atlas` wechselt in die vorhandene Rolle `Auto` und lädt den Skill [`atlas`](skills/atlas/SKILL.md) im Ablauf für Modellpräferenzen. Er ermittelt die verfügbaren Modelle über `opencode models`, fragt die persönlichen Präferenzen gesammelt ab und speichert sie in `atlas.json` neben der mitgelieferten [`atlas.json.example`](atlas.json.example). Der Befehl kann bestehende Einstellungen aktualisieren. Anschließend kann wieder die vorherige Rolle ausgewählt werden.

Der Aufruf benötigt keine Argumente. Zusätzlicher Text wird als freier Einrichtungshinweis übernommen, beispielsweise `/setup-atlas Bitte nur Modelle meines OpenAI-Providers vorschlagen`. Es gibt keine festen Parameter oder Flags; offene Angaben werden im Dialog geklärt.

| Einstellung | Bedeutung |
|---|---|
| `atlas-setup` | `false` in der Vorlage; nach abgeschlossener Einrichtung `true`. Nur der boolesche Wert `true` unterdrückt den Setup-Hinweis. |
| `models.fast` | Bevorzugtes Modell für einfache Aufgaben |
| `models.standard` | Bevorzugtes Modell für normale Aufgaben |
| `models.deep` | Bevorzugtes Modell für anspruchsvolle Aufgaben |

Die Vorlage enthält `null` als Modellwerte: Es gibt damit keine persönliche Vorgabe. Modell-IDs haben die Form `provider/model`, gegebenenfalls mit einer unterstützten `#variant`. Die Stufe richtet sich nach dem Arbeitspaket, nicht nach der Rolle.

`atlas.json` wird von Git ignoriert; `atlas.json.example` wird mitgeliefert. Alternativ zum Skill kann die Vorlage manuell als `atlas.json` gespeichert und angepasst werden. Bei manueller Einrichtung setze abschließend `"atlas-setup": true` und belasse den Eintrag am Dateianfang, damit der Startcheck kurz bleibt. Die Datei speichert den Setup-Status und persönliche Präferenzen; sie ist keine OpenCode-Konfiguration und bewirkt noch keinen automatischen Modellwechsel oder eine automatische Zuordnung durch den Planner.

### Im Projekt verwenden

Wähle im `/atlas`-Dialog das Projekt oder verwende den Installer direkt:

```sh
python3 atlas-installer.py install --project /pfad/zum/projekt --ref opencode
```

Atlas liegt dann unter `.opencode/`. Der Installer ergänzt dort die lokale
`opencode.json` bzw. `opencode.jsonc` um die Atlas-Instruction, erhält vorhandene
JSONC-Kommentare und eigene Einstellungen und ergänzt gezielte Ignore-Einträge.
Die `.gitignore` des Atlas-Quellrepos wird nicht in dein Projekt kopiert.
Eigene globale Regeln stehen außerhalb eines markierten Atlas-Blocks in
`AGENTS.md` und bleiben bei Updates erhalten.

Projektlokale Atlas-Einstellungen haben Vorrang vor globalen. Die persönliche
Datei `.opencode/atlas.json` bleibt lokal und wird nicht vom Installer verändert.

## Was die Dateien leisten

Atlas liefert Rollen, gemeinsame Arbeitsregeln und Bedarfsanleitungen. Die jeweilige Laufzeit bestimmt verfügbare Werkzeuge, Delegationstiefe und Berechtigungen; ist direkte Delegation nicht verfügbar, gibt die Rolle dem Parent eine konkrete Folgeanforderung zurück. Frischer Kontext, Zuständigkeiten und knappe Übergaben sind Anweisungen, keine Laufzeitprüfung.

Bei tatsächlicher Git-Arbeit gehören nachvollziehbare Commits zur Übergabe; eine temporäre Implementierung ohne autorisierte Originaländerung entsteht in einer separaten Kopie, ohne automatische Git-Initialisierung.

Installer, Paketbau und Konfliktfälle werden automatisiert unter `checks/` geprüft. Ein vollständiger Dialog in einer laufenden OpenCode-V2-Instanz ist nicht automatisiert geprüft. Persönliche Konfigurationen (Modelle, Provider, MCP-Verbindungen) sind nicht Teil dieses Repositorys.

## Dokumentation

- [OpenCode V2: Agents](https://dev.opencode.ai/v2/docs/agents/)

## Lizenz

Atlas steht unter der **Apache License 2.0 mit Commons Clause 1.0**.
Beide Texte stehen gemeinsam in [LICENSE](LICENSE) und gelten zusammen;
Apache 2.0 ist keine separate Lizenzoption. Atlas ist damit Source available.

- Private und berufliche Nutzung, auch bei Kunden, ist kostenlos erlaubt.
- Mit Atlas entwickelte eigene Software darf verkauft werden. Die Lizenz
  beansprucht keine Rechte an unabhängig erstellten Arbeitsergebnissen.
- Änderungen und kostenlose Forks sind erlaubt. Bei Weitergabe müssen die
  Lizenz einschließlich Commons Clause sowie die relevanten Urheber- und
  Herkunftshinweise erhalten bleiben; geänderte Dateien sind zu kennzeichnen.
- Atlas oder einen Fork als „Better Atlas“ zu verkaufen, ist ohne gesonderte
  Erlaubnis nicht gestattet, wenn der Wert des Angebots vollständig oder
  wesentlich aus Atlas stammt. Das gilt auch für entsprechend geprägte
  kostenpflichtige Hosting-, Beratungs- und Supportangebote.

Für eine gesonderte Verkaufserlaubnis und die zugehörigen Konditionen kontaktiere
[Medough / DevelopingMedo](https://github.com/DevelopingMedo).
Diese Zusammenfassung ersetzt nicht den verbindlichen Text in [LICENSE](LICENSE).

Der Lizenzwechsel gilt ab dem Commit, der ihn einführt. Bereits unter MIT
veröffentlichte Versionen behalten ihre bisherigen Nutzungsrechte. Der letzte
Stand vor dem Wechsel ist
[`2e65061`](https://github.com/DevelopingMedo/atlas/commit/2e650613a5ade4049d4c263888a3132acaed89f4).
