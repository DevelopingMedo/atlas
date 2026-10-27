# Entwurf: Atlas als installierbares Gesamtpaket

Status: Konzept zur Diskussion, noch kein implementierter Installer.
Stand: 27.10.2026. Ausgangspunkt ist das gesamte Repository auf
`fba69d52aca53297bc3a5164998ab2578506f858`, einschließlich PR #9.
Dieser Entwurf ersetzt noch keine bestehende Installationsanleitung.

## Ziel

Ein Nutzer installiert einmal den Einstieg `atlas` und richtet anschließend
das vollständige Atlas über einen geführten Dialog ein. Er muss keinen
Atlas-Klon selbst verwalten und keine Rollen oder Regeln einzeln kopieren.

Zum Umfang gehören alle acht Rollen, gemeinsame Regeln, Delegationsregeln,
sämtliche Bedarfsanleitungen und das persönliche Modell-Setup aus PR #9.
Atlas bleibt dasselbe Rollensystem; geändert werden Verpackung und Einrichtung.

Ein neues Repository und ein selbst entwickelter Marketplace sind dafür
nicht erforderlich. Das bestehende Repository bleibt die einzige Quelle.
Releases liefern das installierbare Paket; skills.sh dient der Auffindbarkeit
und Skill-Installation. Ein eigener OpenCode-V2-HTTP-Katalog ist eine
optionale weitere Auslieferung desselben Pakets.

## Was bereits vorhanden ist und was fehlt

| Bestandteil | Vorhandener Stand | Für das Gesamt-Setup nötig |
|---|---|---|
| Acht Rollen in `agents/` | Native V2-Profile inklusive Berechtigungen | Vollständig ausliefern und am gewählten Ziel registrieren |
| `AGENTS.md`, `SUBAGENTS.md` | Gemeinsame Regeln und Delegation | Erhalten und ihre tatsächliche Einbindung prüfen |
| Vier Dateien in `guide/` | Bedarfsanleitungen mit relativen Verweisen | Zusammen mit den Rollen installieren |
| `skills/setup-atlas/SKILL.md` | Persönliche Modelle auswählen und speichern | Als Modell-Schritt des Gesamt-Setups weiterverwenden |
| `commands/setup-atlas.md` | Einstieg, der bereits `Auto` voraussetzt | Als kompatiblen Einstieg für reine Präferenzänderungen erhalten |
| `atlas.json.example` | Vorlage mit Abschlussflag und drei Modellstufen | Ausliefern; persönliche `atlas.json` am Ziel anlegen |
| `.gitignore` | Schutz persönlicher/lokaler Dateien im Atlas-Repo | Am Ziel nur passende Ignore-Einträge ergänzen |
| `README.md`, `LICENSE` | Erklärung und Lizenz | Im Release erhalten; nicht als Produktdateien ins Zielprojekt kopieren |
| Release-Paket, Bootstrap, `/atlas` | Noch nicht vorhanden | Neu hinzufügen und mit sauberer OpenCode-Installation prüfen |

Die Anforderungen betreffen das gesamte Repository, nicht nur den bisherigen
Modell-Setup-PR. Die vorhandenen Inhalte sind weitgehend wiederverwendbar;
Installation, Konfliktbehandlung, Command-Registrierung und Release-Bau fehlen.

## Der erste Einstieg ist eine eigene Aufgabe

OpenCode V2 dokumentiert Skills über den `skill`-Aufruf bzw. `@atlas`.
Slash-Commands werden separat als Command-Datei oder in der Konfiguration
definiert. Aus der Installation eines `SKILL.md` allein folgt deshalb keine
hier zugesicherte Registrierung von `/atlas`.

Der erste Start darf auch nicht von Atlas-eigenen Rollen abhängen:
`Auto` und `Orchestrate` sind vor der Installation noch nicht vorhanden.
Der Bootstrap verwendet einen bereits verfügbaren Agent mit den nötigen
Werkzeugen und achtet auf dessen vorhandene Berechtigungen.

### Empfohlener kleiner Einstieg über den vorhandenen Skill-Installer

Nach Veröffentlichung eines Skills `atlas` kann dessen Installation so
aussehen; dieser Befehl ist heute noch kein funktionierender Atlas-Installer:

```sh
npx skills add DevelopingMedo/atlas --skill atlas -a opencode -g
```

