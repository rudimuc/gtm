# Betriebs-Anleitung für den Workshop-Tag

Alle Befehle laufen auf dem **VPS** (SSH) und nutzen `docker`. Container heißen unter Dokploy z. B.
`gesamttribemeeting-n8ngtm1-gslrhz-gtm3-1`. Dieser Helfer findet sie über das Ende des Namens.
Einmal in die Shell einfügen:

```bash
# n8n-Befehl in einer Instanz ausführen:   n8n_in gtm3 "n8n list:workflow"
n8n_in() { docker exec -u node "$(docker ps -qf name=-$1-1)" sh -c "$2" 2>&1 | grep -v 'license SDK'; }
# Container-Name einer Instanz:            cn gtm3
cn() { docker ps -aqf name=-$1-1; }
```
Alle Befehle kannst du auch im Dokploy-Terminal der Instanz ausführen, dann ohne `n8n_in`.

---

## 1. Vorher (Tag davor und am Morgen)

- **Nicht benötigte Instanzen stoppen** (spart RAM), z. B. bei 6 Gruppen `gtm7` bis `gtm9`:
  `docker stop $(cn gtm7) $(cn gtm8) $(cn gtm9)`
  Aufrufe dieser Adressen liefern dann `502`. Das ist gewollt. Ein Deploy in Dokploy startet sie wieder.
  Mindestens **eine freie Reserve-Instanz** laufen lassen (siehe 4.7).
- **RAM aufzeichnen** (Start vor dem Workshop, Ende danach):
  `nohup ./scripts/ram-tracking.sh 15 >/dev/null 2>&1 &`   (im Repo-Ordner auf dem VPS)
  Beenden mit `pkill -f ram-tracking.sh`. Ergebnis: `ram-container.csv` und `ram-host.csv`.
  Zwischendurch live: `docker stats --no-stream` und `free -m`.
- **Limit prüfen:** `docker inspect --format '{{.Name}} {{.HostConfig.Memory}}' $(docker ps -q) | grep gtm`
  Bei 750 MB steht `786432000`. Steht dort `536870912`, wurde nur neu gestartet, nicht neu deployt.
- **Durchlauf als Gruppe 1:** Anmelden, Aufgabe 1 und 2 einmal komplett spielen, Agent-Chat mit echtem Modell.
- **Zugangszettel drucken:** `./scripts/zugangsliste.sh > unterlagen/zugang-1.md` (nicht committen).

## 2. Schnelldiagnose (30 Sekunden)

```bash
docker ps --format 'table {{.Names}}\t{{.Status}}' | grep -E "gtm|tools|edge|llm-gw"   # laufen alle? "Restarting" = Absturz
docker logs --since 5m $(cn edge) 2>&1 | tail -20           # wer bekommt 502/4xx?
docker logs --since 5m $(cn llm-gw) 2>&1 | tail -20         # LLM-Aufrufe und Statuscodes
docker logs --since 5m $(cn gtm3) 2>&1 | tail -30           # n8n der betroffenen Gruppe
docker inspect --format '{{.State.OOMKilled}} {{.RestartCount}}' $(cn gtm3)   # true = RAM-Limit erreicht
```

## 3. Symptom, Ursache, Maßnahme

| Symptom | Wahrscheinliche Ursache | Maßnahme |
|---|---|---|
| Seite lädt nicht, `502` im `edge`-Log | Container gestoppt, startet noch oder OOM | `docker start $(cn gtmN)`, Log prüfen, 4.1 |
| Zertifikatswarnung / "TRAEFIK DEFAULT CERT" | DNS-Eintrag fehlt oder Router nicht geladen | Traefik-Log im Container `dokploy-traefik` |
| Login geht nicht, Passwort vergessen | Zettel verloren | 4.4 |
| "Execute" zeigt nichts / hängt, Seite zeigt `connection lost` | Netz blockiert den Live-Kanal (WebSocket), z. B. Firmen-VPN | Gerät ohne VPN / Hotspot nutzen |
| Chat-Modell liefert `402` | OpenRouter-Kreditlimit der Gruppe leer | In OpenRouter Limit erhöhen, Key in Dokploy-Env prüfen (4.8) |
| Chat-Modell `401` | Key ungültig oder falsch eingetragen | Key in OpenRouter prüfen, 4.8 |
| Chat-Modell `429` | Rate-Limit | Kurz warten, anderes Modell (4.9) |
| Agent: "Workflow is not active" | Sub-Workflow nicht veröffentlicht | `n8n_in gtmN "n8n publish:workflow --id=subMitarbeiter"`, danach Instanz neu starten |
| Agent kennt Tool nicht / Tool-Fehler | Tool am Agenten nicht über das **Plus-Zeichen** verbunden | Hilfekarte, Punkt 4 |
| Formular-/Webhook-URL gibt `404` | Workflow nicht aktiv (Production) oder Test-URL benutzt | Veröffentlichen (Schalter oben rechts) oder Testadresse nutzen |
| `404` auf `tools:5678/webhook/...` | Mock-Workflow fehlt/ist deaktiviert | 4.3 (Tools-Instanz) |
| Instanz träge | RAM/Swap knapp | `free -m`, `docker stats`, ungenutzte Instanzen stoppen |
| Team hat Workflow kaputtgebaut | | 4.2 (Aufgabe zurücksetzen) |

## 4. Rezepte

