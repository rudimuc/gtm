#!/usr/bin/env bash
# Löscht alle Ausführungen (Executions) einer oder mehrerer n8n-Instanzen. Auf dem VPS ausführen.
#   ./scripts/executions-loeschen.sh gtm3            # eine Instanz
#   ./scripts/executions-loeschen.sh gtm1 gtm2 tools # mehrere
#   ./scripts/executions-loeschen.sh alle            # gtm1..gtm9 und tools (läuft nur für laufende Container)
# Benötigt die Passwörter (PW_GTM1..9, PW_TOOLS): aus der Umgebung oder aus ./.env im Repo-Ordner.
# Die Workflows, Credentials und Konten bleiben erhalten. Nur die Ausführungsverläufe werden gelöscht.
set -u
cd "$(dirname "$0")/.."
[ $# -ge 1 ] || { sed -n '2,7p' "$0"; exit 1; }
[ "$1" = alle ] && set -- gtm1 gtm2 gtm3 gtm4 gtm5 gtm6 gtm7 gtm8 gtm9 tools
getpw() { local v="PW_$(echo "$1" | tr a-z A-Z)"; if [ -n "${!v:-}" ]; then echo "${!v}"; elif [ -f .env ]; then grep -E "^$v=" .env | head -1 | cut -d= -f2- | sed -e 's/^"//' -e 's/"$//'; fi; }
js='
const base = "http://localhost:5678";
(async () => {
  const login = await fetch(base + "/rest/login", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ emailOrLdapLoginId: process.env.N8N_USER, password: process.env.N8N_PW }) });
  if (!login.ok) { console.log("Login fehlgeschlagen: HTTP " + login.status); process.exit(1); }
  const cookie = login.headers.getSetCookie().map(c => c.split(";")[0]).join("; ");
  const h = { "Content-Type": "application/json", cookie, browserid: "cli" };
  const count = async () => { const j = await (await fetch(base + "/rest/executions?limit=1", { headers: h })).json(); return j.data && (j.data.count ?? j.data.estimated); };
  const vorher = await count();
  const d = await fetch(base + "/rest/executions/delete", { method: "POST", headers: h, body: JSON.stringify({ deleteBefore: new Date(Date.now() + 60000).toISOString() }) });
  console.log("vorher " + vorher + ", Löschen HTTP " + d.status + ", nachher " + await count());
})();'
rc=0
for t in "$@"; do
  c="${N8N_CONTAINER:-$(docker ps -qf "name=-$t-1" | head -1)}"
  [ -n "$c" ] || { echo "$t: kein laufender Container"; rc=1; continue; }
  pw="$(getpw "$t")"; [ -n "$pw" ] || { echo "$t: Passwort PW_$(echo "$t" | tr a-z A-Z) nicht gefunden"; rc=1; continue; }
  user="$t@workshop.example"
  printf '%s: ' "$t"
  docker exec -e N8N_USER="$user" -e N8N_PW="$pw" "$c" node -e "$js" || rc=1
done
exit $rc
