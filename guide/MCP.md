# MCP: allgemeine Rollen- und Zugriffsregeln

Diese Regeln gelten plattformunabhängig für alle MCP-Integrationen. Sie sind
nicht an bestimmte Serverprodukte, Installationsarten oder Betriebssysteme
gebunden.

## Rollen

- `Auto` darf MCP-Tools und -Ressourcen direkt verwenden.
- `Run` übernimmt gezielte MCP-Aufträge im autorisierten Umfang, zusätzlich zu
  lokalen Befehlen, Builds und Tests. Diese Zusammenführung schirmt
  Ausführungsdetails von den Fachrollen ab: ein Fachagent beauftragt den
  Vorgang und erhält von `Run` einen knappen, belegten Status; `Run` merkt
  sich die tatsächliche Job-/Shell-ID und fragt bei einer Folgefrage denselben
  Vorgang erneut ab, statt ihn neu zu starten.
- Alle anderen Rollen delegieren MCP-Aufträge an `Run`, mit Sessionwahl nach
  `SUBAGENTS.md`. Sie umgehen diese Trennung nicht über Shell oder eigene
  HTTP-Clients.
- Ein Prüfauftrag erlaubt keine Änderungen an externen Systemen.

## Verbindungen und Berechtigungen

Persönliche Verbindungen werden unter `mcp.servers` in der lokalen
OpenCode-Konfiguration eingerichtet. Endpunkte, Zugangsdaten, Programmpfade
und Installationsanweisungen für einzelne Rechner gehören nicht in die
allgemeinen Agent-Regeln dieses Repositorys; die Rollenprofile selbst nennen
nur Prinzipien, keine konkreten privaten Servernamen oder Endpunkte.

Für jeden eingerichteten Server werden dessen normalisierte Tool-Aktionen
standardmäßig gesperrt und gezielt für `Auto` und `Run` freigegeben. Bevorzuge
dafür eine knappe Allowlist der tatsächlich benötigten Tool-Aktionen je
Server; wo eine serverweite Freigabe (`<server>_*`) nötig ist, bleibt sie auf
diesen Server beschränkt. Eine pauschale Freigabe aller Werkzeuge (`*`/`*`)
für eine Rolle ersetzt diese Allowlist nicht. Dasselbe Prinzip gilt für
`opencode_list_mcp_resources` (Ressource: Servername) und
`opencode_read_mcp_resource` (Ressource: `<server>:<uri>`). Bei einem neuen
Server sind diese Regeln und die Regressionstests entsprechend zu ergänzen;
die aktuell enthaltenen Servernamen sind keine Beschränkung der allgemeinen
Rollenregel auf bestimmte Produkte.

Berechtigungen steuern sichtbare Werkzeuge und zulässige Aufrufe. Sie beenden
nicht die gemeinsam genutzten MCP-Serverprozesse und sind keine
Betriebssystem-Sandbox für Shell oder Netzwerkzugriffe.

Eine erfolgreiche MCP-Verbindung bestätigt Transport und Werkzeugkatalog,
nicht automatisch die Anmeldung oder Erreichbarkeit eines angebundenen
Geräts oder Dienstes. Diese Eigenschaften sind getrennt und mit möglichst
kleinen, lesenden Abfragen zu prüfen. Testwerte belegen keinen echten Zugang.

## Geheimnisse und Ergebnisse

Keine `.env`- oder `.env.*`-Dateien durch Agents lesen oder kopieren lassen.
Keine Zugangsdaten, Tokens, privaten Schlüssel, Auth-Header oder
Prozessumgebungen ausgeben oder versionieren. Die globalen Geheimnisregeln
gelten unverändert.

MCP-Aufträge sollen nur benötigte Daten erheben. Filtere Antworten möglichst
bereits vor dem Modellkontext, etwa durch Limit-, Feld- oder
Zeitraumparameter beim Aufruf selbst; lässt ein Tool keine solche Filterung
zu, ist diese Grenze in der Rückgabe zu benennen. Rückgaben nennen Ergebnis,
verwendete Tools, nicht geheime relevante Argumente, Prüfungen und offene
Punkte. Für große Antworten gilt `guide/ARTIFACTS.md`.
