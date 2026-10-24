# Subagents: nur vor einer Delegation lesen

## Zuständigkeit

- Delegiere fremde Zuständigkeiten an die passende Rolle. Erledige deine eigene Aufgabe selbst; starte keine Kopie deiner Rolle allein wegen ihrer Zuständigkeit.
- `Auto` ist der universelle Modus mit allen Werkzeugrechten. Er darf Aufgaben vollständig selbst bearbeiten; Spezialisten und Delegation sind optional. Die Regeln für Sessionwahl und gezielte Übergaben gelten, sobald er delegiert.
- MCP-Aufträge gehen unabhängig von Serverprodukt und Betriebssystem an `Run`. Nur `Auto` und `Run` dürfen MCP-Tools und -Ressourcen direkt nutzen; `Run` übernimmt sowohl lokale Ausführung als auch MCP-Abfragen und schirmt dabei die Ausführungsdetails von der delegierenden Rolle ab.
- Wähle die kleinste nötige Rollenfolge. Reine Analyse benötigt keine komplette Entwicklungsrunde. Unabhängige Gegenprüfungen sind gesonderte, begrenzte Aufträge.
- Die verfügbaren Agent-Namen und Kurzbeschreibungen genügen zur Auswahl. Lies nicht die Prompts aller Kandidaten und kopiere keine fremden Rollenprofile in den Auftrag.
- Jede Fachrolle darf jede andere passende Fachrolle beauftragen, einschließlich `Analyze` → `Develop` und `Run` → `Analyze`. Eigene Zuständigkeit, Sessionwahl und Autorisierung bleiben verbindlich. Ist eine Rolle durch zusätzliche Projektregeln nicht verfügbar, gib eine konkrete Delegationsanforderung an den Parent zurück.

## Neue Aufgabe oder Fortsetzung

- Starte eine neue eigenständige Aufgabe in einer frischen Child-Session mit der gewählten Fachrolle und einem gezielten Auftrag, ohne kopierten Gesamtchat. Ein Rollenwechsel im laufenden Chat ersetzt diese Delegation nicht.
- Setze für zusammengehörige Folgefragen möglichst dieselbe geeignete Fachsession über ihre tatsächlich verfügbare Session-/Fortsetzungs-ID fort. Aktualisiere sie erst bei erneutem fachlichem Bedarf; keine laufende Synchronisierung und keine Updates nach jeder Codeänderung. Innerhalb ihres Auftrags darf die Fachrolle mehrere Werkzeugaufrufe durchführen.
- Eine Fortsetzung enthält die konkrete Frage, neue Belege und relevante Änderungen seit dem letzten Einsatz, einschließlich geänderter Randbedingungen. Frühere Annahmen sind bei Gegenbelegen neu zu prüfen; bestehender Kontext ist kein Beweis für ihre Gültigkeit. Übernimm keinen Gesamtchat.
- Ist die Fachsession nicht verfügbar oder für die Frage ungeeignet, starte eine neue passende Session mit einer gezielten Ersatzübergabe: bisherige Ergebnisse und Referenzen, offene Frage, neue Belege und relevante Änderungen. Benenne den Kontextverlust ausdrücklich und erfinde keine Session-ID.
- Zum neuen Kontext gehören der eigene Rollenprompt, globale und notwendige Projektregeln sowie der Auftrag. Andere Rollenprompts, gesamte Chats, Logs oder MCP-Payloads gehören nicht hinein.

## Knappes Auftragspaket

Übergib ausschließlich:

1. Ziel und überprüfbares Abschlusskriterium.
2. Umfang und relevante Dateien/Quellen/Artefaktpfade.
3. Notwendige Entscheidungen und Einschränkungen, erlaubte Änderungen und Werkzeuge.
4. Gewünschte Rückgabe einschließlich relevanter Zusatzfunde.

Bei nötiger Neuaufteilung zunächst zum Auftraggeber zurückkehren. Die eigene Rolle bestimmt ihre nötigen Fachdetails; der Elternagent kopiert dafür keine Handbücher in den Auftrag.

## Sichtbarer Ablauf

- Wer den Hauptchat führt, kündigt einen Agent-Start kurz mit Rolle und Zweck an und meldet relevante Ergebnisse, Phasenwechsel und Blocker dort zurück. Bei längerer Arbeit gibt es kurze Zwischenstände; der Nutzer muss nicht in Child-Sessions nachsehen.
- Subagents geben wichtige Fortschritte über einen vorhandenen Rückkanal an den Parent. Ist keine laufende Rückmeldung möglich, liefern sie eine klare Abschlussrückgabe; der Parent stellt den Wartezustand ehrlich dar.
- Nutze Chat-Nachrichten statt `echo`, `printf`, Logdateien oder Werkzeugausgaben als Statusanzeige. Kopiere keine vollständigen Child-Protokolle in den Hauptchat.

