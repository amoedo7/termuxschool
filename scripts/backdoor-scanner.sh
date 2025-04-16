#!/data/data/com.termux/files/usr/bin/bash

# 🎨 Colores
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
MAGENTA='\033[1;35m'
WHITE='\033[1;37m'
RESET='\033[0m'

# 📁 Log
FECHA=$(date +"%Y%m%d_%H%M%S")
LOGDIR="$HOME/.termuxschool/logs"
mkdir -p "$LOGDIR"
LOGFILE="$LOGDIR/backdoor-scan-$FECHA.log"

clear
echo -e "${MAGENTA}🛡️ Backdoor Scanner — TermuxSchool Edition${RESET}"
echo -e "${WHITE}🔍 Escaneando en busca de puertas traseras y shells ocultas...${RESET}\n"
sleep 1

THREATS=0

# 🌐 1. Revisar conexiones abiertas o puertos sospechosos
echo -e "${CYAN}📡 Revisando conexiones activas y puertos...${RESET}"
ss -tulpen 2>/dev/null | grep -vE "127.0.0.1|::1" | while read -r conn; do
    echo -e "${RED}⚠️ Conexión sospechosa: $conn${RESET}"
    echo "⚠️ Conexión sospechosa: $conn" >> "$LOGFILE"
    ((THREATS++))
done
sleep 1

# 🕵️ 2. Buscar procesos sospechosos
echo -e "\n${CYAN}🔍 Buscando procesos sospechosos (nc, ncat, python server)...${RESET}"
ps -ef | grep -iE "nc|ncat|socat|python -m http.server|reverse_shell" | grep -v grep | while read -r proc; do
    echo -e "${RED}🚨 Proceso sospechoso: $proc${RESET}"
    echo "🚨 Proceso sospechoso: $proc" >> "$LOGFILE"
    ((THREATS++))
done
sleep 1

# 🧠 3. Verificar archivos de inicio que ejecuten scripts
echo -e "\n${CYAN}📂 Revisando archivos de inicio...${RESET}"
grep -iE "nc|bash|wget|curl|python" ~/.bashrc ~/.profile ~/.termux/boot/* 2>/dev/null | while read -r linea; do
    echo -e "${YELLOW}🧬 Script sospechoso en arranque: $linea${RESET}"
    echo "🧬 Script en arranque: $linea" >> "$LOGFILE"
    ((THREATS++))
done
sleep 1

# 🔎 4. Buscar archivos ocultos con extensiones raras
echo -e "\n${CYAN}📁 Buscando archivos ocultos peligrosos (.sh, .py, .php, .bin)...${RESET}"
find /sdcard /storage -type f \( -iname ".*.sh" -o -iname ".*.py" -o -iname ".*.php" -o -iname ".*.bin" \) 2>/dev/null | while read -r file; do
    echo -e "${YELLOW}👀 Archivo sospechoso: $file${RESET}"
    echo "👀 Archivo oculto: $file" >> "$LOGFILE"
    ((THREATS++))
done
sleep 1

# 🧾 Resultado final
echo -e "\n${WHITE}🔎 Escaneo completado.${RESET}"
if [ "$THREATS" -eq 0 ]; then
    echo -e "${GREEN}✅ Sistema limpio. No se detectaron posibles puertas traseras.${RESET}"
else
    echo -e "${RED}🚨 Se detectaron $THREATS posibles amenazas.${RESET}"
    echo -e "${YELLOW}📝 Log guardado en:${RESET} ${GREEN}$LOGFILE${RESET}"
fi
