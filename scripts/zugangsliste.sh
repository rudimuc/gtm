#!/usr/bin/env bash
# Erzeugt aus .env eine druckbare Zugangsliste (Markdown, Zettel je Gruppe).
# Die Ausgabe enthält Passwörter: nicht committen (unterlagen/zugang-*.md steht in .gitignore).
set -euo pipefail
cd "$(dirname "$0")/.."
[ -f .env ] || { echo ".env fehlt (Kopie der Dokploy-Environment)" >&2; exit 1; }
get() { grep -E "^$1=" .env | head -1 | cut -d= -f2- | sed -e 's/^"//' -e 's/"$//'; }
domain=$(get DOMAIN)
for n in 1 2 3 4 5 6 7 8 9; do
  pw=$(get "PW_GTM$n")
  printf '## Gruppe %s\n\n- Adresse: https://gtm%s.%s\n- Benutzer: gtm%s@workshop.example\n- Passwort: %s\n\n---\n\n' "$n" "$n" "$domain" "$n" "$pw"
done
