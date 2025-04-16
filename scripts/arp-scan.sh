#!/data/data/com.termux/files/usr/bin/bash
# █▓▒░ ARP Scan ░▒▓█
echo -e "\e[1;33m[*]\e[0m Escaneando red local (requiere root)"

ip route | grep wlan0 | awk '{print $1}' | while read -r subnet; do
    arp-scan --interface=wlan0 "$subnet"
done
