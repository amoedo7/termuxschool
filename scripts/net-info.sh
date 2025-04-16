#!/data/data/com.termux/files/usr/bin/bash

# 🎨 Colores
CYAN='\033[1;36m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
MAGENTA='\033[1;35m'
RESET='\033[0m'

function loading_bar() {
    echo -ne "${CYAN}⏳ Cargando"
    for i in {1..5}; do
        echo -ne "."
        sleep 0.3
    done
    echo -e "${RESET}"
}

function print_banner() {
    clear
    echo -e "${MAGENTA}"
    echo "╔══════════════════════════════════════╗"
    echo "║    📡 Net Info — Hacker Scanner     ║"
    echo "╚══════════════════════════════════════╝"
    echo -e "${RESET}"
}

print_banner
loading_bar

echo -e "\n${YELLOW}📍 Recolectando información de red...${RESET}"
sleep 0.5

ip_local=$(ip addr show wlan0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1)
gateway=$(ip route | grep default | awk '{print $3}')
interfaz=$(ip route | grep default | awk '{print $5}')
dns=$(getprop | grep dns | grep -v "::" | awk -F'[][]' '{print $2}' | head -n 1)
ip_publica=$(curl -s ifconfig.me)

echo -e "\n${GREEN}📶 IP LOCAL        : ${CYAN}$ip_local${RESET}"
echo -e "${GREEN}🌍 IP PÚBLICA      : ${CYAN}$ip_publica${RESET}"
echo -e "${GREEN}🚪 PUERTA DE ENLACE: ${CYAN}$gateway${RESET}"
echo -e "${GREEN}🔌 INTERFAZ ACTIVA : ${CYAN}$interfaz${RESET}"
echo -e "${GREEN}🧠 SERVIDOR DNS    : ${CYAN}$dns${RESET}"
echo -e "\n${YELLOW}✅ Escaneo completo. Listo para la misión.${RESET}"
