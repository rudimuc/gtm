# Live-Demo (5 Minuten, Minute 5 bis 10)

> Für die **ausführliche Einführung (30 Min.)** siehe `einfuehrung-30min.md`. Diese Seite ist die Kurzfassung (5 Min.).

Instanz: eigene, z. B. `gtm1`. Vorher: Workflow *Aufgabe 1: Lösung* importieren oder `solutions/aufgabe-1-loesung.json` per Drag-and-drop einfügen.

| Zeit | Was du zeigst | Satz dazu |
|---|---|---|
| 0:00 | Leerer Canvas, **+** und Trigger wählen | „Ein Workflow beginnt mit einem Auslöser. Hier ein Formular.“ |
| 0:45 | Formular ausfüllen, Ausgabe zeigen, **Pin** | „Jeder Node zeigt Ein- und Ausgabe. Mit Pin merkt er sich die Daten.“ |
| 1:30 | **HTTP Request** an `http://tools:5678/webhook/mitarbeiter?abteilung=IT-Support` | „So spricht n8n mit jeder REST-Schnittstelle.“ |
| 2:30 | **IF** und zwei **Edit Fields**, `{{ $json.feld }}` zeigen | „Ausdrücke holen Werte aus früheren Nodes.“ |
| 3:30 | Aufgabe 2 öffnen, im Chat „Wer arbeitet im IT-Support?“ | „Ein Agent wählt die Werkzeuge selbst.“ |
| 4:15 | Ausführung öffnen: aufgerufenes Tool und Eingaben | „Hier siehst du, was der Agent getan hat.“ |
| 4:45 | Hilfekarte und Zugangsdaten zeigen | „Jetzt seid ihr dran: Aufgabe 1.“ |

**Vorbereitung am Tag davor:** Anmeldung prüfen, Chat-Frage einmal durchspielen, Tab mit `tools`-Instanz bereithalten.
**Plan B:** Läuft die Demo nicht, die Lösung aus `solutions/` zeigen und nur das Ergebnis erklären.
