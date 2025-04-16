#!/data/data/com.termux/files/usr/bin/bash
# █▓▒░ WiFi Pirate ░▒▓█
echo -e "\e[1;36m[+]\e[0m Escaneando redes WiFi cercanas..."
pkg install iwlist -y
iwlist wlan0 scanning | grep -E "Cell|ESSID|Signal|Channel" | sed 's/^[ \t]*//'
