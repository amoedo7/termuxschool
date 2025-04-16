#!/data/data/com.termux/files/usr/bin/bash

echo -e "\n\033[1;36m🔐 Bienvenido al escáner de puertos - TermSchool edition\033[0m"
sleep 1
echo -ne "\033[1;35m🌐 Ingresa IP o dominio a escanear (Enter para usar 127.0.0.1): \033[0m"
read target
target=${target:-127.0.0.1}

echo -e "\n\033[1;34m🚀 Iniciando escaneo de puertos en: \033[1;33m$target\033[0m"
sleep 1

echo -ne "\033[1;32m⏳ Escaneando puertos"; for i in {1..5}; do echo -n "."; sleep 0.3; done; echo -e "\n"

open_ports=()
for port in $(seq 20 25); do
    timeout 1 bash -c "echo >/dev/tcp/$target/$port" 2>/dev/null && result="open" || result="closed"

    if [[ $result == "open" ]]; then
        echo -e "🟢 \033[1;32mPuerto $port abierto\033[0m"
        open_ports+=($port)
    else
        echo -e "🔴 \033[1;31mPuerto $port cerrado\033[0m"
    fi
    sleep 0.2
done

# Bonus dramático
echo -e "\n\033[1;36m🔍 Analizando hallazgos...\033[0m"
sleep 1

if [ ${#open_ports[@]} -eq 0 ]; then
    echo -e "⚪ \033[1;37mNo se encontraron puertos abiertos.\033[0m"
else
    echo -e "\n\033[1;32m📡 Puertos abiertos encontrados:\033[0m"
    for port in "${open_ports[@]}"; do
        echo -e "  ➤ \033[1;32m$port\033[0m"
    done
fi

echo -e "\n\033[1;35m✔️ Escaneo finalizado. Presiona Enter para volver al menú...\033[0m"
read