Der erste ausdrückliche Aufruf lautet dann `@atlas Richte Atlas ein`.
Der Skill installiert das Gesamtpaket und registriert `/atlas`.
Nach der nachgewiesenen Neuladung der Konfiguration steht dieser Command
für weitere Aufrufe bereit. Eine neue Session allein wird nicht ohne
Laufzeittest als ausreichender Reload versprochen.

Damit gibt es bereits eine praktische Skill-basierte Installation ohne
eigenen Marketplace. Der einmalige erste Aufruf ist allerdings noch nicht
die gewünschte unmittelbare `/atlas`-Erfahrung.

### Wenn schon der allererste Aufruf exakt /atlas sein soll

Dann muss die einmalige Bootstrap-Installation **Skill und Command gemeinsam**
bereitstellen. Dafür ist ein kleiner zusätzlicher Installer nötig, der nur
den Einstieg registriert; die eigentliche Einrichtung bleibt im Skill.

Ein gemeinsames Release kann beides enthalten. Der gewählte Installer muss
beide Dateien tatsächlich an die richtigen Stellen bringen. Der oben genannte
`skills add`-Befehl darf nicht als Installer für benachbarte Command-Dateien
beworben werden. Ein npm-Paket, ein OpenCode-Plugin oder ein eigenes
Installationsskript ist erst auszuwählen; dafür wird in diesem Entwurf
kein bereits veröffentlichtes Kommando erfunden.

**Empfehlung für das gewünschte Ziel:** Den gemeinsamen Bootstrap in den
primären Implementierungsumfang aufnehmen, damit bereits der erste Aufruf
`/atlas` lautet. Der reine Skill-Installer bleibt ein ergänzender Weg über
`@atlas`. Der konkrete Bootstrap-Transport ist vor der Umsetzung festzulegen;
ein eigener Marketplace ist dafür nicht nötig.

## Ablauf des Gesamt-Setups

1. OpenCode-Version, Projektpfad und vorhandene Atlas-Installation bestimmen.
   Atlas verwendet V2-Profile. V1 wird nicht ohne eigene Portierung als
   kompatibel behandelt.
2. Noch offene Angaben gesammelt klären: nur dieses Projekt oder global,
   gewünschte Modelle und optionaler Standardagent. Bereits genannte
   Angaben übernehmen. Den aktuellen Provider-Hinweis aus PR #9 erhalten
   und eine bereits genannte Eingrenzung direkt berücksichtigen. Globales Installieren des Einstiegsskills entscheidet
   noch nicht, wo das Atlas-Gesamtpaket eingerichtet wird.
3. Aus dem mitgelieferten Paket einen konkreten Änderungsplan erzeugen:
   Zielpfade, neue Dateien, Ergänzungen an Konfigurationen und Konflikte.
   Vorhandene eigene Regeln und Agent-IDs berücksichtigen. Der Nutzer kann
   den vorgesehenen Aufbau ansehen.
4. Die vereinbarten Änderungen aus dem Paket deterministisch anwenden.
   Keine Regelsammlung durch das Modell neu formulieren lassen.
5. Den bewährten Modell-Dialog aus PR #9 ausführen. Bekannte Einstellungen
   übernehmen, unbekannte JSON-Felder erhalten und keine Modell-IDs erfinden.
   `atlas-setup` bleibt bei unvollständiger Einrichtung `false`;
   erst nach erfolgreicher Installation und abgeschlossener Modellauswahl
   wird es als boolescher erster Eintrag auf `true` gesetzt.
6. Ergebnis prüfen: Dateien, auflösbare Verweise, geladene Regeln, Rollen,
   Command und gültige persönliche Einstellungen. Dateien auf der Platte
   allein beweisen noch keine aktive OpenCode-Registrierung.
7. Knapp erklären, welche Rollen und Commands verfügbar sind und ob die
   aktive OpenCode-Instanz ihre Konfiguration noch neu laden muss.

Der Dialog soll sich wie eine Einrichtung anfühlen. Er fragt nicht für jede
Datei einzeln, sondern behandelt offene Entscheidungen und konkrete Konflikte
gesammelt.

## Ein veröffentlichter Skill, vollständiger Inhalt

Der öffentliche Einstieg heißt `atlas`. Seine `SKILL.md` bleibt kurz und
steuert Installation bzw. erneute Einrichtung. Rollen und Handbücher sind
Dateien im Paket und werden erst bei ihrem tatsächlichen Einsatz geladen.

