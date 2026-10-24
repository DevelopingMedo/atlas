# Atlas: Wegweiser

- Im Hauptchat: Sage vor dem ersten Werkzeugaufruf kurz, was du vorhast. Nenne bei Delegation Rolle und Zweck; melde bei längerer Arbeit zwischendurch den Stand. Keine Statusmeldungen per `echo` oder Werkzeugausgabe.
- Facharbeit gehört zur passenden Rolle; innerhalb deiner Rolle arbeitest du selbst. `Auto` darf Aufgaben vollständig selbst planen, analysieren, umsetzen und prüfen; Delegation ist optional. Interne Wartungsagents bleiben bei ihrer Systemaufgabe.
- Jeder delegierte Auftrag startet frisch: kein übernommener Chatverlauf, keine fortgesetzte Child-Session; nur ein gezielter Arbeitsauftrag.
- Gib dem Parent relevante Zusatzfunde mit Beleg, Bedeutung und offenen Folgen weiter; insbesondere bei Analyse und Umsetzung.
- Lade Anleitungen ausschließlich beim unten genannten Anlass. Lies keine Sammlung aller Rollen oder Anleitungen auf Vorrat.

## Geheimnisse: verbindlich für alle Agents

- `.env` und `.env.*` niemals lesen, durchsuchen, ausgeben, kopieren oder committen — auch nicht über Shell, Skripte, Subagents oder andere Umwege. Keine Ausgabe von Umgebungsvariablen, Prozessumgebungen oder expandierten Auth-Headern; kein Shell-Tracing (`set -x`) bei der Verwendung von Secrets.
- `~/.config/opencode/.env` bleibt die einzige Quelle für den Langdock-Key. Ausschließlich Bash darf sie zum Laden der Umgebung sourcen (ohne Tracing/Ausgabe); Agents verwenden den Key nur als Umgebungsvariable `$LANGDOCK_API_KEY` zur Authentifizierung gegen `https://api.langdock.com`. OpenCode bezieht ihn über `env: ["LANGDOCK_API_KEY"]`, niemals als Klartext oder Dateisubstitution in der Konfiguration.
- Secrets niemals in Chat, Logs, Werkzeugrückgaben, Diffs oder Commits übernehmen. Diese Regel in jeden delegierten Auftrag aufnehmen. Die `read`-Permissions und -Policies ersetzen keinen Shell-Sandbox-Schutz.
- Den laufenden OpenCode-Dienst nicht aus seiner eigenen Agent-Sitzung neu starten. Neustarts führt der Nutzer in einer separaten Bash mit geladener Umgebung aus.

## Rollenwahl

`Orchestrate`: koordinieren · `Plan`: planen · `Analyze`: untersuchen · `Develop`: ändern · `Run`: ausführen/prüfen · `Review`: unabhängig begutachten · `MCP`: MCP-Aufträge ausführen · `Auto`: universell selbstständig arbeiten.

Nur `Auto` und `MCP` verwenden MCP-Tools und -Ressourcen direkt. Das gilt für alle MCP-Server unabhängig vom Betriebssystem. Alle anderen Rollen starten dafür einen frischen `MCP`; keine Umgehung über Shell oder eigene HTTP-Clients. Die Serververbindungen selbst bleiben in der persönlichen OpenCode-Konfiguration.

Starte die Rolle über ihren Agent-Namen. OpenCode lädt ihren eigenen Prompt aus `~/.config/opencode/agents/<AGENT-ID>.md`. Lies fremde Rollenprofile nicht vor dem Start ein.

## Bei Bedarf nachlesen

- Bevor du einen Subagent startest: `~/.config/opencode/SUBAGENTS.md`.
- Wenn du große Logs, Testausgaben oder MCP-Antworten verarbeitest: `~/.config/opencode/guide/ARTIFACTS.md`.
- Sonst genügt dein eigenes Rollenprofil samt auftragsrelevanten Projektregeln. Bereits gelesene, unveränderte Anleitungen im selben Kontext nicht erneut laden.
