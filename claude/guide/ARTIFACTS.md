# Große Ausgaben und Artefakte

Nur lesen, wenn du große Logs, Testausgaben oder externe/MCP-Antworten tatsächlich verarbeitest.

- Halte vollständige Rohdaten außerhalb der Rückgabe. Nutze einen bestehenden Projektstandard oder eindeutige Pfade unter `work/agent-artifacts/<auftrag-id>/`.
- Führe erwartbar umfangreiche Befehle mit Ausgabe in eine Logdatei aus und werte gezielt Ausschnitte aus. Bewahre den tatsächlichen Exitcode; ein erfolgreicher nachfolgender Anzeige-Befehl ersetzt ihn nicht.
- Bei MCP nutze Filter, begrenzte Ergebnisse oder Paginierung, soweit verfügbar. Erhebe nur benötigte Daten. Ein nötiger großer Payload bleibt beim ausführenden Spezialisten; der Elternagent bekommt einen gezielten Befund.
- Bewahre entscheidende Fehlerzeilen, Gegenbelege und Unsicherheiten in der Zusammenfassung. Verdichtung darf einen fehlgeschlagenen Test nicht als Erfolg erscheinen lassen.
- Ein Ausführungsnachweis nennt Befehl bzw. Tool und relevante Argumente, Arbeitsverzeichnis, Exitcode bzw. Fehlerstatus, entscheidenden Auszug und Artefaktpfad. Behaupte nur tatsächlich durchgeführte Prüfungen.
- Unterscheide Produkt-, Umgebungs- und Infrastrukturprobleme anhand von Belegen. Melde unklare Ursachen als unklar. Wiederhole teure Läufe nur für eine konkrete offene Frage oder nach relevanten Änderungen.
- Speichere keine unnötigen Geheimnisse. Dateien, Datenbankzustände oder fremde Änderungen dürfen nicht allein zur Vereinfachung der Prüfung verändert werden.
