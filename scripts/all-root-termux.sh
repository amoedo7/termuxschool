#!/data/data/com.termux/files/usr/bin/bash

# Colores
GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
CYAN="\033[1;36m"
MAGENTA="\033[1;35m"
WHITE="\033[1;37m"
RESET="\033[0m"

# Banner
clear
echo -e "${CYAN}╔════════════════════════════════════╗"
echo -e "${CYAN}║   🔓 all-root-termux.sh - HackerOS  ║"
echo -e "${CYAN}╚════════════════════════════════════╝${RESET}"

# Estado actual
echo -e "${MAGENTA}🔍 Verificando nivel actual de privilegio...${RESET}"
sleep 1

if command -v su >/dev/null; then
    echo -e "${GREEN}🎉 Root detectado. Nivel: Supremo${RESET}"
elif command -v fakeroot >/dev/null; then
    echo -e "${YELLOW}🧪 FakeRoot activo. Nivel: Simulación${RESET}"
else
    echo -e "${RED}🔒 Sistema cerrado. Nivel: Mortal${RESET}"
fi

# Menú
echo -e "\n${WHITE}Seleccione su identidad:${RESET}"
echo -e "  1) 🎉 Root detectado. Nivel: Supremo"
echo -e "  2) 🧪 FakeRoot activo. Nivel: Simulación"
echo -e "  3) 🔒 Sistema cerrado. Nivel: Mortal"
echo -ne "\nElija (1-3): "; read -r opcion

# Acción
case $opcion in
    1)
        echo -e "\n${GREEN}🌟 Intentando ingresar al modo Root...${RESET}"
        if command -v su >/dev/null; then
            su
            echo -e "${GREEN}✅ Ahora eres: Root detectado. Nivel: Supremo${RESET}"
        else
            echo -e "${RED}❌ No se detectó acceso a 'su'. Verifica Magisk o root.${RESET}"
        fi
        ;;
    2)
        echo -e "\n${YELLOW}🧪 Activando entorno FakeRoot...${RESET}"
        pkg install proot fakeroot -y
        echo -e "${MAGENTA}🧬 Iniciando entorno simulado con fakeroot...${RESET}"
        fakeroot bash
        ;;
    3)
        echo -e "\n${CYAN}🚪 Cerrando todos los privilegios de root...${RESET}"
        echo -e "${WHITE}🔒 Ahora eres: Sistema cerrado. Nivel: Mortal${RESET}"
        # Salimos de cualquier entorno elevado
        if [ "$EUID" -eq 0 ]; then
            exit
        fi
        ;;
    *)
        echo -e "${RED}❌ Opción inválida. Ejecute de nuevo.${RESET}"
        ;;
esac
