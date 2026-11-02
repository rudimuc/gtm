# Aufgabe 3 (optional, für Schnelle)

Such dir **eine** Variante aus.

## A) Eigenes Tool: Räume finden
Baue einen **Tool-Workflow** (wie *Tool: Mitarbeiter suchen*), der `http://tools:5678/webhook/raeume` mit dem Parameter `plaetze` abfragt. Binde ihn an den Agenten an und lass ihn „den kleinsten freien Raum für 5 Personen“ nennen.

## B) Dein Workflow als Schnittstelle
Ersetze den Formular-Trigger aus Aufgabe 1 durch einen **Webhook**. Rufe ihn mit dem Browser oder `curl` auf und gib die Antwort als JSON zurück (*Respond to Webhook*).

## C) Der Agent schreibt die Antwort
Nutze in Aufgabe 1 statt der festen Antworttexte eine **Basic LLM Chain**, die je nach Dringlichkeit einen passenden Text formuliert.
