# Modellrouting: Verhaltensprüfung

Diese Fälle prüfen die Agent-Anweisungen und anschließend die native OpenCode-Integration. Textprüfung allein belegt keinen tatsächlichen Modellwechsel. Testläufe mit echten Modellen verursachen Kosten und sind bewusst auszuführen; keine automatische Live-Probe im Setup.

## Fixture

```json
{
  "atlas-setup": true,
  "models": {
    "fast": "langdock/gpt-6-luna",
    "standard": "langdock/gpt-6.1-sol",
    "deep": "langdock/gpt-6-astra"
  },
  "routing": {"mode": "automatic", "modelOverrideAuthorized": true}
}
```

Für einen echten Lauf die drei IDs durch verfügbare Modelle ersetzen und ihre Verwendung ausdrücklich autorisieren. Einen Parent auf Deep starten. Als Nachweis native Aufrufargumente und tatsächliche Session-Modellmetadaten erfassen; Selbstauskunft im Antworttext genügt nicht.

| Fall | Erwartung |
|---|---|
| Neue Hauptsession, nur Stacktrace erklären und Aufrufstelle nennen | Analyze mit Fast-ID im `model`-Argument, kein erneutes init |
| Anschließend Handler und Aufrufkette untersuchen | dieselbe abgeschlossene Analyze-Session per `sessionID`, Standard-ID ausdrücklich setzen |
| Schwierige Race Condition mit widersprüchlichen Belegen untersuchen | Deep mit fachlichem Grund |
| Danach einfache Folgefrage in derselben Session | passende günstigere ID ausdrücklich setzen; bestehende Session bleibt erhalten |
| Child delegiert git remote -v an Run | liest wirksame Konfiguration; Run mit Fast-ID; keine Übernahme der Parent-Stufe |
| Nur Stacktrace vorhanden, Ursache nicht eindeutig | Grenze benennen; keine Deep-Eskalation allein wegen fehlenden Codes |
| Alte Datei: setup true, models vorhanden, routing fehlt | fehlende Aktivierung melden; gespeicherte Modelle im init vorauswählen; keine automatische Delegation |
| Init mit drei gewählten IDs und ausdrücklicher Routing-Freigabe | automatic/true speichern und erneut parsen; kein kostenpflichtiger Teststart |
| Init: nur speichern | off/false; native Wahl bewusst ohne Atlas-Override |
| Native Schnittstelle ohne model | Blocker; kein Parameter erfinden und kein Aufruf ohne Override als Ersatz |
| Modell/Variante nicht verfügbar | Fehler sichtbar; kein stiller Fallback auf Parent oder anderes Tier |
| Automatik mit null, fehlendem Modell oder unbekanntem Routingmodus | Konfigurationsfehler; keine automatische Delegation |
| Projektlokale und globale Installation | lokale Regeln und lokale Konfiguration zusammen verwenden |
| Änderung durch init in derselben Session | Cache erneuern und neue ausdrücklich bestätigte IDs verwenden |
| Hauptsession/Auto bearbeitet selbst | kein automatischer Wechsel behauptet |
| Tool meldet nur sessionID/status/output | Modell als angefordert, nicht als unabhängig verifiziert ausweisen |

## Prüfschritte in OpenCode V2

1. Setup in einer isolierten Testinstallation durchführen, danach eine neue Session starten.
2. Die ersten fünf Fälle ausführen und native `subagent`-Argumente mit der Fixture vergleichen.
3. Die gespeicherte Modellreferenz jedes Childs prüfen, einschließlich vor und nach Fortsetzung. Stufenbezeichnung und tatsächlich aufgelöste Modellreferenz müssen übereinstimmen.
4. Negativfälle mit separaten Konfigurationskopien prüfen; kein unbeabsichtigter Child-Start darf stattfinden.
5. Ein Release-ZIP bauen und sicherstellen, dass `guide/MODEL_ROUTING.md` enthalten ist und `tests/` ausgeschlossen bleibt.

In der Entwicklungsumgebung ohne OpenCode können Szenarien mit einem unabhängigen Agenten auf konsistente Entscheidungen und Argumente geprüft werden. Das ersetzt die Schritte 1–4 nicht.
