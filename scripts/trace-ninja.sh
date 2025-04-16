#!/data/data/com.termux/files/usr/bin/bash
# █▓▒░ Network Ninja ░▒▓█
echo -e "\e[1;34m[🌍] Detectando conexiones activas...\e[0m"

lsof -i -nP | grep ESTABLISHED | awk '{print $1,$2,$9}' | sort | uniq | while read -r proc pid ip; do
    ip_clean=$(echo "$ip" | cut -d':' -f1)
    loc=$(curl -s "https://ipinfo.io/$ip_clean/city")
    echo -e "\e[1;32m[+]\e[0m Proceso: $proc (PID: $pid) ↔ IP: $ip_clean [$loc]"
done
