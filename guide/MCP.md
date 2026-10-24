# MCP: allgemeine Rollen- und Zugriffsregeln

Diese Regeln gelten plattformunabhängig für alle MCP-Integrationen. Sie sind
nicht an bestimmte Serverprodukte, Installationsarten oder Betriebssysteme
gebunden.

## Rollen

- `Auto` darf MCP-Tools und -Ressourcen direkt verwenden.
- `MCP` bearbeitet gezielte MCP-Aufträge im autorisierten Umfang.
- Alle anderen Rollen delegieren MCP-Aufträge an einen frischen `MCP`.
  Sie umgehen diese Trennung nicht über Shell oder eigene HTTP-Clients.
- Ein Prüfauftrag erlaubt keine Änderungen an externen Systemen.

## Verbindungen und Berechtigungen

Persönliche Verbindungen werden unter `mcp.servers` in der lokalen
OpenCode-Konfiguration eingerichtet. Endpunkte, Zugangsdaten, Programmpfade
und Installationsanweisungen für einzelne Rechner gehören nicht in die
allgemeinen Agent-Regeln dieses Repositorys.

Für jeden eingerichteten Server werden dessen normalisierte Tool-Aktionen
`<server>_*` standardmäßig gesperrt und für `Auto` und `MCP` freigegeben.
Dasselbe gilt für `opencode_list_mcp_resources` (Ressource: Servername) und
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

MCP-Aufträge sollen nur benötigte Daten erheben. Rückgaben nennen Ergebnis,
verwendete Tools, nicht geheime relevante Argumente, Prüfungen und offene
Punkte. Für große Antworten gilt `guide/ARTIFACTS.md`.
