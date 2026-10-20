# n8n-Workshop in Dokploy

Ein Compose-Service in Dokploy, Quelle ist ein Git-Repo. Ohne Terminal-Schritte.

```
Browser -> Traefik (Dokploy, TLS) -> edge (nginx) -> gtm1..gtm9 / tools   (Netz "internal", ohne Internet)
n8n -> http://llm-gw:8080/gtmN/api/v1 -> (Key wird ergänzt) -> openrouter.ai
n8n -> http://tools:5678/...          -> Mock-API / MCP-Server
```

- 9 Gruppen-Instanzen (`gtm1.rudimuc.de` bis `gtm9.rudimuc.de`), je mit eigener SQLite, plus eine Tools-Instanz (`tools.rudimuc.de`).
- Die n8n-Container haben keinen Internetzugang. Raus geht nur das Gateway zu OpenRouter.
- Die echten OpenRouter-Keys liegen nur im Gateway. In n8n steht ein Platzhalter.
- Beim ersten Start jeder Instanz werden Credential und Workflows aus `seed/` importiert.
  Die Owner-Accounts legt der Container `bootstrap` automatisch an.

## Einrichtung

1. **Repo anlegen** (z. B. in Forgejo/GitHub, privat) und den Inhalt dieses Ordners committen
   (ohne `.env`). Dokploy braucht Lesezugriff (Deploy-Key oder Git-Provider).
2. **DNS:** `*.rudimuc.de` auf die VPS-IP (oder gtm1..gtm9 und tools einzeln).
   Existiert für `rudimuc.de` schon ein Wildcard-Eintrag auf einen anderen Server, brauchst du die zehn Einzeleinträge.
3. **Dokploy:** Project -> Create Service -> **Compose**
   - Provider: Git, Repo und Branch wählen, Compose Path `./docker-compose.yml`, Type: Docker Compose
   - Tab **Environment:** Inhalt von `.env.example` einfügen und ausfüllen
   - Tab **Advanced:** "Isolated Deployment" und "Randomize Compose" aus lassen. Sonst kann Dokploy
     den n8n-Containern ein zusätzliches Netz mit Internetzugang anhängen.
   - Keine Einträge im Tab "Domains" nötig: die Traefik-Labels stehen im Compose (Service `edge`).
4. **Deploy.** Im Log von `bootstrap` steht je Instanz die Antwort von n8n mit `[HTTP 200]`
   (Bei 400 steht der Grund im Text, z. B. Passwort zu schwach: mind. 8 Zeichen, Zahl, Großbuchstabe.)
5. **Zugang:** `gtmN@workshop.example` bzw. `tools@workshop.example` mit den `PW_*`-Werten.
   Die Werte kannst du als Zettel für die Gruppen ausdrucken.

## Prüfen (Dokploy -> Compose -> Terminal des jeweiligen Containers, oder Logs)
- In `gtm1`: `wget -T4 -qO- https://example.com` muss fehlschlagen (kein Internet).
- In `gtm1`: `wget -qO- http://llm-gw:8080/gtm1/api/v1/models | head -c 200` zeigt JSON von OpenRouter.
- In `gtm1`: `wget -qO- http://tools:5678/healthz` antwortet.
- Im Browser: unter gtm1.rudimuc.de erscheint n8n, und unter Credentials "OpenRouter (Workshop)".

## Workflows einspielen
- Starter-Workflows der Gruppen als JSON nach `seed/workflows/`, Workflows der Tools-Instanz nach `seed/tools/`.
- Der Import läuft nur beim ersten Start einer Instanz (Marker `.seeded` im Volume).
  Danach lieferst du Änderungen so nach: Repo aktualisieren, in Dokploy Redeploy, dann im
  Terminal der Instanz `n8n import:workflow --separate --input=/seed/workflows`.
- Vollständiger Neustart des Workshops: Compose-Service samt Volumes löschen und neu anlegen.
- In den Workflows: Chat-Model-Node mit dem Credential "OpenRouter (Workshop)", Credential-ID `or-workshop`.
  Modellnamen im OpenRouter-Format, z. B. `openai/gpt-4o-mini`.

## MCP in Aufgabe 2
Auf der Tools-Instanz einen Workflow mit **MCP Server Trigger** bauen (Pfad z. B. `workshop`).
Die Gruppen tragen im **MCP Client Tool** ein: `http://tools:5678/mcp/workshop`
(Transport je nach n8n-Version SSE oder HTTP Streamable).

## Arbeitsspeicher: 10 Instanzen auf 4 GB sind knapp
- Eine n8n-Instanz braucht im Leerlauf grob 250 MB, unter Last bis etwa 500 MB. Zehn Instanzen
  plus Dokploy, Traefik und die nginx-Container kommen im Leerlauf auf ungefähr 3 bis 3,5 GB.
  Das ist eine Schätzung, kein Messwert.
- Empfehlung: für den Workshop-Tag den VPS auf 8 GB hochstufen. Falls das nicht geht: 2 GB Swap,
  `MEM_LIMIT` bei 512m lassen und vorher mit mehreren Browser-Tabs pro Instanz testen.

## Bewusst nicht getestet (bitte beim ersten Deploy beachten)
- Der Endpunkt `/rest/owner/setup` ist intern in n8n. Falls er in deiner Version abweicht, steht
  im `bootstrap`-Log ein Fehlercode, und du legst den Owner einmal im Browser an.
- Der Start über `entrypoint` + `n8n import:credentials` vor dem ersten `n8n start` ist ein
  verbreitetes Muster. Prüfe in `gtm1`, ob das Credential da ist. Wenn nicht, zeigt das Log der Instanz warum.
- Der Credential-Typ ist `openRouterApi` (n8n 2.15.0, passt zum Node "OpenRouter Chat Model") mit der Gateway-URL.
- Alle zehn Hostnamen laufen über einen Traefik-Router und damit über ein Zertifikat.
  Es müssen also alle zehn DNS-Namen auflösen, sonst scheitert das Zertifikat insgesamt.
- Mehr als 9 Gruppen: einen Service `gtmN`, einen `PW_GTMN`, einen Key und einen Block im Gateway
  per Copy-and-paste ergänzen und `gtm[1-9]` in `edge/default.conf` sowie die Host-Liste anpassen.
