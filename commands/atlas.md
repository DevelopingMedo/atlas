---
description: 'Atlas verwalten: init, update [Release-Tag], models [Filter], config'
agent: Auto
subagent: false
---

Lade den Skill `atlas` aus der verwendeten Atlas-Installation und führe genau die angeforderte Aktion aus.
Das erste Wort ist die Aktion (`init`, `update`, `models` oder `config`); der restliche Text sind deren Argumente.
Ohne Aktion oder bei unbekannter Aktion zeige nur die verfügbaren Aufrufe. Starte kein implizites Setup oder Update.
Aufruf: /atlas $ARGUMENTS
