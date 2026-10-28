# Subagents: nur vor einer Delegation lesen

## Zuständigkeit

- Verfügbare Rollen: `Orchestrate` (koordinieren) · `Plan` (planen) · `Analyze` (untersuchen) · `Develop` (ändern) · `Run` (ausführen/prüfen inklusive MCP-Aufträge) · `Review` (unabhängig begutachten) · `Auto` (universell selbstständig arbeiten) · `Build` (eigenständiger Modus mit Pflichtbestätigung vor jedem Shell-Befehl). Starte die gewählte Rolle über ihren Agent-Namen; OpenCode lädt dafür ihren eigenen Prompt aus `agents/<AGENT-ID>.md`. Fremde Rollenprofile nicht vor dem Start einlesen.
- Delegiere fremde Zuständigkeiten an die passende Rolle. Erledige deine eigene Aufgabe selbst; starte keine Kopie deiner Rolle allein wegen ihrer Zuständigkeit.
- `Auto` ist der universelle Modus mit allen Werkzeugrechten. Er darf Aufgaben vollständig selbst bearbeiten; Spezialisten und Delegation sind optional. Die Regeln für Sessionwahl und gezielte Übergaben gelten, sobald er delegiert.
- MCP-Aufträge gehen unabhängig von Serverprodukt und Betriebssystem an `Run`. Nur `Auto` und `Run` dürfen MCP-Tools und -Ressourcen direkt nutzen; `Run` übernimmt sowohl lokale Ausführung als auch MCP-Abfragen und schirmt dabei die Ausführungsdetails von der delegierenden Rolle ab.
- Wähle die kleinste nötige Rollenfolge. Reine Analyse benötigt keine komplette Entwicklungsrunde. Unabhängige Gegenprüfungen sind gesonderte, begrenzte Aufträge.
- Die verfügbaren Agent-Namen und Kurzbeschreibungen genügen zur Auswahl. Lies nicht die Prompts aller Kandidaten und kopiere keine fremden Rollenprofile in den Auftrag.
- Jede Fachrolle darf jede andere passende Fachrolle beauftragen, einschließlich `Analyze` → `Develop` und `Run` → `Analyze`. Eigene Zuständigkeit, Sessionwahl und Autorisierung bleiben verbindlich. Ist eine Rolle durch zusätzliche Projektregeln nicht verfügbar, gib eine konkrete Delegationsanforderung an den Parent zurück.

## Modellwahl beim Delegieren

Diese Regeln richten sich an den Agenten, der einen Subagenten startet oder fortsetzt — unabhängig von seiner Rolle. Ein gestarteter Subagent bewertet sein eigenes Startmodell nicht erneut; erst wenn er selbst delegiert, wählt er das Modell für seinen nächsten Subagenten.

- Lies vor deiner ersten Delegation `models` und `routing.mode` aus der `atlas.json` der verwendeten Atlas-Installation: projektlokales `.opencode/` vor globalem `~/.config/opencode/`. Verwende bekannte Werte weiter und lies sie nach einer Einstellungsänderung neu.
- Bei `routing.mode: "automatic"` wähle unabhängig von der Fachrolle die kleinste ausreichende Stufe für den konkreten Auftrag:

| Stufe | Kriterium | Beispiele |
|---|---|---|
| `fast` | Klar begrenzte, direkt lösbare Aufgabe | Stacktrace erklären, Fundstelle suchen, vorgegebenen Test ausführen |
| `standard` | Mehrere zusammenhängende Schritte mit überschaubaren Wechselwirkungen | Aufrufkette untersuchen, normalen Bug beheben, begrenztes Feature implementieren |
| `deep` | Schwierige Ursachenabwägung oder weitreichende Entscheidung mit komplexen Folgen | Race Condition untersuchen, systemübergreifende Architektur planen |

