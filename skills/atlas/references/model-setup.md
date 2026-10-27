# Atlas einrichten

Speichere die persönlichen Präferenzen in `atlas.json`. Das Setup kann erneut ausgeführt werden. Setze nach abgeschlossener Einrichtung `"atlas-setup": true` als ersten Eintrag der Datei; die Vorlage enthält den booleschen Wert `false`. Verwende keine Strings für dieses Flag und keine zusätzliche Markerdatei.

## Einstieg und Einrichtungshinweise

Zeige bei einem Aufruf ohne Einrichtungshinweis zu Beginn einmal kurz:

> Du kannst die Modellauswahl auf einen Provider eingrenzen, zum Beispiel mit `/setup-atlas "Bitte nur Modelle meines OpenAI-Providers vorschlagen"`. Du kannst deinen Wunsch auch direkt im laufenden Setup nennen.

Fahre anschließend mit der Einrichtung fort. Für diesen Hinweis ist weder ein erneuter Aufruf noch eine Bestätigung erforderlich. Ist bereits ein Einrichtungshinweis angegeben, berücksichtige ihn direkt und wiederhole den allgemeinen Tipp nicht. Wende eine gewünschte Provider-Eingrenzung auf die Modellvorschläge an; ist der Provider unklar, kläre ihn im Auswahldialog.

## Ziel und vorhandene Einstellungen

1. Verwende das im Atlas-Einstieg ausdrücklich ermittelte Installationsziel. Es enthält `atlas.json.example`, `agents/` und `commands/`. Global liegt es normalerweise in `~/.config/opencode/`, projektlokal in `<projekt>/.opencode/`; eine projektlokale Installation hat Vorrang. Leite das Ziel nicht aus einem angenommenen Arbeitsverzeichnis oder der Position dieser Referenz ab.
2. Lies die Vorlage `atlas.json.example` am Installationsziel. Ist daneben bereits `atlas.json` vorhanden, übernimm ihre Einstellungen als Vorauswahl. Lies zunächst höchstens 100 Zeilen. Ist die Datei größer, extrahiere mit einem lokalen JSON-Parser ausschließlich `atlas-setup` und `models`, ohne den übrigen Inhalt auszugeben. Erhalte unbekannte Felder bei einer Aktualisierung. Bei ungültigem JSON erkläre den konkreten Fehler und kläre die Korrektur, statt die Datei durch die Vorlage zu ersetzen.

## Modelle und Präferenzen

3. Ermittle die Modelle mit `opencode models` im betroffenen Projektverzeichnis. Nutze bei Bedarf `opencode models --help` für die installierte Version. Große Ausgaben lokal filtern und nur passende Kandidaten zurückgeben; den Katalog nicht in `atlas.json` speichern. Lies keine Zugangsdaten, `.env`-Dateien oder Prozessumgebungen. Eine gelistete Modell-ID bestätigt weder funktionierende Authentifizierung noch verfügbares Kontingent.
4. Kläre die Auswahl gesammelt in einem kompakten Dialog, soweit sie nicht bereits aus dem Auftrag feststeht:
   - `fast`: einfache, klar abgegrenzte Aufgaben.
   - `standard`: normale Aufgaben mit überschaubarer Unsicherheit.
   - `deep`: anspruchsvolle Aufgaben mit hoher Unsicherheit oder weitreichenden Folgen.
5. Schlage nur tatsächlich gefundene Modell-IDs im Format `provider/model` vor; verwende `#variant` nur bei nachgewiesener Unterstützung. Begründe Vorschläge kurz und kennzeichne Unsicherheit über Eignung oder Kosten. Ordne die Stufen nach der konkreten Aufgabe zu, nicht pauschal nach Agent-Rolle. Dasselbe Modell darf mehreren Stufen zugeordnet werden. `null` bedeutet keine persönliche Vorgabe. Ist OpenCode nicht verfügbar oder liefert keine Modelle, biete die Einrichtung ohne Modellvorgaben an; erfinde keine IDs und installiere oder verbinde keine Provider automatisch.

## Speichern und Abschluss

6. Prüfe nach der Auswahl die vorgesehenen Werte gemäß Schritt 7. Speichere anschließend gültiges JSON neben der Vorlage als `atlas.json` mit `"atlas-setup": true` als erstem Eintrag; bei einem Abbruch lege keine neue Datei an und erhalte eine vorhandene unverändert. Speichere nur Setup-Status und Modellpräferenzen, keine Secrets, Modellkataloge oder Gesprächsverläufe. Für eine bestehende Datei erhalte außerdem die unbekannten Felder aus Schritt 2.
7. Prüfe vor dem Speichern die vorgesehenen Werte und danach die Datei durch erneutes Parsen: `atlas-setup` ist der boolesche Wert `true`, `models` enthält `fast`, `standard` und `deep`, jeweils als Modell-ID oder `null`. Prüfe bei einer Git-Installation gezielt, dass `atlas.json` ignoriert und nicht bereits getrackt ist. Committe oder pushe persönliche Einstellungen niemals; falls die Datei bereits getrackt ist, melde das, ohne eigenständig den Git-Index zu ändern.
8. Nenne den Speicherort und die gewählten Präferenzen knapp. Erkläre, dass dies Atlas-Präferenzen sind: OpenCode liest `atlas.json` nicht als eigene Konfiguration. Dieses Setup richtet keinen automatischen Modellwechsel ein und verändert weder Agent-Profile noch `opencode.json`. Behaupte keinen angewendeten Modellwechsel. Weise zum Abschluss knapp darauf hin, dass der Nutzer bei Bedarf wieder seine vorherige Rolle auswählen kann.
