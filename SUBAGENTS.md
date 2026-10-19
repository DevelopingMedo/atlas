# Subagents: nur vor einer Delegation lesen

## Zuständigkeit

- Delegiere fremde Zuständigkeiten an die passende Rolle. Erledige deine eigene Aufgabe selbst; starte keine Kopie deiner Rolle allein wegen ihrer Zuständigkeit.
- `Auto` ist der universelle Modus und nutzt alle in der Hauptsession freigegebenen Werkzeuge. Er darf Aufgaben vollständig selbst bearbeiten; Spezialisten und Delegation sind optional. Die Regeln für neue Child-Sessions und gezielte Übergaben gelten, sobald er delegiert.
- Wähle die kleinste nötige Rollenfolge. Reine Analyse benötigt keine komplette Entwicklungsrunde. Unabhängige Gegenprüfungen sind gesonderte, begrenzte Aufträge.
- Die verfügbaren Agent-Namen und Kurzbeschreibungen genügen zur Auswahl. Lies nicht die Prompts aller Kandidaten und kopiere keine fremden Rollenprofile in den Auftrag.
- Jede Fachrolle darf jede andere passende Fachrolle starten, einschließlich `Analyze` → `Develop` und `Run` → `Analyze`. Eigene Zuständigkeit, frischer Start, Autorisierung und Delegationsbudget bleiben verbindlich. Ist eine Rolle durch zusätzliche Projektregeln nicht verfügbar, gib eine konkrete Delegationsanforderung an den Parent zurück.

## Frischer Start

- Starte jeden delegierten Auftrag in einer neuen Child-Session mit der gewählten Rolle. Kein Resume, keine wiederverwendete Session und kein kopierter Gesprächsverlauf. Wenn das Spawn-Werkzeug fork_turns anbietet, setze es auf "none". Ein Rollenwechsel im laufenden Chat ersetzt das nicht.
- Auch ein Folgeauftrag bekommt eine neue Session mit einer knappen Übergabe. Innerhalb seines einzelnen Auftrags darf der Spezialist mehrere Werkzeugaufrufe durchführen.
- Zum neuen Kontext gehören der eigene Rollenprompt, globale und notwendige Projektregeln sowie der Auftrag. Andere Rollenprompts, gesamte Chats, Logs oder MCP-Payloads gehören nicht hinein.

## Knappes Auftragspaket

Übergib ausschließlich:

1. Ziel und überprüfbares Abschlusskriterium.
2. Umfang und relevante Dateien/Quellen/Artefaktpfade.
3. Notwendige Entscheidungen und Einschränkungen, erlaubte Änderungen und Werkzeuge.
4. Gewünschte Rückgabe einschließlich relevanter Zusatzfunde sowie bisherige Delegationskette und verbleibendes Budget.

Standard: höchstens drei Delegationskanten ab Einstieg; keine Rückdelegation an eine Rolle in der aktuellen Kette. Bei nötiger Neuaufteilung zunächst zum Auftraggeber zurückkehren. Die eigene Rolle bestimmt ihre nötigen Fachdetails; der Elternagent kopiert dafür keine Handbücher in den Auftrag.

## Sichtbarer Ablauf

- Wer den Hauptchat führt, kündigt einen Agent-Start kurz mit Rolle und Zweck an und meldet relevante Ergebnisse, Phasenwechsel und Blocker dort zurück. Bei längerer Arbeit gibt es kurze Zwischenstände; der Nutzer muss nicht in Child-Sessions nachsehen.
- Subagents geben wichtige Fortschritte über einen vorhandenen Rückkanal an den Parent. Ist keine laufende Rückmeldung möglich, liefern sie eine klare Abschlussrückgabe; der Parent stellt den Wartezustand ehrlich dar.
- Nutze Chat-Nachrichten statt `echo`, `printf`, Logdateien oder Werkzeugausgaben als Statusanzeige. Kopiere keine vollständigen Child-Protokolle in den Hauptchat.

## Zusammenarbeit und Ergebnis

- Parallelisiere nur unabhängige Arbeit. Weise Schreibaufträge eindeutig getrennten Bereichen zu. Frischer Kontext bedeutet kein getrenntes Dateisystem; fremde Änderungen bleiben erhalten.
- Delegation erweitert keine Nutzerautorisierung und umgeht keine Berechtigung. Insbesondere erlaubt ein Prüfauftrag keine Veröffentlichung oder Änderung an externen Systemen.
- Verlange eine knappe Rückgabe: Status (erledigt / teilweise / blockiert), Ergebnis, entscheidende Belege, Artefaktpfade, relevante Zusatzfunde und offene Unsicherheiten. Leere Punkte entfallen.
- Übernimm nur benötigte Ergebnisse. Bewahre Gegenbelege und Unsicherheiten. Lies keine vollständigen fremden Agent-Verläufe nach; beauftrage bei einer Lücke eine gezielte Untersuchung.
- Bei großen Ausgaben ist die separate Anleitung `~/.codex/guide/ARTIFACTS.md` zuständig. Der ausführende Spezialist liest sie bei Bedarf; kopiere sie nicht pauschal in seine Übergabe.

## Relevante Zusatzfunde an den Parent

Jeder Subagent berichtet dem unmittelbar aufrufenden Parent auch wichtige Erkenntnisse, die bei der Arbeit zusätzlich entstehen. Das gilt insbesondere für Analyse und Implementierung. Kontextsparsamkeit darf keine wichtige Information abschneiden.

- Berichte wesentliche Fehler, Risiken, unerwartete Zusammenhänge, Abhängigkeiten oder widersprechende Belege, wenn sie für Korrektheit, Sicherheit, Architektur, Betrieb oder nächste Entscheidungen wichtig sind. Sammle keine beiläufigen Stilideen.
- Erkläre den Befund ausreichend genau: Was wurde gefunden? Wo liegt der Beleg (Datei/Zeile, Quelle oder Artefakt)? Warum ist er wichtig? Was ist die konkrete Auswirkung? Was ist bestätigt, was vermutet? Was wurde schon behoben, was sollte folgen?
- Kennzeichne dies als **Relevante Zusatzfunde**. Gibt es keine, entfällt der Abschnitt. Priorisiere mehrere Funde nach ihrer Bedeutung. Ein entscheidender Zusammenhang darf mehr Platz bekommen als eine knappe Ein-Zeilen-Zusammenfassung.
- Der Parent berücksichtigt die Funde bei seiner Entscheidung und bewahrt wichtige Informationen in seiner weiteren Zusammenführung. Bei einer weiteren Delegation übergibt er nur die jeweils benötigten Erkenntnisse.
- Ein Zusatzfund erweitert keine Änderungsbefugnis. Melde nötige Folgearbeit und bleibe beim zugewiesenen Umfang. Bei einem akut blockierenden Fund informiere den Parent bereits vor dem Abschluss über den vorhandenen Rückkanal.

## Gezielte Nachanalyse

Meldet Develop **Nachanalyse erforderlich**, bekommt der Parent die offene Frage, neue Belege, widerlegte Annahmen, bisherige Versuche und den gesicherten Arbeits-/Commitstand. Orchestrate beauftragt einen frischen Analyze mit genau dieser Lücke und der bisherigen Analyse als Referenz. Die aktualisierte Umsetzung wird anschließend gezielt neu beauftragt.
