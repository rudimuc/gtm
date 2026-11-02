# Hilfekarte: die fünf häufigsten Stolperstellen

**1. Ausdrücke (Expressions)**
Werte aus dem vorigen Node holst du mit `{{ $json.feld }}` oder, für frühere Nodes, `{{ $('Node-Name').item.json.feld }}`. Das Feld muss genau so heißen wie in der Ausgabe (auch Groß- und Kleinschreibung: `Name` ist nicht `name`). Am einfachsten: das Feld aus dem Eingabe-Panel links in das Eingabefeld ziehen.

**2. Pinning**
Drück auf das Pin-Symbol in der Ausgabe eines Nodes, dann bleiben seine Testdaten erhalten. Du musst das Formular nicht neu ausfüllen. Pins entfernen: noch einmal drücken.

**3. Credential auswählen**
Bei Chat-Modellen im Node *Credential to connect with* **OpenRouter (Workshop)** auswählen. Einen eigenen API-Schlüssel brauchst du nicht. Modellnamen im Format `openai/gpt-4o-mini`.

**4. Nodes verbinden**
Ein Node ohne Linie zum nächsten läuft nicht mit. Am Agenten hängen Memory, Tools und Modell an den **Kreisen unten**, nicht an den Pfeilen rechts.

**5. Test oder Produktion**
*Execute workflow* ist ein Test mit Ansicht der Daten. Die **Production-URL** eines Formulars oder Webhooks funktioniert nur, wenn der Workflow **aktiv** ist (Schalter oben rechts, *Publish*). Test-URL und Production-URL sind verschieden.

---
**Hilft alles nichts?**
- Oben rechts *Executions*: Dort steht jede Ausführung mit Fehlermeldung am roten Node.
- Rote Fehlermeldung vorlesen. Meistens steht der Grund im ersten Satz.
- Frag dein Team, dann Rudi.

**Adressen im Workshop**
- Mitarbeiter-API: `http://tools:5678/webhook/mitarbeiter` (Parameter `name`, `abteilung`)
- Räume-API: `http://tools:5678/webhook/raeume` (Parameter `plaetze`)
- MCP-Server: `http://tools:5678/mcp/workshop`