- Fehlende Belege allein rechtfertigen kein teureres Modell. Erhöhe die Stufe nur bei zusätzlicher fachlicher Schwierigkeit.
- Bei `routing.mode: "automatic"` übergib die konkrete ID aus `models[Stufe]` im nativen `subagent.model`-Parameter; eine Empfehlung im Prompt genügt nicht. Setze sie auch beim Fortsetzen einer abgeschlossenen Fachsession über `sessionID` ausdrücklich, damit eine einfache Folgeaufgabe wieder günstiger laufen kann.
- `automatic` hält die im Setup erteilte Nutzerfreigabe für die drei gewählten Modelle fest. Bei `off` bleibt die native Modellwahl ohne Atlas-Override bestehen. Fehlt der Modus, melde die fehlende Einrichtung; nur die Hauptsession empfiehlt einmal `/atlas init`. Subagents geben den Blocker an ihren Parent zurück und wiederholen weder Setup-Prüfung noch Setup-Empfehlung. Ohne eingerichtetes Routing oder ausdrückliche Modellvorgabe keine Delegation starten.
- Bei ungültiger Konfiguration, fehlender Modell-ID, fehlendem `model`-Parameter oder einem Modellfehler im automatischen Modus: melde den Blocker, statt ohne Override oder mit einem anderen Modell weiterzumachen. Bezeichne ein Modell nur mit Laufzeitnachweis als tatsächlich verwendet, sonst als angefordert.

## Neue Aufgabe oder Fortsetzung

- Neue eigenständige Aufgabe: frische Child-Session mit gewählter Fachrolle und gezieltem Auftrag, ohne kopierten Gesamtchat. Ein Rollenwechsel im laufenden Chat ersetzt diese Delegation nicht. Innerhalb ihres Auftrags darf die Fachrolle mehrere Werkzeugaufrufe durchführen.
- Zusammengehörige Folgefragen: möglichst dieselbe Fachsession über ihre tatsächlich verfügbare Session-/Fortsetzungs-ID fortsetzen, aktualisiert erst bei erneutem fachlichem Bedarf, nicht laufend oder nach jeder Codeänderung. Die Fortsetzung nennt die konkrete Frage, neue Belege und relevante Änderungen seit dem letzten Einsatz, einschließlich geänderter Randbedingungen. Gegenbelege erfordern eine Neuprüfung früherer Annahmen; bestehender Kontext beweist ihre Gültigkeit nicht. Keinen Gesamtchat übernehmen.
- Ist die Fachsession nicht verfügbar oder für die Frage ungeeignet, starte eine neue passende Session mit gezielter Ersatzübergabe: bisherige Ergebnisse und Referenzen, offene Frage, neue Belege, relevante Änderungen. Kontextverlust ausdrücklich benennen, keine Session-ID erfinden.
- Zum neuen Kontext gehören nur der eigene Rollenprompt, globale und notwendige Projektregeln sowie der Auftrag — keine fremden Rollenprompts, Gesamtchats, Logs oder MCP-Payloads.

## Knappes Auftragspaket

Übergib ausschließlich:

1. Ziel und überprüfbares Abschlusskriterium.
2. Umfang und relevante Dateien/Quellen/Artefaktpfade.
3. Notwendige Entscheidungen und Einschränkungen, erlaubte Änderungen und Werkzeuge.
4. Gewünschte Rückgabe einschließlich relevanter Zusatzfunde.

Bei nötiger Neuaufteilung zunächst zum Auftraggeber zurückkehren. Die eigene Rolle bestimmt ihre nötigen Fachdetails; der Elternagent kopiert dafür keine Handbücher in den Auftrag.

## Sichtbarer Ablauf

- Wer den Hauptchat führt, kündigt einen Agent-Start kurz mit Rolle und Zweck an und meldet relevante Ergebnisse, Phasenwechsel und Blocker dort zurück. Bei längerer Arbeit kurze Zwischenstände; der Nutzer muss nicht in Child-Sessions nachsehen.
- Subagents geben wichtige Fortschritte über einen vorhandenen Rückkanal an den Parent, sonst eine klare Abschlussrückgabe; der Parent stellt den Wartezustand ehrlich dar.
- Chat-Nachrichten statt `echo`, `printf`, Logdateien oder Werkzeugausgaben als Statusanzeige. Keine vollständigen Child-Protokolle in den Hauptchat kopieren.