**4.1 Eine Instanz neu starten** (Daten bleiben): `docker restart $(cn gtm3)`

**4.2 Aufgabe einer Gruppe zurücksetzen** (Instanz läuft weiter, andere Workflows bleiben):
```bash
n8n_in gtm3 "n8n import:workflow --input=/seed/workflows/aufgabe-1-start.json"   # Aufgabe 1
n8n_in gtm3 "n8n import:workflow --input=/seed/workflows/aufgabe-2-start.json"   # Aufgabe 2
```
Das überschreibt den Workflow mit gleichem Namen auf den Startzustand (die Arbeit der Gruppe darin geht verloren).
Danach im Browser die Seite neu laden. Importiere **nie das ganze Verzeichnis** `/seed/workflows`, sonst werden die Tool-Workflows
deaktiviert und der Agent meldet "Workflow is not active".

**4.3 Tool-Workflows oder Mock-API wieder aktivieren**
- Gruppen-Instanz:
  `n8n_in gtm3 "n8n publish:workflow --id=subMitarbeiter; n8n publish:workflow --id=subAbteilungen"`, dann `docker restart $(cn gtm3)`.
- Tools-Instanz: `n8n_in tools "n8n list:workflow"` zeigt die IDs. Je ID: `n8n_in tools "n8n publish:workflow --id=<ID>"`, dann `docker restart $(cn tools)`.
- Mock-Workflow komplett neu einspielen: `n8n_in tools "n8n import:workflow --input=/seed/workflows/mock-mitarbeiter.json"`
  (analog `mock-raeume.json`, `mock-abteilungen.json`, `mcp-workshop.json`), danach publish und Neustart wie oben.

**4.4 Passwort vergessen / Anmeldung kaputt** (getestet mit n8n 2.45.7; Workflows bleiben erhalten):
```bash
n8n_in gtm3 "n8n user-management:reset"
docker restart $(cn gtm3)
# Warten, bis die Instanz läuft, dann Owner neu anlegen (Passwort wie auf dem Zettel):
n8n_in gtm3 "wget -qO- --header='Content-Type: application/json' --post-data='{\"email\":\"gtm3@workshop.example\",\"firstName\":\"Workshop\",\"lastName\":\"gtm3\",\"password\":\"DEIN_PASSWORT\"}' http://localhost:5678/rest/owner/setup"
```
Das Passwort braucht mindestens 8 Zeichen, eine Zahl und einen Großbuchstaben. Ein gültiges Ergebnis beginnt mit `{"data":`.

**4.5 Eine Instanz komplett neu aufsetzen** (löscht alles in dieser Instanz, auch die Konten):
```bash
docker rm -f $(cn gtm3)
docker volume rm $(docker volume ls -q | grep -- '-gtm3-data$')
```
Dann in Dokploy **Deploy** auslösen. Die fehlende Instanz wird neu angelegt und frisch geseedet, `bootstrap` legt den Owner an
(bei den anderen Instanzen meldet er `HTTP 400`, das ist normal). Ob Dokploy dabei die anderen Container in Ruhe lässt, hängt davon ab, ob sich
deren Konfiguration geändert hat. Ohne Änderung bleiben sie in der Regel unberührt, ich habe das nicht geprüft.

**4.6 Alles zurücksetzen** (nach dem Workshop oder bei Totalschaden): In Dokploy den Compose-Service stoppen,
die Volumes (`...-gtmN-data`, `...-tools-data`) löschen und neu deployen. Das ist der saubere Weg für den nächsten Durchlauf.

**4.7 Gruppe auf eine Reserve-Instanz umziehen:** Eine nicht belegte Instanz (z. B. `gtm9`) starten (`docker start $(cn gtm9)`),
der Gruppe deren Zettel geben und auf Wunsch den Workflow der alten Instanz exportieren
(`n8n_in gtm3 "n8n export:workflow --id=a1Start --output=/tmp/a1.json"`; Datei dann mit `docker cp` holen und in der neuen Instanz importieren).
Meist ist es schneller, die Gruppe die Aufgabe noch einmal beginnen zu lassen.

**4.8 OpenRouter-Key tauschen:** In Dokploy im Tab Environment `OPENROUTER_KEY_N` ändern und deployen.
Betroffen ist nur der Container `llm-gw`. Die Gruppen-Instanzen merken nichts, der Key steckt nur im Gateway.

**4.9 Modell wechseln:** Im Node *OpenRouter Chat Model* den Namen im Feld *Model* ändern, z. B. `openai/gpt-4o-mini`.

**4.10 Neue Inhalte aus dem Repo einspielen:** Repo in Dokploy ziehen (Deploy startet alle Container neu, Seeds werden **nicht** erneut importiert,
Marker `.seeded`). Neue/geänderte Workflows danach einzeln mit `import:workflow --input=...` (siehe 4.2) und bei Tool-Workflows mit `publish`
plus Neustart nachliefern.

## 5. Nach dem Workshop
- `pkill -f ram-tracking.sh`, `ram-container.csv` und `ram-host.csv` sichern. Die Spalte `prozent` zeigt die Auslastung des Container-Limits, `ram-host.csv` den Gesamt-RAM und den Swap.
- OpenRouter: Verbrauch je Key ansehen, Keys deaktivieren oder löschen.
- Ggf. Instanzen und Volumes entfernen (4.6).
