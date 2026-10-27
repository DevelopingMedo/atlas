---
name: setup-atlas
description: Persönliche Modellpräferenzen für Atlas in atlas.json einrichten oder aktualisieren. Bei /setup-atlas oder einem ausdrücklichen Wunsch nach Einrichtung bzw. Änderung dieser Einstellungen verwenden.
---

# Atlas einrichten

Speichere die persönlichen Präferenzen in `atlas.json`. Das Setup bleibt optional und kann erneut ausgeführt werden. Die bloße Existenz der Datei unterdrückt die Setup-Empfehlung; verwende weder Statusflag noch Markerdatei.

## Ziel und vorhandene Einstellungen

1. Verwende die Atlas-Installation, aus der dieser Skill geladen wurde. Ihr Stamm liegt zwei Verzeichnisse über der Skill-Basis und enthält `atlas.json.example`, `agents/` und `commands/`. Global liegt sie normalerweise in `~/.config/opencode/`, projektlokal in `<projekt>/.opencode/`. Bei beiden Installationen gilt die projektlokale. Löse den Pfad aus der Skill-Basis auf, nicht aus einem angenommenen Shell-Arbeitsverzeichnis.
2. Lies die Vorlage [`atlas.json.example`](../../atlas.json.example). Ist daneben bereits `atlas.json` vorhanden, übernimm ihre Einstellungen als Vorauswahl. Lies zunächst höchstens 100 Zeilen. Ist die Datei größer, extrahiere mit einem lokalen JSON-Parser ausschließlich `models` und `selectionApproval`, ohne den übrigen Inhalt auszugeben. Erhalte unbekannte Felder bei einer Aktualisierung. Bei ungültigem JSON erkläre den konkreten Fehler und kläre die Korrektur, statt die Datei durch die Vorlage zu ersetzen.

## Modelle und Präferenzen

3. Ermittle die Modelle mit `opencode models` im betroffenen Projektverzeichnis. Nutze bei Bedarf `opencode models --help` für die installierte Version. Große Ausgaben lokal filtern und nur passende Kandidaten zurückgeben; den Katalog nicht in `atlas.json` speichern. Lies keine Zugangsdaten, `.env`-Dateien oder Prozessumgebungen. Eine gelistete Modell-ID bestätigt weder funktionierende Authentifizierung noch verfügbares Kontingent.
4. Kläre die Auswahl gesammelt in einem kompakten Dialog, soweit sie nicht bereits aus dem Auftrag feststeht:
   - `fast`: einfache, klar abgegrenzte Aufgaben.
   - `standard`: normale Aufgaben mit überschaubarer Unsicherheit.
   - `deep`: anspruchsvolle Aufgaben mit hoher Unsicherheit oder weitreichenden Folgen.
   - `selectionApproval`: `batch` für eine gemeinsame Bestätigung der vorgeschlagenen Modellzuordnung aller Arbeitspakete oder `automatic` für eine selbstständige Auswahl innerhalb der persönlichen Präferenzen. Dies ersetzt keine Werkzeug- oder Änderungsfreigaben.
5. Schlage nur tatsächlich gefundene Modell-IDs im Format `provider/model` vor; verwende `#variant` nur bei nachgewiesener Unterstützung. Begründe Vorschläge kurz und kennzeichne Unsicherheit über Eignung oder Kosten. Ordne die Stufen nach der konkreten Aufgabe zu, nicht pauschal nach Agent-Rolle. Dasselbe Modell darf mehreren Stufen zugeordnet werden. `null` bedeutet keine persönliche Vorgabe. Ist OpenCode nicht verfügbar oder liefert keine Modelle, biete die Einrichtung ohne Modellvorgaben an; erfinde keine IDs und installiere oder verbinde keine Provider automatisch.

## Speichern und Abschluss

6. Speichere nach der Auswahl gültiges JSON neben der Vorlage als `atlas.json`; bei einem Abbruch lege keine neue Datei an und erhalte eine vorhandene unverändert. Speichere nur Modellpräferenzen und die Auswahlregel, keine Secrets, Modellkataloge oder Gesprächsverläufe. Für eine bestehende Datei erhalte außerdem die unbekannten Felder aus Schritt 2.
7. Prüfe durch erneutes Parsen die gespeicherten Werte: `selectionApproval` ist `batch` oder `automatic`, `models` enthält `fast`, `standard` und `deep`, jeweils als Modell-ID oder `null`. Prüfe bei einer Git-Installation gezielt, dass `atlas.json` ignoriert und nicht bereits getrackt ist. Committe oder pushe persönliche Einstellungen niemals; falls die Datei bereits getrackt ist, melde das, ohne eigenständig den Git-Index zu ändern.
8. Nenne den Speicherort und die gewählten Präferenzen knapp. Erkläre, dass dies Atlas-Präferenzen sind: OpenCode liest `atlas.json` nicht als eigene Konfiguration. Dieses Setup richtet keinen automatischen Modellwechsel ein und verändert weder Agent-Profile noch `opencode.json`. Behaupte keinen angewendeten Modellwechsel. Der Command läuft in `Auto`; weise zum Abschluss kurz darauf hin, dass der Nutzer bei Bedarf wieder seine vorherige Rolle auswählen kann.
