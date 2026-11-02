# Aufgabe 2: Ein Agent mit Tools (erwünscht, 25 Minuten)

**Ziel:** Ein **AI Agent** entscheidet selbst, welche Werkzeuge er benutzt. Alle Bausteine liegen schon da, du verbindest sie.

**Dein Start:** Workflow *Aufgabe 2: Agent (Start)*.

## Schritte

1. **Memory verbinden.** Am AI Agent beim Anschluss *Memory* auf das **Plus-Zeichen** klicken und *Window Buffer Memory* wählen (oder vom Plus-Zeichen zum vorhandenen Node ziehen).
2. **Tool verbinden.** Am Anschluss *Tool* auf das **Plus-Zeichen**, dann *Mitarbeiter suchen*. Er ruft den Workflow *Tool: Mitarbeiter suchen* auf.
3. **Testen.** *Open chat*, dann: *Wer arbeitet im IT-Support?*
4. **Zweites Tool.** Verbinde *Abteilungen auflisten* (ruft den Workflow *Tool: Abteilungen auflisten* auf). Der Agent kann nun die genauen Abteilungsnamen nachschlagen. Teste: *Wer arbeitet in der IT?* Schau in der Ausführung, in welcher Reihenfolge er die Tools aufruft.
5. **MCP-Tool verbinden.** Verbinde *MCP Client Tools-Server*. Der Agent kennt dann auch freie Räume und das Wetter.
   Frage: *Gibt es einen freien Raum für 8 Personen?*
6. **Systemprompt schreiben.** AI Agent öffnen, *Add Option*, *System Message*. Gib Rolle, Sprache und Regeln vor, z. B. „Du bist der freundliche Assistent der Firma. Antworte kurz auf Deutsch. Erfinde keine Personen.“

## Beobachte
Öffne nach einer Frage die Ausführung. Du siehst, **welches Tool** der Agent mit **welchen Eingaben** aufgerufen hat.

## Fertig, wenn
Der Agent diese drei Fragen richtig beantwortet:
- Wer arbeitet im IT-Support?
- Gibt es einen freien Raum für 8 Personen?
- Wie ist das Wetter in München?

## Fragen zum Ausprobieren
- Was passiert, wenn du nach jemandem fragst, den es nicht gibt?
- Wie ändert sich die Antwort mit einem anderen Systemprompt?
- Merkt sich der Agent die vorige Frage („Und wer ist dort der Leiter?“)?
