#!/data/data/com.termux/files/usr/bin/bash
# █▓▒░ Anti-Sniffer ░▒▓█
echo -e "\e[1;31m[!] Analizando red para detectar sniffers..."
read -p "IP del router: " router
for i in {1..5}; do
    ping -c 1 -s 65000 "$router" | grep -i "frag needed" && echo -e "\e[1;31m[⚠] Posible sniffer/interceptor detectado"
done
