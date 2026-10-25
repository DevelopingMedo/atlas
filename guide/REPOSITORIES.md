# Repository-Arbeit: Kopie, Original und Commits

Nur durch die tatsächlich ausführende Rolle lesen, wenn ein Git-Repository nachgewiesen ist und konkrete Änderungen, Commits oder eine Git-Arbeitskopie daran anstehen. Als Nachweis genügen bekannte Repository-Metadaten oder eine passende `.git`-Datei bzw. ein `.git`-Verzeichnis am Ziel oder im bekannten Projektstamm. Keine pauschale Dateisystemsuche zur Auslösung dieser Anleitung.

Orchestrate und andere delegierende Parents lesen diese Anleitung nicht für die Arbeit ihrer Subagents. Reine Analyse, einfache Datei-/Konfigurationsarbeit ohne Git, MCP-Abfragen und ein bloß möglicher Repository-Bezug sind kein Leseanlass.

## Arbeitsort

- Ändere das Original nur, wenn der Nutzerauftrag oder ein davon gedeckter delegierter Auftrag dies ausdrücklich erlaubt und das Ziel eindeutig ist. Eine reine Analyse, ein Prüfauftrag oder ein temporärer Umsetzungsversuch autorisiert keine Originaländerung.
- Fehlt diese Autorisierung, erstelle eine separate Kopie des Repos oder der benötigten Source unter einem eindeutigen Arbeitspfad. Das gilt insbesondere, wenn `Analyze` einen kurzen Auftrag an `Develop` gibt. Weise den Parent auf den Kopierpfad hin.
- Übernimm den für die Reproduktion relevanten aktuellen Quellstand, einschließlich notwendiger uncommitteter Änderungen. Ein Clone nur des letzten Commits reicht dafür nicht immer. Dokumentiere Ausgangs-Commit und Abweichungen.
- Halte Git-Metadaten der Kopie unabhängig. Übernimm keine `.git`-Datei, die auf das Original verweist. Prüfe vor Änderungen und Commits, welches Repository und welcher Arbeitsbaum tatsächlich betroffen sind. Nutze keine unnötigen Geheimnisse, Abhängigkeitssammlungen oder alten Artefakte als Kopierinhalt.

## Mit Commits arbeiten

- Dokumentiere inhaltliche Änderungen an Repository-Dateien durch kleine, nachvollziehbare Commits. Prüfe den Diff und committe nur die zum Auftrag gehörenden Dateien; keine pauschale Aufnahme fremder Änderungen, Geheimnisse oder generierter Logs.
- Eine Source-Kopie ohne Git bleibt ohne Git, solange das Anlegen eines Repositorys nicht ausdrücklich beauftragt ist. Keine automatische Git-Initialisierung zur Erfüllung dieser Anleitung. Bei einer Kopie eines vorhandenen Repositorys bewahre einen nachvollziehbaren Git-Ausgangsstand und erstelle für deine Änderungen eigene Commits. Bestehende Nutzeränderungen im Original bleiben unangetastet.
- Verwende eine vorhandene gültige Git-Identität. Erfinde keine Identität und ändere keine globalen Git-Einstellungen. Fehlt die Identität oder scheitert ein Hook, melde den konkreten Blocker; umgehe ihn nicht stillschweigend.
- Schreibe keine fremden Commits um. Push, Veröffentlichung und automatische Übernahme einer Kopie ins Original brauchen eine passende ausdrückliche Autorisierung. Die lokale Commit-Pflicht allein erlaubt das nicht.
- Wenn Tests, Implementierung und Git-Abschluss unterschiedliche Rollen benötigen, darf jede Rolle die passende andere Rolle beauftragen, mit Sessionwahl nach `SUBAGENTS.md`. Die Verantwortung für einen nachvollziehbaren Abschluss bleibt beim aufrufenden Agent.

## Rückgabe an den Parent

Nenne Original oder Kopie, Arbeits-/Repository-Pfad, Ausgangsstand, eigene Commit-IDs, durchgeführte Prüfungen und deren Ergebnisse. Fasse relevante Zusatzfunde mit Belegen, Auswirkungen und offenen Folgen ausreichend genau zusammen. Sage ausdrücklich, ob das Original unverändert blieb und welche Änderungen noch übernommen werden müssten. Behaupte keine Commits, die nicht erstellt wurden.
