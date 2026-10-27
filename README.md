# Atlas

**Hier herunterladen:** [Neuestes Release](https://github.com/DevelopingMedo/atlas/releases/latest) · [atlas.zip](https://github.com/DevelopingMedo/atlas/releases/latest/download/atlas.zip)

## So startest du

Voraussetzung: **OpenCode V2**. Entpacke das ZIP nach `~/.config/opencode/`.

<details>
<summary><strong>macOS & Linux – Befehle anzeigen</strong></summary>

```sh
curl -fL https://github.com/DevelopingMedo/atlas/releases/latest/download/atlas.zip -o atlas.zip
mkdir -p "$HOME/.config/opencode"
unzip -n atlas.zip -d "$HOME/.config/opencode/"
```

</details>

<details>
<summary><strong>Windows (PowerShell) – Befehle anzeigen</strong></summary>

```powershell
Invoke-WebRequest -Uri "https://github.com/DevelopingMedo/atlas/releases/latest/download/atlas.zip" -OutFile "atlas.zip"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.config\opencode" | Out-Null
Expand-Archive -Path "atlas.zip" -DestinationPath "$env:USERPROFILE\.config\opencode"
```

</details>

Öffne danach eine neue OpenCode-Session und starte `/atlas init`.
Bestehende eigene Regeln in `AGENTS.md` mit den Atlas-Regeln zusammenführen.

## Usage: Atlas-Skill

| Befehl | Funktion |
|---|---|
| `/atlas init` | Modelle auswählen und persönliche Einstellungen speichern |
| `/atlas update [Release-Tag]` | Atlas auf das neueste oder ein bestimmtes Release aktualisieren |
| `/atlas models [Filter]` | Verfügbare Modelle anzeigen |
| `/atlas config` | Persönliche Konfiguration lesbar anzeigen |

Beispiele:

```text
/atlas init Bitte nur Modelle meines OpenAI-Providers vorschlagen
/atlas models openai
```

`/atlas` zeigt die Hilfe. Angaben in eckigen Klammern sind optional.
Updates erhalten deine `atlas.json` und lokale Anpassungen; danach eine neue Session öffnen.

## Was ist Atlas?

Atlas bietet Agent-Rollen für OpenCode, die Planung, Analyse, Umsetzung und Prüfung aufteilen.
**Orchestrate** koordiniert größere Aufgaben; **Auto** bearbeitet Aufträge direkt und eigenständig.
Die Rollen können in OpenCode ausgewählt werden.

## Lizenz

[Apache License 2.0 mit Commons Clause 1.0](LICENSE).
