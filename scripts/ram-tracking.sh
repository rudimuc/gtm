#!/usr/bin/env bash
# RAM-Verlauf während des Workshops aufzeichnen (auf dem VPS ausführen).
#   nohup ./scripts/ram-tracking.sh 15 >/dev/null 2>&1 &     # alle 15 s, im Hintergrund
#   pkill -f ram-tracking.sh                                  # beenden
# Schreibt ins aktuelle Verzeichnis:
#   ram-container.csv   Zeit, Container, CPU %, Speicher, Limit, Speicher %
#   ram-host.csv        Zeit, RAM gesamt/benutzt/verfügbar (MB), Swap benutzt (MB)
set -u
iv="${1:-15}"
[ -f ram-container.csv ] || echo "zeit,container,cpu,speicher,limit,prozent" > ram-container.csv
[ -f ram-host.csv ] || echo "zeit,ram_gesamt_mb,ram_benutzt_mb,ram_verfuegbar_mb,swap_benutzt_mb" > ram-host.csv
while true; do
  t=$(date '+%F %T')
  docker stats --no-stream --format '{{.Name}};{{.CPUPerc}};{{.MemUsage}};{{.MemPerc}}' 2>/dev/null |
    awk -F';' -v t="$t" '{split($3,m," / "); print t","$1","$2","m[1]","m[2]","$4}' >> ram-container.csv
  free -m | awk -v t="$t" '/^Mem:/{r=$2","$3","$7} /^Swap:/{s=$3} END{print t","r","s}' >> ram-host.csv
  sleep "$iv"
done
