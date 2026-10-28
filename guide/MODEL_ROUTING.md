# Aufgabenbezogene Modellwahl

## Installation und Freigabe

Verwende dieselbe Atlas-Installation wie die geladenen Atlas-Regeln: projektlokales `.opencode/` vor globalem `~/.config/opencode/`. Mische niemals die Regeln einer Installation mit den Einstellungen einer anderen. Ist der Pfad unklar, kläre ihn vor einer kostenpflichtigen Delegation.

Lies `atlas-setup`, `routing` und `models` aus deren `atlas.json`, zunächst höchstens 100 Zeilen. Bei größeren Dateien lasse Run ausschließlich diese Felder extrahieren; starte Run dafür nur mit bereits ausdrücklich freigegebenem Modell, sonst melde den Blocker. Gib keine unbekannten Felder oder Secrets aus. Wiederverwende gelesene Werte innerhalb derselben Session; lade nach einer bekannten Konfigurationsänderung neu. Neue Haupt- und Child-Sessions lesen die Einstellungen erneut. Keine erneute Einrichtung pro Session; die kurze Setup-Statusprüfung aus `AGENTS.md` bleibt bestehen.

`routing.mode: "automatic"` zusammen mit `routing.modelOverrideAuthorized: true` hält die ausdrückliche Nutzerentscheidung aus `/atlas init` fest: Atlas darf für einzelne delegierte Aufgaben eines der drei vom Nutzer gewählten Modelle anfordern. Diese Freigabe gilt für neue Child-Sessions und deren Fortsetzungen, einschließlich verschachtelter Delegation. Übermittle den Konfigurationspfad und diese Freigabe knapp an Children; die Stufe des Parents ist keine Vorgabe für deren nächste Aufgabe.

`atlas-setup: true` allein ist keine solche Freigabe. Bei einer alten Konfiguration ohne `routing` melde einmal, dass die Modellwahl noch nicht aktiviert ist und `/atlas init` die vorhandenen Modelle übernimmt und die Freigabe ergänzt. Starte bis dahin keine automatische modellabhängige Delegation; eine ausdrückliche Modellvorgabe im aktuellen Nutzerauftrag bleibt möglich. Bei `routing.mode: "off"` gilt bewusst die native OpenCode-Modellwahl ohne Atlas-Override. Unbekannte Modi und widersprüchliche Werte sind Fehler, kein stiller Rückfall auf `off`.

## Drei Stufen

Wähle die kleinste für den konkreten Auftrag ausreichende Stufe. Beurteile nötige Schlussfolgerungen, Unsicherheit und Folgen; weder Rollenname, Textlänge noch Dateianzahl entscheiden allein.

| Stufe | Wann | Beispiele |
|---|---|---|
| `fast` | Klarer, begrenzter Auftrag; Belege lassen sich direkt lesen oder das Ergebnis einfach prüfen | Stacktrace erklären und relevante Aufrufstelle nennen; Symbol suchen; vorgegebenen Test ausführen und Ergebnis zusammenfassen |
| `standard` | Mehrere zusammenhängende Schritte, begrenzte Ursachenabwägung oder Implementierung mit überschaubaren Wechselwirkungen | Handler und Aufrufkette untersuchen; gewöhnlichen Bug beheben und testen; abgegrenztes Feature oder Review |
| `deep` | Schwierige widersprüchliche Belege, komplexe Wechselwirkungen oder weitreichende Entscheidungen | Sporadischen Race-Condition-Fehler untersuchen; systemübergreifende Architektur oder riskante Datenmigration entwerfen |

Ein bekannter Fehlercode mit Stacktrace ist zunächst `fast`, wenn nur Erklärung und Fundstelle gefragt sind. Fehlt der Code für eine sichere Ursachenaussage, benenne diese Grenze. Ein teureres Modell ersetzt fehlende Belege nicht. Wird anschließend eine Untersuchung des Handlers beauftragt, kann diese Aufgabe `standard` sein.

Wähle bei gewöhnlicher mehrschrittiger Arbeit `standard`, wenn `fast` erkennbar nicht genügt. Nutze `deep` nur mit konkretem fachlichem Grund, nicht pauschal für Plan oder Analyze. Ein großer Auftrag kann kleine Fast-Aufgaben und eine Deep-Entscheidung enthalten.

Bei unzureichendem Ergebnis bestimme zuerst, ob Informationen, Werkzeuge oder Modellfähigkeit fehlen. Nur im letzten Fall erhöhe gezielt die Stufe und übergib bisherige Belege und die offene Frage. Keine automatische Eskalationsschleife. Ein Follow-up darf wieder günstiger sein.

## Native Ausführung