Für das Ziel „nur ein Skill“ wird der Modell-Setup-Ablauf aus
`skills/setup-atlas/SKILL.md` in eine bedarfsweise geladene Referenz des
Skills `atlas` überführt. Dabei muss die heutige Ableitung des
Installationsstamms aus „zwei Verzeichnisse über der Skill-Basis“ durch
das ausdrücklich ermittelte Installationsziel ersetzt werden.
Das ist eine notwendige Pfadanpassung, keine Änderung der Modellauswahl.

`/setup-atlas` bleibt als kompatibler Command erhalten, lädt aber denselben
Skill im Ablauf „persönliche Präferenzen“. `/atlas` führt durch das gesamte
Setup. Es gibt damit einen veröffentlichten und am Ziel aktiven
Atlas-Einstiegsskill, keine zweite notwendige Skill-Installation.
Die Quelldateien des jetzigen Setups bleiben bis zu dieser Umsetzung erhalten.

Beim Release-Bau werden die benötigten Inhalte aus genau einem Git-Stand
gebündelt: Rollen, Regeln, Guides, Vorlage, Lizenz und die Setup-Referenz.
Keine zweite handgepflegte Kopie der Rollen unter `skills/atlas/assets/`.
Eine generierte Payload kann als Archiv im Skill liegen; dadurch werden
enthaltene Markdown-Dateien nicht versehentlich als weitere Skills entdeckt.

## Zielorte und Integration

| Inhalt | Projektlokal | Global |
|---|---|---|
| Acht Rollen | `<projekt>/.opencode/agents/` | `~/.config/opencode/agents/` |
| Regeln und Guides | `<projekt>/.opencode/` | `~/.config/opencode/` |
| Command-Wrapper | `<projekt>/.opencode/commands/` | `~/.config/opencode/commands/` |
| Einstiegsskill | `<projekt>/.opencode/skills/atlas/` | `~/.config/opencode/skills/atlas/` |
| Vorlage und persönliche Datei | `<projekt>/.opencode/atlas.json.example`, daneben `atlas.json` | `~/.config/opencode/atlas.json.example`, daneben `atlas.json` |

Die Pfade stehen für die üblichen V2-Verzeichnisse. Abweichende aktive
Konfigurationspfade müssen erkannt oder ausdrücklich vereinbart werden.

Projektlokal wird `.opencode/AGENTS.md` in das bestehende `instructions`-Array
der OpenCode-Konfiguration aufgenommen. Bestehende Einträge bleiben erhalten.
Globale Regeln werden mit vorhandenen Regeln zusammengeführt, statt
`AGENTS.md` blind zu ersetzen. Relative Verweise müssen danach weiterhin
gegen den wirklichen Atlas-Installationsstamm auflösbar sein.

`opencode.json` und `opencode.jsonc` werden gezielt ergänzt. Bei JSONC bleiben
Kommentare und fremde Einstellungen erhalten. Eine Umstellung von
`default_agent` auf `Orchestrate` ist eine eigene Setup-Auswahl und erfolgt
nicht allein wegen der Installation.

Die bisherige `.gitignore` wird nicht komplett ins Produktprojekt übernommen:
Einträge wie `tests/` oder `opencode.json` wären dort zu weitreichend.
Persönliche `atlas.json` wird gezielt ignoriert; das Setup prüft außerdem,
dass sie nicht schon getrackt ist. Secrets und private Provider-/MCP-Daten
sind weder Paketinhalt noch Commit-Inhalt.

„Im GitHub anlegen“ bedeutet im Projektfall zunächst Änderungen in der
Arbeitskopie des gewählten Repositories. Ein GitHub-Login ist für globale
Installation oder lokale Einrichtung nicht notwendig. Soll ausdrücklich
ein PR im Zielrepo entstehen, kann derselbe vorbereitete Änderungsstand auf
einem Branch veröffentlicht werden. `atlas.json` bleibt dabei lokal.

## Releases, Katalog und erneute Ausführung

- Ein Release bindet Einstieg, Payload und Manifest an denselben Git-Stand.
  Das Manifest nennt Version, Quellcommit und enthaltene Dateien/Prüfsummen.
  Laufzeitinhalte werden nicht aus einem wechselnden Branch nachgeladen.
