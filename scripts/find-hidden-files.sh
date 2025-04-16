#!/data/data/com.termux/files/usr/bin/bash

# Colores
RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
YELLOW='\033[1;33m'
MAGENTA='\033[1;35m'
WHITE='\033[1;37m'
RESET='\033[0m'

# Fecha para log
FECHA=$(date +"%Y%m%d_%H%M%S")
LOGDIR="$HOME/.termuxschool/logs"
mkdir -p "$LOGDIR"
LOGFILE="$LOGDIR/hidden-scan-$FECHA.log"

# Detectar modo
MODO="deep"
if [[ "$1" == "--fast" ]]; then
    MODO="fast"
    echo -e "${YELLOW}⚡ Modo rápido activado. Solo escaneo en /sdcard y /storage${RESET}"
elif [[ "$1" == "--deep" ]]; then
    echo -e "${CYAN}🔍 Modo profundo activado. Escaneo completo del sistema.${RESET}"
else
    echo -e "${MAGENTA}ℹ️  Usa --fast o --deep como parámetro (por defecto: deep)${RESET}"
fi
sleep 1

# Rutas
RUTAS_FAST=(/sdcard /storage)
RUTAS_DEEP=(/sdcard /data /etc /storage /usr /home)

# Mostrar banner
clear
echo -e "${MAGENTA}🔎 Buscador de Archivos Ocultos & Backups — TermuxSchool Edition${RESET}"
echo -e "${WHITE}📁 Escaneo iniciado: $FECHA${RESET}\n"
sleep 1

TOTAL=0
ALERTA_DESCARGAS=0

# Animación por carpeta
animar() {
    echo -ne "${YELLOW}🛰️ Escaneando: $1...${RESET} "
    for i in {1..4}; do echo -n "."; sleep 0.2; done
    echo ""
}

# Función principal
buscar_archivos() {
    ruta=$1
    animar "$ruta"

    resultados=$(find "$ruta" \( -name ".*" -o -name "*.log" -o -name "*.bak" -o -name "*.old" -o -name "*.tmp" \) 2>/dev/null)

    for archivo in $resultados; do
        ((TOTAL++))
        tipo="📄 Archivo"
        [[ $archivo == *".log" ]] && tipo="📜 Log"
        [[ $archivo == *".bak" || $archivo == *".old" || $archivo == *".tmp" ]] && tipo="🗂️ Backup"
        [[ $(basename "$archivo") == .* ]] && tipo="🕵️ Oculto"

        # Alerta especial si está en Downloads
        if echo "$archivo" | grep -qi 'downloads' && ([[ $archivo == *.bak ]] || [[ $archivo == *.log ]]); then
            echo -e "${RED}⚠️ Alerta crítica: archivo sospechoso en Downloads: $archivo${RESET}"
            echo "⚠️ ALERTA: $archivo" >> "$LOGFILE"
            ((ALERTA_DESCARGAS++))
        else
            echo -e "${GREEN}[$tipo]${WHITE} $archivo${RESET}"
            echo "[$tipo] $archivo" >> "$LOGFILE"
        fi

        sleep 0.03
    done
}

# Elegir rutas según modo
if [[ "$MODO" == "fast" ]]; then
    RUTAS=("${RUTAS_FAST[@]}")
else
    RUTAS=("${RUTAS_DEEP[@]}")
fi

# Escanear
for ruta in "${RUTAS[@]}"; do
    buscar_archivos "$ruta"
done

# Resultados finales
echo -e "\n${CYAN}✅ Archivos encontrados: ${YELLOW}$TOTAL${RESET}" | tee -a "$LOGFILE"
if [ $ALERTA_DESCARGAS -gt 0 ]; then
    echo -e "${RED}🚨 $ALERTA_DESCARGAS archivo(s) sospechoso(s) encontrados en Downloads.${RESET}" | tee -a "$LOGFILE"
fi

echo -e "${WHITE}📝 Log guardado en:${RESET} ${GREEN}$LOGFILE${RESET}"
