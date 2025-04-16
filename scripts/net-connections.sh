#!/data/data/com.termux/files/usr/bin/bash

RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
MAGENTA='\033[1;35m'
RESET='\033[0m'
BOLD='\033[1m'

DATE=$(date +"%Y%m%d_%H%M%S")
LOGDIR="$HOME/.termuxschool/logs"
mkdir -p "$LOGDIR"
LOGFILE="$LOGDIR/net-connections-$DATE.log"

declare -A ip_counter
THRESHOLD=10
INTERVAL=4
MAX_IPS=15

# Lista negra simple (se puede expandir)
BLACKLIST_COUNTRIES=("Russia" "China" "North Korea")
BLACKLIST_TERMS=("TOR" "proxy" "VPN")

function get_country() {
    local ip=$1
    local geo=""
    if command -v geoiplookup >/dev/null 2>&1; then
        geo=$(geoiplookup "$ip" | cut -d: -f2- | tr -d '\n')
    elif command -v whois >/dev/null 2>&1; then
        geo=$(whois "$ip" | grep -Ei 'country|org|netname' | head -n 3 | tr '\n' ' ')
    else
        geo="Geo info no disponible"
    fi
    echo "$geo"
}

function is_suspicious() {
    local info="$1"
    for bad in "${BLACKLIST_COUNTRIES[@]}" "${BLACKLIST_TERMS[@]}"; do
        echo "$info" | grep -qi "$bad" && return 0
    done
    return 1
}

function draw_ranking() {
    clear
    echo -e "${MAGENTA}🌐 Conexiones activas — NetMonitor TermuxSchool${RESET}"
    echo -e "${CYAN}⏱️  Escaneando cada ${INTERVAL}s. Top IPs:${RESET}\n"

    local count=0
    for ip in "${!ip_counter[@]}"; do
        ((count++))
        [[ $count -gt $MAX_IPS ]] && break

        hits=${ip_counter[$ip]}
        bar=$(printf "%${hits}s" | tr " " "█")

        geo=$(get_country "$ip")
        is_suspicious "$geo" && alert="⚠️" || alert=""

        if [ "$hits" -ge "$THRESHOLD" ]; then
            echo -e "${RED}${alert} $ip [$hits] $bar${RESET}"
            echo -e "     ↳ ${YELLOW}${geo}${RESET}"
        else
            echo -e "${GREEN}🔹 $ip [$hits] $bar${RESET}"
            echo -e "     ↳ ${CYAN}${geo}${RESET}"
        fi
    done
    echo ""
}

function scan_loop() {
    while true; do
        ips=$(ss -tnp 2>/dev/null | awk '{print $5}' | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | sort)
        for ip in $ips; do
            ((ip_counter[$ip]++))
        done
        draw_ranking | tee "$LOGFILE"
        sleep $INTERVAL
    done
}

if [ "$1" == "--bg" ]; then
    echo -e "${YELLOW}🛡️ Ejecutando en segundo plano... log: $LOGFILE${RESET}"
    (scan_loop) &
    exit 0
fi

scan_loop
