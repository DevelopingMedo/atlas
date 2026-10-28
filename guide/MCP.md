# MCP: allgemeine Rollen- und Zugriffsregeln

Diese Regeln gelten plattformunabhängig für alle MCP-Integrationen, nicht
gebunden an bestimmte Serverprodukte, Installationsarten oder Betriebssysteme.

## Rollen

- Alle Rollen dürfen konfigurierte MCP-Tools und -Ressourcen direkt verwenden,
  einschließlich Subagents. Sie wählen den direkten Aufruf oder delegieren
  gezielt an eine Fachrolle wie `Run`, wenn das den Kontext oder die Ausführung
  sinnvoll abschirmt.
- `Run` kann zusätzlich lokale Befehle, Builds und Tests ausführen und große
  MCP-Antworten für den Auftraggeber verdichten.
- Ein Prüfauftrag erlaubt keine Änderungen an externen Systemen.

## Verbindungen und Berechtigungen

Persönliche Verbindungen werden unter `mcp.servers` in der lokalen
OpenCode-Konfiguration eingerichtet. Endpunkte, Zugangsdaten, Programmpfade
und Installationsanweisungen für einzelne Rechner gehören nicht in die
allgemeinen Agent-Regeln; die Rollenprofile nennen nur Prinzipien, keine
konkreten privaten Servernamen oder Endpunkte.

Für eingerichtete Server sind normalisierte MCP-Tool-Aktionen zunächst für alle
Rollen freigegeben. Explizite spätere `deny`-Regeln dienen als Blacklist; eine
notwendige serverweite Freigabe (`<server>_*`) bleibt auf diesen Server
beschränkt. Eine pauschale Freigabe aller Werkzeuge (`*`/`*`) für eine Rolle
ersetzt diese MCP-Freigabe nicht. Dasselbe Prinzip gilt für
`opencode_list_mcp_resources` (Ressource: Servername) und
`opencode_read_mcp_resource` (Ressource: `<server>:<uri>`). Bei einem neuen
Server müssen nur notwendige Blacklist-Regeln ergänzt werden; die Rollenregel
ist nicht auf bestimmte Serverprodukte beschränkt.

Berechtigungen steuern sichtbare Werkzeuge und zulässige Aufrufe. Sie beenden
nicht die gemeinsam genutzten MCP-Serverprozesse und sind keine
Betriebssystem-Sandbox für Shell- oder Netzwerkzugriffe.

Eine erfolgreiche MCP-Verbindung bestätigt Transport und Werkzeugkatalog,
nicht automatisch die Anmeldung oder Erreichbarkeit eines angebundenen Geräts
oder Dienstes. Diese Eigenschaften sind getrennt und mit möglichst kleinen,
lesenden Abfragen zu prüfen; Testwerte belegen keinen echten Zugang.

## Geheimnisse und Ergebnisse

Keine `.env`- oder `.env.*`-Dateien durch Agents lesen oder kopieren lassen.
Keine Zugangsdaten, Tokens, privaten Schlüssel, Auth-Header oder
Prozessumgebungen ausgeben oder versionieren. Die globalen Geheimnisregeln
gelten unverändert.

MCP-Aufträge sollen nur benötigte Daten erheben. Filtere Antworten möglichst
bereits vor dem Modellkontext, etwa durch Limit-, Feld- oder
Zeitraumparameter beim Aufruf selbst; lässt ein Tool keine solche Filterung
zu, ist diese Grenze in der Rückgabe zu benennen. Wähle dafür nach Möglichkeit
Parameter oder Feldauswahlen, die geheimhaltungsbedürftige Werte (Tokens,
Schlüssel, Passwort- oder Auth-Header-Felder) gar nicht erst in die Antwort
aufnehmen. Eine Entfernung erst in der eigenen Zusammenfassung an den Parent
ist die letzte Instanz, nicht die erste: Ein unvermeidbar in der Rohantwort
enthaltenes Geheimnis hat `Run` bereits in seinem eigenen Kontext gesehen und
muss in jedem Fall vor Weitergabe, Artefaktspeicherung oder Protokollierung
entfernt werden. Rückgaben nennen Ergebnis, verwendete Tools, nicht geheime
relevante Argumente, Prüfungen und offene Punkte. Für große Antworten gilt
`guide/ARTIFACTS.md`.
