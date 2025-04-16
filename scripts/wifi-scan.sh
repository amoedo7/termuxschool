#!/data/data/com.termux/files/usr/bin/bash

echo -e "\033[1;35m📶 Iniciando escaneo de redes Wi-Fi...\033[0m"
sleep 1
echo -ne "\033[1;34m🔍 Escaneando"; for i in {1..5}; do echo -n "."; sleep 0.3; done; echo ""

termux-wifi-scaninfo > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "\033[1;31m❌ Error: Se requiere acceso a termux-api.\033[0m"
    echo -e "\033[1;33m🔧 Solución: Ejecuta 'pkg install termux-api' y otorga permisos.\033[0m"
    exit 1
fi

echo -e "\n\033[1;36m📡 Redes Wi-Fi detectadas:\033[0m"

termux-wifi-scaninfo | jq -c '.[]' | while read -r red; do
    ssid=$(echo "$red" | jq -r '.ssid')
    bssid=$(echo "$red" | jq -r '.bssid')
    level=$(echo "$red" | jq -r '.level')
    security=$(echo "$red" | jq -r '.capabilities')

    signal_color="\033[1;32m"
    if [ "$level" -lt -70 ]; then signal_color="\033[1;33m"; fi
    if [ "$level" -lt -85 ]; then signal_color="\033[1;31m"; fi

    echo -e "\n📡 \033[1;37mSSID:\033[0m $ssid"
    echo -e "🔐 \033[1;37mSeguridad:\033[0m $security"
    echo -e "📶 \033[1;37mSeñal:\033[0m $signal_color${level}dBm\033[0m"
    echo -e "📍 \033[1;37mMAC:\033[0m $bssid"
done

echo -e "\n\033[1;32m✅ Escaneo finalizado.\033[0m"