Diese Schritte gelten im automatischen Modus. Bei ausdrücklich gewähltem `off` bleibt das native Verhalten ohne Atlas-Override erlaubt. Beachte zusätzliche Anforderungen des tatsächlich angebotenen Werkzeugschemas, insbesondere eine dort verlangte Modellkatalog-Abfrage. Nutze dafür das angebotene Modellwerkzeug; fehlen erforderliche Möglichkeiten, melde den Blocker.

1. Prüfe, dass das angebotene native `subagent`-Werkzeug `model` unterstützt. Erfinde keine Parameter und ersetze fehlende Unterstützung nicht durch Shell-Starts, API-Aufrufe oder neue Rollen mit mehr Rechten.
2. Löse die gewählte Stufe über `models[Stufe]` auf. Im automatischen Modus müssen alle drei Einträge konkrete, beim Setup nachgewiesene IDs sein. `null`, fehlende Werte und ungültige IDs blockieren automatisches Routing. Verwende keine geratenen Modellnamen.
3. Übergib die exakte ID als `model`, optional einschließlich einer beim Setup verifizierten `#variant`. Beispiel bei entsprechender Nutzerkonfiguration:

```json
{
  "agent": "Analyze",
  "description": "Stacktrace und Aufrufstelle erklären",
  "prompt": "Erkläre den beigefügten Stacktrace und nenne die relevante Aufrufstelle. Trenne belegte Aussagen von Hypothesen. Lies keine Secrets oder .env/.env.* und gib keine Secrets in Chat oder Werkzeugrückgaben aus. Atlas-Konfiguration: [verifizierter absoluter Pfad zur atlas.json]; automatische Auswahl der dort gewählten Modelle wurde vom Nutzer ausdrücklich freigegeben. [Hier vollständigen Stacktrace einsetzen.]",
  "model": "langdock/gpt-6-luna"
}
```

4. Bei einem zusammengehörigen Follow-up innerhalb derselben Fachrolle ergänze die tatsächlich zurückgegebene `sessionID` und setze `model` erneut ausdrücklich. So bleibt eine zuvor gewählte Deep-Stufe nicht versehentlich an einer einfachen Folgeaufgabe hängen. Setze erst nach Abschluss des vorherigen Aufrufs fort; ändere keinen laufenden Child-Aufruf parallel.
5. Meldet OpenCode ein nicht verfügbares Modell, eine nicht verfügbare Variante oder einen anderen Fehler, melde ihn. Wiederhole nicht ohne `model` und wähle kein anderes Modell als stillen Ersatz.

Die native Auswahl lautet bei einem neuen Child: explizites `model`, sonst Agent-Profil, sonst Parent-Modell. Ein explizites `model` wechselt auch das Modell einer fortgesetzten Child-Session. Deshalb genügt ein Prompt wie „verwende standard“ nicht.

Die Hauptsession behält ihr ausgewähltes Modell. Atlas routet delegierte Arbeit; Auto/Build wechseln bei eigener Bearbeitung nicht automatisch das Modell. Ein direkt angesprochener Fachagent wechselt ebenfalls nicht rückwirkend. Weise auf diese Grenze beim Setup hin, statt den Wechsel der gesamten Unterhaltung zu behaupten.

## Nachweis und Kommunikation

Halte mit der Session-ID auch Stufe, angeforderte Modell-ID und den knappen fachlichen Grund fest. Unterscheide angefordert und tatsächlich gemeldet: Die native Tool-Rückgabe enthält nicht zwingend das effektive Modell. Behaupte es nur bei belastbaren Laufzeitmetadaten; Selbstauskunft des Modells ist kein unabhängiger Nachweis. Normale Starts brauchen keine zusätzlichen Verwaltungstabellen im Chat. Nenne Abweichungen und Blocker, auf Nachfrage auch die Auswahl.

Dies ist eine verbindliche Agent-Anweisung, keine technische Sperre gegen fehlerhafte Werkzeugaufrufe. OpenCode wendet einen übergebenen Override technisch an; Atlas selbst interceptiert keine Aufrufe. Eine harte Kostenbegrenzung benötigt zusätzlich eine Laufzeit-/Provider-Policy.

## Technische Grundlage

Geprüft am 28.10.2026: [OpenCode V2 Agents](https://dev.opencode.ai/v2/docs/agents/) und [native Subagent-Implementierung](https://github.com/anomalyco/opencode/blob/950111ff2ad0a324db7950f172c84760bc962469/packages/core/src/tool/plugin/subagent.ts). Das native Schema verlangt ausdrückliche Nutzerwahl für `model`; diese wird im Setup eingeholt, nicht aus bloß vorhandenen Präferenzen abgeleitet. Maßgeblich bleibt das tatsächlich angebotene Werkzeugschema der installierten Version.
