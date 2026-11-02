# Einführung in n8n (30 Minuten inkl. Fragen)

**Ziel:** Nach diesen 30 Minuten kann jede Gruppe Aufgabe 1 anfangen, ohne zu raten. Alles, was dafür nicht nötig ist, kommt nicht vor.
Die Einführung wird **live in einer eigenen Instanz** gebaut (z. B. `gtm1` oder die Reserve), nicht per Folie. Fragen sind jederzeit erlaubt, ein Puffer ist eingeplant.

## Zeitplan

| Min. | Thema | Was du zeigst |
|---|---|---|
| 0 bis 3 | **Was ist ein Workflow?** | Ein Bild: **Auslöser (Trigger) -> Schritte (Nodes) -> Ergebnis**. n8n verbindet Systeme, ohne dass man alles programmiert. Eine Linie ist ein Datenfluss. |
| 3 bis 8 | **Die Oberfläche** | Canvas, `+` zum Hinzufügen von Nodes, Doppelklick öffnet einen Node (links Eingabe, Mitte Einstellungen, rechts Ausgabe). *Execute workflow*, *Executions* (Verlauf), Schalter *Publish*. **Test vs. Production** in einem Satz: Beim Testen siehst du die Daten, produktiv läuft der Workflow von selbst. |
| 8 bis 13 | **Trigger** | Neuen Workflow bauen mit **Formular-Trigger** (Felder Name, Dringlichkeit), Formular abschicken, Ausgabe lesen. Kurz erwähnen: Webhook (andere Systeme rufen an), Chat (kommt in Aufgabe 2), Zeitplan. **Pin** zeigen. |
| 13 bis 21 | **Datenfluss** (wichtigster Block) | Jeder Node bekommt **Items** (Zeilen mit JSON) und gibt Items weiter. **Expressions:** `{{ $json.Name }}` per Drag-and-drop aus der Eingabe in ein Feld ziehen. Einen **Edit Fields**-Node bauen. Dann das Problem zeigen: Nach einem HTTP Request ist `$json` die Antwort der API. Frühere Werte holt man mit `{{ $('Anfrage-Formular').item.json.Name }}`. Das ist die häufigste Stolperstelle in Aufgabe 1. |
| 21 bis 26 | **REST und Logik** | **HTTP Request** an `http://tools:5678/webhook/mitarbeiter?abteilung=IT-Support`: Methode GET, URL, Query-Parameter, Antwort als JSON. **IF** mit zwei Ausgängen, je ein Edit Fields, **Form Ending** (Completion Message = `{{ $json.antwort }}`). Alles in einer Linie durchspielen, mit *hoch* und mit *normal*. |
| 26 bis 30 | **Ausblick Agent und Fragen** | Aufgabe 2 öffnen (nicht bauen): AI Agent hat Anschlüsse unten (**Modell, Memory, Tools**, jeweils mit **Plus-Zeichen**). Eine Frage im Chat stellen, die Ausführung öffnen und zeigen, welches Tool der Agent mit welchen Eingaben aufruft. Hilfekarte zeigen. Zugangszettel verteilen. |

## Tipps für die Durchführung
- **Nicht zu schnell tippen.** Jeden Klick laut benennen. Bildschirm in großer Schrift, Browser-Zoom 125 bis 150 %.
- **Fehler absichtlich zeigen:** Einmal einen Feldnamen falsch schreiben (`$json.name` statt `Name`) und den roten Node lesen. Das spart später Fragen.
- **Fragen sammeln,** die nicht passen, auf einem Flipchart. Am Ende der Einführung abarbeiten.
- **Nicht zeigen:** Credentials anlegen (ist vorbereitet), Sub-Workflows im Detail, Code-Node, Community-Nodes.
- **Vorher spielen:** Alles einmal in der Instanz durchlaufen lassen. Die Lösung liegt in `solutions/aufgabe-1-loesung.json` und kann als Plan B per Drag-and-drop in den Canvas gezogen werden.

## Zeitplan des Workshops (75 Minuten): Achtung, es wird eng
Mit 30 Minuten Einführung bleiben nur 45 Minuten für die Aufgaben. Vorschlag:

| Min. | Block |
|---|---|
| 0 bis 5 | Ankommen, Zettel, Anmelden |
| 5 bis 35 | Einführung (diese Seite) |
| 35 bis 55 | Aufgabe 1 (Pflicht, 20 Min.) |
| 55 bis 70 | Aufgabe 2 (Agent, 15 Min.: Tools verbinden und testen, der Systemprompt ist Zusatz) |
| 70 bis 75 | Showcase: Ein bis zwei Gruppen zeigen ihr Ergebnis |

Wenn Aufgabe 1 in 20 Minuten für gemischte Teams zu knapp ist, ist die Einführung der Ort zum Kürzen, nicht die Aufgabe. Eine Möglichkeit:
Block "REST und Logik" (21 bis 26) auf 3 Minuten verkürzen und die Teilschritte in der Aufgabe führen lassen.
