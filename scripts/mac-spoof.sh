#!/data/data/com.termux/files/usr/bin/bash
# █▓▒░ MAC Spoofer ░▒▓█
echo -e "\e[1;35m[*]\e[0m Spoofing MAC de wlan0..."
ifconfig wlan0 down
mac=$(openssl rand -hex 6 | sed 's/\(..\)/\1:/g; s/:$//')
ifconfig wlan0 hw ether "$mac"
ifconfig wlan0 up
echo -e "\e[1;32m[✓]\e[0m Nueva MAC: $mac"
