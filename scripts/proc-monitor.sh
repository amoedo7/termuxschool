#!/data/data/com.termux/files/usr/bin/bash

suspect_list=("keylogger" "logkeys" "tcpdump" "strace" "netcat" "nc" "ncat" "nmap" "hydra" "ettercap" "wireshark" "dumpcap" "aircrack-ng" "reaver" "msfconsole")

echo -e "\033[1;35m🔍 Iniciando escaneo de procesos activos...\033[0m"
sleep 1

echo -ne "\033[1;34m💻 Analizando procesos"; for i in {1..8}; do echo -n "."; sleep 0.2; done; echo ""

echo -e "\n\033[1;36m📋 Lista de procesos:\033[0m\n"

# Obtener procesos y escanear
ps -aux | grep -v "grep" > /tmp/procs_termux

found_any=false

while read -r proc; do
    for word in "${suspect_list[@]}"; do
        if echo "$proc" | grep -iq "$word"; then
            echo -e "\033[1;31m⚠️  Proceso sospechoso detectado:\033[0m"
            echo -e "\033[1;37m$proc\033[0m"
            echo -e "\033[1;33m🔎 Coincidencia:\033[0m \033[1;31m$word\033[0m\n"
            found_any=true
        fi
    done
done < /tmp/procs_termux

if ! $found_any; then
    echo -e "\033[1;32m✅ No se encontraron procesos sospechosos.\033[0m"
fi

# Mostrar resumen visual
echo -e "\n\033[1;36m📊 Procesos Totales:\033[0m $(wc -l < /tmp/procs_termux)"
echo -e "\033[1;32m✔️ Escaneo finalizado.\033[0m\n"

# Limpiar
rm /tmp/procs_termux

# Esperar tecla
echo -ne "\033[1;34m🔁 Volver al menú en 5s...\033[0m"; sleep 5
