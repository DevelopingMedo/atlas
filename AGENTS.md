# Atlas: Wegweiser

- Im Hauptchat: Vor dem ersten Werkzeugaufruf kurz das Vorhaben nennen, bei Delegation Rolle und Zweck, bei längerer Arbeit Zwischenstände. Keine Statusmeldungen per `echo` oder Werkzeugausgabe.
- Facharbeit gehört zur passenden Rolle; innerhalb deiner Rolle arbeitest du selbst. Interne Wartungsagents bleiben bei ihrer Systemaufgabe.
- Neue eigenständige Aufgaben starten in einer frischen Fachsession mit gezieltem Auftrag, ohne Gesamtchat. Zusammengehörige Folgefragen gehen möglichst an dieselbe Fachsession, aktualisiert nur bei erneutem fachlichem Bedarf, nicht laufend. Details zu Fortsetzung und Ersatzübergabe: `SUBAGENTS.md`.
- Gib dem Parent relevante Zusatzfunde mit Beleg, Bedeutung und offenen Folgen weiter; insbesondere bei Analyse und Umsetzung.
- Lade Anleitungen nur beim jeweils genannten Anlass, nicht als Sammlung auf Vorrat.

## Persönliches Setup

- Prüfe einmal zu Beginn einer Hauptsession den Eintrag `atlas-setup` in `atlas.json` der verwendeten Atlas-Installation: global neben dieser Anleitung, projektlokal in `.opencode/`. Eine projektlokale Atlas-Installation hat Vorrang vor der globalen. Lies zunächst höchstens 20 Zeilen; das Setup schreibt den Eintrag an den Dateianfang. Lade für diese Prüfung keine vollständige Konfiguration und starte dafür keinen Subagent.
- Nur der boolesche Wert `"atlas-setup": true` bestätigt die Einrichtung; dann entfällt die Setup-Empfehlung. Eine bloß vorhandene Datei oder der String `"true"` genügt nicht.
- Fehlt die Datei nachweislich oder ist der Eintrag `false` bzw. in einer vollständig gelesenen Datei nicht gesetzt, empfehle einmal knapp: „Mit `/atlas init` kannst du Atlas auf deine Modelle abstimmen. Ich empfehle dir, das Setup durchzuführen.“ Bearbeite den eigentlichen Auftrag direkt weiter. Bei unbekanntem Pfad, fehlendem Lesezugriff oder nicht eindeutig ermittelbarem Status keine fehlende Einrichtung behaupten und die Datei nicht vollständig auf Verdacht laden.
- Subagents und interne Wartungsagents wiederholen diese Prüfung und Empfehlung nicht. Bei einem bereits erteilten Setup-Auftrag entfällt die Empfehlung ebenfalls. Lade die übrigen persönlichen Einstellungen erst, wenn sie für den Auftrag benötigt werden. Vor einer Delegation gilt die Modellwahl aus `SUBAGENTS.md`; ein bestätigtes Setup ersetzt diese Prüfung nicht.

## Geheimnisse: verbindlich für alle Agents

- `.env` und `.env.*` niemals lesen, durchsuchen (auch nicht per `grep`), ausgeben, kopieren oder committen — auch nicht über Shell, Skripte, Subagents oder andere Umwege. Keine Ausgabe von Umgebungsvariablen, Prozessumgebungen, expandierten Auth-Headern oder ungefilterten MCP-Rückgaben; kein Shell-Tracing (`set -x`) bei der Verwendung von Secrets. Verboten ist die Offenlegung von Secret-Werten an den Agenten — nicht die Authentifizierung über Umgebungsvariablen als solche; die ist der vorgesehene Weg.
- Secrets niemals in Chat, Logs, Werkzeugrückgaben, Diffs oder Commits übernehmen. Diese Regel in jeden delegierten Auftrag aufnehmen. Die `read`- und `grep`-Permissions, Shell-`ask`-Regeln und gespeicherte Freigaben ersetzen keine Betriebssystem-Sandbox: Sie wirken zuverlässig nur, wenn das Werkzeug direkt auf einen `*.env`-Pfad zielt, nicht zwingend bei einem rekursiven `grep`/Shell-Zugriff über einen übergeordneten Pfad oder bei einer bereits gespeicherten „immer erlauben“-Freigabe für ein weites Muster. Diese Lücke ist durch Promptregeln adressiert, nicht durch zusätzliche Laufzeitisolation geschlossen.
- Den laufenden OpenCode-Dienst nicht aus seiner eigenen Agent-Sitzung neu starten. Neustarts führt der Nutzer in einer separaten Shell (Bash/Zsh bzw. PowerShell) mit geladener Umgebung aus.

## Bei Bedarf nachlesen

- Bevor du einen Subagent beauftragst oder fortsetzt: [`SUBAGENTS.md`](SUBAGENTS.md).
- Wenn du große Logs, Testausgaben oder MCP-Antworten verarbeitest: [`guide/ARTIFACTS.md`](guide/ARTIFACTS.md).
- Sonst genügt dein eigenes Rollenprofil samt auftragsrelevanten Projektregeln. Bereits gelesene, unveränderte Anleitungen im selben Kontext nicht erneut laden.

## Umgang mit Ideen und Aufträgen

Behandle meine Ideenfragen als Diskussionsangebote, nicht als Umsetzungsaufträge. Prüfe Vorschläge am Ziel und an denselben Kriterien wie bisher; unterscheide „möglich“ von „besser“. Ändere deine Empfehlung aufgrund neuer Informationen, besserer Argumente oder geänderter Prioritäten – nicht allein, weil ich eine Alternative vorschlage. Explizite Umsetzungsaufträge führst du aus, auch wenn du eine andere Lösung sinnvoller findest. Sachliche Bedenken kannst du anschließend knapp nennen, ohne den Auftrag dadurch zu ersetzen oder unnötig zu verzögern.

## Kommentare im Quellcode

- Setze Kenntnisse der verwendeten Sprache und gängiger Framework-
  Konventionen voraus, aber kein Wissen über projektspezifische Fachregeln
  und Entscheidungsgründe.
- Kommentare und Javadoc ergänzen relevante Information, die der Code
  nicht bereits verständlich ausdrückt: etwa Gründe, fachliche Regeln,
  nicht offensichtliche Verträge, Nebenwirkungen oder Einschränkungen.
  Erzähle keine Implementierung nach und erkläre keine Standardkonstrukte
  oder die übliche Wirkung von Framework-Annotationen.
- Keine Kommentar- oder Javadoc-Pflicht allein aufgrund der Existenz oder
  Sichtbarkeit einer Klasse oder Methode. Übernimm redundante Kommentare
  auch dann nicht als Muster, wenn sie im Bestand üblich sind.
- Bevor du schwer verständlichen Code kommentierst, prüfe, ob bessere
  Namen oder eine einfachere Struktur die Erklärung überflüssig machen.
- Ein Lernwunsch begründet keine zusätzlichen Kommentare im Produktcode.
  Lernhilfen gehören standardmäßig in den Chat; ausdrücklich gewünschte
  temporäre Lernkommentare dürfen nicht committed werden.
- Prüfe bei Umsetzung und Review die Kommentare im geänderten Code:
  Welche relevante Information würde beim Entfernen verloren gehen?
  Gibt es keine, entfällt der Kommentar. Erfinde keine Begründungen,
  um einen Kommentar zu rechtfertigen.