## Zusammenarbeit und Ergebnis

- Parallelisiere nur unabhängige Arbeit. Weise Schreibaufträge eindeutig getrennten Bereichen zu. Frischer Kontext bedeutet kein getrenntes Dateisystem; fremde Änderungen bleiben erhalten.
- Delegation erweitert keine Nutzerautorisierung und umgeht keine Berechtigung. Insbesondere erlaubt ein Prüfauftrag keine Veröffentlichung oder Änderung an externen Systemen.
- Verlange eine knappe Rückgabe: Status (erledigt / teilweise / blockiert), Ergebnis, entscheidende Belege, Artefaktpfade, relevante Zusatzfunde und offene Unsicherheiten. Leere Punkte entfallen.
- Übernimm nur benötigte Ergebnisse. Bewahre Gegenbelege und Unsicherheiten. Lies keine vollständigen fremden Agent-Verläufe nach; beauftrage bei einer Lücke eine gezielte Untersuchung.
- Bei großen Ausgaben ist die separate Anleitung [`guide/ARTIFACTS.md`](guide/ARTIFACTS.md) zuständig. Der ausführende Spezialist liest sie bei Bedarf; kopiere sie nicht pauschal in seine Übergabe.

## Relevante Zusatzfunde an den Parent

Jeder Subagent berichtet dem unmittelbar aufrufenden Parent auch wichtige Erkenntnisse, die bei der Arbeit zusätzlich entstehen. Das gilt insbesondere für Analyse und Implementierung. Kontextsparsamkeit darf keine wichtige Information abschneiden.

- Berichte wesentliche Fehler, Risiken, unerwartete Zusammenhänge, Abhängigkeiten oder widersprechende Belege, wenn sie für Korrektheit, Sicherheit, Architektur, Betrieb oder nächste Entscheidungen wichtig sind. Sammle keine beiläufigen Stilideen.
- Erkläre den Befund ausreichend genau: Was wurde gefunden? Wo liegt der Beleg (Datei/Zeile, Quelle oder Artefakt)? Warum ist er wichtig? Was ist die konkrete Auswirkung? Was ist bestätigt, was vermutet? Was wurde schon behoben, was sollte folgen?
- Kennzeichne dies als **Relevante Zusatzfunde**. Gibt es keine, entfällt der Abschnitt. Priorisiere mehrere Funde nach ihrer Bedeutung. Ein entscheidender Zusammenhang darf mehr Platz bekommen als eine knappe Ein-Zeilen-Zusammenfassung.
- Der Parent berücksichtigt die Funde bei seiner Entscheidung und bewahrt wichtige Informationen in seiner weiteren Zusammenführung. Bei einer weiteren Delegation übergibt er nur die jeweils benötigten Erkenntnisse.
- Ein Zusatzfund erweitert keine Änderungsbefugnis. Melde nötige Folgearbeit und bleibe beim zugewiesenen Umfang. Bei einem akut blockierenden Fund informiere den Parent bereits vor dem Abschluss über den vorhandenen Rückkanal.

## Gezielte Nachanalyse

Meldet Develop **Nachanalyse erforderlich**, bekommt der unmittelbar aufrufende Parent die offene Frage, neue Belege, widerlegte Annahmen, bisherige Versuche und den gesicherten Arbeits-/Commitstand. Ist Orchestrate der Parent, setzt er möglichst die ursprüngliche Analyze-Session mit dieser gezielten Frage, den neuen Belegen und den relevanten Änderungen seit dem letzten Einsatz fort. Ist Analyze selbst der Parent von Develop, geht die Meldung direkt an diesen ursprünglichen Analysten zurück; er prüft die Gegenbelege und seine bisherigen Annahmen in seiner bestehenden Session neu, statt einen weiteren Analyze zu starten. Eine größere Neuplanung oder Umfangserweiterung geht an seinen Auftraggeber zurück. Ist die ursprüngliche Fachsession nicht verfügbar oder ungeeignet, gilt die gezielte Ersatzübergabe mit benanntem Kontextverlust. Nach der Klärung erhält möglichst dieselbe Develop-Session einen aktualisierten Auftrag; Änderungen und Commitstände bleiben erhalten. Zwischen diesen fachlichen Einsätzen ist keine Synchronisierung nötig.
