#!/data/data/com.termux/files/usr/bin/bash
# █▓▒░ Cámara Hunt ░▒▓█
echo -e "\e[1;31m[🎥] Buscando cámaras IP en red local...\e[0m"

for ip in $(seq 1 254); do
    target="192.168.1.$ip"
    echo -ne "\rAnalizando: $target"
    headers=$(curl -s --connect-timeout 1 $target | grep -Ei "camera|ipcam|hikvision|admin")
    if [[ ! -z "$headers" ]]; then
        echo -e "\n\e[1;32m[✔]\e[0m Posible cámara: $target"
    fi
done
