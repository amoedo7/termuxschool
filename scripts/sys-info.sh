#!/data/data/com.termux/files/usr/bin/bash

clear
echo -e "\033[1;36m"
echo "╔═══════════════════════════════════════════╗"
echo "║     🧠 TERMUX SYSTEM DASHBOARD v1.0       ║"
echo "╚═══════════════════════════════════════════╝"
echo -e "\033[0m"

sleep 0.5

# Función para formatear título
print_section() {
    echo -e "\033[1;35m\n📦 $1\033[0m"
    echo -e "\033[1;30m──────────────────────────────────────────\033[0m"
}

# Info del dispositivo
print_section "DISPOSITIVO"
echo -e "📱 Nombre      : \033[1;37m$(getprop ro.product.model 2>/dev/null || echo '🔐 Dato oculto')\033[0m"
echo -e "📦 Android     : \033[1;37m$(getprop ro.build.version.release 2>/dev/null || echo '🔐 Dato oculto')\033[0m"
echo -e "🧠 Procesador  : \033[1;37m$(getprop ro.hardware 2>/dev/null || echo '🔐 Dato oculto')\033[0m"

# CPU y RAM
print_section "RECURSOS"
cpu_cores=$(grep -c ^processor /proc/cpuinfo)
ram_info=$(free -m | awk '/Mem:/ {print $3 " MB usados / " $2 " MB totales"}')
echo -e "🧩 Núcleos     : \033[1;32m$cpu_cores\033[0m"
echo -e "🧬 RAM         : \033[1;32m$ram_info\033[0m"

# Disco
print_section "ALMACENAMIENTO"
df_out=$(df -h /data 2>/dev/null | awk 'NR==2 {print $3 " usados / " $2 " totales"}')
echo -e "💾 Disco       : \033[1;34m${df_out:-'🔐 Dato oculto'}\033[0m"

# IP
print_section "RED"
ipaddr=$(ip a | grep inet | grep wlan0 | awk '{print $2}' | cut -d/ -f1)
echo -e "🌐 Dirección IP: \033[1;36m${ipaddr:-'🔐 Dato oculto'}\033[0m"

# Batería
print_section "ENERGÍA"
if command -v termux-battery-status &>/dev/null; then
    battery=$(termux-battery-status | jq '.percentage')
    echo -e "🔋 Batería     : \033[1;33m${battery}%\033[0m"
else
    echo -e "🔋 Batería     : \033[1;33m🔐 No disponible en este entorno\033[0m"
fi

# Final
echo -e "\n\033[1;30m──────────────────────────────────────────\033[0m"
echo -e "\033[1;32m✅ Análisis completo. Presiona Enter para volver.\033[0m"
read
