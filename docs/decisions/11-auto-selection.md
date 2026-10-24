# Paket11: Auto bewusst auswählen?

**Status: offen – Entscheidungsvorlage, keine Umsetzungsentscheidung.**
Auto bleibt in beiden Varianten bestehen. Dieses Dokument ändert weder Rollen
noch Berechtigungen oder Delegationsregeln und führt keine Einschränkung ein.

## Ausgangspunkt und Optionen

Am Ausgangsstand `ba782a6fbc27f9d2eb19210ac9267c3175738ef5` ist Auto der
universelle Modus; alle Rollen sind delegierbar. Belege: `AGENTS.md`
(Rollenwahl), `SUBAGENTS.md` (Zuständigkeit), `README.md` (Global verwenden).
Zu entscheiden ist nicht Autos Fortbestand, sondern wer seinen Einsatz auswählt.

| Variante | Praktische Auswirkungen | Abwägung |
|---|---|---|
| **A – freie Delegierbarkeit beibehalten** | Ein Parent kann Auto im autorisierten Auftragsumfang ohne zusätzliche Auto-Freigabe wählen; direkte Nutzerauswahl bleibt möglich. | Weniger Rückfragen und flexible End-to-End-Bearbeitung; die bewusste Wahl einer spezialisierten Rolle kann für den Nutzer weniger vorhersehbar in einen universellen Modus übergehen. Autorisierung und Schutzregeln gelten dennoch unverändert. |
| **B – bewusste Auswahl verlangen** | Auto wird direkt vom Nutzer gewählt oder für den konkreten Auftrag ausdrücklich zur Delegation freigegeben. Fehlt diese Freigabe, bleiben passende Fachrollen oder eine Rückfrage. | Klarere Erwartung und nachvollziehbare Zustimmung zum universellen Modus; zusätzliche Rückfragen und möglicher Mehraufwand bei gemischten Aufgaben. Eine allgemeine Umsetzungserlaubnis wäre nicht automatisch eine Auto-Freigabe. |

## Empfehlung, nicht Beschluss

**B bevorzugen:** Die bewusste Auswahl passt besser zur transparenten Rollenwahl,
ohne Auto abzuschaffen. Eine ausdrückliche, auftragsbezogene Freigabe könnte
wiederholte Auswahlfragen innerhalb dieses Umfangs vermeiden; sie dürfte weder
Folgeaufträge pauschal erfassen noch zusätzliche Rechte verleihen. Vor einer
Umsetzung wären Geltungsdauer und Weitergabe der Freigabe eindeutig festzulegen.
Wenn minimale Rückfragen höher gewichtet werden, ist A die einfachere Alternative.
Bis zu einer gesonderten Entscheidung wird hier keine neue Auswahlregel gesetzt.

## Unabhängige Grenzen im Zielbild

- **Build** ist als künftiger zusätzlicher, beaufsichtigter Primary vorgesehen:
  vor **jedem Shell-Befehl** Nutzerbestätigung, auch bei Delegation. Das darf
  **niemals über Auto umgangen werden**, unabhängig von A oder B. Eine Auto-Auswahl
  oder Auftragsfreigabe ersetzt diese einzelne Bestätigung nicht.
- Die gesonderte Entscheidung zu **Review bleibt offen**; diese Vorlage legt
  weder dessen Rollenstatus noch Auswahl- oder Prüfpflichten fest.
- Die Auswahlfrage ersetzt keine Auftragsautorisierung und keine bestehenden
  Schutzregeln. Die Build-Grenze ist eine Zielvorgabe, kein hier behaupteter
  technischer Durchsetzungsnachweis.

## Späterer Integrationsabgleich

Nach Entscheidung Rollenwahl, Delegationsregeln und README auf konsistente
Beschreibung von A oder B abgleichen; Auto muss erhalten bleiben. Build-Bestätigung
einschließlich delegierter Shell-Befehle und Ausschluss einer Auto-Umgehung separat
nachweisen; Review nicht vorentscheiden. Diese Vorlage dokumentiert keine aktuellen
Laufzeit-, Berechtigungs- oder Build-Prüfungen.
