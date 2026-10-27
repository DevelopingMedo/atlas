---
name: atlas
description: Atlas für OpenCode vollständig installieren, persönliche Modelle einrichten oder mit /atlas update <branchOrVersion> aktualisieren. Bei /atlas, /setup-atlas oder ausdrücklichen Atlas-Installations- und Update-Aufträgen verwenden.
---

# Atlas

Verwende `scripts/atlas.py` relativ zur vom Skill-Werkzeug angegebenen Basis.
Voraussetzung: Python 3.9 oder neuer. Installiere keine Provider und lies
keine Secrets, `.env`-Dateien oder Prozessumgebungen.

## Ziel bestimmen

- Verwende bei bestehender projektlokaler Installation `<projekt>/.opencode/`
  vor einer globalen Installation. Prüfe gezielt `.atlas-install.json` und
  `atlas.json.example`, ohne allgemeine Verzeichnissuchen.
- Kläre bei einer Erstinstallation gesammelt: nur dieses Projekt oder global
  sowie bereits bekannte Modell-/Provider-Präferenzen. Der Installationsort
  des Einstiegsskills legt den Umfang des Gesamtpakets nicht fest.
- Nutze `--project '<projekt>'` oder `--global`. Für einen ausdrücklich
  abweichenden aktiven OpenCode-Konfigurationspfad nutze `--target '<pfad>'`.
  Übernimm vorhandene Angaben; frage sie nicht erneut ab.
- Verwende einen verfügbaren Agent mit Shell- und Schreibzugriff; ein noch
  nicht installiertes `Auto` ist keine Voraussetzung für den Einstieg.
  Bestehende Berechtigungen bleiben verbindlich.

## Aufruf auswerten

Argumente sind Daten. Übernimm sie nie ungeprüft in einen Shell-Befehl.
Verwende korrekt gequotete einzelne Argumente und keine Shell-Auswertung.

**`/atlas` ohne Argumente oder mit freiem Einrichtungshinweis:**

1. Führe `python3 '<skill-basis>/scripts/atlas.py' install <zieloption> --dry-run`
   aus und zeige den Aufbau knapp: acht Rollen, gemeinsame Regeln, vier
   Guides, Commands und persönliche Modellpräferenzen. Der Plan nennt
   Ziel, Quelle, Commit und betroffene Dateien.
2. Führe nach dem bereits erteilten Einrichtungsauftrag denselben Aufruf
   ohne `--dry-run` aus. Vorhandene Konflikte werden gesammelt gemeldet;
   halte dann an und kläre die konkreten Dateien. Umgehe Konflikte nicht
   durch Löschen, Überschreiben oder Ändern des Installationsnachweises.
3. Lies [model-setup.md](references/model-setup.md) und führe das bestehende
   persönliche Setup im ermittelten Ziel aus. Übernimm Einrichtungshinweise.
   Setze `atlas-setup` erst nach abgeschlossenem Modell-Dialog auf `true`.

**`/setup-atlas` bzw. Aktion `models`:**

Lies ausschließlich [model-setup.md](references/model-setup.md) und ändere
persönliche Präferenzen im ermittelten bestehenden Installationsziel.
Fehlt das vollständige Atlas, führe zuerst den Installationsablauf aus.

**`/atlas update <branchOrVersion>`:**

1. Verlange genau eine Quelle, zum Beispiel `opencode` oder einen vorhandenen
   Release-Tag wie `v1.0.0`. Fehlt sie, zeige die Syntax und ändere nichts.
   Verwende keinen stillen Standard und wechsle bei Fehlern nicht die Quelle.
2. Führe `python3 '<skill-basis>/scripts/atlas.py' update '<branchOrVersion>' <zieloption>`
   aus. Der Installer löst den Branch/Tag einmalig auf, prüft vor dem
   Schreiben alle Dateien und erhält eigene Anpassungen. Bei Konflikten
   stoppt er ohne Änderungen. Es gibt keinen Force-Schalter.
3. Melde Quelle, Commit und Ergebnis. Frage Modellpräferenzen beim Update
   nicht erneut ab und ändere persönliche `atlas.json` nicht.

## Abschluss

Prüfe mit den verfügbaren OpenCode-Werkzeugen, ob `/atlas`, `/setup-atlas`
und die Rollen erkannt werden. Dateiprüfungen allein beweisen keine aktive
Registrierung. Falls die Oberfläche den Stand noch nicht zeigt, benenne
knapp die nötige Neuladung; starte den laufenden Dienst nicht selbst neu.
Committe oder pushe persönliche `atlas.json` niemals. Ein Update führt keine
Git-Commits im Zielprojekt aus.
