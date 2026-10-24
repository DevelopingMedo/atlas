# Paket12: Eigenständige Review-Rolle

**Status: Entscheidung offen.** Dies ist nur eine Entscheidungsvorlage; keine
Rolle wird geändert oder entfernt, keine Berechtigung angepasst.

## Gemeinsames Zielbild

Orchestrate übernimmt Projektleitung, klärt Abnahmekriterien mit dem Menschen
und ordnet deren Nachweise zu. Plan unterstützt das Refinement. Develop
verantwortet Umsetzung und Entwicklungsprüfungen. Run führt lokale Prüfungen
sowie MCP-Aufträge aus; direkte MCP-Rechte anderer Rollen werden dadurch nicht
erweitert. Auto bleibt bestehen.
Build ist als beaufsichtigter Primary geplant, wird hier aber nicht eingeführt.

## Varianten und Zuständigkeiten

| Bereich | A: Eigenständigen Review entfernen | B: Begrenzte optionale Fehlersuche behalten |
|---|---|---|
| Abnahmekriterien | Orchestrate klärt und dokumentiert mit dem Menschen Soll und Nachweise; Plan unterstützt das Refinement. | Wie A; Review prüft nur ausdrücklich beauftragte Kriterien, setzt kein eigenes Soll. |
| Tests | Develop wählt/ergänzt Entwicklungsprüfungen; Run führt beauftragte Tests aus; Orchestrate bewertet die Kriterienabdeckung. | Wie A; Review kann konkrete Testlücken melden, übernimmt aber weder Testverantwortung noch Freigabe. |
| Regressionen | Develop verantwortet Schutz betroffener Bestandsfunktionen; Run liefert Prüfnachweise; Orchestrate macht verbleibende Risiken sichtbar. | Wie A; Review sucht zusätzlich unabhängig nach konkreten Fehlern im begrenzten Prüfbereich. |
| Menschliche fachliche Entscheidungen | Der Mensch entscheidet über fachliches Soll, Zielkonflikte, Restrisiken und Freigabe; Orchestrate legt offene Punkte vor. | Unverändert; Review berät, entscheidet und genehmigt nicht. |

**A – Konsequenzen:** Weniger Übergaben und keine zusätzliche Prüfinstanz;
unabhängige Fehlersuche entfällt als eigene Rolle. Kriterien- und Testlücken
werden damit nicht automatisch geschlossen, sondern bleiben bei den genannten
Verantwortlichen.

**B – Konsequenzen:** Ein zweiter Blick bleibt bei begründetem Risiko verfügbar,
kostet aber zusätzlichen Kontext und Zeit. Orchestrate beauftragt ihn nur mit
konkreter Frage, Prüfbereich und Zeit-/Rundenbudget; kein Pflichtdurchlauf.

## Befund- und Abschlussregeln für beide Varianten

- Ein Bug braucht ein Soll mit Quelle (z. B. freigegebenes Kriterium, dokumentierter
  Vertrag oder menschliche Entscheidung) und eine beobachtete Abweichung mit
  Beleg. Ohne belastbare Anforderung ist der Befund eine Hypothese bzw. Rückfrage,
  kein Reparaturauftrag. Keine automatische Reparatur; Develop ändert nur im
  autorisierten Umfang nach Klärung.
- Ein grüner Test belegt nur das geprüfte Verhalten, nicht die Richtigkeit des Solls.
- Eine weitere Prüfrunde braucht einen konkreten Befund oder eine relevante
  Änderung und bleibt darauf begrenzt. Nachweise und offene Risiken gehen an
  Orchestrate; keine endlose Verbesserungsschleife, kein Ersatz menschlicher Freigabe.

## Empfehlung und offene Entscheidung

**B empfohlen:** Begrenzte optionale Fehlersuche erhält unabhängige Fehlerfunde,
ohne eine generelle Freigabestufe oder Qualitätsgarantie vorzutäuschen. Das lohnt
sich bei riskanten Änderungen; bei einfachen Aufgaben darf sie entfallen.
Der Mensch entscheidet noch zwischen A und B. Eine spätere Umsetzung wäre ein
separater Auftrag; diese Vorlage ändert weder Rollen noch Rechte.