- Ein HTTP-Katalog für OpenCode V2 kann im selben Repository erzeugt und
  beispielsweise über GitHub Pages veröffentlicht werden. Er benötigt
  `index.json`, sichere relative Dateipfade und eine neue `version` bei
  Inhaltsänderungen. Er registriert allein noch keinen Slash-Command.
- Die vorhandenen Dateien müssen als vollständiges Release-Asset abrufbar
  sein. Ein nackter Link auf `SKILL.md` liefert die Payload nicht automatisch.
  Der genaue Release-Downloadweg ist mit dem gewählten Installer zu prüfen.
- Erneutes Setup mit gleichem Paket erzeugt keine Duplikate und überschreibt
  keine persönliche Konfiguration. Bereits vorhandene manuelle Atlas-Kopien
  werden berücksichtigt.
- Ein Update des Einstiegsskills über `skills update` aktualisiert nicht
  automatisch die bereits ins Ziel kopierten Atlas-Dateien. Erneutes
  `/atlas` muss einen expliziten Abgleich anbieten und lokale Änderungen als
  Konflikte zeigen.
- Der MVP darf bei Änderungen an verwalteten Dateien gezielt anhalten.
  Ein eigener allgemeiner Merge- oder Rollback-Manager ist nicht erforderlich.
  Vor Änderungen werden betroffene vorhandene Dateien gesichert; bei einem
  Fehler wird kein vollständig abgeschlossenes Setup behauptet.

## Kleine Umsetzungsschritte

1. Release-Bau aus den bestehenden Dateien, Manifest und vollständiges
   Skill-Paket ergänzen. Modell-Setup als Referenz einbinden.
2. Einstiegsskill samt Installation in ein ausdrücklich ermitteltes Ziel
   umsetzen. Vorhandene Regeln, JSONC und Ignore-Einträge berücksichtigen.
3. `/atlas` registrieren und `/setup-atlas` als kompatiblen Wrapper anbinden.
   Falls der erste Aufruf schon `/atlas` sein muss: gemeinsamen Bootstrap
   ebenfalls liefern.
4. Installation und Wiederholung in isolierten Konfigurationen prüfen.
   Anschließend einen tatsächlichen OpenCode-V2-Dialog mit sauberer
   Ausgangskonfiguration und eine Migration einer bisherigen Atlas-Kopie
   erproben.
5. README auf den nachgewiesenen Einstieg umstellen, Release veröffentlichen
   und Auffindbarkeit über skills.sh separat verifizieren.

## Prüfkriterien für die Umsetzung

- Sauberes Ziel: alle acht Rollen, gemeinsamen Regeln, vier Guides,
  Commands und persönliches Setup verfügbar; kein Nutzer-Klon erforderlich.
- Dateiverweise und Lizenz vollständig; Payload stammt aus einem Git-Stand.
- Bestehende eigene Regeln, Rollen gleichen Namens und JSONC werden erkannt
  und ohne stilles Überschreiben behandelt.
- Projektlokale Einrichtung hat bei paralleler globaler Installation
  nachvollziehbar Vorrang; das Modell-Setup schreibt ins gewählte Ziel.
- Wiederholung verändert keine bereits identischen Dateien und erhält
  persönliche Präferenzen sowie unbekannte JSON-Felder.
- Abbruch oder Fehler lässt das Abschlussflag nicht fälschlich auf `true`.
- `atlas.json` wird nicht getrackt; vorhandene Produkt-Tests bleiben sichtbar.
- Command und Rollen sind nach der dokumentierten Neuladung tatsächlich
  aufrufbar. Vorher wird kein aktives Setup zugesichert.
- Linux, macOS und Windows werden nur entsprechend real durchgeführter
  Installationsprüfungen als unterstützt ausgewiesen.

## Quellen und Grenzen

Geprüft am 27.10.2026:

- [OpenCode V2: Skills, Quellen und HTTP-Kataloge](https://opencode.ai/v2/docs/skills/)
- [OpenCode V2: Commands und deren Registrierung](https://opencode.ai/v2/docs/commands/)
- [skills CLI: Installation, Archive und Updates](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)
- [skills CLI: unterstützte Agents](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)
- [skills.sh: Auffindbarkeit](https://skills.sh/docs)

Das sind dokumentierte Möglichkeiten der Werkzeuge, keine bereits
bestandenen Atlas-Laufzeittests. Dieser PR fügt ausschließlich den Entwurf
hinzu; er veröffentlicht kein Release, keinen Katalog und keinen Installer.
