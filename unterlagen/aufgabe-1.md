# Aufgabe 1: Anfrage bearbeiten (Pflicht, 30 Minuten)

**Ziel:** Ein Formular nimmt Anfragen an. Dein Workflow findet die passende Ansprechperson und antwortet je nach Dringlichkeit.

**Dein Start:** In deiner n8n-Instanz öffnest du den Workflow *Aufgabe 1: Anfrage bearbeiten (Start)*. Darin liegt schon der Formular-Trigger.

## Schritte

1. **Formular testen.** Doppelklick auf den Trigger, *Execute step*, Formular ausfüllen und abschicken.
   Tipp: Danach den Trigger **anpinnen** (Pin-Symbol), dann musst du nicht jedes Mal neu ausfüllen.
2. **HTTP Request** anhängen.
   - Methode `GET`, URL `http://tools:5678/webhook/mitarbeiter`
   - Query-Parameter `abteilung` mit dem Wert `{{ $json.Abteilung }}` (Abteilung aus dem Formular)
   - Ausführen: Du siehst Mitarbeitende dieser Abteilung.
3. **IF** anhängen: Ist die Dringlichkeit gleich `hoch`?
   Achtung: Nach dem HTTP Request ist `$json` die Antwort der API. Das Formular erreichst du mit `{{ $('Anfrage-Formular').item.json.Dringlichkeit }}`.
4. **Zwei Edit Fields** (einer pro Zweig). Jeder baut ein Feld `antwort`, z. B.
   - dringend: „Danke {{ $('Anfrage-Formular').item.json.Name }}, wir melden uns heute noch. Ansprechperson: {{ $json.mitarbeiter[0].name }}“
   - normal: „Danke, wir melden uns in den nächsten Tagen.“
5. **Form** (Operation *Form Ending*) an beide Zweige hängen.
   - *Completion Title*: `Anfrage eingegangen`
   - *Completion Message*: `{{ $json.antwort }}` (auf **Expression** umschalten)

## Fertig, wenn
Du das Formular mit *hoch* und mit *normal* abschickst und jedes Mal die passende Antwort siehst.

## Bonus (wenn du früh fertig bist)
Baue eine **Basic LLM Chain** ein, die die Nachricht in einem Satz zusammenfasst. Modell: **OpenRouter Chat Model**, Credential *OpenRouter (Workshop)*, Modell z. B. `openai/gpt-4o-mini`.

## Zum Nachdenken
Die Mitarbeiter-Daten kommen über eine **REST-Schnittstelle** (HTTP GET mit Parametern). Jedes Tool mit so einer Schnittstelle kannst du genauso anbinden.
