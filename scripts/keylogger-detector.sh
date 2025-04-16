#!/data/data/com.termux/files/usr/bin/bash
function hacker_banner() {
    clear
    echo -e "${RED}"
    echo "   ⠀⢀⣀⣀⣤⣤⣤⣤⣀⣀"
    echo " ⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⢀⣀⣤⣤"
    echo " ⠀⢸⣿⣿⣿⣿⠿⠿⠛⠉⠀⣿⣿⣿⣿   🛡️ KEYLOGGER DETECTOR"
    echo " ⠀⠘⠿⠟⠁⠀⠀⠀⠀⠀⠀⠈⠙⠿⠟   ⚡ TERMUX SCHOOL EDITION"
    echo -e "${RESET}\n"
}

# 🎨 Colores
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
MAGENTA='\033[1;35m'
WHITE='\033[1;37m'
RESET='\033[0m'

# 🗂️ Log
FECHA=$(date +"%Y%m%d_%H%M%S")
LOGDIR="$HOME/.termuxschool/logs"
mkdir -p "$LOGDIR"
LOGFILE="$LOGDIR/keylogger-scan-$FECHA.log"

clear
echo -e "${MAGENTA}🛡️ Keylogger Detector — TermuxSchool Edition${RESET}"
echo -e "${WHITE}🔍 Escaneo iniciado: $FECHA${RESET}\n"
sleep 1

SUSPICIOUS_FOUND=0

# 🧬 1. Buscar procesos sospechosos
echo -e "${CYAN}📦 Buscando procesos sospechosos...${RESET}"
ps -ef | grep -iE "logkeys|keylog|lkl|inputsniffer|uberkey|key_sniff" | grep -v grep | while read -r proc; do
    echo -e "${RED}⚠️ Proceso sospechoso: $proc${RESET}"
    echo "⚠️ Proceso sospechoso: $proc" >> "$LOGFILE"
    ((SUSPICIOUS_FOUND++))
done
sleep 1

# 🧠 2. Buscar módulos del kernel (si disponible)
echo -e "\n${CYAN}📂 Revisando módulos cargados...${RESET}"
cat /proc/modules 2>/dev/null | grep -iE "keylog|keyboard|input" | while read -r mod; do
    echo -e "${RED}⚠️ Módulo sospechoso: $mod${RESET}"
    echo "⚠️ Módulo sospechoso: $mod" >> "$LOGFILE"
    ((SUSPICIOUS_FOUND++))
done
sleep 1

# 🗂️ 3. Buscar archivos tipo log de pulsaciones
echo -e "\n${CYAN}📁 Buscando archivos sospechosos...${RESET}"
find /sdcard /storage -type f \( -iname "*.key" -o -iname "*.input" -o -iname "*.dump" -o -iname "key*.log" \) 2>/dev/null | while read -r archivo; do
    echo -e "${YELLOW}🧐 Archivo encontrado: ${WHITE}$archivo${RESET}"
    echo "🧐 Archivo sospechoso: $archivo" >> "$LOGFILE"
    ((SUSPICIOUS_FOUND++))
done
sleep 1

# 📊 Resultado
echo -e "\n${WHITE}🔎 Análisis finalizado.${RESET}"
if [ "$SUSPICIOUS_FOUND" -eq 0 ]; then
    echo -e "${GREEN}✅ No se encontraron indicios de keyloggers.${RESET}"
else
    echo -e "${RED}🚨 Se encontraron $SUSPICIOUS_FOUND indicio(s) de keylogger.${RESET}"
fi

echo -e "${WHITE}📝 Log guardado en:${RESET} ${GREEN}$LOGFILE${RESET}"