## Zusammenarbeit und Ergebnis

- Parallelisiere nur unabhängige Arbeit. Weise Schreibaufträge eindeutig getrennten Bereichen zu. Frischer Kontext bedeutet kein getrenntes Dateisystem; fremde Änderungen bleiben erhalten.
- Delegation erweitert keine Nutzerautorisierung und umgeht keine Berechtigung. Insbesondere erlaubt ein Prüfauftrag keine Veröffentlichung oder Änderung an externen Systemen.
- Verlange eine knappe Rückgabe: Status (erledigt / teilweise / blockiert), Ergebnis, entscheidende Belege, Artefaktpfade, relevante Zusatzfunde und offene Unsicherheiten. Leere Punkte entfallen.
- Übernimm nur benötigte Ergebnisse. Bewahre Gegenbelege und Unsicherheiten. Lies keine vollständigen fremden Agent-Verläufe nach; beauftrage bei einer Lücke eine gezielte Untersuchung.
- Bei großen Ausgaben ist die separate Anleitung [`guide/ARTIFACTS.md`](guide/ARTIFACTS.md) zuständig. Der ausführende Spezialist liest sie bei Bedarf; kopiere sie nicht pauschal in seine Übergabe.

## Relevante Zusatzfunde an den Parent

Jeder Subagent berichtet dem unmittelbar aufrufenden Parent auch wichtige Erkenntnisse, die bei der Arbeit zusätzlich entstehen, insbesondere bei Analyse und Implementierung. Kontextsparsamkeit darf keine wichtige Information abschneiden.

- Berichte wesentliche Fehler, Risiken, unerwartete Zusammenhänge, Abhängigkeiten oder widersprechende Belege, wenn sie für Korrektheit, Sicherheit, Architektur, Betrieb oder nächste Entscheidungen wichtig sind — keine beiläufigen Stilideen.
- Erkläre den Befund ausreichend genau: Was wurde gefunden, wo liegt der Beleg (Datei/Zeile, Quelle, Artefakt), warum ist er wichtig, was ist die Auswirkung, was ist bestätigt oder vermutet, was wurde schon behoben und was bleibt offen?
- Kennzeichne dies als **Relevante Zusatzfunde**; ohne Fund entfällt der Abschnitt. Priorisiere nach Bedeutung — ein entscheidender Zusammenhang darf mehr Platz bekommen als eine Ein-Zeilen-Zusammenfassung.
- Der Parent berücksichtigt die Funde bei seiner Entscheidung, bewahrt sie bei der Zusammenführung und gibt bei weiterer Delegation nur die jeweils benötigten Erkenntnisse weiter.
- Ein Zusatzfund erweitert keine Änderungsbefugnis: nötige Folgearbeit melden, zugewiesenen Umfang einhalten. Bei akut blockierendem Fund den Parent schon vor Abschluss über den vorhandenen Rückkanal informieren.

## Gezielte Nachanalyse

Meldet Develop **Nachanalyse erforderlich**, bekommt der unmittelbar aufrufende Parent die offene Frage, neue Belege, widerlegte Annahmen, bisherige Versuche und den gesicherten Arbeits-/Commitstand.

- Ist Orchestrate der Parent, setzt er möglichst die ursprüngliche Analyze-Session mit dieser Frage, den neuen Belegen und den relevanten Änderungen seit dem letzten Einsatz fort.
- Ist Analyze selbst der Parent von Develop, geht die Meldung direkt an diesen ursprünglichen Analysten zurück; er prüft Gegenbelege und bisherige Annahmen in seiner bestehenden Session neu, statt einen weiteren Analyze zu starten. Größere Neuplanung oder Umfangserweiterung geht an seinen eigenen Auftraggeber zurück.
- Ist die ursprüngliche Fachsession nicht verfügbar oder ungeeignet, gilt die gezielte Ersatzübergabe mit benanntem Kontextverlust.
- Nach der Klärung erhält möglichst dieselbe Develop-Session einen aktualisierten Auftrag; Änderungen und Commitstände bleiben erhalten. Zwischen den fachlichen Einsätzen ist keine Synchronisierung nötig.
